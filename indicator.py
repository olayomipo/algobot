import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def initialize_mt5():
    """Initialize MetaTrader 5 and return True if successful."""
    if not mt5.initialize():
        print("Failed to initialize MetaTrader 5")
        return False
    return True


def get_data(symbol, timeframe, num_candles):
    """Fetch historical data for a given symbol and timeframe."""
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_candles)
    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')
    data.set_index('time', inplace=True)
    return data


def find_indicator(df, condition_func, column_name):
    """
    Generic function to add an indicator column based on a condition function.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        condition_func (callable): Function defining the condition.
        column_name (str): Name of the output column.
    """
    df[column_name] = np.nan
    for i in range(2, len(df) - 1):
        if condition_func(df, i):
            df.at[df.index[i], column_name] = df.iloc[i]['close']  # or another relevant value
    return df


# Specific condition functions
def is_fvg(df, i):
    return df['low'][i - 1] > df['high'][i] and df['low'][i - 2] > df['high'][i + 1]


def is_ifvg(df, i):
    return is_fvg(df, i)


def is_order_block(df, i):
    return df['close'][i] < df['open'][i] and df['close'][i + 1] > df['open'][i + 1]


def is_breaker_block(df, i):
    return df['close'][i] > df['open'][i] and df['close'][i + 1] < df['open'][i + 1]


def find_liquidity(df):
    """Identify sell-side and buy-side liquidity levels."""
    df['sell_liquidity'] = df['low'][df['low'] < df['low'].shift()]
    df['buy_liquidity'] = df['high'][df['high'] > df['high'].shift()]
    return df


# Main analysis
if initialize_mt5():
    symbol = "EURUSD"
    timeframe = mt5.TIMEFRAME_M15
    data = get_data(symbol, timeframe, 500)
    mt5.shutdown()

    data = find_indicator(data, is_fvg, 'fvg')
    data = find_indicator(data, is_ifvg, 'ifvg')
    data = find_indicator(data, is_order_block, 'order_block')
    data = find_indicator(data, is_breaker_block, 'breaker_block')
    data = find_liquidity(data)

    # Display and plot
    print(data.tail())
    plt.figure(figsize=(14, 8))
    plt.plot(data.index, data['close'], label='Close Price')
    plt.scatter(data.index, data['fvg'], color='red', label='FVG')
    plt.scatter(data.index, data['ifvg'], color='blue', label='IFVG')
    plt.scatter(data.index, data['order_block'], color='green', label='Order Block')
    plt.legend()
    plt.show()
