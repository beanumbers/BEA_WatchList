import streamlit as st
import pandas as pd
from datetime import datetime


st.logo('assets/Logo1.ico', size="large", link=None, icon_image=None)

st.set_page_config(
    page_title="BEA Watchlist",            # Title of the page
    page_icon="assets/Logo1.ico",          # Favicon/icon for the app
    layout="wide",                         # Layout: 'centered' or 'wide'
    initial_sidebar_state="expanded",      # Sidebar: 'auto', 'expanded', 'collapsed'
)

# Get current date
current_date = datetime.now().strftime("%B %d, %Y")

# Display the date in the app
st.markdown(
    f"""
    <div style="text-align: right;">
        {current_date}
    </div>
    """,
    unsafe_allow_html=True
)

# Page Navigation
pages = {
    "Home": [
        st.Page("pages/home.py", title = "Today"),
    ],
    "Dashboards": [
        st.Page("pages/page_1.py", title = "Watch List"),
        st.Page("pages/page_2.py",title = "Portfolio")
    ],
}

# Sidebar
if "name" not in st.session_state:
    st.session_state.name = "Savvy"  # Default name
if "df_watchlist" not in st.session_state:
    st.session_state.df_watchlist = None

with st.sidebar:
    st.session_state.name = st.text_input("Name/Nickname", st.session_state.name)
    st.write('Continue where you left')
    uploaded_file = st.file_uploader(
        "Upload CSV watchlist",type=['CSV','XLSX']
    )
    if uploaded_file is not None:
        st.session_state.df_watchlist = pd.read_csv(uploaded_file)

    st.write('Or start a new one')

pg = st.navigation(pages)
pg.run()

