import streamlit as st
from data_loader import load_price_data
from indicators import add_sma, add_rsi, add_macd, get_signal
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Dashboard SP500")



# Selectboxy obok siebie
col1, col2 = st.columns(2)
with col1:
    okres = st.selectbox("Wybierz okres", ["1y", "2y", "5y"])
with col2:
    ticker = st.selectbox("Wybierz ticker", ["^GSPC", "SPY", "AAPL", "MSFT", "NVDA"])
st.title(f'Dashboard {ticker}')
df = load_price_data(ticker, period=okres)
df = add_sma(df)
df = add_rsi(df)
df = add_macd(df)

ostatni = df.iloc[-1]
poprzedni = df.iloc[-2]

sygnał, powód = get_signal(df)

if sygnał == "KUP":
    st.success(f"✅ SYGNAŁ: {sygnał} — {powód}")
elif sygnał == "SPRZEDAJ":
    st.error(f"🔴 SYGNAŁ: {sygnał} — {powód}")
else:
    st.warning(f"⚠️ SYGNAŁ: {sygnał} — {powód}")

col1, col2, col3 = st.columns(3)
col1.metric("Cena", f"{ostatni['Close']:.0f}", f"{ostatni['Close'] - poprzedni['Close']:.0f}")
col2.metric("RSI", f"{ostatni['RSI']:.1f}")
col3.metric("SMA 200", f"{ostatni['SMA_200']:.0f}")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Cena z SMA")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"],   name="Close"))
    fig.add_trace(go.Scatter(x=df.index, y=df["SMA_20"],  name="SMA 20"))
    fig.add_trace(go.Scatter(x=df.index, y=df["SMA_50"],  name="SMA 50"))
    fig.add_trace(go.Scatter(x=df.index, y=df["SMA_200"], name="SMA 200"))
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("RSI")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["RSI"], name="RSI"))
    fig.add_hline(y=70, line_color="red",   line_dash="dash")
    fig.add_hline(y=30, line_color="green", line_dash="dash")
    st.plotly_chart(fig, use_container_width=True)

col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader("MACD")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["MACD"],        name="MACD"))
    fig.add_trace(go.Scatter(x=df.index, y=df["MACD_signal"], name="Signal"))
    st.plotly_chart(fig, use_container_width=True)

with col_right2:
    st.subheader("MACD Histogram")
    fig = go.Figure()
    kolory = ["green" if v > 0 else "red" for v in df["MACD_hist"]]

    fig.add_trace(go.Bar(
        x=df.index,
        y=df["MACD_hist"],
        name="Histogram",
        marker_color=kolory
    ))
    st.plotly_chart(fig, use_container_width=True)






























    