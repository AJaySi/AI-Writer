import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import pandas_ta as ta
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_technical_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates a suite of technical indicators using pandas_ta.

    Args:
        data (pd.DataFrame): DataFrame containing historical stock price data.

    Returns:
        pd.DataFrame: DataFrame with added technical indicators.
    """
    try:
        # Moving Averages
        data.ta.macd(append=True)
        data.ta.sma(length=20, append=True)
        data.ta.ema(length=50, append=True)

        # Momentum Indicators
        data.ta.rsi(append=True)
        data.ta.stoch(append=True)

        # Volatility Indicators
        data.ta.bbands(append=True)
        data.ta.adx(append=True)

        # Other Indicators
        data.ta.obv(append=True)
        data.ta.willr(append=True)
        data.ta.cmf(append=True)
        data.ta.psar(append=True)

        # Custom Calculations
        data['OBV_in_million'] = data['OBV'] / 1e6 
        data['MACD_histogram_12_26_9'] = data['MACDh_12_26_9']

        logging.info("Technical indicators calculated successfully.")
        return data
    except KeyError as e:
        logging.error(f"Missing key in data: {e}")
    except ValueError as e:
        logging.error(f"Value error: {e}")
    except Exception as e:
        logging.error(f"Error during technical indicator calculation: {e}")
    return None

def get_last_day_summary(data: pd.DataFrame) -> pd.Series:
    """
    Extracts and summarizes technical indicators for the last trading day.

    Args:
        data (pd.DataFrame): DataFrame with calculated technical indicators.

    Returns:
        pd.Series: Summary of technical indicators for the last day.
    """
    try:
        last_day_summary = data.iloc[-1][[
            'Adj Close', 'MACD_12_26_9', 'MACD_histogram_12_26_9', 'RSI_14', 
            'BBL_5_2.0', 'BBM_5_2.0', 'BBU_5_2.0', 'SMA_20', 'EMA_50',
            'OBV_in_million', 'STOCHk_14_3_3', 'STOCHd_14_3_3', 'ADX_14', 
            'WILLR_14', 'CMF_20', 'PSARl_0.02_0.2', 'PSARs_0.02_0.2'
        ]]
        logging.info("Last day summary extracted.")
        return last_day_summary
    except KeyError as e:
        logging.error(f"Missing columns in data: {e}")
    except Exception as e:
        logging.error(f"Error extracting last day summary: {e}")
    return None

def analyze_stock(ticker_symbol: str, start_date: datetime, end_date: datetime) -> pd.Series:
    """
    Fetches stock data, calculates technical indicators, and provides a summary.

    Args:
        ticker_symbol (str): The stock symbol.
        start_date (datetime): Start date for data retrieval.
        end_date (datetime): End date for data retrieval.

    Returns:
        pd.Series: Summary of technical indicators for the last day.
    """
    try:
        # Fetch stock data
        stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
        logging.info(f"Stock data fetched for {ticker_symbol} from {start_date} to {end_date}")

        # Calculate technical indicators
        stock_data = calculate_technical_indicators(stock_data)

        # Get last day summary
        if stock_data is not None:
            last_day_summary = get_last_day_summary(stock_data)
            if last_day_summary is not None:
                print("Summary of Technical Indicators for the Last Day:")
                print(last_day_summary)
                return last_day_summary
        else:
            logging.error("Stock data is None, unable to calculate indicators.")
    except Exception as e:
        logging.error(f"Error during analysis: {e}")
    return None

def get_finance_data(symbol: str) -> pd.Series:
    """
    Fetches financial data for a given stock symbol.

    Args:
        symbol (str): The stock symbol.

    Returns:
        pd.Series: Summary of technical indicators for the last day.
    """
    end_date = datetime.today()
    start_date = end_date - timedelta(days=120)

    # Perform analysis
    last_day_summary = analyze_stock(symbol, start_date, end_date)
    return last_day_summary

def analyze_options_data(ticker: str, expiry_date: str) -> tuple:
    """
    Analyzes option data for a given ticker and expiry date.

    Args:
        ticker (str): The stock ticker symbol.
        expiry_date (str): The option expiry date.

    Returns:
        tuple: A tuple containing calculated metrics for call and put options.
    """
    call_df = options.get_calls(ticker, expiry_date)
    put_df = options.get_puts(ticker, expiry_date)

    # Implied Volatility Analysis:
    avg_call_iv = call_df["Implied Volatility"].str.rstrip("%").astype(float).mean()
    avg_put_iv = put_df["Implied Volatility"].str.rstrip("%").astype(float).mean()
    logging.info(f"Average Implied Volatility for Call Options: {avg_call_iv}%")
    logging.info(f"Average Implied Volatility for Put Options: {avg_put_iv}%")

    # Option Prices Analysis:
    avg_call_last_price = call_df["Last Price"].mean()
    avg_put_last_price = put_df["Last Price"].mean()
    logging.info(f"Average Last Price for Call Options: {avg_call_last_price}")
    logging.info(f"Average Last Price for Put Options: {avg_put_last_price}")

    # Strike Price Analysis:
    min_call_strike = call_df["Strike"].min()
    max_call_strike = call_df["Strike"].max()
    min_put_strike = put_df["Strike"].min()
    max_put_strike = put_df["Strike"].max()
    logging.info(f"Minimum Strike Price for Call Options: {min_call_strike}")
    logging.info(f"Maximum Strike Price for Call Options: {max_call_strike}")
    logging.info(f"Minimum Strike Price for Put Options: {min_put_strike}")
    logging.info(f"Maximum Strike Price for Put Options: {max_put_strike}")

    # Volume Analysis:
    total_call_volume = call_df["Volume"].str.replace('-', '0').astype(float).sum()
    total_put_volume = put_df["Volume"].str.replace('-', '0').astype(float).sum()
    logging.info(f"Total Volume for Call Options: {total_call_volume}")
    logging.info(f"Total Volume for Put Options: {total_put_volume}")

    # Open Interest Analysis:
    call_df['Open Interest'] = call_df['Open Interest'].str.replace('-', '0').astype(float)
    put_df['Open Interest'] = put_df['Open Interest'].str.replace('-', '0').astype(float)
    total_call_open_interest = call_df["Open Interest"].sum()
    total_put_open_interest = put_df["Open Interest"].sum()
    logging.info(f"Total Open Interest for Call Options: {total_call_open_interest}")
    logging.info(f"Total Open Interest for Put Options: {total_put_open_interest}")

    # Convert Implied Volatility to float
    call_df['Implied Volatility'] = call_df['Implied Volatility'].str.replace('%', '').astype(float)
    put_df['Implied Volatility'] = put_df['Implied Volatility'].str.replace('%', '').astype(float)

    # Calculate Put-Call Ratio
    put_call_ratio = total_put_volume / total_call_volume
    logging.info(f"Put-Call Ratio: {put_call_ratio}")

    # Calculate Implied Volatility Percentile
    call_iv_percentile = (call_df['Implied Volatility'] > call_df['Implied Volatility'].mean()).mean() * 100
    put_iv_percentile = (put_df['Implied Volatility'] > put_df['Implied Volatility'].mean()).mean() * 100
    logging.info(f"Call Option Implied Volatility Percentile: {call_iv_percentile}")
    logging.info(f"Put Option Implied Volatility Percentile: {put_iv_percentile}")

    # Calculate Implied Volatility Skew
    implied_vol_skew = call_df['Implied Volatility'].mean() - put_df['Implied Volatility'].mean()
    logging.info(f"Implied Volatility Skew: {implied_vol_skew}")

    # Determine market sentiment
    is_bullish_sentiment = call_df['Implied Volatility'].mean() > put_df['Implied Volatility'].mean()
    sentiment = "bullish" if is_bullish_sentiment else "bearish"
    logging.info(f"The overall sentiment of {ticker} is {sentiment}.")

    return (avg_call_iv, avg_put_iv, avg_call_last_price, avg_put_last_price,
            min_call_strike, max_call_strike, min_put_strike, max_put_strike,
            total_call_volume, total_put_volume, total_call_open_interest, total_put_open_interest,
            put_call_ratio, call_iv_percentile, put_iv_percentile, implied_vol_skew, sentiment)

def get_fin_options_data(ticker: str) -> list:
    """
    Fetches and analyzes options data for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        list: A list of sentences summarizing the options data.
    """
    current_price = round(stock_info.get_live_price(ticker), 3)
    option_expiry_dates = options.get_expiration_dates(ticker)
    nearest_expiry = option_expiry_dates[0]

    results = analyze_options_data(ticker, nearest_expiry)

    # Unpack the results tuple
    (avg_call_iv, avg_put_iv, avg_call_last_price, avg_put_last_price,
    min_call_strike, max_call_strike, min_put_strike, max_put_strike,
    total_call_volume, total_put_volume, total_call_open_interest, total_put_open_interest,
    put_call_ratio, call_iv_percentile, put_iv_percentile, implied_vol_skew, sentiment) = results

    # Create a list of complete sentences with the results
    results_sentences = [
        f"Average Implied Volatility for Call Options: {avg_call_iv}%",
        f"Average Implied Volatility for Put Options: {avg_put_iv}%",
        f"Average Last Price for Call Options: {avg_call_last_price}",
        f"Average Last Price for Put Options: {avg_put_last_price}",
        f"Minimum Strike Price for Call Options: {min_call_strike}",
        f"Maximum Strike Price for Call Options: {max_call_strike}",
        f"Minimum Strike Price for Put Options: {min_put_strike}",
        f"Maximum Strike Price for Put Options: {max_put_strike}",
        f"Total Volume for Call Options: {total_call_volume}",
        f"Total Volume for Put Options: {total_put_volume}",
        f"Total Open Interest for Call Options: {total_call_open_interest}",
        f"Total Open Interest for Put Options: {total_put_open_interest}",
        f"Put-Call Ratio: {put_call_ratio}",
        f"Call Option Implied Volatility Percentile: {call_iv_percentile}",
        f"Put Option Implied Volatility Percentile: {put_iv_percentile}",
        f"Implied Volatility Skew: {implied_vol_skew}",
        f"The overall sentiment of {ticker} is {sentiment}."
    ]

    # Print each sentence
    for sentence in results_sentences:
        logging.info(sentence)

    return results_sentences
