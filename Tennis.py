import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# Portfolio stocks
symbols = ['UBER', 'NVDA', 'MSFT', 'JPM', 'BAC', 'ABT', 'VERI']

# Fetch historical data for 15th October 2025 for all stocks
historical_data = yf.download(
    tickers=symbols,
    start='2025-10-15',
    end='2025-10-16',
    interval='1d',
    progress=False
)

# Extract closing prices on 15/10/2025
cost_prices = historical_data['Close'].iloc[0]

# Fetch today's data (latest close)
today_data = yf.download(
    tickers=symbols,
    period='1d',
    interval='1d',
    progress=False
)

current_prices = today_data['Close'].iloc[-1]

# Define my opinion on allocation weights summing to 1
allocation_weights = {
    'UBER': 0.20,
    'NVDA': 0.20,
    'MSFT': 0.15,
    'JPM': 0.15,
    'BAC': 0.15,
    'ABT': 0.10,
    'VERI': 0.05
}

# Calculate how much USD invested per stock out of $7000 total
total_investment = 7000
invested_amount = {symbol: total_investment * allocation_weights[symbol] for symbol in symbols}

# Create portfolio DataFrame
portfolio_df = pd.DataFrame({
    'Cost Price (15/10/2025)': cost_prices,
    'Current Price': current_prices,
    'Invested Amount (USD)': pd.Series(invested_amount)
})

# Calculate number of shares bought at cost price
portfolio_df['Shares'] = portfolio_df['Invested Amount (USD)'] / portfolio_df['Cost Price (15/10/2025)']

# Calculate current value of the shares
portfolio_df['Current Value (USD)'] = portfolio_df['Shares'] * portfolio_df['Current Price']

# Calculate returns
portfolio_df['Return %'] = ((portfolio_df['Current Price'] - portfolio_df['Cost Price (15/10/2025)']) /
                           portfolio_df['Cost Price (15/10/2025)']) * 100

# Display results
st.title("Portfolio Performance Tracker with Investment Amounts")
st.write(f"Data as of: {datetime.now().strftime('%Y-%m-%d')}")

st.dataframe(portfolio_df.style.format({
    'Cost Price (15/10/2025)': '${:,.2f}',
    'Current Price': '${:,.2f}',
    'Invested Amount (USD)': '${:,.2f}',
    'Shares': '{:,.2f}',
    'Current Value (USD)': '${:,.2f}',
    'Return %': '{:.2f}%'
}))

total_current_value = portfolio_df['Current Value (USD)'].sum()
total_return = ((total_current_value - total_investment) / total_investment) * 100

st.write(f"### Total portfolio value today: ${total_current_value:,.2f}")
st.write(f"### Total portfolio return since 15/10/2025: {total_return:.2f}%")
