import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import coint
import time

class PairTradingStrategy:
    def __init__(self, api):
        self.api = api
        self.symbol_a = 'BTC/USDT'
        self.symbol_b = 'ETH/USDT'
        self.amount = 0.01

    def check_cointegration(self, prices_a, prices_b):
        score, pvalue, _ = coint(prices_a, prices_b)
        return pvalue < 0.05

    def run(self):
        while True:
            data_a = self.api.fetch_ohlcv(self.symbol_a)
            data_b = self.api.fetch_ohlcv(self.symbol_b)
            prices_a = np.array([x[4] for x in data_a])
            prices_b = np.array([x[4] for x in data_b])

            if self.check_cointegration(prices_a, prices_b):
                spread = prices_a - prices_b
                zscore = (spread[-1] - spread.mean()) / spread.std()

                print(f"Z-Score: {zscore}")
                if zscore > 2:
                    print("Short A, Long B")
                    self.api.create_order(self.symbol_a, 'sell', self.amount)
                    self.api.create_order(self.symbol_b, 'buy', self.amount)
                elif zscore < -2:
                    print("Long A, Short B")
                    self.api.create_order(self.symbol_a, 'buy', self.amount)
                    self.api.create_order(self.symbol_b, 'sell', self.amount)
            else:
                print("Pair not cointegrated")

            time.sleep(60)