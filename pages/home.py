import streamlit as st
import pandas as pd
import yfinance as yf
from assets.utils import load_css

st.markdown(load_css("assets/styles.css"), unsafe_allow_html=True)
st.markdown(f'<h class="title">Welcome back {st.session_state.name}</h>', unsafe_allow_html=True)
st.markdown(f'<p1 class="fontstyle1">World Today: Financial Highlights</p1>', unsafe_allow_html=True)

# Create a Streamlit layout with square frames

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="square-frame">Stock A</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="square-frame">Stock B</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="square-frame">Stock C</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="square-frame">Stock 4</div>', unsafe_allow_html=True)


# Section: Top Stocks
st.subheader("Top Stocks Today")

# Define the tickers for the top stocks
stock_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

# Fetch stock data
stock_data = []
for ticker in stock_tickers:
    stock = yf.Ticker(ticker)
    info = stock.history(period="1d")
    price = info['Close'].iloc[-1] if not info.empty else None
    change = ((info['Close'].iloc[-1] - info['Open'].iloc[-1]) / info['Open'].iloc[-1]) * 100 if not info.empty else None
    stock_data.append({"Stock": ticker, "Price": price, "Change (%)": change})

# Create DataFrame and display
df_stocks = pd.DataFrame(stock_data).dropna()
st.table(df_stocks)

# Section: Currency Pairs
st.subheader("Currency Pairs")

# Define currency pairs
currency_tickers = ["EURUSD=X", "USDJPY=X", "GBPUSD=X"]

# Fetch currency data
currency_data = []
for ticker in currency_tickers:
    currency = yf.Ticker(ticker)
    info = currency.history(period="1d")
    rate = info['Close'].iloc[-1] if not info.empty else None
    change = ((info['Close'].iloc[-1] - info['Open'].iloc[-1]) / info['Open'].iloc[-1]) * 100 if not info.empty else None
    currency_data.append({"Pair": ticker, "Rate": rate, "Change (%)": change})

# Create DataFrame and display
df_currency = pd.DataFrame(currency_data).dropna()
st.table(df_currency)

# Section: Financial News
st.subheader("Financial News")
# Example Data - Replace with News API results
news_items = [
    {"headline": "Stock Markets Surge Amid Optimism", "url": "https://example.com/news1"},
    {"headline": "Fed Hints at Rate Hike", "url": "https://example.com/news2"},
    {"headline": "Cryptocurrency Prices Plummet", "url": "https://example.com/news3"},
]
for news in news_items:
    st.write(f"- [{news['headline']}]({news['url']})")

