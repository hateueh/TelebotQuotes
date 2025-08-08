import time
import random
import requests
from threading import Thread
from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# جلب المحتوى من GitHub
url = "https://gist.githubusercontent.com/hateueh/22148fc45d3347e49bbfbe52b972c00e/raw/126e4d046fc26311a8a9d3c0b077dbfb68307a5f/gistfile1.txt"
response = requests.get(url)
quotes_list = response.text.splitlines()
print('✅ تم جلب المحتوى')

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

def run_bot():
    while True:
        if quotes_list:
            random_quote = random.choice(quotes_list)
            if random_quote.strip():
                send_message(random_quote)
                print(f"✅ تم الإرسال: {random_quote[:50]}...")
            else:
                print("🚫 سطر فارغ، يتم تخطيه.")
        else:
            print("🚫 لا يوجد اقتباسات متاحة.")
        time.sleep(1800)

app = Flask('')

@app.route('/')
def home():
    return 'Bot is running!', 200

def run_web():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    t1 = Thread(target=run_web)
    t2 = Thread(target=run_bot)
    t1.start()
    t2.start()