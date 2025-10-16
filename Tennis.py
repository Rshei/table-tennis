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

# Create portfolio DataFrame
portfolio_df = pd.DataFrame({
    'Cost Price (15/10/2025)': cost_prices,
    'Current Price': current_prices
})

# Calculate returns
portfolio_df['Return %'] = ((portfolio_df['Current Price'] - portfolio_df['Cost Price (15/10/2025)']) /
                           portfolio_df['Cost Price (15/10/2025)']) * 100

# Display results
st.title("Dynamic Portfolio Performance Tracker")
st.write(f"Data as of: {datetime.now().strftime('%Y-%m-%d')}")
st.dataframe(portfolio_df.style.format({
    'Cost Price (15/10/2025)': '${:,.2f}',
    'Current Price': '${:,.2f}',
    'Return %': '{:.2f}%'
}))

total_return = ((portfolio_df['Current Price'].sum() - portfolio_df['Cost Price (15/10/2025)'].sum()) /
                portfolio_df['Cost Price (15/10/2025)'].sum()) * 100

st.write(f"Total portfolio return since 15/10/2025: {total_return:.2f}%")
