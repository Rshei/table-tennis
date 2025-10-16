import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Portfolio with stock ticker and allocation weight
portfolio = {
    'UBER': 0.20,  # Uber Technologies
    'NVDA': 0.20,  # Nvidia
    'MSFT': 0.15,  # Microsoft
    'JPM': 0.15,   # JPMorgan Chase
    'BAC': 0.15,   # Bank of America
    'ABT': 0.10,   # Abbott Laboratories
    'VERI': 0.05   # Veritone
}

# Define dates to fetch price data
end_date = datetime.today()
start_date = end_date - timedelta(days=7)  # A buffer for possible market holidays

symbols = list(portfolio.keys())

# Download historical data for the portfolio stocks
data = yf.download(symbols, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

# Adjusted close prices
adj_close = data['Adj Close']

# Cost price is yesterday's closing price (last available close before today)
cost_prices = adj_close.iloc[-2]

# Create dataframe to track portfolio
portfolio_df = pd.DataFrame({
    'Weight': [portfolio[s] for s in symbols],
    'Cost Price': cost_prices
})

# Current price is today's last available close price (simulate 'today's price')
current_prices = adj_close.iloc[-1]

portfolio_df['Current Price'] = current_prices

# Assume total investment of $7000 allocated according to weights
portfolio_df['Position Value Today'] = portfolio_df['Weight'] * 7000 * portfolio_df['Current Price'] / portfolio_df['Cost Price']

# Calculate unrealized profit/loss percentage
portfolio_df['Unrealized P/L %'] = (portfolio_df['Current Price'] / portfolio_df['Cost Price'] - 1) * 100

# Calculate total portfolio value
total_value_today = portfolio_df['Position Value Today'].sum()

# Streamlit app UI
st.title('Stock Portfolio Status Tracker')

st.write(f'Date: {adj_close.index[-1].strftime("%Y-%m-%d")}')

st.write('### Portfolio Holdings')
st.dataframe(portfolio_df.style.format({
    'Cost Price': '${:,.2f}',
    'Current Price': '${:,.2f}',
    'Position Value Today': '${:,.2f}',
    'Unrealized P/L %': '{:.2f}%'
}))

st.write(f'### Total Portfolio Value Today: ${total_value_today:,.2f}')

st.write("Cost price is set to yesterday's closing price. Current price is today's last close price for simulation.")
