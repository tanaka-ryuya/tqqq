from flask import Flask, send_from_directory, jsonify
from datetime import datetime, timezone, timedelta
import os
import json
import generate_chart
import matplotlib.dates as mdates
import numpy as np
from scipy.stats import linregress
import time

app = Flask(__name__, static_folder='static')

def needs_update(file_path):
    """ファイルの更新日が今日かどうかを判定"""
    if not os.path.exists(file_path):
        return True
    file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path), tz=timezone.utc)
    now = datetime.now(tz=timezone.utc)
    return file_mtime.date() != now.date()

@app.route('/')
def index():
    return '''
    <h1>TQQQ Chart API</h1>
    <p>
    <a href="/tqqq_chart">/tqqq_chart</a><br>
    <a href="/tqqq_chart_log">/tqqq_chart_log</a><br>
    <a href="/latest_price">/latest_price</a><br>
    <a href="/forecast">/forecast</a><br>
    <a href="/usd_jpy">/usd_jpy</a>
    </p>
    '''

@app.route('/tqqq_chart')
def get_chart():
    if needs_update("static/tqqq_chart.svg"):
        print("✅ チャートが古いため再生成します...")
        generate_chart.generate_tqqq_chart()
        for _ in range(5):
            if os.path.exists("static/tqqq_chart.svg"):
                break
            time.sleep(0.5)  # 0.5秒待つ
    else:
        print("✅ チャートは最新。再生成しません。")
    return send_from_directory('static', 'tqqq_chart.svg', mimetype='image/svg+xml')

@app.route('/tqqq_chart_log')
def get_chart_log():
    if needs_update("static/tqqq_chart_log.svg"):
        print("✅ チャートが古いため再生成します...")
        generate_chart.generate_tqqq_chart_log()
        for _ in range(5):
            if os.path.exists("static/tqqq_chart_log.svg"):
                break
            time.sleep(0.5)  # 0.5秒待つ
    else:
        print("✅ チャートは最新。再生成しません。")
    return send_from_directory('static', 'tqqq_chart_log.svg', mimetype='image/svg+xml')

@app.route('/latest_price')
def latest_price():
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

@app.route('/forecast')
def forecast():
    with open('TQQQ_chart_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open('usd_jpy_rate.json', 'r', encoding='utf-8') as f:
        usd_data = json.load(f)

    dates = [datetime.strptime(item['Date'], '%Y-%m-%d') for item in data]
    closes = [item.get('Close') or item.get('Adj Close') or item.get("('Close', 'TQQQ')") or item.get("('Adj Close', 'TQQQ')") for item in data]

    x = mdates.date2num(dates)
    y = np.array(closes)
    log_y = np.log(y)
    slope, intercept, *_ = linregress(x, log_y)

    latest_date = dates[-1]
    forecast_date = latest_date + timedelta(days=365*15)
    forecast_x = mdates.date2num(forecast_date)
    forecast_price_usd = np.exp(intercept + slope * forecast_x)
    forecast_price_jpy = forecast_price_usd * usd_data['usd_jpy']

    return jsonify({
        'forecast_date': forecast_date.strftime('%Y-%m-%d'),
        'forecast_price_usd': round(forecast_price_usd, 2),
        'forecast_price_jpy': round(forecast_price_jpy)
    })

@app.route('/usd_jpy')
def usd_jpy():
    with open('usd_jpy_rate.json', 'r', encoding='utf-8') as f:
        usd_data = json.load(f)

    return jsonify({
        'date': usd_data['date'],
        'usd_jpy': round(usd_data['usd_jpy'], 2)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
