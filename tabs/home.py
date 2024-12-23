import streamlit as st
import pandas as pd
import yfinance as yf
from assets.utils import load_css
from assets.utils import stocks_lists

# ---- Functions ------
def plot_hist(info):
    import plotly.graph_objects as go
    if info['Close'].iloc[-1] > info['Close'].iloc[0]:
        color = 'green'
        fillcolor = 'rgba(0, 255, 0, 0.2)'
    else:
        color = 'red'
        fillcolor = 'rgba(255, 0, 0, 0.2)'
    first_value = info['Close'].iloc[0]
    last_value = info['Close'].iloc[-1]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=info.index,
        y=info['Close'],
        mode='lines',
        fill='tozeroy',
        fillcolor=fillcolor,
        line=dict(color=color),
        name='',
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=[info.index[0]],
        y=[first_value],
        mode='markers+text',
        marker=dict(size=10, color=color),
        text=[f"{first_value:.2f}"],
        textposition="top center",
        textfont=dict(
            color=color,  # Text color
            size=14,  # Text font size
            family='Arial',  # Font family
            weight='bold'  # Font weight (you can also use 'normal', 'bold', etc.)
        ),
        name='',
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=[info.index[-1]],
        y=[last_value],
        mode='markers+text',
        marker=dict(size=10, color=color),
        text=[f"{last_value:.2f}"],
        textposition="top center",
        textfont=dict(
            color=color,  # Text color
            size=14,  # Text font size
            family='Arial',  # Font family
            weight='bold'  # Font weight (you can also use 'normal', 'bold', etc.)
        ),
        name='',
        showlegend=False
    ))

    # Update the layout for transparency and no axis ticks
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False,
                   range=[0.8 * min([first_value, last_value]), 1.2 * max([first_value, last_value])]),
    )

    return fig

# Function to fetch stock data safely
@st.cache_data
def fetch_stock_data(tickers):
    data = []
    figs = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            name = stock.info.get('shortName', 'N/A')
            info = stock.history(period="1y")
            price = round(info['Close'].iloc[-1], 2) if not info.empty else None
            change = round((info['Close'].iloc[-1] - info['Close'].iloc[-2]), 2) if not info.empty else None
            change_p = round((change / info['Open'].iloc[-1]) * 100, 2) if not info.empty else None
            data.append({"Stock": ticker, "Name": name, "Price": price, "Change ($)": change, "Change (%)": change_p})
            f = plot_hist(info)
            figs.append(f)
        except Exception as e:
            st.warning(f"Error fetching data for {ticker}: {e}")
    return {"Table":pd.DataFrame(data).dropna(),"Figure":figs}

@st.cache_data
def fetch_currency_data(tickers):
    data = []
    for ticker in tickers:
        try:
            currency = yf.Ticker(ticker)
            info = currency.history(period="1y")
            name = currency.info.get('shortName', 'N/A')
            rate = info['Close'].iloc[-1] if not info.empty else None
            change = ((info['Close'].iloc[-1] - info['Open'].iloc[-1]) / info['Open'].iloc[-1]) * 100 if not info.empty else None
            data.append({"Pair": ticker,"Name":name, "Rate": rate, "Change (%)": change})
        except Exception as e:
            st.warning(f"Error fetching data for {ticker}: {e}")
    return pd.DataFrame(data).dropna()

# ---- The Home page begins here ----

st.markdown(load_css("assets/styles.css"), unsafe_allow_html=True)
st.markdown(f'<h class="title">Welcome back {st.session_state.name}</h>', unsafe_allow_html=True)
st.markdown(f'<p1 class="fontstyle1">World Today: Financial Highlights</p1>', unsafe_allow_html=True)

# Fetch and display stock data
stock_tickers = stocks_lists['US']
df_stocks = fetch_stock_data(stock_tickers)

# ----- US Markets ------
st.write("---")
st.markdown(f'<p1 class="fontstyle1">US Markets</p1>', unsafe_allow_html=True)

cols = st.columns(len(df_stocks['Table']))
for col, i, fig in zip(cols, df_stocks['Table'].index, df_stocks['Figure']):
    if df_stocks["Table"].iloc[i, 4] > 0:
        change_class = "positive"
        arrow = "↑"
    else:
        change_class = "negative"
        arrow = "↓"
    with col:
        st.markdown(
            f"""
            <div class="square-frame">
                <p class="ticker">{df_stocks['Table'].iloc[i, 1]} ({df_stocks['Table'].iloc[i, 0]})</p>
                <p class="price"><strong>${df_stocks['Table'].iloc[i, 2]:.2f}</strong></p>
                <p class="{change_class}"> $ {df_stocks['Table'].iloc[i, 3]:+.2f}</p>  
                <p class="{change_class}"> {arrow} {abs(df_stocks['Table'].iloc[i, 4]):.2f}%</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.plotly_chart(fig)

# ---- Country Selection -----
st.write("---")
st.markdown(f'<p1 class="fontstyle1">Selected Markets</p1>', unsafe_allow_html=True)
countries = ['Canada','Mexico']
s_country = st.selectbox("Select country to display market tickers", countries,index=None,placeholder="country")

if s_country is not None:
    stock_tickers = stocks_lists[s_country]
    df1_stocks = fetch_stock_data(stock_tickers)
    st.dataframe(df1_stocks)

# ---- Currency Pairs Section -----
st.write("---")
st.markdown(f'<p1 class="fontstyle1">Currency Pairs</p1>', unsafe_allow_html=True)
currency_tickers = stocks_lists["Currencies"]
df_currency = fetch_currency_data(currency_tickers)

cols1 = st.columns(len(df_currency))
for col, i in zip(cols1, df_currency.index):
    if df_currency.iloc[i, 3] > 0:
        change_class = "positive"
        arrow = "↑"
    else:
        change_class = "negative"
        arrow = "↓"
    with col:
        st.markdown(
            f"""
            <div class="square-frame">
                <p class="ticker">{df_currency.iloc[i, 1]}</p>
                <p class="price"><strong>{df_currency.iloc[i, 2]:.2f}</strong></p>
                <p class="{change_class}"> {arrow} {abs(df_currency.iloc[i, 3]):.2f}%</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

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
