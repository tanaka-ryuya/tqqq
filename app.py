from flask import Flask, send_from_directory
from datetime import datetime,timezone
import os
import generate_chart

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
    return '<h1>TQQQ Chart API</h1><p>Access <a href="/static/tqqq_chart.svg">/static/tqqq_chart.svg</a><br><a href="/static/tqqq_chart_log.svg">/static/tqqq_chart_log.svg</a> to get the latest chart.</p>'

@app.route('/tqqq_chart')
def get_chart():
    if needs_update("static/tqqq_chart.svg"):
        print("✅ チャートが古いため再生成します...")
        generate_chart.generate_tqqq_chart()
    else:
        print("✅ チャートは最新。再生成しません。")
    return send_from_directory('static', 'tqqq_chart.svg', mimetype='image/svg+xml')

@app.route('/tqqq_chart_log')
def get_chart_log():
    if needs_update("static/tqqq_chart_log.svg"):
        print("✅ チャートが古いため再生成します...")
        generate_chart.generate_tqqq_chart_log()
    else:
        print("✅ チャートは最新。再生成しません。")
    return send_from_directory('static', 'tqqq_chart_log.svg', mimetype='image/svg+xml')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)