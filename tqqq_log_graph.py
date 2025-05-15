import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import ScalarFormatter, LogLocator
from datetime import datetime, timedelta
import numpy as np
from scipy.stats import linregress

def generate_tqqq_chart(
        tqqq_data_file='TQQQ_chart_data.json',
        usd_jpy_file='usd_jpy_rate.json',
        output_file='static/tqqq_chart_log.svg'
    ):
    """TQQQチャートSVGを作成して保存"""

    # ✅ データ読み込み
    with open(tqqq_data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    sample_keys = data[0].keys()
    print(f"👉 JSONカラム一覧: {sample_keys}")

    possible_keys = [
        'Adj Close',
        'Close',
        "('Adj Close', 'TQQQ')",
        "('Close', 'TQQQ')",
    ]
    price_key = next((key for key in possible_keys if key in sample_keys), None)
    if price_key is None:
        raise KeyError("データに価格カラムが見つかりませんでした。")

    dates = [datetime.strptime(item['Date'], '%Y-%m-%d') for item in data]
    closes = [item[price_key] for item in data]

    # ✅ 対数線形回帰
    x = mdates.date2num(dates)
    y = np.array(closes)
    log_y = np.log(y)
    slope, intercept, *_ = linregress(x, log_y)
    print(f"👉 対数回帰直線: slope={slope:.6f}, intercept={intercept:.2f}")

    # ✅ 最新価格
    latest_date = dates[-1]
    latest_price = closes[-1]

    # ✅ 年成長率
    TRADING_DAYS_PER_YEAR = 252
    annual_growth_rate = np.exp(slope * TRADING_DAYS_PER_YEAR) - 1
    annual_growth_percent = annual_growth_rate * 100

    # ✅ 15年後予測
    future_date = latest_date + timedelta(days=365*15)
    future_x = mdates.date2num(future_date)
    future_price = np.exp(intercept + slope * future_x)

    # ✅ 回帰線
    start_date = min(dates)
    extended_dates = mdates.drange(start_date, future_date, timedelta(days=1))
    regression_line = np.exp(intercept + slope * extended_dates)

    # ✅ ドル円レート
    with open(usd_jpy_file, 'r', encoding='utf-8') as f:
        usd_jpy_data = json.load(f)
    usd_jpy = usd_jpy_data['usd_jpy']
    usd_jpy_date = usd_jpy_data['date']

    # ✅ 円換算価格
    latest_price_jpy = latest_price * usd_jpy
    future_price_jpy = future_price * usd_jpy

    # ✅ プロット
    plt.figure(figsize=(12, 6))
    plt.plot(dates, closes, label=f'TQQQ {price_key}', color='blue', linewidth=1.5)
    plt.plot(mdates.num2date(extended_dates), regression_line,
             label=f'Log-Linear Regression (to {future_date.strftime("%Y-%m-%d")})',
             color='red', linestyle='--', linewidth=2)
    plt.title('TQQQ Chart with Log-Scale Linear Regression (+15 years forecast)')
    plt.xlabel('Date')
    plt.ylabel('Price (USD, Log Scale)')
    plt.yscale('log')
    plt.grid(True, which='both')
    plt.legend()

    # x軸
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    # y軸
    ax.yaxis.set_major_locator(LogLocator(base=10.0, subs=(1.0, 2.0, 5.0), numticks=100))
    ax.yaxis.set_major_formatter(ScalarFormatter())

    plt.gcf().autofmt_xdate()

    # ✅ 注釈
    print(f"👉 年成長率: {annual_growth_percent:.2f}%")
    print(f"👉 最新価格 ({latest_date.strftime('%Y-%m-%d')}): ${latest_price:.2f} / ¥{latest_price_jpy:,.0f}")
    print(f"👉 {future_date.strftime('%Y-%m-%d')} 予測価格: ${future_price:.2f} / ¥{future_price_jpy:,.0f}")

    textstr = (
        f"Latest Close ({latest_date.strftime('%Y-%m-%d')}): ${latest_price:.2f} / ¥{latest_price_jpy:,.0f}\n"
        f"USDJPY Rate ({usd_jpy_date}): {usd_jpy:.2f} ¥/$\n"
        f"Estimated Annual Growth Rate: {annual_growth_percent:.2f}%\n"
        f"Predicted Price on {future_date.strftime('%Y-%m-%d')}: ${future_price:.2f} / ¥{future_price_jpy:,.0f}"
    )
    plt.text(0.02, 0.98, textstr, transform=ax.transAxes,
             fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))

    # ✅ 保存
    plt.savefig(output_file, format='svg')
    plt.close()
    print(f"✅ SVGファイル ({output_file}) を作成しました")

# モジュール実行時
if __name__ == '__main__':
    generate_tqqq_chart()


