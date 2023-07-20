import pandas as pd
import json

def compute_product_summary(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    orders = pd.json_normalize(data, 'products', ['order_id', 'warehouse_name', 'highway_cost'])

    orders['total_quantity'] = orders.groupby('order_id')['quantity'].transform('sum')
    orders['tariff'] = -orders['highway_cost'] / orders['total_quantity']
    
    orders['income'] = orders['price'] * orders['quantity']
    orders['expenses'] = orders['tariff'] * orders['quantity']
    orders['profit'] = orders['income'] - orders['expenses']

    product_summary = orders.groupby('product').agg(
        quantity=('quantity', 'sum'),
        income=('income', 'sum'),
        expenses=('expenses', 'sum'),
        profit=('profit', 'sum')
    ).reset_index()

    return product_summary

if __name__ == "__main__":
    summary = compute_product_summary('trial_task.json')
    print(summary)