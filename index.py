from flask import Flask, Response


app = Flask(__name__)

tpl = """\
<!DOCTYPE html>
<html>
    <head>
        <title>Nasdaqtrader RSS</title>
    </head>
    <body>
        <h1>Nasdaqtrader RSS</h1>
        <p>Transform Nasdaqtrader news html page to rss API
        <br/>
        RSS List:
        </p>
        <ul>
            <li>News - Corporate Action Alerts: <a href="/rss">/rss</a>
            (<a href="https://www.nasdaqtrader.com/Trader.aspx?id=archiveheadlines&cat_id=105">source</a>)</li>
        </ul>
    </body>
</html>
"""


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return Response(tpl, mimetype='text/html')
