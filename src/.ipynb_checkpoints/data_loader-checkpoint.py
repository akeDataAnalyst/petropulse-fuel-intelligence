import yfinance as yf
import pandas as pd

def get_market_data():
    tickers = {
        "BZ=F": "Brent_Crude",
        "CL=F": "WTI_Crude",
        "RB=F": "Gasoline_Futures"
    }
    data = yf.download(list(tickers.keys()), period="2y", interval="1d")
    
    # We select only the 'Close' price and rename using our dictionary
    df = data['Close'].rename(columns=tickers)
    return df

if __name__ == "__main__":
    df = get_market_data()
    print("Successfully fetched market data:")
    print(df.tail())
