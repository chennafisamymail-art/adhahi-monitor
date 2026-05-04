import time
import requests

TELEGRAM_TOKEN = "8322512803:AAHnsXUd1Qn3f-ckcAwo3E2LRfYmo1DNOw0"
CHAT_ID = "5875283956"
CHECK_INTERVAL = 600

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ar,fr;q=0.9,en;q=0.8",
}

API_ENDPOINTS = [
    "https://adhahi.dz/api/wilayas",
    "https://adhahi.dz/api/locations",
    "https://adhahi.dz/api/availability",
    "https://adhahi.dz/api/wilayas/available",
    "https://adhahi.dz/api/communes",
    "https://adhahi.dz/api/slots",
]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}, timeout=10)
    except Exception as e:
        print(f"Telegram error: {e}")

def check_availability():
    for endpoint in API_ENDPOINTS:
        try:
            r = requests.get(endpoint, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                data = r.json()
                text = str(data)
                if "بومرداس" in text or "boumerdes" in text.lower():
                    if "false" in text.lower() or "غير متوفر" in text:
                        return False
                    if "true" in text.lower() or "متوفر" in text:
                        return True
        except:
            continue
    try:
        r = requests.get("https://adhahi.dz/register", headers=HEADERS, timeout=15)
        html = r.text
        if "بومرداس" in html:
            idx = html.find("بومرداس")
            snippet = html[idx:idx+300]
            if "غير متوفر" in snippet:
                return False
            elif "متوفر" in snippet:
                return True
    except Exception as e:
        print(f"HTML error: {e}")
    return None

def main():
    print("Monitor démarré!")
    send_telegram("🐑 <b>Monitor Adhahi démarré!</b>\nJe surveille <b>بومرداس</b> toutes les 10 minutes. 🔔")
    was_available = False
    check_count = 0
    while True:
        check_count += 1
        print(f"Check #{check_count}")
        available = check_availability()
        if available is True and not was_available:
            send_telegram("🎉🎉🎉 <b>بومرداس متاحة الآن!</b>\n👉 https://adhahi.dz/register")
            was_available = True
        elif available is False and was_available:
            send_telegram("❌ بومرداس أصبحت غير متاحة مجدداً.")
            was_available = False
        if check_count % 6 == 0:
            status = "✅ متوفر" if was_available else "❌ غير متوفر"
            send_telegram(f"📊 <b>Rapport horaire</b>\nبومرداس: {status}\nVérifications: {check_count}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
