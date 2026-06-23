import yfinance as yf

def load_price_data(ticker: str, period: str = "1y"):
    df = yf.download(ticker, period=period, auto_adjust=True)
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    return df

# Test
if __name__ == "__main__":
    df = load_price_data("^GSPC", period="1y")
    print(df.head())