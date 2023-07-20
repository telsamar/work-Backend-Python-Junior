import pandas as pd
import json

with open('trial_task.json', 'r') as f:
    data = json.load(f)

orders = pd.json_normalize(data, 'products', ['order_id', 'warehouse_name', 'highway_cost'])

orders['total_quantity'] = orders.groupby('order_id')['quantity'].transform('sum')
orders['tariff'] = -orders['highway_cost'] / orders['total_quantity']

unique_orders = orders.drop_duplicates(subset='order_id')

average_tariffs = unique_orders.groupby('warehouse_name').tariff.mean().reset_index()

print(average_tariffs)