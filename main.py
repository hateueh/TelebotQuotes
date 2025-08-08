import time
import random
import requests
from threading import Thread
from flask import Flask

TOKEN = "8147378986:AAEZebfAw_Kd6YTVPZUtG8yc48QMyjSKzFo"
CHAT_ID = "@kitquotes"

# بيانات GitHub
GITHUB_TOKEN = "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"
GIST_ID = "22148fc45d3347e49bbfbe52b972c00e"
FILENAME = "gistfile1.txt"

# جلب الاقتباس من GitHub Gist
def get_quote():
    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        gist_data = response.json()
        content = gist_data["files"][FILENAME]["content"]
        lines = content.splitlines()
        return random.choice(lines) if lines else "لا توجد اقتباسات متاحة."
    else:
        print("فشل في جلب البيانات:", response.status_code)
        return "لا يمكن تحميل الاقتباسات حاليا."

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
        message = get_quote()
        if message.strip():  # التأكد من أن الرسالة ليست فارغة
            send_message(message)
            print("✅ تم الإرسال:", message)
        else:
            print("🚫 لا يوجد اقتباسات لإرسالها.")
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
