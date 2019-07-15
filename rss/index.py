import requests
import datetime
from bs4 import BeautifulSoup
from flask import Flask, Response
from feedgen.feed import FeedGenerator
import arrow


app = Flask(__name__)
source = 'https://github.com/zeit/now-examples/tree/master/python-flask'
css = '<link rel="stylesheet" href="/css/style.css" />'

"""
curl 'https://www.nasdaqtrader.com/RPCHandler.axd' -H 'Origin: https://www.nasdaqtrader.com' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36' -H 'Content-type: application/json' -H 'Accept: */*' -H 'Referer: https://www.nasdaqtrader.com/Trader.aspx?id=archiveheadlines&cat_id=105' -H 'Cookie: ASP.NET_SessionId=3go24gkjl30e4s3aehunangp' -H 'Connection: keep-alive' --data-binary '{"id":2,"method":"BL_NewsListing.GetArchiveHeadlinesPageData","params":"[\"105\",2019,0]","version":"1.1"}' --compressed
"""

source_url = 'https://www.nasdaqtrader.com/Trader.aspx?id=archiveheadlines&cat_id=105'
url = 'https://www.nasdaqtrader.com/RPCHandler.axd'
headers = {
    'Content-type': 'application/json',
    'Host': 'www.nasdaqtrader.com',
    'Origin': 'https://www.nasdaqtrader.com',
    'Referer': source_url,
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}
req_data = {
    "id": 2,
    "method": "BL_NewsListing.GetArchiveHeadlinesPageData",
    "params": "[\"105\",2019,0]",
    "version": "1.1",
}


class RequestError(Exception):
    pass


def get_corporate_actions_html():
    resp = requests.post(url, headers=headers, json=req_data)
    if resp.status_code != 200:
        raise RequestError()
    d = resp.json()
    return d['result']  # raise KeyError


def parse_html_to_feed(html):
    soup = BeautifulSoup(html, features='html.parser')
    fg = FeedGenerator()
    fg.language('en')
    fg.title('Nasdaqtrader Corporate Actions')
    fg.description('Nasdaqtrader Corporate Actions')
    fg.link(dict(
        href=source_url,
        rel='alternate',
    ))

    tb = soup.find('table')

    """
    Date		Market	Alert #		Headline
    Jul 05, 2019	NASDAQ	#2019-129	<a>(UPDATED) Information Regarding the Merger of Realm Therapeutics plc (RLM)</a>

    rss example: https://www.nasdaqtrader.com/rss.aspx?feed=currentheadlines&categorylist=2,6,7
    """

    for tr in tb.find('tbody').find_all('tr'):
        if not tr:
            continue
        tds = tr.find_all('td')
        if not tds:
            continue
        row = []
        fe = fg.add_entry()
        for item in tds:
            row.append(item.text.strip())
        # lg.debug('parsing table row: %s', row)

        url = tds[-1].find('a')['href']
        date_str, market, id, headline = row[0], row[1], row[2], row[3]
        date = datetime.datetime.strptime(date_str, '%b %d, %Y')
        arrow_date = arrow.get(date, 'America/New_York')
        fe.id(url)
        fe.title(headline)
        fe.link(dict(
            href=url,
            rel='alternate',
        ))
        fe.description(headline)
        fe.content("""
<table>
    <thead>
        <th>
            <td>Date</td>
            <td>Market</td>
            <td>Alert #</td>
            <td>Headline</td>
        <th>
    </thead>
    <tbody>
        <tr>
            {}
        </tr>
    </tbody>
</table>
""".format(tr))
        #fe.link(url)
        fe.pubDate(arrow_date.datetime)

    return fg.rss_str(pretty=True)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    try:
        html = get_corporate_actions_html()
    except (KeyError, RequestError) as e:
        return Response(f'Error: {e}', mimetype='text/html')
    feed = parse_html_to_feed(html)
    return Response(feed, mimetype='text/xml')
