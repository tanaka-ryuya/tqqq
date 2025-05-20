## 私の億万長者計画

読者諸君、新NISAがはじまって久しいが、賢明な防衛的投資家である諸君はS&P500と米国債券に積み立て投資して幾ばくかの含み益を得ていることであろう。  
私は多少の冒険的投資家であるからして、S&P500に月々**10万円積み立て投資**していた。

米国の経済成長が現状を維持し続け、このまま**25年**ぐらいたてば、資産**1億円**を超える計画であるが、私も今年**40歳**。  
**65歳**でそのような大金手にしたところで墓場には持ってゆけないことに不満を覚えた。

かくなるうえは健全な市民としてジャンボ宝くじによる一攫千金をこころみるも、あたるわけもない。

そこで今、巷で流行中である**ChatGPT**に問いかけた。  
**今後15年で資産1億円を超え、55歳で早期退職し、海外旅行三昧の悠々自適生活をおくるためにはいかなる投資方法で夢をみるべきか。**

月々積み立てられる限度額は**10万円**。  
なかなか難しい条件ではあるが、私は幸いにして**ある信念**を有している。

世界の基軸通貨を持ち、常に技術の最先端にあり、自国経済のためには他国と争うこともいとわない国。  
**米国の経済は今後も持続的な成長を維持する**という信念である。

この信念に従って冒険するにはいかなる投資をすべきか問い続けたところ**ChatGPTの回答**によって以下の結論を得た。

- **TQQQに毎月10万円投資せよ。**

## TQQQとは何か？

**TQQQ**とは、NASDAQ100指数の**3倍の値動き**を目指す米国ETFである。  
通常のNASDAQ100が1%上昇すれば、TQQQは理論上**3%上昇**する。  
もちろん下落時も同様に3倍となるため**非常にハイリスク・ハイリターン**な投資商品である。
チャートをみると下のような感じ。

<h2>✅ TQQQチャート（普通スケール）</h2>

<iframe src="https://enjaku.com/tqqq-graph.html" width="800" height="500" frameborder="0"></iframe>

青い線がTQQQの終値を結んだもの。
赤い線は私が期待してる成長の曲線。
山が並んで、すさまじい暴投と暴落を繰り返してるように見える。
がまぁいつのタイミングで見てもこんな感じである。
対数グラフで表示するとよく見えてくる。

<h2>✅ TQQQチャート（対数スケール）</h2>
<iframe src="https://enjaku.com/tqqq-graph-log.html" width="800" height="600" frameborder="0"></iframe>

対数グラフになると大体ずっと同じ直線の上を歩んでいるのがわかるだろう。
このまま未来永劫進みそうではないか。
未来もこうであってほしいものである。普通スケールでみているとすさまじい暴投と暴落に
みえるが、対数グラフでみるといつもの変動にみえてくる。ちなみに
このグラフでいくと今日の1万円が15年後2000万円になっている計算である。

## 夢の億万長者計画：TQQQシミュレーション

私の計画はこうだ。

**月々10万円 × 15年間 = 元本1,800万円**

TQQQの過去の年平均成長率は**約46%**（実績ベースでは30～50%の範囲とも言われる）。  
仮に**年平均25%で複利運用**できた場合  
15年後には約**1億円**に達する計算となる。
そして、なんと過去の成長が続いて46％の場合には
15年後には約**3億円**に到達する。

- 宝くじでは夢物語だった**3億円**が
- 資産運用なら**現実味のある数値**として見えてくる。




## 最後に

**55歳までに１億円達成**  
👉 **その瞬間に会社を辞めることをここに宣言する。**

