import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Portfolio stocks with allocation weights
portfolio = {
    'UBER': 0.20*100,  # Uber Technologies
    'NVDA': 0.20,  # Nvidia
    'MSFT': 0.15,  # Microsoft
    'JPM': 0.15,   # JPMorgan Chase
    'BAC': 0.15,   # Bank of America
    'ABT': 0.10,   # Abbott Laboratories
    'VERI': 0.05   # Veritone
}

# Define date range for fetching data with buffer for weekends/holidays
end_date = datetime.today()
start_date = end_date - timedelta(days=7)

symbols = list(portfolio.keys())

# Download historical price data without auto adjustment (to keep both Close and Adj Close if available)
data = yf.download(symbols, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), auto_adjust=False)

# If 'Adj Close' is missing (common issue), use 'Close' as fallback
if 'Adj Close' in data.columns.levels[0]:
    price_data = data['Adj Close']
else:
    price_data = data['Close']

# Extract yesterday's close prices as cost basis
cost_prices = price_data.iloc[-2]

# Current price simulated as last available close price
current_prices = price_data.iloc[-1]

# Create portfolio dataframe to track holdings
portfolio_df = pd.DataFrame({
    'Weight': [portfolio[s] for s in symbols],
    'Cost Price': cost_prices,
    'Current Price': current_prices
})

# Calculate current position values based on allocation and price changes
total_investment = 7000
portfolio_df['Position Value Today'] = portfolio_df['Weight'] * total_investment * portfolio_df['Current Price'] / portfolio_df['Cost Price']

# Calculate unrealized profit/loss percentage per stock
portfolio_df['Unrealized P/L %'] = (portfolio_df['Current Price'] / portfolio_df['Cost Price'] - 1) * 100

# Calculate total portfolio value today
total_value_today = portfolio_df['Position Value Today'].sum()

# Streamlit UI
st.title('Stock Portfolio Status Tracker')

st.write(f'Date: {price_data.index[-1].strftime("%Y-%m-%d")}')

st.write('### Portfolio Holdings')
st.dataframe(portfolio_df.style.format({
    'Cost Price': '${:,.2f}',
    'Current Price': '${:,.2f}',
    'Position Value Today': '${:,.2f}',
    'Unrealized P/L %': '{:.2f}%'
}))

st.write(f'### Total Portfolio Value Today: ${total_value_today:,.2f}')

st.write("Note: Cost price is set to yesterday's closing price. Current price is today's last close for simulation purposes.")
