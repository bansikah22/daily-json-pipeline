import pandas as pd
import json

def analyze_data(latest_file, previous_file=None):
    """
    Analyzes the product data from JSON files and compares for differences.
    """
    with open(latest_file, 'r') as f:
        latest_data = json.load(f)
    df_latest = pd.DataFrame(latest_data)

    differences = {
        "average_price": df_latest["price"].mean(),
        "cheapest_product": df_latest.loc[df_latest["price"].idxmin()].to_dict(),
        "most_expensive_product": df_latest.loc[df_latest["price"].idxmax()].to_dict(),
        "stock_count": df_latest[df_latest["availability"].str.lower().str.contains("in stock", na=False)].shape[0],
        "total_products": len(df_latest),
    }

    if previous_file:
        with open(previous_file, 'r') as f:
            previous_data = json.load(f)
        df_previous = pd.DataFrame(previous_data)

        # Find new products
        latest_names = set(df_latest["name"])
        previous_names = set(df_previous["name"])
        new_products = latest_names - previous_names
        removed_products = previous_names - latest_names

        # Price changes
        merged = pd.merge(df_latest, df_previous, on="name", suffixes=("_latest", "_previous"), how="inner")
        price_changes = []
        for _, row in merged.iterrows():
            if row["price_latest"] != row["price_previous"]:
                price_changes.append({
                    "name": row["name"],
                    "old_price": row["price_previous"],
                    "new_price": row["price_latest"],
                    "change": row["price_latest"] - row["price_previous"]
                })

        differences.update({
            "new_products": list(new_products),
            "removed_products": list(removed_products),
            "price_changes": price_changes
        })

    return differences
