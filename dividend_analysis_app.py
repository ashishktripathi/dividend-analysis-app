import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📈 Dividend Analysis Dashboard")

# --- Sidebar for Stock Selection ---
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., CJ.TO)", "CJ.TO")
stock = yf.Ticker(ticker)

# --- Fetch Historical Data ---
dividends = stock.dividends
history = stock.history(period="max")

if dividends.empty:
    st.warning("No dividend data found for this ticker.")
else:
    dividends_df = dividends.reset_index()
    dividends_df.columns = ['Date', 'Dividend']
    dividends_df['Year'] = dividends_df['Date'].dt.year
    dividends_df['Quarter'] = dividends_df['Date'].dt.to_period('Q')

    # -- 1. Dividend Amount Per Quarter --
    st.subheader("1. Dividend Amount Per Quarter")
    per_quarter = dividends_df.groupby('Quarter').sum().reset_index()
    per_quarter['Quarter'] = per_quarter['Quarter'].astype(str)

    fig1, ax1 = plt.subplots(figsize=(12, 5))
    ax1.plot(per_quarter['Quarter'], per_quarter['Dividend'], marker='o', label=ticker)
    ax1.set_title(f"Dividend Amount paid per quarter for {ticker}")
    ax1.set_xlabel("Quarter")
    ax1.set_ylabel("Dividend Paid")
    plt.xticks(rotation=90)
    ax1.legend()
    st.pyplot(fig1)

    # -- 2. Number of Times Dividend Paid Per Year --
    st.subheader("2. Number of Times Dividend Paid Per Year")
    monthly_dividends = dividends_df.groupby('Year')['Date'].count()

    fig2, ax2 = plt.subplots()
    ax2.plot(monthly_dividends.index, monthly_dividends.values, marker='o', label=f"{ticker} - Consistency")
    ax2.set_title("Number of times Dividend paid per year")
    ax2.set_ylabel("Months Dividends Paid")
    ax2.set_xlabel("Year")
    ax2.legend()
    st.pyplot(fig2)

    # -- 3. Amount of Dividend Paid Per Year --
    st.subheader("3. Total Dividend Paid Per Year")
    total_yearly_div = dividends_df.groupby('Year')['Dividend'].sum()

    fig3, ax3 = plt.subplots()
    ax3.plot(total_yearly_div.index, total_yearly_div.values, marker='o', label=f"{ticker} - Total Dividend")
    ax3.set_title("Amount of Dividend paid per year")
    ax3.set_ylabel("Total Dividend Paid")
    ax3.set_xlabel("Year")
    ax3.legend()
    st.pyplot(fig3)

# -- 4. Closing Price for the Last 10–15 Years --
st.subheader("4. Closing Price (Historical)")
history_filtered = history[['Close']].copy()
history_filtered['Date'] = history_filtered.index

fig4, ax4 = plt.subplots(figsize=(14, 5))
ax4.plot(history_filtered['Date'], history_filtered['Close'], color='blue', label=f"{ticker} Closing Price")
avg = history_filtered['Close'].mean()
med = history_filtered['Close'].median()
ax4.axhline(avg, linestyle='--', color='green', label=f"Average: {avg:.2f}")
ax4.axhline(med, linestyle='--', color='orange', label=f"Median: {med:.2f}")
ax4.set_title(f"Closing Price for {ticker} Over Time")
ax4.set_ylabel("Closing Price (CAD)")
ax4.set_xlabel("Date")
ax4.legend()
st.pyplot(fig4)
