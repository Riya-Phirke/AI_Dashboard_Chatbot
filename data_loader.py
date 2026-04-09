import pandas as pd

def load_data():
    df = pd.read_csv("customer_shopping_behavior.csv")

    # Clean columns
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("(", "")
        .str.replace(")", "")
    )

    documents = []

    # 🔥 Add aggregated insights (VERY IMPORTANT)
    total_sales = df['purchase_amount_usd'].sum()
    avg_sales = df['purchase_amount_usd'].mean()
    top_category = df['category'].mode()[0]

    summary = f"""
    BUSINESS SUMMARY:
    Total sales: {total_sales}
    Average purchase: {avg_sales}
    Most popular category: {top_category}
    """

    documents.append(summary)

    # 🔥 Add grouped insights
    category_sales = df.groupby('category')['purchase_amount_usd'].sum()

    for cat, val in category_sales.items():
        documents.append(f"Category {cat} has total sales of {val}")

    # 🔥 Add some sample rows (not all)
    for _, row in df.head(50).iterrows():
        text = f"""
        Customer aged {row['age']} ({row['gender']}) bought {row['item_purchased']}
        from {row['category']} for {row['purchase_amount_usd']} USD.
        """
        documents.append(text)

    return documents