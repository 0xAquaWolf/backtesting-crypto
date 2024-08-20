import pandas as pd
import ccxt
import datetime
import time
import os
from tqdm import tqdm
from termcolor import colored

# Initialize the exchange - Using Phemex
# exchange = ccxt.phemex({"enableRateLimit": True})
exchange = ccxt.binance()  # need a VPN if your in the US

# Define the symbols
symbol = "BTCUSDT"  # This is the correct symbol for Phemex USDT-margined perpetual
timeframe = "1s"  # You can change this to any of the supported timeframes

# Calculate start and end times
end_time = datetime.datetime.now()
start_time = end_time - datetime.timedelta(days=365 * 5)  # 5 year worth of data

"""
'timeframes': {
    '1s': '1s',  # spot only for now
    '1m': '1m',
    '3m': '3m',
    '5m': '5m',
    '15m': '15m',
    '30m': '30m',
    '1h': '1h',
    '2h': '2h',
    '4h': '4h',
    '6h': '6h',
    '8h': '8h',
    '12h': '12h',
    '1d': '1d',
    '3d': '3d',
    '1w': '1w',
    '1M': '1M',
},
"""


# Function to fetch data in chunks
def fetch_ohlcv_data(start_time, end_time, timeframe):
    all_candles = []
    current_time = start_time

    timeframe_durations = {
        "1s": datetime.timedelta(seconds=1),
        "1m": datetime.timedelta(minutes=1),
        "3m": datetime.timedelta(minutes=3),
        "5m": datetime.timedelta(minutes=5),
        "15m": datetime.timedelta(minutes=15),
        "30m": datetime.timedelta(minutes=30),
        "1h": datetime.timedelta(hours=1),
        "2h": datetime.timedelta(hours=2),
        "4h": datetime.timedelta(hours=4),
        "6h": datetime.timedelta(hours=6),
        "8h": datetime.timedelta(hours=8),
        "12h": datetime.timedelta(hours=12),
        "1d": datetime.timedelta(days=1),
        "3d": datetime.timedelta(days=3),
        "1w": datetime.timedelta(weeks=1),
        "1M": datetime.timedelta(days=30),  # Approximation for 1 month
    }

    if timeframe not in timeframe_durations:
        raise ValueError(f"Unsupported timeframe: {timeframe}")

    duration = timeframe_durations[timeframe]

    # Calculate total number of iterations for progress bar
    total_iterations = (end_time - start_time) // duration

    # Start the timer
    start_time_perf = time.time()

    # Initialize progress bar
    pbar = tqdm(
        total=total_iterations,
        desc=colored("Fetching data", "cyan"),
        ncols=100,
        position=0,
        leave=True,
    )

    while current_time < end_time:
        try:
            candles = exchange.fetch_ohlcv(
                symbol,
                timeframe,
                since=int(current_time.timestamp() * 1000),
                limit=1000,
            )

            if not candles:
                break

            all_candles.extend(candles)

            # Update current_time to the last candle's time + 1 timeframe
            last_candle_time = datetime.datetime.fromtimestamp(candles[-1][0] / 1000)
            current_time = last_candle_time + duration

            # Update progress bar
            pbar.update(len(candles))

            # Print colored log message above the progress bar
            pbar.write(
                colored(
                    f"Fetched {len(candles)} candles. Next fetch from {current_time}",
                    "green",
                )
            )

            # Sleep to respect rate limits
            time.sleep(exchange.rateLimit / 1000)

        except ccxt.NetworkError as e:
            pbar.write(
                colored(
                    f"Network error occurred: {str(e)}. Retrying in 10 seconds...",
                    "yellow",
                )
            )
            time.sleep(10)
        except ccxt.ExchangeError as e:
            pbar.write(colored(f"Exchange error occurred: {str(e)}. Stopping.", "red"))
            break

    # Close progress bar
    pbar.close()

    # End the timer
    end_time_perf = time.time()

    # Calculate the execution time
    execution_time = end_time_perf - start_time_perf

    print(
        colored(f"\nData fetching completed in {execution_time:.2f} seconds", "magenta")
    )

    return all_candles, execution_time


# Fetch the data and measure performance
candles, fetch_time = fetch_ohlcv_data(start_time, end_time, timeframe)

# Create DataFrame
df = pd.DataFrame(
    candles, columns=["Timestamp", "Open", "High", "Low", "Close", "Volume"]
)

