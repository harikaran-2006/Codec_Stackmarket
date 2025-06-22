import pandas as pd
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from datetime import datetime
import requests
import traceback

try:
    # Place your existing code here
    pass
except Exception as e:
    print("Error:", e)
    print(traceback.format_exc())


# Function to fetch live stock data
def fetch_stock_data(stock_symbol, interval="1min"):
    api_key = "659S7FKPSID34LV9"  # Replace this with your Alpha Vantage API key
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_symbol}&interval={interval}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    if f"Time Series ({interval})" in data:
        time_series = data[f"Time Series ({interval})"]
        df = pd.DataFrame(time_series).T
        df = df.rename(columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume"
        })
        df.index = pd.to_datetime(df.index)
        df = df.astype(float)
        return df
    else:
        print("Error fetching data. Check your API key or stock symbol.")
        return pd.DataFrame()

# User input for stock symbol and interval
stock_symbol = input("Enter Stock Symbol (e.g., AAPL): ").upper()
interval = input("Enter Interval (1min, 5min, 15min, 30min, 60min): ")

# Fetch stock data
stock_data = fetch_stock_data(stock_symbol, interval)

if not stock_data.empty:
    print(f"\nLive Data for {stock_symbol} retrieved at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    print(stock_data.head(10))  # Display top 10 rows of data

    # Plot candlestick chart
    fig = go.Figure(data=[go.Candlestick(
        x=stock_data.index,
        open=stock_data['Open'],
        high=stock_data['High'],
        low=stock_data['Low'],
        close=stock_data['Close']
    )])
    fig.update_layout(
        title=f"{stock_symbol} Stock Price",
        xaxis_title="Time",
        yaxis_title="Price (USD)",
        template="plotly_dark"
    )
    fig.show()

    # Simple Moving Average (SMA)
    sma = stock_data['Close'].rolling(window=10).mean()
    plt.figure(figsize=(10, 5))
    plt.plot(stock_data.index, stock_data['Close'], label="Close Price")
    plt.plot(stock_data.index, sma, label="10-period SMA", color="orange")
    plt.title(f"{stock_symbol} - Close Price & SMA")
    plt.xlabel("Time")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid()
    plt.show()

    # Volume traded as bar chart
    plt.figure(figsize=(10, 5))
    plt.bar(stock_data.index, stock_data['Volume'], color='blue')
    plt.title(f"{stock_symbol} - Volume Traded")
    plt.xlabel("Time")
    plt.ylabel("Volume")
    plt.show()

else:
    print("No data available for the selected stock.")
