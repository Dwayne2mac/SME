# app.py
import yfinance as yf
import pandas as pd
import streamlit as st

st.set_page_config(page_title="LSE Volume Surge Scanner", layout="wide")
st.title("📊 LSE Volume Surge Swing Trade Scanner")

tickers = ['HSBA.L', 'BARC.L', 'BP.L', 'GSK.L', 'LLOY.L', 'VOD.L']  # Add more LSE tickers here

def check_volume_spikes(tickers):
    results = []

    for ticker in tickers:
        try:
            data = yf.download(ticker, period='1mo')
            if data.empty or len(data) < 21:
                continue

            today = data.iloc[-1]
            avg_volume = data['Volume'].iloc[-21:-1].mean()

            if today['Volume'] > 2 * avg_volume and today['Close'] > today['Open']:
                results.append({
                    'Ticker': ticker,
                    'Price Change %': round((today['Close'] - today['Open']) / today['Open'] * 100, 2),
                    'Volume': int(today['Volume']),
                    'Volume Surge %': round((today['Volume'] / avg_volume) * 100, 2),
                    'Close': round(today['Close'], 2)
                })
        except:
            continue

    return pd.DataFrame(results).sort_values(by='Volume Surge %', ascending=False)

df = check_volume_spikes(tickers)

if df.empty:
    st.info("No volume surges detected today. Try again later.")
else:
    st.success(f"📈 Found {len(df)} volume surge(s) today")
    st.dataframe(df, use_container_width=True)