読者諸君。  
共にこの**夢の実験**に立ち会ってくれたまえ。

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
(async function() {
    const infoDiv = document.getElementById("info");
    infoDiv.innerHTML = "⏳ データ読み込み中...";
    const response = await fetch("https://tqqq-server.onrender.com/tqqq_data");
    const data = await response.json();

    const keys = Object.keys(data[0]);
    const possibleKeys = [
        'Adj Close', 'Close',
        "('Adj Close', 'TQQQ')", "('Close', 'TQQQ')"
    ];
    const priceKey = possibleKeys.find(key => keys.includes(key));
    if (!priceKey) return alert("価格データがありません");

    const dates = data.map(item => item.Date);
    const closes = data.map(item => item[priceKey]);

    function linearRegression(x, y) {
        const n = x.length;
        const logY = y.map(v => Math.log(v));
        const sumX = x.reduce((a,b) => a+b, 0);
        const sumY = logY.reduce((a,b) => a+b, 0);
        const sumXY = x.reduce((acc, xi, i) => acc + xi * logY[i], 0);
        const sumX2 = x.reduce((acc, xi) => acc + xi * xi, 0);
        const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
        const intercept = (sumY - slope * sumX) / n;
        return { slope, intercept };
    }

    const dateNums = dates.map((_, i) => i);
    const { slope, intercept } = linearRegression(dateNums, closes);
    const regression = dateNums.map(x => Math.exp(intercept + slope * x));

    // 👇 WordPress複数ロード防止
    if (window.tqqqChartInstance) window.tqqqChartInstance.destroy();
    const ctx = document.getElementById('tqqqChart').getContext('2d');
    window.tqqqChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [
                { label: 'TQQQ', data: closes, borderColor: 'blue', borderWidth: 1.5, tension: 0, pointRadius: 0 },
                { label: 'Log-Linear Regression', data: regression, borderColor: 'red', borderWidth: 2, borderDash: [5, 5], tension: 0, pointRadius: 0 }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: { type: 'category', title: { display: true, text: 'Date' }, ticks: { maxTicksLimit: 15 }},
                y: { title: { display: true, text: 'Price (USD)' }}
            },
            plugins: { legend: { display: true }, title: { display: true, text: 'TQQQ Chart with Log-Linear Regression' }}
        }
    });
})();
</script>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
(async function() {
    const infoDiv2 = document.getElementById("info");
    infoDiv2.innerHTML = "⏳ データ読み込み中...";
    // --- fetch メインデータ ---
    const response = await fetch("https://tqqq-server.onrender.com/tqqq_data");
    const data = await response.json();

    const keys = Object.keys(data[0]);
    const possibleKeys = [
        'Adj Close', 'Close',
        "('Adj Close', 'TQQQ')", "('Close', 'TQQQ')"
    ];
    const priceKey = possibleKeys.find(key => keys.includes(key));
    if (!priceKey) return alert("価格データがありません");

    const dates = data.map(item => item.Date);
    const closes = data.map(item => item[priceKey]);

    function linearRegression(x, y) {
        const n = x.length;
        const logY = y.map(v => Math.log(v));
        const sumX = x.reduce((a,b) => a+b, 0);
        const sumY = logY.reduce((a,b) => a+b, 0);
        const sumXY = x.reduce((acc, xi, i) => acc + xi * logY[i], 0);
        const sumX2 = x.reduce((acc, xi) => acc + xi * xi, 0);
        const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
        const intercept = (sumY - slope * sumX) / n;
        return { slope, intercept };
    }

    const dateNums = dates.map((_, i) => i);
    const { slope, intercept } = linearRegression(dateNums, closes);

    const extraDays = Math.round(365 * 15);
    const extendedNums = [...dateNums];
    const last = dateNums[dateNums.length - 1];

    const lastDateStr = dates[dates.length - 1];
    const lastDate = new Date(lastDateStr);
    for (let i = 1; i <= extraDays; i++) {
        const futureDate = new Date(lastDate);
        futureDate.setDate(futureDate.getDate() + i);
        const yyyy = futureDate.getFullYear();
        const mm = String(futureDate.getMonth() + 1).padStart(2, '0');
        const dd = String(futureDate.getDate()).padStart(2, '0');
        dates.push(`${yyyy}-${mm}-${dd}`);
        extendedNums.push(last + i);
    }

    const regression = extendedNums.map(x => Math.exp(intercept + slope * x));
    const closesExtended = [...closes];
    for (let i = 0; i < extraDays; i++) closesExtended.push(null);

    // --- fetch ドル円 & 最新価格 ---
    const [usdJpyRes, latestPriceRes] = await Promise.all([
        fetch("https://tqqq-server.onrender.com/usd_jpy"),
        fetch("https://tqqq-server.onrender.com/latest_price")
    ]);
    const usdJpyData = await usdJpyRes.json();
    const latestPriceData = await latestPriceRes.json();

    const usdJpy = usdJpyData.usd_jpy;
    const latestUsd = latestPriceData.price_usd;
    const latestJpy = latestPriceData.price_jpy;
    const forecastUsd = regression[regression.length - 1];
    const forecastJpy = forecastUsd * usdJpy;

    // --- info表示 ---
    const infoDiv = document.getElementById("info");
    infoDiv.innerHTML = `
        <b>📅 現在: ${usdJpyData.date}</b><br>
        💱 ドル円: ${usdJpy.toFixed(2)}<br>
        📊 前日終値: ${latestUsd.toFixed(2)} USD / ${latestJpy.toLocaleString()} 円<br>
        🔮 15年後予測: ${forecastUsd.toFixed(2)} USD / ${Math.round(forecastJpy).toLocaleString()} 円
    `;

    // --- Chart描画 ---
    if (window.tqqqLogChartInstance) window.tqqqLogChartInstance.destroy();
    const ctx = document.getElementById('tqqqLogChart').getContext('2d');
    window.tqqqLogChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [
                { label: 'TQQQ', data: closesExtended, borderColor: 'blue', borderWidth: 1.5, tension: 0, pointRadius: 0 },
                { label: 'Log-Linear Regression (+15 years)', data: regression, borderColor: 'red', borderWidth: 2, borderDash: [5, 5], tension: 0, pointRadius: 0 }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: { type: 'category', title: { display: true, text: 'Date' }, ticks: { maxTicksLimit: 15 }},
                y: { type: 'logarithmic', title: { display: true, text: 'Price (USD)' }, ticks: {
                    callback: function(value) {
                        if (value === 1000) return '1k';
                        if (value === 1000000) return '1M';
                        return value;
                    }
                }}
            },
            plugins: { legend: { display: true }, title: { display: true, text: 'TQQQ Log Chart with 15-Year Forecast' }}
        }
    });

})();
</script>
