import streamlit as st
import pandas as pd
import yfinance as yf
from assets.utils import load_css


# ---- Functions ------
# Function to fetch stock data safely
@st.cache_data
def fetch_stock_data(tickers):
    data = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            name = stock.info.get('shortName', 'N/A')
            info = stock.history(period="1y")
            price = round(info['Close'].iloc[-1], 2) if not info.empty else None
            change = round((info['Close'].iloc[-1] - info['Close'].iloc[-2]), 2) if not info.empty else None
            change_p = round((change / info['Open'].iloc[-1]) * 100, 2) if not info.empty else None
            data.append({"Stock": ticker, "Name": name, "Price": price, "Change ($)": change, "Change (%)": change_p})
        except Exception as e:
            st.warning(f"Error fetching data for {ticker}: {e}")
    return pd.DataFrame(data).dropna()

@st.cache_data
def fetch_currency_data(tickers):
    data = []
    for ticker in tickers:
        try:
            currency = yf.Ticker(ticker)
            info = currency.history(period="1d")
            rate = info['Close'].iloc[-1] if not info.empty else None
            change = ((info['Close'].iloc[-1] - info['Open'].iloc[-1]) / info['Open'].iloc[-1]) * 100 if not info.empty else None
            data.append({"Pair": ticker, "Rate": rate, "Change (%)": change})
        except Exception as e:
            st.warning(f"Error fetching data for {ticker}: {e}")
    return pd.DataFrame(data).dropna()

# ---- The Home page begins here ----

st.markdown(load_css("assets/styles.css"), unsafe_allow_html=True)
st.markdown(f'<h class="title">Welcome back {st.session_state.name}</h>', unsafe_allow_html=True)
st.markdown(f'<p1 class="fontstyle1">World Today: Financial Highlights</p1>', unsafe_allow_html=True)

# Fetch and display stock data
stock_tickers = ["^GSPC", "^DJI", "^IXIC", "^RUT"]
df_stocks = fetch_stock_data(stock_tickers)

# ----- US Markets ------
st.write("---")
st.markdown(f'<p1 class="fontstyle1">US Markets</p1>', unsafe_allow_html=True)

cols = st.columns(len(df_stocks))
for col, i in zip(cols, df_stocks.index):
    if df_stocks.iloc[i, 4] > 0:
        change_class = "positive"
        arrow = "↑"
    else:
        change_class = "negative"
        arrow = "↓"
    with col:
        st.markdown(
            f"""
            <div class="square-frame">
                <p class="ticker">{df_stocks.iloc[i, 1]} ({df_stocks.iloc[i, 0]})</p>
                <p class="price"><strong>${df_stocks.iloc[i, 2]:.2f}</strong></p>
                <p class="{change_class}"> $ {df_stocks.iloc[i, 3]:+.2f}</p>  
                <p class="{change_class}"> {arrow} {abs(df_stocks.iloc[i, 4]):.2f}%</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---- Currency Pairs Section -----
st.markdown(f'<p1 class="fontstyle1">Currency Pairs</p1>', unsafe_allow_html=True)

currency_tickers = ["EURUSD=X", "USDJPY=X", "GBPUSD=X"]
df_currency = fetch_currency_data(currency_tickers)
st.table(df_currency)

# Financial News Section
st.subheader("Financial News")
# Example dynamic fetching
# Replace with NewsAPI results
news_items = [
    {"headline": "Stock Markets Surge Amid Optimism", "url": "https://example.com/news1"},
    {"headline": "Fed Hints at Rate Hike", "url": "https://example.com/news2"},
    {"headline": "Cryptocurrency Prices Plummet", "url": "https://example.com/news3"},
]
for news in news_items:
    st.markdown(f"- [{news['headline']}]({news['url']})")
