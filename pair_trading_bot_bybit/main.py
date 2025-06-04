from strategies.pair_trading import PairTradingStrategy
from exchange.bybit_api import BybitAPI

if __name__ == "__main__":
    api = BybitAPI()
    strategy = PairTradingStrategy(api)
    strategy.run()