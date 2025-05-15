import yfinance as yf
import json
from datetime import datetime

def download_tqqq_data(symbol='TQQQ', start_date='2010-02-01', filename=None):
    """TQQQチャートデータを取得してJSONに保存"""
    end_date = datetime.today().strftime('%Y-%m-%d')
    data = yf.download(symbol, start=start_date, end=end_date)

    # MultiIndex 対策
    data.columns = [str(col) for col in data.columns]

    # DataFrameをJSON形式に変換
    json_data = []
    for date, row in data.iterrows():
        record = row.to_dict()
        record['Date'] = date.strftime('%Y-%m-%d')
        json_data.append(record)

    if filename is None:
        filename = f"{symbol}_chart_data.json"

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    print(f"✅ {filename} に保存しました")

def download_usd_jpy_rate(filename='usd_jpy_rate.json'):
    """現在のドル円レートを取得してJSONに保存"""
    usd_jpy_series = yf.download('USDJPY=X', period='1d')['Close']
    usd_jpy = float(usd_jpy_series.iloc[-1])

    usd_jpy_data = {
        "date": datetime.today().strftime('%Y-%m-%d'),
        "usd_jpy": usd_jpy
    }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(usd_jpy_data, f, ensure_ascii=False, indent=4)

    print(f"👉 現在のドル円レート: {usd_jpy:.2f} 円/USD")
    print(f"✅ {filename} に保存しました")

def main():
    download_tqqq_data()
    download_usd_jpy_rate()

if __name__ == '__main__':
    main()

