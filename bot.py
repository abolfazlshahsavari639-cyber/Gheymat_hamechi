import telebot
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os
import threading
from flask import Flask

TELEGRAM_TOKEN = '8858601461:AAFzFZTwR7K1tN2vFZ-jqXyjbCs7kMJUgBk'
GEMINI_API_KEY = 'AQ.Ab8RN6KWJy78mPoRbjVxawxlnR7To2k4884dY0gxo4BijYg1wA'

bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-3.5-flash')

app = Flask(__name__)
@app.route('/')
def home(): 
    return "Bot is Running!"

def run_server(): 
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

def get_raw_data(query):
    # این تابع را بعداً می‌توانی توسعه دهی تا قیمت واقعی را با BeautifulSoup استخراج کند
    if "دلار" in query:
        return "دلار امروز حدود ۶۰,۰۰۰ تومان معامله می‌شود." # دیتای فرضی برای تست
    else:
        return f"محصول {query} در سایت‌ها موجود است." # دیتای فرضی برای تست

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! اسم محصول یا کلمه 'دلار' رو بفرست تا با هوش مصنوعی قیمتش رو تحلیل کنم. 🤖")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    wait_msg = bot.reply_to(message, "در حال استخراج و تحلیل با جمنای... ⏳")
    
    try:
        # مرحله اول: استخراج اطلاعات خام از اینترنت
        raw_data = get_raw_data(user_text)
        
        # مرحله دوم: ارسال اطلاعات به جمنای برای ساخت جواب هوشمند
        prompt = f"تو یک دستیار مالی هوشمند در تلگرام هستی. کاربر درخواست داده: '{user_text}'. دیتای خامی که از اینترنت گرفتیم این است: '{raw_data}'. یک جواب کوتاه، جذاب و دقیق به زبان فارسی برای کاربر بنویس."
        ai_response = model.generate_content(prompt)
        
        # مرحله سوم: نمایش جواب جمنای در تلگرام
        bot.edit_message_text(ai_response.text, chat_id=message.chat.id, message_id=wait_msg.message_id)
        
    except Exception as e:
        bot.edit_message_text(f"❌ خطا در پردازش:\n{str(e)}", chat_id=message.chat.id, message_id=wait_msg.message_id)

if __name__ == '__main__':
    threading.Thread(target=run_server).start()
    bot.infinity_polling()
