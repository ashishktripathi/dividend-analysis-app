import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(layout="wide")
st.title("📈 Dividend Analysis Dashboard")

# Sidebar
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., CJ.TO)", "CJ.TO")
stock = yf.Ticker(ticker)

# Fetch data
dividends = stock.dividends
history = stock.history(period="max")

if dividends.empty:
    st.warning("No dividend data found for this ticker.")
else:
    # Preprocess dividend data
    dividends_df = dividends.reset_index()
    dividends_df.columns = ['Date', 'Dividend']
    dividends_df['Year'] = dividends_df['Date'].dt.year
    dividends_df['Quarter'] = dividends_df['Date'].dt.to_period('Q').astype(str)

    # 1. Dividend Amount Per Quarter
    st.subheader("1. Dividend Amount Per Quarter")
    per_quarter = dividends_df.groupby('Quarter')['Dividend'].sum().reset_index()
    fig1 = px.line(per_quarter, x='Quarter', y='Dividend', markers=True,
                   title=f"Dividend Amount Paid Per Quarter for {ticker}")
    st.plotly_chart(fig1, use_container_width=True)

    # 2. Number of Times Dividend Paid Per Year
    st.subheader("2. Number of Times Dividend Paid Per Year")
    count_per_year = dividends_df.groupby('Year')['Date'].count().reset_index()
    count_per_year.columns = ['Year', 'Payments']
    fig2 = px.line(count_per_year, x='Year', y='Payments', markers=True,
                   title="Number of Dividend Payments Per Year")
    st.plotly_chart(fig2, use_container_width=True)

    # 3. Total Dividend Paid Per Year
    st.subheader("3. Total Dividend Paid Per Year")
    total_per_year = dividends_df.groupby('Year')['Dividend'].sum().reset_index()
    fig3 = px.line(total_per_year, x='Year', y='Dividend', markers=True,
                   title="Total Dividend Paid Per Year")
    st.plotly_chart(fig3, use_container_width=True)

# 4. Historical Closing Price
st.subheader("4. Closing Price History")
if history.empty:
    st.warning("No historical price data found.")
else:
    price_df = history[['Close']].reset_index()
    price_df['Year'] = price_df['Date'].dt.year
    avg = price_df['Close'].mean()
    med = price_df['Close'].median()

    fig4 = px.line(price_df, x='Date', y='Close', title=f"{ticker} Historical Closing Prices")
    fig4.add_hline(y=avg, line_dash="dash", line_color="green", annotation_text=f"Avg: {avg:.2f}")
    fig4.add_hline(y=med, line_dash="dash", line_color="orange", annotation_text=f"Med: {med:.2f}")
    st.plotly_chart(fig4, use_container_width=True)
