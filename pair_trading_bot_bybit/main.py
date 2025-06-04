import threading
import time
from strategy import PairTradingStrategy
from bybit_api import BybitAPI

# Add Flask for minimal web server
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Pair Trading Bot is Running!"

def start_bot():
    api = BybitAPI()
    strategy = PairTradingStrategy(api)
    strategy.run()

if __name__ == "__main__":
    # Run your bot in a background thread
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.daemon = True
    bot_thread.start()

    # Start Flask server (required for Render Web Service)
    app.run(host="0.0.0.0", port=10000)
