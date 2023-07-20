import pandas as pd
import json

def compute_order_profit(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    orders = pd.json_normalize(data, 'products', ['order_id', 'warehouse_name', 'highway_cost'])

    orders['total_quantity'] = orders.groupby('order_id')['quantity'].transform('sum')
    orders['tariff'] = -orders['highway_cost'] / orders['total_quantity']
    
    orders['income'] = orders['price'] * orders['quantity']
    orders['expenses'] = orders['tariff'] * orders['quantity']
    orders['profit'] = orders['income'] - orders['expenses']

    order_profit = orders.groupby('order_id').profit.sum().reset_index()
    order_profit.columns = ['order_id', 'order_profit']

    return order_profit

if __name__ == "__main__":
    order_profit_summary = compute_order_profit('trial_task.json')
    print(order_profit_summary)

    average_profit = order_profit_summary['order_profit'].mean()
    print(f"\nСредняя прибыль заказов: {average_profit:.2f}")