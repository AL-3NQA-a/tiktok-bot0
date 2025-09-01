import telebot
import requests
import re
import os
import pycountry

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

def escape_md(text: str) -> str:
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', str(text))

def format_num(num: int) -> str:
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    return str(num)

# 🔥 تحويل كود الدولة إلى علم (🇸🇦)
def country_flag(alpha2: str) -> str:
    if not alpha2 or len(alpha2) != 2:
        return ""
    return chr(ord(alpha2[0].upper()) + 127397) + chr(ord(alpha2[1].upper()) + 127397)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "أرسل يوزر تيك توك بدون @ ، وأنا أعطيك كل التفاصيل 📊")

@bot.message_handler(func=lambda msg: True)
def get_info(message):
    username = message.text.strip().replace("@", "")
    try:
        url = f"https://www.tikwm.com/api/user/info?unique_id={username}"
        r = requests.get(url)

        if r.status_code != 200:
            bot.reply_to(message, f"❌ الحساب @{username} غير موجود أو خاص")
            return

        data = r.json().get("data", {})
        user = data.get("user", {})
        stats = data.get("stats", {})

        nickname = escape_md(user.get("nickname", "غير متوفر"))

        # الدولة مع العلم
        region_code = user.get("region", "")
        if region_code:
            country = pycountry.countries.get(alpha_2=region_code.upper())
            if country:
                flag = country_flag(region_code)
                region = f"{flag} {country.name}"
            else:
                region = f"غير معروف ({region_code})"
        else:
            region = "غير معروف"

        followers = format_num(stats.get("followerCount", 0))
        following = format_num(stats.get("followingCount", 0))
        likes = format_num(stats.get("heartCount", 0))
        videos = format_num(stats.get("videoCount", 0))
        bio = escape_md(user.get("signature", "ما عنده بايو"))
        avatar = user.get("avatarLarger", "")
        link = escape_md(f"https://www.tiktok.com/@{username}")

        caption = (
            "```python\n"
            f"# 📌 معلومات حساب تيك توك\n\n"
            f"👤 اليوزر: @{escape_md(username)}\n"
            f"🔥 الاسم: {nickname}\n"
            f"🌍 الدولة / المنطقة: {region}\n\n"
            f"👥 عدد المتابعين: {followers}\n"
            f"➡️ يتابع: {following}\n"
            f"🎥 عدد الفيديوهات: {videos}\n"
            f"❤️ عدد الإعجابات: {likes}\n\n"
            f"📝 البايو: {bio}\n"
            f"🔗 الرابط: {link}\n"
            "```"
        )

        if avatar:
            bot.send_photo(message.chat.id, avatar, caption=caption, parse_mode="MarkdownV2")
        else:
            bot.send_message(message.chat.id, caption, parse_mode="MarkdownV2")

    except Exception as e:
        bot.reply_to(message, f"❌ صار خطأ: {e}")

print("✅ البوت شغال ...")
bot.polling(none_stop=True)
