import time
from datetime import datetime, timezone, timedelta
from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio
from threading import Thread
from flask import Flask

# ১. Render ফ্রি টিয়ার সচল রাখার জন্য ছোট্ট ওয়েব সার্ভার
app = Flask('')

@app.route('/')
def home():
    return "Telegram Userbot is running 24/7 successfully!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# ২. আপনার টেলিগ্রাম তথ্যগুলো এখানে দিন
API_ID = 38531343  # আপনার সংখ্যাবাচক API ID
API_HASH = "822fce332e02a101007fcc0027ed5971"
SESSION_STRING = "1BVtsOL8Bu7roKkA_8-Ql0L0L-KJvMjKXuJ2VgNHIMhL_w0YJKynLSr32qahLWYYL5D34IJSJ1KzO1L9GeMKWbYrDxMYQl5hm1vfRcHrSPaNJHv0IIMnYBi2An4m8zuLsIFlJY02gOWmJ0VeHKRDD-eCACINL1XBOCV0AgAcT2800Ot-eMjv3UeT_QLiensylAoMCElZ_VWJIVF5fGHg4Wiz-y98Ac5jw2XjpMqJKt2tbx-9HvkFIrSpM0HJmgs36g69X_InrwPjzhtohBWL71QlmoxhvavoJ03fY3cFAzrl13SvS8QdRA0Qc254q1fe5B_mhyQvQhXh4Lgi_FjqVLWvelnG7z54="
CHAT_ID = -1004447970911  # আপনার গ্রুপের Chat ID

BD_OFFSET = timezone(timedelta(hours=6))

# ৩. মেসেজ শিডিউল
MESSAGES_SCHEDULE = [
    {"time": "19:10", "text": "/likes 10291533820"},
    {"time": "19:12", "text": "/likes 1713314437"},
    {"time": "19:14", "text": "/like bd 1713314437"},
    {"time": "19:16", "text": "/like bd 10291533820"},
    {"time": "19:18", "text": "/likes 7266770972"}
    {"time": "19:20", "text": "/like bd 7266770972"}
]

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def telegram_main():
    await client.start()
    print("Userbot সফলভাবে ক্লাউডে চালু হয়েছে!")
    await client.send_message(CHAT_ID, "Userbot ক্লাউড থেকে অনলাইন হয়েছে!")
    
    last_checked_minute = ""
    while True:
        current_minute = datetime.now(BD_OFFSET).strftime("%H:%M")
        
        if current_minute != last_checked_minute:
            for item in MESSAGES_SCHEDULE:
                if item["time"] == current_minute:
                    await client.send_message(CHAT_ID, item["text"])
                    now_bd = datetime.now(BD_OFFSET).strftime('%H:%M:%S')
                    print(f"[{now_bd} BD] মেসেজ পাঠানো হয়েছে: {item['text']}")
            last_checked_minute = current_minute
            
        await asyncio.sleep(10)

if __name__ == '__main__':
    # ব্যাকগ্রাউন্ডে ওয়েব সার্ভার রান করা
    t = Thread(target=run_flask)
    t.start()
    
    # টেলিগ্রাম ইউজারবট লুপ রান করা
    with client:
        client.loop.run_until_complete(telegram_main())
