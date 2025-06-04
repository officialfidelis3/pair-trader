from flask import Flask, render_template, jsonify
import threading
from strategy import PairTradingStrategy
from bybit_api import BybitAPI
import json
import os

app = Flask(__name__)

def run_bot():
    api = BybitAPI()
    strategy = PairTradingStrategy(api)
    strategy.run()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data')
def data():
    if os.path.exists('dashboard_data.json'):
        with open('dashboard_data.json', 'r') as f:
            return jsonify(json.load(f))
    return jsonify({"zscore": 0, "symbol_a": "N/A", "symbol_b": "N/A", "last_trade": "None", "timestamp": "N/A"})

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    app.run(host='0.0.0.0', port=10000)