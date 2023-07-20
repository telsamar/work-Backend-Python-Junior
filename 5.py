import pandas as pd
import json

def compute_warehouse_profit(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)

    df = pd.DataFrame(data)

    products_df = df.explode('products').reset_index(drop=True)
    
    products_df[['product', 'price', 'quantity']] = pd.json_normalize(products_df['products'])
    products_df.drop(columns='products', inplace=True)

    products_df['product_profit'] = products_df['price'] * products_df['quantity']
    products_df['order_profit'] = products_df['product_profit'] + products_df['highway_cost']

    warehouse_profit = products_df.groupby(['warehouse_name', 'product']).agg(
        quantity=('quantity', 'sum'),
        profit=('product_profit', 'sum')
    ).reset_index()

    warehouse_total_profit = products_df.groupby('warehouse_name').agg(
        total_profit=('order_profit', 'sum')
    ).reset_index()

    warehouse_profit = warehouse_profit.merge(warehouse_total_profit, on='warehouse_name', how='left')

    warehouse_profit['percent_profit_product_of_warehouse'] = (warehouse_profit['profit'] / warehouse_profit['total_profit']) * 100

    warehouse_profit = warehouse_profit[['warehouse_name', 'product', 'quantity', 'profit', 'percent_profit_product_of_warehouse']]
    
    return warehouse_profit

def compute_accumulated_percent(warehouse_profit):

    warehouse_profit = warehouse_profit.sort_values(by='percent_profit_product_of_warehouse', ascending=False)

    warehouse_profit['accumulated_percent_profit_product_of_warehouse'] = warehouse_profit.groupby('warehouse_name')['percent_profit_product_of_warehouse'].cumsum()

    return warehouse_profit

if __name__ == "__main__":
    warehouse_summary = compute_warehouse_profit('trial_task.json')
    result = compute_accumulated_percent(warehouse_summary)
    print(result)
