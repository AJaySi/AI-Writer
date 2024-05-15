import sys
import os
from textwrap import dedent
from pathlib import Path
from datetime import datetime

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

from ..ai_web_researcher.finance_data_researcher import get_finance_data, get_fin_options_data
from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


def write_basic_ta_report(symbol):
    """ Write financial TA for given ticker symbol """
    try:
        symbol_fin_data = get_finance_data(symbol)
        #get_visual_reports
        fin_report = gen_finta_report(symbol_fin_data, symbol)
        logger.info(f"Done: Final Technical Analysis for {symbol}:\n\n")
    except Exception as err:
        logger.error(f"Error: Failed to generate Financial report: {err}")

    #fin_options_data = get_fin_options_data(symbol)
    #options_report = gen_options_report(fin_options_data, symbol)



def gen_options_report(results_sentences, ticker):
    """ Call LLM to generate options report """
    prompt = f"""
        You are a financial expert specializing in options trading and market sentiment analysis. 
        You have been provided with the following technical analysis of options data for the ticker symbol {ticker} with the nearest expiry date:

        {chr(10).join(results_sentences)}

        Based on this data, provide a comprehensive analysis of the options market for {ticker}.

        Your analysis should include:

        1. **Implied Volatility Interpretation:** Discuss the significance of the average implied volatility for both call and put options. What does it suggest about market expectations of future price movements?
        2. **Volume and Open Interest Insights:** Analyze the volume and open interest for call and put options. What does this data reveal about current market positioning and potential future trading activity?
        3. **Sentiment Analysis:** Evaluate the put-call ratio, implied volatility skew, and overall market sentiment. What do these indicators suggest about trader sentiment and potential future price direction?
        4. **Potential Trading Strategies:** Based on your analysis, suggest potential options trading strategies that could be employed for {ticker}, considering the current market conditions and sentiment.

        Please provide your analysis in a clear and concise manner, suitable for someone with a good understanding of options trading.
    """
    logger.info("Generating Financial Technical report..")
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)


def gen_finta_report(last_day_summary, symbol):
    """ Get AI to write TA report from given data """
    prompt = f"""
        You are a seasoned Technical Analysis (TA) expert, rivaling legends like Charles Dow, John Bollinger, and Alan Andrews. 
        Your deep understanding of market dynamics, coupled with mastery of technical indicators, 
        allows you to decipher complex patterns and offer precise predictions.

        Your expertise extends to practical tools like the pandas_ta module, enabling you to extract valuable insights from raw data.

        **Objective:**
        Analyze the provided technical indicators for {symbol} on its last trading day and predict its price movement over the next few trading sessions.

        **Instructions:**
        1. **Identify Potential Trading Signals:** Highlight specific indicators suggesting bullish, bearish, or neutral signals. Explain the rationale behind each signal, referencing historical patterns or comparable market scenarios.
        2. **Detect Patterns and Divergences:** Analyze the interplay between different indicators. Detect patterns like moving average crossovers, candlestick formations, or divergences between price action and indicators. Explain the significance of each pattern.
        3. **Price Movement Prediction:** Based on your analysis, provide a clear prediction for {symbol}'s price movement in the next few days. State the expected direction (up, down, sideways) and potential price targets if identifiable.
        4. **Risk Assessment:** Briefly discuss any potential risks or factors that could invalidate your predictions, promoting a balanced and informed perspective.

        **Technical Indicators for {symbol} on the Last Trading Day:**
        {last_day_summary}

        Remember, your analysis should be detailed, insightful, and actionable for traders seeking to capitalize on market movements.
    """

    logger.info("Generating Financial Technical report..")
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)
