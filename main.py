import itertools
import typing
import logging
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import QuantLib as ql
import yfinance as yf
import pandas_market_calendars as mcal
import datetime
import time
from pathlib import Path
import os

# Own modules
from src.utils import path

if __name__ == "__main__":
    #############################################
    # SET UP LOGGER

    cur_dir = Path(__file__).parent
    log_file = path.get_logs_path(cur_dir=cur_dir).joinpath(
        f"log_file_{datetime.datetime.now().strftime('%Y%m%d_%H')}.log")
    


    logging.basicConfig(filename=log_file,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG) # TODO:
    
    logger_yq = logging.getLogger(name='main')
    logger_yq.info("\n##########START##########\n")
    
    hist_start = pd.to_datetime('2024-01-04') # Historical start date
    hist_end = pd.to_datetime('2024-01-12')
    # Define the ticker list
    ticker_list = ['BA']

    # Fetch the data
    dl_data = yf.download(ticker_list, start=hist_start, end=hist_end) # Auto adjust is false

    dl_data = pd.DataFrame(dl_data)
    data = dl_data.drop(columns=['Close'], axis=1)
    data = data.rename(columns={'Adj Close': 'Close'})
    logger_yq.debug(f'NA value count for each col: {data.isna().sum(axis=0)}') # Axis=0: along the indices, row-wise opertaion
    # Gives the sum for rows in a column
    data.index = pd.to_datetime(data.index)

    # TODO: Add the sentiment scores before the next market-open day
    # data['Sentiment'] = np.random.random(len(data)) * 2 - 1
    logger_yq.debug(f'Length of data df: {len(data)}')
    sentiment = np.array([0, -1, -0.8, 0, 0, 0]) # Put -1 on 01-05 (Before the whole thing Boeing case appeared after market closed on 01-05 to prepare to trade for 01-08)
    data['Sentiment'] = sentiment
    logger_yq.debug(f'The last 20 data:\n{data.tail(20)}')




