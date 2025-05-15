from flask import Flask, jsonify
from datetime import datetime, timezone, timedelta
import os
import json
from flask_cors import CORS
import tqqq

app = Flask(__name__)
CORS(app)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    return response

@app.route('/')
def index():
    return '''
    <h1>TQQQ Data API</h1>
    <p>
    <a href="/latest_price">/latest_price</a><br>
    <a href="/usd_jpy">/usd_jpy</a><br>
    <a href="/tqqq_data">/tqqq_data</a>
    </p>
    '''

@app.route('/latest_price')
def latest_price():
    try:
        
        tqqq.download_tqqq_data()

        with open('TQQQ_chart_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        with open('usd_jpy_rate.json', 'r', encoding='utf-8') as f:
            usd_data = json.load(f)

        latest = data[-1]
        price_usd = latest.get('Close') or latest.get('Adj Close') or latest.get("('Close', 'TQQQ')") or latest.get("('Adj Close', 'TQQQ')")
        date = latest['Date']
        price_jpy = price_usd * usd_data['usd_jpy']

        return jsonify({
            'date': date,
            'price_usd': round(price_usd, 2),
            'price_jpy': round(price_jpy)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/usd_jpy')
def usd_jpy():
    try:
        tqqq.download_usd_jpy_rate()

        with open('usd_jpy_rate.json', 'r', encoding='utf-8') as f:
            usd_data = json.load(f)

        return jsonify({
            'date': usd_data['date'],
            'usd_jpy': round(usd_data['usd_jpy'], 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tqqq_data')
def tqqq_data():
    try:
        tqqq.download_tqqq_data()

        if not os.path.exists('TQQQ_chart_data.json'):
            return jsonify({"error": "TQQQ_chart_data.json not found"}), 500

        with open('TQQQ_chart_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

