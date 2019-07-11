import requests
from flask import Flask, Response


app = Flask(__name__)
source = 'https://github.com/zeit/now-examples/tree/master/python-flask'
css = '<link rel="stylesheet" href="/css/style.css" />'

"""
curl 'https://www.nasdaqtrader.com/RPCHandler.axd' -H 'Origin: https://www.nasdaqtrader.com' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36' -H 'Content-type: application/json' -H 'Accept: */*' -H 'Referer: https://www.nasdaqtrader.com/Trader.aspx?id=archiveheadlines&cat_id=105' -H 'Cookie: ASP.NET_SessionId=3go24gkjl30e4s3aehunangp' -H 'Connection: keep-alive' --data-binary '{"id":2,"method":"BL_NewsListing.GetArchiveHeadlinesPageData","params":"[\"105\",2019,0]","version":"1.1"}' --compressed
"""

url = 'https://www.nasdaqtrader.com/RPCHandler.axd'
headers = {
    'Content-type': 'application/json',
    'Host': 'www.nasdaqtrader.com',
    'Origin': 'https://www.nasdaqtrader.com',
    'Referer': 'https://www.nasdaqtrader.com/Trader.aspx?id=archiveheadlines&cat_id=105',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}
req_data = {
    "id": 2,
    "method": "BL_NewsListing.GetArchiveHeadlinesPageData",
    "params": "[\"105\",2019,0]",
    "version": "1.1",
}


def get_corporate_actions_html():
    resp = requests.post(url, headers=headers, json=req_data)
    if resp.status_code != 200:
        return resp.content
    d = resp.json()
    return d['result']


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return Response(get_corporate_actions_html(), mimetype='text/html')
