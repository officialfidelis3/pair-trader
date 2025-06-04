from flask import Flask
import threading
from strategy import PairTradingStrategy
from bybit_api import BybitAPI

app = Flask(__name__)

def run_bot():
    api = BybitAPI()
    strategy = PairTradingStrategy(api)
    strategy.run()

@app.route('/')
def home():
    return "Pair Trading Bot is running."

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    app.run(host='0.0.0.0', port=10000)