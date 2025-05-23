from flask import Flask, request, Response
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

@app.route('/')
def index():
    return "Proxy Server is running!"

@app.route('/go')
def proxy():
    url = request.args.get('url')
    if not url:
        return "Missing URL", 400

    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, stream=True)
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(k, v) for k, v in resp.raw.headers.items() if k.lower() not in excluded_headers]
        return Response(resp.content, resp.status_code, headers)
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
