import streamlit as st
from data_loader import load_data
from vector_store import create_vector_store, retrieve
from dotenv import load_dotenv
import os
from groq import Groq

# Load API key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Page config
st.set_page_config(page_title="AI Dashboard Assistant", page_icon="🤖", layout="wide")

# 🔥 CUSTOM CSS (PREMIUM UI)
st.markdown("""
<style>
body {
    background-color: #f5f7fb;
}
.chat-container {
    padding: 10px;
}
.user-msg {
    background-color: #6A0DAD;
    color: white;
    padding: 10px;
    border-radius: 10px;
    text-align: right;
    margin: 5px;
}
.bot-msg {
    background-color: #EAEAEA;
    color: black;
    padding: 10px;
    border-radius: 10px;
    text-align: left;
    margin: 5px;
}
.stButton>button {
    border-radius: 10px;
    height: 50px;
    width: 100%;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# 🔥 HEADER
st.markdown("""
<h1 style='text-align: center; 
background: linear-gradient(to right, #6A0DAD, #9D4EDD);
-webkit-background-clip: text;
color: transparent;'>
🤖 AI Dashboard Assistant
</h1>
<p style='text-align: center;'>Ask questions and get insights instantly</p>
""", unsafe_allow_html=True)

# Load data
if "index" not in st.session_state:
    documents = load_data()
    index, docs = create_vector_store(documents)
    st.session_state.index = index
    st.session_state.docs = docs

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔥 SUGGESTION BUTTONS (CENTERED)
st.markdown("### 💡 Try Quick Insights")

col1, col2, col3 = st.columns(3)

if col1.button("💰 Total Sales"):
    st.session_state.sample_query = "What is total sales?"

if col2.button("📊 Best Category"):
    st.session_state.sample_query = "Which category performs best?"

if col3.button("📈 Insights"):
    st.session_state.sample_query = "Give complete business insights"

# Display chat
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>{msg['content']}</div>", unsafe_allow_html=True)

# Input
query = st.chat_input("Ask your question...")

# Handle button click
if "sample_query" in st.session_state:
    query = st.session_state.sample_query
    del st.session_state.sample_query

if query:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": query})

    # Show user message
    st.markdown(f"<div class='user-msg'>{query}</div>", unsafe_allow_html=True)

    # Retrieve context
    context = retrieve(query, st.session_state.index, st.session_state.docs)

    # AI response
    with st.spinner("Analyzing data..."):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": """
                You are a business data analyst.
                Give insights with numbers, trends and recommendations.
                """},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion:{query}"}
            ]
        )

        answer = response.choices[0].message.content

    # Show bot message
    st.markdown(f"<div class='bot-msg'>{answer}</div>", unsafe_allow_html=True)

    # Save response
    st.session_state.messages.append({"role": "assistant", "content": answer})