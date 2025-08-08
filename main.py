import time
import random
import requests
from threading import Thread
from flask import Flask

TOKEN = "8147378986:AAEZebfAw_Kd6YTVPZUtG8yc48QMyjSKzFo"
CHAT_ID = "@kitquotes"

# جلب المحتوى من GitHub
url = "https://gist.githubusercontent.com/hateueh/22148fc45d3347e49bbfbe52b972c00e/raw/126e4d046fc26311a8a9d3c0b077dbfb68307a5f/gistfile1.txt"
response = requests.get(url)
quotes_list = response.text.splitlines()  # تقسيم النص إلى أسطر (كل سطر عبارة عن اقتباس)
print('✅ تم جلب المحتوى')

# إرسال الرسالة عبر Telegram
def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

# تشغيل البوت
def run_bot():
    while True:
        if quotes_list:
            random_quote = random.choice(quotes_list)  # اختيار سطر عشوائي
            if random_quote.strip():  # التأكد من أن السطر ليس فارغًا
                send_message(random_quote)
                print(f"✅ تم الإرسال: {random_quote[:50]}...")  # طباعة جزء من الاقتباس لتجنب إطالة الإخراج
            else:
                print("🚫 سطر فارغ، يتم تخطيه.")
        else:
            print("🚫 لا يوجد اقتباسات متاحة.")
        time.sleep(1800)  # انتظر 30 دقيقة (1800 ثانية)

# سيرفر ويب صغير
app = Flask('')

@app.route('/')
def home():
    return 'Bot is running!', 200

def run_web():
    app.run(host='0.0.0.0', port=8080)

# تشغيل كل شيء
if __name__ == '__main__':
    t1 = Thread(target=run_web)
    t2 = Thread(target=run_bot)
    t1.start()
    t2.start()