import pandas as pd

# Load your dataset
file_path = 'data.csv'  # Update with your file path
data = pd.read_csv(file_path)

# Group data by 'symbol' and calculate the count of trades and sum of 'profit_usd'
symbol_summary = data.groupby('symbol').agg(
    trade_count=('symbol', 'count'),
    total_profit_usd=('profit_usd', 'sum')
).reset_index()

# Calculate the total profit across all symbols
total_profit_usd = symbol_summary['total_profit_usd'].sum()

# Print the summary table
print(symbol_summary)

# Print the total profit across all symbols
print(f"Total profit across all symbols: {total_profit_usd}")
