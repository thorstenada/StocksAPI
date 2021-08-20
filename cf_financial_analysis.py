import pandas as pd
import numpy as np
import talib
import yfinance as yf

import matplotlib.pyplot as plt
from matplotlib.pylab import date2num
from mplfinance.original_flavor import candlestick_ohlc

def compute_indicators(df):
    #https://www.ta-lib.org/function.html
    #https://acatay.de/aktienanalyse/schnellstart-technische-aktienanalyse-mit-python/
    # compute macd
    df['macd'], df['macd_signal'], df['macd_hist'] = talib.MACD(df['Close'])
    
    # compute moving averages for 10 and 30 days
    df['ma10'] = talib.MA(df['Close'], timeperiod=10)
    df['ma30'] = talib.MA(df['Close'],timeperiod=30)
    
    # compute rsi
    df['rsi'] = talib.RSI(df['Close'])
    
    #compute momentum
    df['mom10'] = talib.MOM(df['Close'], timeperiod=10)
    df['mom30'] = talib.MOM(df['Close'], timeperiod=10)
    
    #compute t3
    df['t3'] = talib.T3(df['Close'], timeperiod=10, vfactor=0)
    
   #compute stochhastic slow
    df['stoch_slowd'], df['stoch_slowk'] = talib.STOCH(df['High'], df['Low'], df['Close'], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    
    #compute stochhastic fast
    df['stoch_fastk'], df['stoch_fastd'] = talib.STOCHF(df['High'], df['Low'], df['Close'], fastk_period=5, fastd_period=3, fastd_matype=0)
    
    #compute BETA
    df['beta'] = talib.BETA(df['High'], df['Low'], timeperiod=5)
    
    #compute three-line-strike
    df['three_line_strike'] = talib.CDL3LINESTRIKE(df['Open'], df['High'], df['Low'], df['Close'])
    
    return df

def get_ticker(ticker):
    # Get Yahoo Finance Data https://pypi.org/project/yfinance/
    df = yf.Ticker(ticker)
    # get historical market data
    hist = df.history(period="max")    
    return hist

def perform_technical_analysis(ticker, n=180):
 
    #df = pd.read_csv(f'./data/{ticker}.csv', sep=';', parse_dates=True, header=0, index_col=0)
    df = get_ticker(ticker)
    
    # filter number of observations to plot
    df = compute_indicators(df)
    df = df.iloc[-n:]
    
    # set up figure and axes for subplots
    fig = plt.figure()
    fig.set_size_inches((20, 16))
    ax_candle = fig.add_axes((0, 0.72, 1, 0.32))
    ax_macd = fig.add_axes((0, 0.48, 1, 0.2), sharex=ax_candle)
    ax_rsi = fig.add_axes((0, 0.24, 1, 0.2), sharex=ax_candle)
    ax_vol = fig.add_axes((0, 0, 1, 0.2), sharex=ax_candle)
    ax_candle.xaxis_date()
    
    # create array of date, open, high, low and close data
    ohlc = []
    for date, row in df.iterrows():
        openp, highp, lowp, closep = row[:4]
        ohlc.append([date2num(date), openp, highp, lowp, closep])
    
    # plot candlestick chart
    ax_candle.set_ylabel("Stock Price")
    ax_candle.plot(df.index, df["ma10"], label="MA10", color='#006699', alpha=0.5)
    ax_candle.plot(df.index, df["ma30"], label="MA30", color="#ff0066")
    candlestick_ohlc(ax_candle, ohlc, colorup="#006699", colordown="#ff0066", width=0.8)
    ax_candle.legend()
    
    # plot macd
    ax_macd.set_ylabel("MACD")
    ax_macd.plot(df.index, df["macd"], label="macd", color="#ff0066")
    ax_macd.bar(df.index, df["macd_hist"] * 3, label="hist", color='lightgrey')
    ax_macd.plot(df.index, df["macd_signal"], label="signal", color='#006699')
    ax_macd.legend()
    
    # plot rsi
    ax_rsi.set_ylabel("RSI (%)")
    ax_rsi.set_ylim(10,90)
    ax_rsi.plot(df.index, [70] * len(df.index), label="overbought", color='#006699', alpha=0.5)
    ax_rsi.plot(df.index, [30] * len(df.index), label="oversold", color='#006699')
    ax_rsi.plot(df.index, df["rsi"], label="rsi", color='#ff0066')
    ax_rsi.legend(loc='upper left')
    
    # plot valume bars
    ax_vol.bar(df.index, df["Volume"] / 1000000, color='lightgrey')
    ax_vol.set_ylabel("Volume (Million)")
    
    # save chart
    ticker = ticker.replace(".", "_")
    fig.savefig(f'Analyse_{ticker}', bbox_inches="tight")
    plt.close(fig) 
    
    return "Analyse_"+ticker+".png" #plt.show()

def get_financial_analysis_df(ticker):
    return compute_indicators(get_ticker(ticker)).reset_index()
