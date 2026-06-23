import pandas as pd
from data_loader import load_price_data

def add_sma(df):
    df["SMA_20"]  = df["Close"].rolling(window=20).mean()
    df["SMA_50"]  = df["Close"].rolling(window=50).mean()
    df["SMA_200"] = df["Close"].rolling(window=200).mean()
    return df

def add_rsi(df):
    delta = df["Close"].diff()
    gain  = delta.clip(lower=0)
    loss  = -delta.clip(upper=0)
    avg_gain = gain.ewm(com=13, adjust=False).mean()
    avg_loss = loss.ewm(com=13, adjust=False).mean()
    df["RSI"] = 100 - (100 / (1 + avg_gain / avg_loss))
    return df
def get_signal(df):
    ostatni = df.iloc[-1]
    rsi = ostatni["RSI"]
    cena = ostatni["Close"]
    sma200 = ostatni["SMA_200"]
    sma50 = ostatni["SMA_50"]

    if rsi < 30 and cena > sma200:
        return "KUP", "RSI wyprzedany + cena powyżej SMA200"
    elif rsi > 70 and cena < sma200:
        return "SPRZEDAJ", "RSI wykupiony + cena poniżej SMA200"
    elif cena > sma200 and sma50 > sma200:
        return "KUP", "Cena i SMA50 powyżej SMA200 — trend wzrostowy"
    elif cena < sma200 and sma50 < sma200:
        return "SPRZEDAJ", "Cena i SMA50 poniżej SMA200 — trend spadkowy"
    else:
        return "CZEKAJ", "Sygnały mieszane — brak wyraźnego trendu"
    

def add_macd(df):
    ema_12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema_26 = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema_12 - ema_26
    df["MACD_signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_hist"] = df["MACD"] - df["MACD_signal"]
    return df





if __name__ == "__main__":
    df = load_price_data("^GSPC", period="1y")
    df = add_sma(df)
    df = add_rsi(df)
    df = add_macd(df)
    print(df[["Close", "SMA_20", "SMA_50", "SMA_200", "RSI"]].tail(5))