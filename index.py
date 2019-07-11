from flask import Flask, Response, __version__


app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return Response('<h1>Flask on Now 2.0 {}</h1>'.format(__version__), mimetype='text/html')