# Convert Timestamp to datetime and set as index
df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="ms")
df.set_index("Timestamp", inplace=True)

# Convert columns to appropriate types
df = df.astype(
    {
        "Open": "float64",
        "High": "float64",
        "Low": "float64",
        "Close": "float64",
        "Volume": "float64",
    }
)

print(df.dtypes)  # Print data types
print(df.head())  # Print the first few rows of the dataframe


# Function to calculate expected number of candles
def calculate_expected_candles(start_time, end_time, timeframe):
    timeframe_minutes = {
        "1s": 1 / 60,
        "1m": 1,
        "3m": 3,
        "5m": 5,
        "15m": 15,
        "30m": 30,
        "1h": 60,
        "2h": 120,
        "4h": 240,
        "6h": 360,
        "8h": 480,
        "12h": 720,
        "1d": 1440,
        "3d": 4320,
        "1w": 10080,
        "1M": 43200,  # Approximation for 1 month (30 days)
    }
    if timeframe not in timeframe_minutes:
        raise ValueError(f"Unsupported timeframe: {timeframe}")
    duration = end_time - start_time
    total_minutes = duration.total_seconds() / 60
    expected_candles = total_minutes / timeframe_minutes[timeframe]
    return int(expected_candles)


# Calculate and print expected number of candles
expected_candles = calculate_expected_candles(start_time, end_time, timeframe)
print(colored(f"Expected number of candles: {expected_candles}", "cyan"))
print(colored(f"Actual number of candles: {len(df)}", "cyan"))
print(colored(f"Total execution time: {fetch_time:.2f} seconds", "magenta"))

# df  # Return the dataframe for display in Jupyter


def save_exchange_data(df, exchange, symbol, timeframe, file_format="parquet"):
    # Extract the exchange name
    exchange_name = exchange.id.lower()  # This will give us 'binance' or 'phemex'

    # Check if 'Timestamp' is the index
    if df.index.name == "Timestamp":
        start_date = df.index.min().strftime("%Y%m%d")
        end_date = df.index.max().strftime("%Y%m%d")
    else:
        start_date = df["Timestamp"].min().strftime("%Y%m%d")
        end_date = df["Timestamp"].max().strftime("%Y%m%d")

    # Validate and set the file format
    if file_format.lower() not in ["csv", "parquet"]:
        raise ValueError("Invalid file format. Choose 'csv' or 'parquet'.")

    file_format = file_format.lower()

    # Create the directory structure
    base_dir = "./saved_candlestick_data"
    if exchange_name == "binance":
        directory = os.path.join(base_dir, exchange_name, file_format)
    else:  # for phemex and potentially other exchanges
        directory = os.path.join(
            base_dir, exchange_name, "parquet"
        )  # Always use 'parquet' for non-Binance exchanges

    os.makedirs(directory, exist_ok=True)

    # Create the dynamic filename
    if exchange_name == "binance":
        filename = f"{exchange_name}_{symbol}_{timeframe}_{start_date}_{end_date}.{file_format}"
    else:  # for phemex and potentially other exchanges
        filename = f"{symbol}_{timeframe}_{start_date}_{end_date}.parquet"  # Always use .parquet for non-Binance exchanges

    output_filename = os.path.join(directory, filename)

    # Save the file in the specified format
    if file_format == "csv" and exchange_name == "binance":
        df.to_csv(output_filename)
    else:  # parquet
        df.to_parquet(output_filename)

    print(f"Data saved as {file_format.upper()} file: {output_filename}")

    return output_filename


# Save the data in both CSV and Parquet formats
csv_file = save_exchange_data(df, exchange, symbol, timeframe, file_format="csv")
parquet_file = save_exchange_data(
    df, exchange, symbol, timeframe, file_format="parquet"
)

print(f"Data saved as CSV: {csv_file}")
print(f"Data saved as Parquet: {parquet_file}")

# Optional: Compare file sizes
import os

csv_size = os.path.getsize(csv_file)
parquet_size = os.path.getsize(parquet_file)

print(f"CSV file size: {csv_size / 1024 / 1024:.2f} MB")
print(f"Parquet file size: {parquet_size / 1024 / 1024:.2f} MB")
print(f"Parquet file is {csv_size / parquet_size:.2f}x smaller than CSV")
