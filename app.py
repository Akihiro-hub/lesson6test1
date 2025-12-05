# app.py
# 標準ライブラリのみで動作するBMI計算Webアプリ
# Render/ローカル共通。PORTは環境変数から取得

import os
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs

def app(environ, start_response):
    # クエリパラメータ取得
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size)
    params = parse_qs(request_body.decode('utf-8'))

    height = params.get('height', [''])[0]
    weight = params.get('weight', [''])[0]
    bmi_result = ""
    eval_result = ""

    try:
        h = float(height) / 100.0  # cm→m
        w = float(weight)
        if h > 0 and w > 0:
            bmi = w / (h * h)
            bmi_result = f"{bmi:.2f}"
            if bmi < 18.5:
                eval_result = "低体重"
            elif bmi < 25:
                eval_result = "標準"
            elif bmi < 30:
                eval_result = "肥満（1度）"
            else:
                eval_result = "肥満（2度以上）"
        else:
            bmi_result = "0"
            eval_result = "入力値が不正です"
    except Exception:
        bmi_result = "0"
        eval_result = "入力値が不正です"

    # HTMLレスポンス
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>BMI計算機</title>
<style>
body {{ font-family: sans-serif; margin: 2em; }}
input {{ margin: 0.5em; }}
.result {{ margin-top: 1em; font-weight: bold; }}
</style>
<script>
function clearForm() {{
    document.getElementById('height').value = '';
    document.getElementById('weight').value = '';
}}
</script>
</head>
<body>
<h1>BMI計算機</h1>
<form method="POST">
    <label>身長(cm): <input type="number" id="height" name="height" value="{height}"></label><br>
    <label>体重(kg): <input type="number" id="weight" name="weight" value="{weight}"></label><br>
    <button type="submit">計算する</button>
    <button type="button" onclick="clearForm()">クリア</button>
</form>
<div class="result">
    BMI: {bmi_result} <br>
    評価: {eval_result}
</div>
</body>
</html>
"""
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    return [html.encode('utf-8')]

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    with make_server("0.0.0.0", port, app) as httpd:
        print(f"Serving on port {port}...")
        httpd.serve_forever()