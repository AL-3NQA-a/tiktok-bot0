import telebot
import requests

TOKEN = "هنا_حط_التوكن_حقك"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 أهلا! أرسل يوزر تيك توك بدون @ عشان أجيبلك معلوماته.")

@bot.message_handler(func=lambda message: True)
def get_tiktok_info(message):
    username = message.text.strip().replace("@", "")
    try:
        url = f"https://www.tikwm.com/api/user/info?unique_id={username}"
        r = requests.get(url)

        if r.status_code != 200:
            bot.reply_to(message, "❌ الحساب غير موجود أو خاص.")
            return

        data = r.json().get("data", {})
        user = data.get("user", {})
        stats = data.get("stats", {})

        nickname = user.get("nickname", "غير متوفر")
        region = user.get("region", "❌ غير متوفرة")
        followers = stats.get("followerCount", 0)
        following = stats.get("followingCount", 0)
        likes = stats.get("heartCount", 0)
        videos = stats.get("videoCount", 0)
        bio = user.get("signature", "ما عنده بايو")
        avatar = user.get("avatarLarger", "")
        link = f"https://www.tiktok.com/@{username}"

        caption = (
            f"✅ معلومات الحساب\\n"
            f"👤 اليوزر: @{username}\\n"
            f"📛 الاسم: {nickname}\\n"
            f"🌍 الدولة/المنطقة: {region}\\n"
            f"👥 المتابعين: {followers}\\n"
            f"➡️ يتابع: {following}\\n"
            f"🎥 الفيديوهات: {videos}\\n"
            f"❤️ اللايكات: {likes}\\n"
            f"📝 البايو: {bio}\\n"
            f"🔗 الرابط: {link}"
        )

        if avatar:
            bot.send_photo(message.chat.id, avatar, caption=caption)
        else:
            bot.reply_to(message, caption)

    except Exception as e:
        bot.reply_to(message, f"❌ خطأ: {e}")

print("✅ البوت شغال...")
bot.polling(non_stop=True)
