import numpy as np
import time
from statsmodels.tsa.stattools import coint

class PairTradingStrategy:
    def __init__(self, api):
        self.api = api
        self.symbol_a = 'SOL/USDT'
        self.symbol_b = 'ADA/USDT'
        self.amount = 10

    def check_cointegration(self, prices_a, prices_b):
        score, pvalue, _ = coint(prices_a, prices_b)
        return pvalue < 0.05

    def run(self):
        while True:
            data_a = self.api.fetch_ohlcv(self.symbol_a)
            data_b = self.api.fetch_ohlcv(self.symbol_b)
            prices_a = [x[4] for x in data_a]
            prices_b = [x[4] for x in data_b]

            if self.check_cointegration(prices_a, prices_b):
                spread = np.array(prices_a) - np.array(prices_b)
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
