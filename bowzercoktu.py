import types
import telebot
import requests
import os
import time
import random
import base64
import os
import re
import json
from bs4 import BeautifulSoup
from telebot import types
from datetime import datetime
from io import BytesIO


TOKEN = "7250474297:AAHJLlK4VbnOH-dHXvjbFdza9524JPQKhyY"
bot = telebot.TeleBot(TOKEN)
        
        
        
        
# Reddit API'yi kullanmak için gerekli bilgileri ayarlıyoruz
REDDIT_API_URL = "https://www.reddit.com/r/all/search.json"

# Reddit arama parametrelerini belirliyoruz
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
        
# Kullanıcı verileri (Örnek olarak, kullanıcıların Premium bilgilerini saklamak için)
user_rank = {}  # Kullanıcılar ve sıralamaları
user_premium_expiry = {}  # Kullanıcıların premium bitiş tarihi

ADMIN_IDS = [6151702016]  # Buraya tüm adminlerin Telegram ID’lerini ekleyin

# Rütbe ve özel menülerin ayarlanması
def get_rank(user_id):
    return user_rank.get(user_id, "Ücretsiz")  # Varsayılan rütbe "Ücretsiz" olacak

# Saat dilimine göre mesajı ayarlama
def get_greeting():
    current_time = datetime.now().hour
    if current_time >= 23:
        return "🌙 İyi Geceler"
    elif current_time >= 7 and current_time < 12:
        return "🌞 Günaydın"
    elif current_time >= 12 and current_time < 17:
        return "🌤️ Tünaydın"
    else:
        return "🌙 İyi Akşamlar"

# Global değişken olarak greeting_message'i tanımlayalım
greeting_message = ""

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

CHANNEL_ID = "-1002384653201"  # Kanal ID'nizi buraya ekledim
CHANNEL_LINK = "https://t.me/BowzerHack"  # Kanal linki

def is_user_subscribed(user_id):
    """ Kullanıcının kanala abone olup olmadığını kontrol eder. """
    try:
        chat_member = bot.get_chat_member(CHANNEL_ID, user_id)
        status = chat_member.status

        # Kullanıcının kanalda olup olmadığını kontrol et
        return status in ["member", "administrator", "creator"]
    except telebot.apihelper.ApiTelegramException as e:
        print(f"Kanal kontrol hatası: {e}")
        return False  # Eğer hata alırsak kullanıcı kanalda değilmiş gibi davranıyoruz
    except Exception as e:
        print(f"Bilinmeyen hata: {e}")
        return False

@bot.message_handler(commands=['start'])
def botu_baslatma(message):
    global greeting_message

    user_id = message.from_user.id
    chat_id = message.chat.id

    # Kullanıcının kanala üye olup olmadığını kontrol et
    if not is_user_subscribed(user_id):
        markup = InlineKeyboardMarkup()
        join_button = InlineKeyboardButton("📢 Kanala Katıl", url=CHANNEL_LINK)
        check_button = InlineKeyboardButton("✅ Katıldım", callback_data="check_subscription")
        markup.add(join_button)
        markup.add(check_button)

        bot.send_message(
            chat_id,
            f"❌ Botu kullanabilmek için önce kanalımıza katılmalısın!\n\n📢 **Kanalımız:** [BowzerHack]({CHANNEL_LINK})",
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=markup
        )
        return  # Kullanıcı kanalda değilse işlemi durdur

    # Kullanıcı kanaldaysa devam et
    video_url = 'https://lab-noted-tuna.ngrok-free.app//efebabey.mp4'

    try:
        bot.send_video(chat_id, video_url)
    except telebot.apihelper.ApiTelegramException as e:
        if "Forbidden: user is deactivated" in str(e):
            print(f"Kullanıcı devre dışı: {user_id}")
            return

    username = message.from_user.username
    greeting_message = f"{get_greeting()} @{username}! 👋\n\nBotu kullanmaya başlamak için aşağıdaki butonları kullanabilirsin. 📋"

    rank_message = f"Rütbeniz: {get_rank(user_id)}"

    try:
        bot.send_message(chat_id, f"{greeting_message}\n{rank_message}", reply_markup=main_menu(message))
    except telebot.apihelper.ApiTelegramException as e:
        if "Forbidden: user is deactivated" in str(e):
            print(f"Kullanıcı devre dışı: {user_id}")
            return

@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_subscription(call):
    """ Kullanıcı 'Katıldım' butonuna bastığında kontrol edilir. """
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    if is_user_subscribed(user_id):
        bot.send_message(chat_id, "✅ Tebrikler! Kanalımıza katıldın. Artık botu kullanabilirsin.")
        bot.delete_message(chat_id, call.message.message_id)  # Eski mesajı sil
        botu_baslatma(call.message)  # Start fonksiyonunu tekrar çalıştır
    else:
        bot.answer_callback_query(call.id, "❌ Henüz kanala katılmadın. Lütfen önce kanala katıl!")

# Ana Menü
def main_menu(message):
    markup = types.InlineKeyboardMarkup()

    # Bilgi ve Komutlar butonlarını ekleyelim
    info_button = types.InlineKeyboardButton("ℹ️ Bilgi", callback_data="bilgi")
    commands_button = types.InlineKeyboardButton("🛠️ Komutlar", callback_data="komutlar")
    markup.add(commands_button, info_button)

    # Yapımcı butonunu farklı bir isimle ekleyelim
    creator_button = types.InlineKeyboardButton("🎉 Kodlayıcım", url="https://t.me/Bowzer_Sik")
    markup.add(creator_button)

    return markup

# Bilgi butonuna tıklayınca mesaj gönderecek callback fonksiyonu
@bot.callback_query_handler(func=lambda call: call.data == "bilgi")
def send_info(call):
    # Bilgi mesajını gönderiyoruz
    info_message = "ℹ️ Bot Hakkında Bilgi\n━━━━━━━━━━━━━━━━━━━━━━━━━━\nMerhaba! Ben, Bowzer. İşlevim Bilgi Sorgulamak. İşte botum hakkında bazı bilgiler:\n💡 Amaç: Kullanıcıları bilgilendirmek ve çeşitli işlemleri kolaylaştırmak.\n🔧 Yapımcı: @bowzer_sik\n👨‍💻 Bot Geliştiricisi: @bowzer_sik\n🌐 Servis API: Bowzer Check\n\n💬 Komutlar:\n   ➡️ /tc: TC bilgilerini sorgulamak.\n   ➡️ /sorgu: Ad Soyad İl İlçe İle TC bilgilerini sorgulamak.\n   ➡️ /sorgu2: Ad Soyad İl İle TC bilgilerini sorgulamak.\n   ➡️ /aile: Aile bilgilerini sorgulamak.\n   ➡️ /adres: TC ile Adres Bilgilerini sorgulamak.\n   ➡️ /okulno: TC ile Okul Bilgilerini sorgulamak.\n   ➡️ /vesika: TC ile Vesikalık Bilgilerini sorgulamak.\n   ➡️ /isyeri: TC ile İşyeri Bilgilerini sorgulamak.\n   ➡️ /yapımcılar: Yapımcı bilgilerini almak.\n\n⚙️ Bot hakkında herhangi bir sorunuz varsa, lütfen @bowzer_sik ile iletişime geçin."
    
    # Inline butonları hazırlıyoruz
    markup = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton("⬅️ Geri Dön", callback_data="geri_don")
    markup.add(back_button)

    # Bilgi mesajını gönderiyoruz ve geri dönme butonunu ekliyoruz
    bot.send_message(call.message.chat.id, info_message, reply_markup=markup)

    # Önceki mesajı siliyoruz
    bot.delete_message(call.message.chat.id, call.message.message_id)

# Geri dönme butonuna tıklandığında önceki mesaja dönmek için callback fonksiyonu
@bot.callback_query_handler(func=lambda call: call.data == "geri_don")
def go_back(call):
    # Kullanıcıya geri döneceği mesajı gönderiyoruz
    bot.send_message(call.message.chat.id, "Geri dönüldü. Lütfen /start yazınız.")
    bot.delete_message(call.message.chat.id, call.message.message_id)

# Komutlar Menü
def commands_menu():
    markup = types.InlineKeyboardMarkup()

    # Komutları kategorilere ayırıyoruz
    citizenship_button = types.InlineKeyboardButton("👨‍👩‍👧‍👦 Vatandaşlık İşlemleri", callback_data="citizenship_menu")
    phone_communication_button = types.InlineKeyboardButton("📱 Telefon İletişim Sistemi", callback_data="phone_communication_menu")
    entertainment_button = types.InlineKeyboardButton("🎉 Eğlence", callback_data="entertainment_menu")
    back_button = types.InlineKeyboardButton("↩️ Geri Dön", callback_data="geri_don")

    markup.add(citizenship_button, phone_communication_button, entertainment_button)
    markup.add(back_button)
    return markup

# Vatandaşlık İşlemleri Menü
def citizenship_menu():
    markup = types.InlineKeyboardMarkup()
    search_button = types.InlineKeyboardButton("🔍 Ad Soyad İl İlçe", callback_data="citizenship_sorgu")
    search2_button = types.InlineKeyboardButton("🔍 Ad Soyad İl", callback_data="citizenship_sorgu2")
    tc_button = types.InlineKeyboardButton("🔍 TC Sorgulama", callback_data="citizenship_tc")
    family_button = types.InlineKeyboardButton("👨‍👩‍👧‍👦 Aile Sorgulama", callback_data="citizenship_aile")
    address_button = types.InlineKeyboardButton("🏠 Adres Sorgulama", callback_data="citizenship_adres")
    okulno_button = types.InlineKeyboardButton("🏫 Okul No Sorgulama", callback_data="citizenship_okulno")
    vesika_button = types.InlineKeyboardButton("📷 Vesika Sorgulama", callback_data="citizenship_vesika")
    isyeri_button = types.InlineKeyboardButton("👨‍💼 İşyeri Sorgulama", callback_data="citizenship_isyeri")
    vefat_button = types.InlineKeyboardButton("☠ Vefat Sorgulama", callback_data="citizenship_vefat")
    back_button = types.InlineKeyboardButton("↩️ Geri Dön", callback_data="geri_don")
    markup.add(search_button, search2_button, tc_button, family_button, address_button, okulno_button, vesika_button, isyeri_button, vefat_button)
    markup.add(back_button)
    return markup

# Telefon İletişim Sistemi Menü
def phone_communication_menu():
    markup = types.InlineKeyboardMarkup()
    tcgsm_button = types.InlineKeyboardButton("📱 Tc GSM Sorgulama", callback_data="phone_communication_tcgsm")
    gsmtc_button = types.InlineKeyboardButton("📞 GSM Tc Sorgulama", callback_data="phone_communication_gsmtc")
    operator_button = types.InlineKeyboardButton("📞 Operatör Sorgulama", callback_data="phone_communication_operator")
    sms_button = types.InlineKeyboardButton("💥 SMS Bomber", callback_data="phone_communication_sms")  # Burada değişiklik yapıldı
    back_button = types.InlineKeyboardButton("↩️ Geri Dön", callback_data="geri_don")
    markup.add(tcgsm_button, gsmtc_button, operator_button)
    markup.add(sms_button)  # Burada da değişiklik yapıldı
    markup.add(back_button)
    return markup

# Eğlence Menü
def entertainment_menu():
    markup = types.InlineKeyboardMarkup()

    penis_button = types.InlineKeyboardButton("😂 Penis Boyu", callback_data="entertainment_penis")
    ayak_button = types.InlineKeyboardButton("👣 Ayak Boyutu", callback_data="entertainment_ayak")
    yaz_button = types.InlineKeyboardButton("📝 Yazı Yaz", callback_data="entertainment_yaz")
    nude_button = types.InlineKeyboardButton("❤ Nude", callback_data="entertainment_nude")
    euro_button = types.InlineKeyboardButton("💶 Euro", callback_data="entertainment_euro")
    dolar_button = types.InlineKeyboardButton("💵 Dolar", callback_data="entertainment_dolar")
    
    back_button = types.InlineKeyboardButton("↩️ Geri Dön", callback_data="geri_don")

    markup.add(penis_button, ayak_button)
    markup.add(yaz_button, nude_button)
    markup.add(euro_button, dolar_button)
    markup.add(back_button)

    return markup

# Komutlara Tıklama ve Sorgu Bilgilerini Gösterme
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "komutlar":
        bot.send_message(call.message.chat.id, "🛠️ Komutlar Menüsüne Hoşgeldiniz! Lütfen bir kategori seçin:", reply_markup=commands_menu())
        bot.delete_message(call.message.chat.id, call.message.message_id)
    
    elif call.data == "citizenship_menu":
        # Vatandaşlık İşlemleri Menüsüne Yönlendir
        bot.send_message(call.message.chat.id, "👨‍👩‍👧‍👦 Vatandaşlık İşlemleri için aşağıdaki seçenekleri kullanabilirsiniz:", reply_markup=citizenship_menu())
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == "phone_communication_menu":
        # Telefon İletişim Sistemi Menüsüne Yönlendir
        bot.send_message(call.message.chat.id, "📱 Telefon İletişim Sistemi komutları için aşağıdaki seçenekleri kullanabilirsiniz:", reply_markup=phone_communication_menu())
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == "entertainment_menu":
        # Eğlence Menüsüne Yönlendir
        bot.send_message(call.message.chat.id, "🎉 Eğlence komutları için aşağıdaki seçenekleri kullanabilirsiniz:", reply_markup=entertainment_menu())
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == "geri_don":
        # Ana Menüyü Göster
        bot.answer_callback_query(call.id, "Ana menüye dönülüyor!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Başka bir işlem yapmak için aşağıdaki seçenekleri kullanabilirsiniz:", reply_markup=main_menu(call.message))

    # Vatandaşlık Sorgusu Butonları
    elif call.data == "citizenship_sorgu":
        bot.send_message(call.message.chat.id, """
        🔍 /sorgu Komutu Kullanımı:
        - Bu komutla Ad, Soyad, İl, ve İlçe bilgilerini kullanarak kişiye ait verilere ulaşabilirsiniz.
        - Format: /sorgu [Ad] [Soyad] [İl] [İlçe]
        """, reply_markup=commands_menu())
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == "citizenship_sorgu2":
        bot.send_message(call.message.chat.id, """
        🔍 /sorgu2 Komutu Kullanımı:
        - Bu komutla Ad, Soyad, ve İl bilgilerini kullanarak kişiye ait verilere ulaşabilirsiniz.
        - Format: /sorgu2 [Ad] [Soyad] [İl]
        """, reply_markup=commands_menu())
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
    elif call.data == "citizenship_tc":
        bot.send_message(call.message.chat.id, """
        🔍 /tcsorgu Komutu Kullanımı:
        - Bu komutla TC Bilgilerini kullanarak kişiye ait verilere ulaşabilirsiniz.
        - Format: /tcsorgu [TC]
        """, reply_markup=commands_menu())
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
    elif call.data == "citizenship_aile":
        bot.send_message(call.message.chat.id, """
        👨‍👩‍👧‍👦 /aile Komutu Kullanımı:
        - Bu komutla TC Bilgilerini kullanarak ailesine ait verilere ulaşabilirsiniz.
        - Format: /aile [TC]
        """, reply_markup=commands_menu())
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
    elif call.data == "citizenship_adres":
        bot.send_message(call.message.chat.id, """
        🏠 /adres Komutu Kullanımı:
        - Bu komutla TC Bilgilerini kullanarak adresine ait verilere ulaşabilirsiniz.
        - Format: /adres [TC]
        """, reply_markup=commands_menu())
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == "citizenship_isyeri":
        bot.send_message(call.message.chat.id, """
        👨‍ /isyeri Komutu Kullanımı:
        - Bu komutla TC Bilgilerini kullanarak İşyerine ait verilere ulaşabilirsiniz.
        - Format: /isyeri [TC]
        """, reply_markup=commands_menu())
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
    elif call.data == "citizenship_okulno":
        bot.send_message(call.message.chat.id, """
        🏫 /okulno Komutu Kullanımı:
        - Bu komutla TC Bilgilerini kullanarak Okuluna ait verilere ulaşabilirsiniz.
        - Format: /okulno [TC]
        """, reply_markup=commands_menu())
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
    elif call.data == "citizenship_vesika":
        bot.send_message(call.message.chat.id, """
        📷‍ /vesika Komutu Kullanımı:
        - Bu komutla TC Bilgilerini kullanarak Vesikasına ait verilere ulaşabilirsiniz.
        - Format: /vesika [TC]
        """, reply_markup=commands_menu())
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
    elif call.data == "citizenship_vefat":
        bot.send_message(call.message.chat.id, """
        ☠‍ /vefat Komutu Kullanımı:
        - Bu komutla TC Bilgilerini kullanarak vefatına ait verilere ulaşabilirsiniz.
        - Format: /vefat [TC]
        """, reply_markup=commands_menu())
        bot.delete_message(call.message.chat.id, call.message.message_id)

    # Telefon İletişim Sistemi Butonları
    elif call.data == "phone_communication_tcgsm":
        bot.send_message(call.message.chat.id, """
📱 /tcgsm Komutu Kullanımı:
- TC kimlik numarasından telefon bilgisi sorgulama
- Format: /tcgsm [TCKN]
- Örnek: /tcgsm 12345678901""", reply_markup=commands_menu())
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == "phone_communication_gsmtc":
        bot.send_message(call.message.chat.id, """
🔍 /gsmtc Komutu Kullanımı:
- Telefon numarasından TCKN sorgulama
- Format: /gsmtc [Telefon]
- Örnek: /gsmtc 5551234567""", reply_markup=commands_menu())
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == "phone_communication_sms":
        bot.send_message(call.message.chat.id, """
💣 /sms Komutu Kullanımı:
- SMS gönderme işlemi
- Format: /sms [Telefon] 
- Örnek: /sms 5551234567
""", reply_markup=commands_menu())
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == "phone_communication_operator":
        bot.send_message(call.message.chat.id, """
📞 /operator Komutu Kullanımı:
- Telefon operatörü sorgulama
- Format: /operator [Telefon]
- Örnek: /operator 5551234567
""", reply_markup=commands_menu())
        bot.delete_message(call.message.chat.id, call.message.message_id)

    # Eğlence Butonları
    elif call.data == "entertainment_penis":
        bot.send_message(call.message.chat.id, """
        😂 /penis Komutu Kullanımı:
        - Çavuşun boyunu gösterir. Sadece eğlencelik bir komuttur.
        - Format: `/penis [TC]`
        """, reply_markup=commands_menu(), parse_mode="Markdown")
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == "entertainment_ayak":
        bot.send_message(call.message.chat.id, """
        👣 /ayak Komutu Kullanımı:
        - Kişinin ayak numarasını öğrenmek için bu komutu kullanabilirsiniz.
        - Format: `/ayak [TC]`
        """, reply_markup=commands_menu(), parse_mode="Markdown")
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == "entertainment_yaz":
        bot.send_message(call.message.chat.id, """
        📝 /yaz Komutu Kullanımı:
        - Yazdığınız metni özel tasarımda oluşturur.
        - Format: `/yaz <metin>`
        """, reply_markup=commands_menu(), parse_mode="Markdown")
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == "entertainment_nude":
        bot.send_message(call.message.chat.id, """
        ❤ /nude Komutu Kullanımı:
        - Random Nude almak için kullanabilirsiniz.
        - Format: `/nude`
        """, reply_markup=commands_menu(), parse_mode="Markdown")
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == "entertainment_euro":
        bot.send_message(call.message.chat.id, """
        💶 /euro Komutu Kullanımı:
        - Güncel Euro kurunu gösterir.
        - Format: `/euro`
        """, reply_markup=commands_menu(), parse_mode="Markdown")
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == "entertainment_dolar":
        bot.send_message(call.message.chat.id, """
        💵 /dolar Komutu Kullanımı:
        - Güncel Dolar kurunu gösterir.
        - Format: `/dolar`
        """, reply_markup=commands_menu(), parse_mode="Markdown")
        bot.delete_message(call.message.chat.id, call.message.message_id)


CHANNEL_ID = "@BowzerHack"

# İstek sayacı ve zamanlayıcı için değişkenler
last_request_time = 0
request_interval = 3  # Saniye cinsinden

@bot.message_handler(commands=['sorgu'])
def sorgu(message):
    global last_request_time
    
    try:
        current_time = time.time()
        if current_time - last_request_time < request_interval:
            time_to_wait = request_interval - (current_time - last_request_time)
            bot.reply_to(message, f"Lütfen {time_to_wait:.1f} saniye bekleyiniz.")
            return
        
        last_request_time = current_time
        
        chat_id = message.chat.id
        user_id = message.from_user.id

        # Kanal kontrolü
        try:
            member_status = bot.get_chat_member(CHANNEL_ID, user_id).status
            if member_status not in ["member", "administrator", "creator"]:
                bot.reply_to(message, f"Bu komutu kullanabilmek için {CHANNEL_ID} kanalına katılmalısınız.")
                return
        except Exception:
            bot.reply_to(message, "Kanal bilgileri alınırken bir hata oluştu. Lütfen daha sonra tekrar deneyin.")
            return

        parameters = message.text.split()[1:]
        if len(parameters) < 2:
            bot.reply_to(message, "Geçersiz komut. Kullanım: /sorgu Ad Soyad [İl] [İlçe]")
            return

        ad = parameters[0]
        soyad = parameters[1]
        il = parameters[2] if len(parameters) > 2 else ''
        ilce = parameters[3] if len(parameters) > 3 else ''

        try:
            # Yeni API endpoint'i kullanılıyor
            response = requests.get(
                "https://api.sowixfree.xyz/sowixapi/adsoyadilice.php",
                params={'ad': ad, 'soyad': soyad, 'il': il, 'ilce': ilce},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if not data.get("success"):
                bot.reply_to(message, "Böyle bir kişi bilgisi bulunamadı. Lütfen bilgilerinizi kontrol edin.")
                return
                
            # Önceki formatta verileri işleme
            for person in data.get("data", []):
                person_info = (
                    f"╭──────────────  ✦\n"
                    f"┃  TC Kimlik No: {person.get('TC', 'Bulunamadı')}\n"
                    f"┃  Ad: {person.get('AD', 'Bulunamadı')}\n"
                    f"┃  Soyad: {person.get('SOYAD', 'Bulunamadı')}\n"
                    f"┃  Doğum Tarihi: {person.get('DOGUMTARIHI', 'Bulunamadı')}\n"
                    f"┃  Adres İl: {person.get('ADRESIL', 'Bulunamadı')}\n"
                    f"┃  Adres İlçe: {person.get('ADRESILCE', 'Bulunamadı')}\n"
                    f"┃  Anne Adı: {person.get('ANNEADI', 'Bulunamadı')}\n"
                    f"┃  Anne TC: {person.get('ANNETC', 'Bulunamadı')}\n"
                    f"┃  Baba Adı: {person.get('BABAADI', 'Bulunamadı')}\n"
                    f"┃  Baba TC: {person.get('BABATC', 'Bulunamadı')}\n"
                    f"┃  Cinsiyet: {person.get('CINSIYET', 'Bulunamadı')}\n"
                    f"┃  Uyruk: Türk\n"
                    f"┃  GSM: {person.get('GSM', 'Bulunamadı')}\n"
                    f"┃  Vefat Tarihi: {person.get('OLUMTARIHI', 'YOK')}\n"
                    f"┃  Doğum Yeri: {person.get('DOGUMYERI', 'Bulunamadı')}\n"
                    f"┃  Memleket İl: {person.get('MEMLEKETIL', 'Bulunamadı')}\n"
                    f"┃  Memleket İlçe: {person.get('MEMLEKETILCE', 'Bulunamadı')}\n"
                    f"┃  Memleket Köy: {person.get('MEMLEKETKOY', 'Bulunamadı')}\n"
                    f"┃  Medeni Hali: {person.get('MEDENIHAL', 'Bulunamadı')}\n"
                    f"┃  Aile Sıra No: {person.get('AILESIRANO', 'Bulunamadı')}\n"
                    f"┃  Bireysel Sıra No: {person.get('BIREYSIRANO', 'Bulunamadı')}\n"
                    f"╰──────────────  ✦"
                )
                bot.send_message(chat_id, person_info)
                
        except requests.exceptions.RequestException:
            bot.reply_to(message, "Sorgu işlemi sırasında bir hata oluştu. Lütfen daha sonra tekrar deneyin.")
        except Exception as e:
            print(f"Hata oluştu: {str(e)}")
            bot.reply_to(message, "Bir hata oluştu. Lütfen tekrar deneyin.")
            
    except IndexError:
        bot.reply_to(message, "Geçersiz komut kullanımı. Lütfen komutu şu şekilde yazın: /sorgu Ad Soyad [İl] [İlçe]")
    except Exception as e:
        print(f"Genel hata: {str(e)}")
        bot.reply_to(message, "Bir hata oluştu. Lütfen tekrar deneyin.")


@bot.message_handler(commands=['sorgu2'])
def sorgu2(message):
    global last_request_time
    
    try:
        current_time = time.time()
        if current_time - last_request_time < request_interval:
            time_to_wait = request_interval - (current_time - last_request_time)
            bot.reply_to(message, f"Lütfen {time_to_wait:.1f} saniye bekleyiniz.")
            return
        
        last_request_time = current_time
        
        chat_id = message.chat.id
        user_id = message.from_user.id

        # Kanal kontrolü
        try:
            member_status = bot.get_chat_member(CHANNEL_ID, user_id).status
            if member_status not in ["member", "administrator", "creator"]:
                bot.reply_to(message, f"Bu komutu kullanabilmek için {CHANNEL_ID} kanalına katılmalısınız.")
                return
        except Exception:
            bot.reply_to(message, "Kanal bilgileri alınırken bir hata oluştu. Lütfen daha sonra tekrar deneyin.")
            return

        parameters = message.text.split()[1:]
        if len(parameters) < 3:
            bot.reply_to(message, "Geçersiz komut. Kullanım: /sorgu2 Ad Soyad İl")
            return

        ad = parameters[0]
        soyad = parameters[1]
        il = parameters[2]

        try:
            response = requests.get(
                "https://api.sowixfree.xyz/sowixapi/adsoyadilice.php",
                params={'ad': ad, 'soyad': soyad, 'il': il},
                timeout=15
            )
            response.raise_for_status()
            data = response.json()
            
            if not data.get("success"):
                bot.reply_to(message, "Böyle bir kişi bilgisi bulunamadı. Lütfen bilgilerinizi kontrol edin.")
                return
                
            for person in data.get("data", []):
                person_info = (
                    f"╭──────────────  ✦\n"
                    f"┃  TC Kimlik No: {person.get('TC', 'Bulunamadı')}\n"
                    f"┃  Ad: {person.get('AD', 'Bulunamadı')}\n"
                    f"┃  Soyad: {person.get('SOYAD', 'Bulunamadı')}\n"
                    f"┃  Doğum Tarihi: {person.get('DOGUMTARIHI', 'Bulunamadı')}\n"
                    f"┃  Adres İl: {person.get('ADRESIL', 'Bulunamadı')}\n"
                    f"┃  Adres İlçe: {person.get('ADRESILCE', 'Bulunamadı')}\n"
                    f"┃  Anne Adı: {person.get('ANNEADI', 'Bulunamadı')}\n"
                    f"┃  Anne TC: {person.get('ANNETC', 'Bulunamadı')}\n"
                    f"┃  Baba Adı: {person.get('BABAADI', 'Bulunamadı')}\n"
                    f"┃  Baba TC: {person.get('BABATC', 'Bulunamadı')}\n"
                    f"┃  Cinsiyet: {person.get('CINSIYET', 'Bulunamadı')}\n"
                    f"┃  Uyruk: Türk\n"
                    f"┃  GSM: {person.get('GSM', 'Bulunamadı')}\n"
                    f"┃  Vefat Tarihi: {person.get('OLUMTARIHI', 'YOK')}\n"
                    f"┃  Doğum Yeri: {person.get('DOGUMYERI', 'Bulunamadı')}\n"
                    f"┃  Memleket İl: {person.get('MEMLEKETIL', 'Bulunamadı')}\n"
                    f"┃  Memleket İlçe: {person.get('MEMLEKETILCE', 'Bulunamadı')}\n"
                    f"┃  Memleket Köy: {person.get('MEMLEKETKOY', 'Bulunamadı')}\n"
                    f"┃  Medeni Hali: {person.get('MEDENIHAL', 'Bulunamadı')}\n"
                    f"┃  Aile Sıra No: {person.get('AILESIRANO', 'Bulunamadı')}\n"
                    f"┃  Bireysel Sıra No: {person.get('BIREYSIRANO', 'Bulunamadı')}\n"
                    f"╰──────────────  ✦"
                )
                bot.send_message(chat_id, person_info)
                
        except requests.exceptions.RequestException as e:
            print(f"API Hatası: {str(e)}")
            bot.reply_to(message, "Sorgu işlemi sırasında bir hata oluştu. Lütfen daha sonra tekrar deneyin.")
        except Exception as e:
            print(f"Genel Hata: {str(e)}")
            bot.reply_to(message, "Bir hata oluştu. Lütfen tekrar deneyin.")
            
    except IndexError:
        bot.reply_to(message, "Geçersiz komut kullanımı. Lütfen komutu şu şekilde yazın: /sorgu2 Ad Soyad İl")
    except Exception as e:
        print(f"Kritik Hata: {str(e)}")
        bot.reply_to(message, "Sistem hatası oluştu. Lütfen yöneticiye bildirin.")

import requests

CHANNEL_ID = "@BowzerHack"  # Kanalın kullanıcı adı

@bot.message_handler(commands=['vefat'])
def vefat(message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id

        # Kullanıcının kanalda olup olmadığını kontrol et
        member_status = bot.get_chat_member(CHANNEL_ID, user_id).status
        if member_status not in ["member", "administrator", "creator"]:
            bot.reply_to(message, f"Bu komutu kullanabilmek için {CHANNEL_ID} kanalına katılmalısınız.")
            return

        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "TC Kimlik No Giriniz")
            return

        tc = parts[1]
        api = f"https://lab-noted-tuna.ngrok-free.app//Restiricted-Area/vefat.php?tc={tc}"
        response = requests.get(api)
        response.encoding = 'utf-8'
        data = response.json()

        if data["success"]:
            efebabey = data["data"]

            sonuc = (
                f"/)    /)\n"
                f"(｡•ㅅ•｡)\n"
                f"╭∪─∪──────────  ✦\n"
                f"┃➥ 𝘛𝘊: {efebabey['TC']}\n" 
                f"┃➥ 𝘪𝘴𝘪𝘮 : {efebabey['Adi']}\n"
                f"┃➥ 𝘚𝘰𝘺𝘪𝘴𝘪𝘮 : {efebabey['Soyadi']}\n"
                f"┃➥ 𝘉𝘢𝘣𝘢 𝘐𝘴𝘪𝘮 : {efebabey['BabaAdi']}\n"
                f"┃➥ 𝘈𝘯𝘯𝘦 𝘐𝘴𝘪𝘮 : {efebabey['AnneAdi']}\n"
                f"┃➥ 𝘋𝘰ğ𝘶𝘮 𝘛𝘢𝘳𝘪𝘩𝘪 : {efebabey['DogumTarihi']}\n"
                f"┃➥ 𝘊𝘪𝘯𝘴𝘪𝘺𝘦𝘵 : {efebabey['Cinsiyet']}\n"
                f"┃➥ 𝘝𝘦𝘧𝘢𝘵 𝘛𝘢𝘳𝘪𝘩𝘪 : {efebabey['VefatTarihi']}\n"
                f"┃➥ 𝘈𝘶𝘵𝘩𝘰𝘳 : {efebabey['Yapımcı']}\n"
                f"╰─────────────  ✦\n"
            )

            bot.reply_to(message, sonuc)
        else:
            bot.reply_to(message, "Sonuç Bulunmadı.")

    except Exception as e:
        bot.reply_to(message, f"Hatayı @bowzer_sik ilet: {str(e)}")



@bot.message_handler(commands=['okulno'])
def okulno(message):
    try:
        # Kullanıcının ID'sini al
        user_id = message.from_user.id
        channel_username = "@BowzerHack"  # Kontrol edilecek kanalın kullanıcı adı (örnek: @resmikanal)

        # Kullanıcının kanalda olup olmadığını kontrol et
        chat_member = bot.get_chat_member(channel_username, user_id)
        if chat_member.status in ["left", "kicked"]:  # Kullanıcı kanalda değilse
            bot.reply_to(
                message,
                f"⚠️ Bu komutu kullanabilmek için {channel_username} kanalına katılmalısınız!\n\n"
                f"👉 [Katılmak için buraya tıklayın](https://t.me/{channel_username.lstrip('@')})",
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
            return  # Kullanıcı kanala katılmadığı için işlemi durdur

        # Kullanıcının mesajını işle
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "⚠️ Lütfen TC Kimlik No Giriniz. Örnek kullanım: /okulno 11111111110")
            return

        tc = parts[1]  # Kullanıcıdan alınan TC numarası
        api = f"http://api.sowixfree.xyz/sowixapi/okulno.php?tc={tc}"
        response = requests.get(api)
        response.encoding = 'utf-8'
        data = response.json()

        # API yanıtını kontrol et
        if isinstance(data, dict) and data.get("success"):
            efebabey_list = data.get("data", [])

            if not efebabey_list:
                bot.reply_to(message, "❌ Sonuç Bulunamadı.")
                return

            sonuc = (
                f"/)    /)\n"
                f"(｡•ㅅ•｡)\n"
                f"╭∪─∪──────────  ✦\n"
            )

            for efebabey in efebabey_list:
                sonuc += (
                    f"┃➥ 𝘛𝘊 : {efebabey.get('tc', 'Bulunamadı')}\n"
                    f"┃➥ 𝘐̇𝘴𝘪𝘮 : {efebabey.get('ad', 'Bulunamadı')}\n"
                    f"┃➥ 𝘚𝘰𝘺𝘪𝘴𝘪𝘮 : {efebabey.get('soyad', 'Bulunamadı')}\n"
                    f"┃➥ 𝘋𝘶𝘳𝘶𝘮𝘶 : {efebabey.get('durumu', 'Bulunamadı')}\n"
                    f"┃➥ 𝘕𝘰 : {efebabey.get('okulno', 'Bulunamadı')}\n"
                    f"┃➥ 𝘈𝘶𝘵𝘩𝘰𝘳 : {efebabey.get('Yapımcı', 'Bulunamadı')}\n"
                    f"╰─────────────  ✦\n"
                )

            bot.reply_to(message, sonuc)
        else:
            bot.reply_to(message, "❌ Beklenmeyen bir hata oluştu veya sonuç bulunamadı.")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Hata oluştu, lütfen /yapımcılar ile iletişime geçin: {str(e)}")


@bot.message_handler(commands=['tcsorgu'])
def tc_sorgu(message):
    try:
        chat_id = message.chat.id
        tc_number = message.text.split()[1]  # Kullanıcıdan gelen TC numarasını alıyoruz.

        # PHP API URL'sini kullanarak aile bilgilerini alıyoruz.
        url = f"http://api.sowixfree.xyz/sowixapi/tcpro.php?tc={tc_number}"
        response = requests.get(url)
        data = response.json()

        if "success" in data and data["success"]:
            family_info = "Sorgu Bilgileri:\n\n"
            
            # Kişisel bilgiler
            family_info += f"/)    /)\n"
            family_info += f"(｡•ㅅ•｡)\n"
            family_info += f"╭∪─∪──────────  ✦\n"
            family_info += f"┃➥ 𝘛𝘊: {data['data']['TC']}\n"
            family_info += f"┃➥ İsim Soy İsim: {data['data']['AD']} {data['data']['SOYAD']}\n"
            family_info += f"┃➥ Telefon Numarası: {data['data']['GSM']}\n"
            family_info += f"┃➥ 𝘋𝘶𝘳𝘶𝘮𝘶 : {data['data']['MEDENIHAL']}\n"
            family_info += f"┃➥ 𝘈𝘯𝘯𝘦: {data['data']['ANNEADI']} {data['data']['ANNETC']}\n"
            family_info += f"┃➥ 𝘉𝘢𝘣𝘢: {data['data']['BABAADI']} {data['data']['BABATC']}\n"
            family_info += f"┃➥ 𝘋𝘰𝘨𝘶𝘮 𝘛𝘢𝘳𝘪𝘩𝘪: {data['data']['DOGUMTARIHI']}\n"
            family_info += f"┃➥ 𝘋𝘰𝘨𝘶𝘮 𝘠𝘦𝘳𝘪: {data['data']['DOGUMYERI']}\n"
            family_info += f"┃➥ Memleket: {data['data']['MEMLEKETIL']} - {data['data']['MEMLEKETILCE']} - {data['data']['MEMLEKETKOY']}\n"
            family_info += f"┃➥ 𝘈𝘥𝘳𝘦𝘴: {data['data']['ADRESIL']} - {data['data']['ADRESILCE']}\n"
            family_info += f"┃➥ 𝘈𝘪𝘭𝘦 𝘚𝘪𝘳𝘢 𝘕𝘰: {data['data']['AILESIRANO']}\n"
            family_info += f"┃➥ 𝘉𝘪𝘳𝘦𝘺 𝘚𝘪𝘳𝘢 𝘕𝘰: {data['data']['BIREYSIRANO']}\n"
            family_info += f"┃➥ Cinsiyet: {data['data']['CINSIYET']}\n"
            family_info += f"┃➥ Uyruk: Türk\n"
            family_info += f"┃➥ Yapımcı: {data['data']['Yapımcı']}\n"
            family_info += f"╰─────────────  ✦\n\n"
            
            # Aile bilgilerini kullanıcıya gönderiyoruz
            bot.reply_to(message, family_info)

        else:
            bot.reply_to(message, "❌ TC bilgisi bulunamadı.")

    except IndexError:
        bot.reply_to(message, "⚠️ Geçersiz komut kullanım: /tcsorgu 11111111110")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Bir hata oluştu: {e}")


import requests

def format_family_info(person_type, person_data):
    """ Aile bireylerinin bilgilerini şekilli formatlar. """
    family_info = f"✨ {person_type} Bilgileri ✨\n"
    family_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    family_info += f"👤 Adı Soyadı: {person_data.get('AD', 'Bilinmiyor')} {person_data.get('SOYAD', 'Bilinmiyor')}\n"
    family_info += f"🔢 TC: {person_data.get('TC', 'Bilinmiyor')}\n"
    family_info += f"🎂 Doğum Tarihi: {person_data.get('DOGUMTARIHI', 'Bilinmiyor')}\n"
    family_info += f"🌍 Doğum Yeri: {person_data.get('DOGUMYERI', 'Bilinmiyor')}\n"
    family_info += f"🏠 Memleket: {person_data.get('MEMLEKETIL', 'Bilinmiyor')} - {person_data.get('MEMLEKETILCE', 'Bilinmiyor')}\n"
    family_info += f"📍 Adres: {person_data.get('ADRESIL', 'Bilinmiyor')} - {person_data.get('ADRESILCE', 'Bilinmiyor')}\n"
    family_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    return family_info

@bot.message_handler(commands=['aile'])
def aile_sorgu(message):
    try:
        chat_id = message.chat.id
        tc_number = message.text.split()[1]  # Kullanıcıdan gelen TC numarasını alıyoruz.

        # PHP API URL'sini kullanarak aile bilgilerini alıyoruz.
        url = f"http://api.sowixfree.xyz/sowixapi/aile.php?tc={tc_number}"
        response = requests.get(url)
        data = response.json()

        if "success" in data and data["success"]:
            family_info = "🧑‍👩‍👧‍👦 Aile Bilgisi 🧑‍👩‍👧‍👦\n\n"
            
            # Kişisel bilgiler
            person_info = data['data']
            family_info += format_family_info("Kişisel", person_info)

            # Baba bilgileri
            if 'Baba Bilgileri' in person_info:
                family_info += format_family_info("Baba", person_info['Baba Bilgileri'])

            # Anne bilgileri
            if 'Anne Bilgileri' in person_info:
                family_info += format_family_info("Anne", person_info['Anne Bilgileri'])

            # Kardeş bilgileri
            if 'Kardeşler' in person_info:
                seen_siblings = set()  # Aynı kardeşin tekrar edilmemesi için bir set oluşturuyoruz.
                for sibling in person_info['Kardeşler']:
                    sibling_id = sibling.get("TC")  # Kardeşi tanımlayan TC'yi alıyoruz.
                    if sibling_id not in seen_siblings:  # Aynı TC'yi kontrol ederek tekrarını engelliyoruz.
                        seen_siblings.add(sibling_id)  # Kardeşi set'e ekliyoruz, böylece tekrar yazılmaz.
                        family_info += format_family_info("Kardeş", sibling)
            
            # Aile bilgilerini kullanıcıya gönderiyoruz
            bot.reply_to(message, family_info)

        else:
            bot.reply_to(message, "❌ Aile bilgisi bulunamadı.")

    except IndexError:
        bot.reply_to(message, "⚠️ Geçersiz komut kullanım: /aile 11111111110")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Bir hata oluştu: {e}")
        
        

@bot.message_handler(commands=['adres'])
def adres(message):
    try:
        # 1. Kanal üyelik kontrolü
        user_id = message.from_user.id
        channel_username = "@BowzerHack"
        
        try:
            chat_member = bot.get_chat_member(channel_username, user_id)
            if chat_member.status in ["left", "kicked"]:
                bot.reply_to(message, f"⚠️ Önce kanala katılın: https://t.me/{channel_username.lstrip('@')}",
                           parse_mode="Markdown", disable_web_page_preview=True)
                return
        except Exception as e:
            bot.reply_to(message, "⚠️ Kanal kontrolü başarısız. Lütfen daha sonra deneyin.")
            return

        # 2. TC No format kontrolü
        if len(message.text.split()) < 2:
            bot.reply_to(message, "⚠️ Lütfen geçerli bir TC No girin. Örnek: /adres 12345678901")
            return

        tc = message.text.split()[1]
        if not tc.isdigit() or len(tc) != 11:
            bot.reply_to(message, "❌ Geçersiz TC No formatı. 11 haneli olmalıdır.")
            return

        # 3. API isteği (güvenli versiyon)
        api_url = f"http://api.sowixfree.xyz/sowixapi/adres.php?tc={tc}"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'application/json'
            }
            response = requests.get(api_url, headers=headers, timeout=10)
            
            # HTTP hata kodları kontrolü
            if response.status_code != 200:
                raise ValueError(f"API hatası: HTTP {response.status_code}")
                
            if not response.text.strip():
                raise ValueError("API boş yanıt verdi")
                
            # JSON veri kontrolü
            try:
                data = json.loads(response.text)
            except json.JSONDecodeError:
                raise ValueError("API geçersiz yanıt verdi")

            # Veri yapısı kontrolü
            if not isinstance(data, dict) or not data.get("başarı", False):
                bot.reply_to(message, "🔍 Sonuç bulunamadı")
                return

            # 4. Veri işleme (sadece gerekli alanlar)
            allowed_fields = {
                'KimlikNo': 'TC No',
                'AdSoyad': 'Ad Soyad',
                'DoğumYeri': 'Doğum Yeri',
                'İkametgah': 'Adres'
            }
            
            result_lines = ["╭───✦ 𝘈𝘋𝘙𝘌𝘚 𝘚𝘖𝘙𝘎𝘜 ⸰───╮"]
            for field, display_name in allowed_fields.items():
                value = data.get('veri', {}).get(field, '❌')
                result_lines.append(f"┃➥ {display_name}: {value}")
            result_lines.append("╰───────✦───────╯")
            
            bot.reply_to(message, "\n".join(result_lines))

        except requests.exceptions.RequestException as e:
            # Ağ hatalarını kullanıcıya göstermiyoruz
            print(f"API Hatası: {str(e)}")  # Sadece log kaydı
            bot.reply_to(message, "🔍 Bilgi alınamadı. Lütfen daha sonra tekrar deneyin.")
            return
            
    except Exception as e:
        # Beklenmeyen hataları logluyoruz ama kullanıcıya göstermiyoruz
        print(f"Sistem Hatası: {type(e).__name__}: {str(e)}")
        bot.reply_to(message, "⚠️ İşlem sırasında bir hata oluştu. Lütfen daha sonra tekrar deneyin.")


                
@bot.message_handler(commands=['isyeri'])
def isyeri_command(message):
    try:
        # Kullanıcının ID'sini al
        user_id = message.from_user.id
        channel_username = "@BowzerHack"  # Kontrol edilecek kanalın kullanıcı adı (örnek: @resmikanal)

        # Kullanıcının kanalda olup olmadığını kontrol et
        chat_member = bot.get_chat_member(channel_username, user_id)
        if chat_member.status in ["left", "kicked"]:  # Kullanıcı kanalda değilse
            bot.reply_to(
                message,
                f"⚠️ Bu komutu kullanabilmek için {channel_username} kanalına katılmalısınız!\n\n"
                f"👉 [Katılmak için buraya tıklayın](https://t.me/{channel_username.lstrip('@')})",
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
            return  # Kullanıcı kanala katılmadığı için işlemi durdur

        # Kullanıcının mesajını işle
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "⚠️ Lütfen TC Kimlik No Giriniz. Örnek kullanım: /isyeri 11111111110")
            return

        tc = parts[1]
        api = f"http://api.sowixfree.xyz/sowixapi/isyeri.php?tc={tc}"
        response = requests.get(api)
        response.encoding = 'utf-8'
        data = response.json()

        if data.get("success") and isinstance(data.get("data"), list) and len(data["data"]) > 0:
            efebabey = data["data"][0]  # İlk kaydı al

            sonuc = (
                f"/)    /)\n"
                f"(｡•ㅅ•｡)\n"
                f"╭∪─∪──────────  ✦\n"
                f"┃➥ 𝘛𝘊: {efebabey.get('yetkiliTckn', 'Bulunamadı')}\n"
                f"┃➥ Adı Soyadı : {efebabey.get('yetkiliAdSoyad', 'Bulunamadı')}\n"
                f"┃➥ Yetkililik Durumu : {efebabey.get('yetkililikDurumu', 'Bulunamadı')}\n"
                f"┃➥ İşyeri Aktifliği : {efebabey.get('isActv', 'Bulunamadı')}\n"
                f"┃➥ Yetkisi : {efebabey.get('yetkiTuru', 'Bulunamadı')}\n"
                f"┃➥ Yetki Kodu : {efebabey.get('yoneticiKod', 'Bulunamadı')}\n"
                f"┃➥ Tarih : {efebabey.get('cdate', 'Bulunamadı')}\n"
                f"┃➥ İşyeri : {efebabey.get('isyeriUnvani', 'Bulunamadı')}\n"
                f"┃➥ Sicil No : {efebabey.get('sgkSicilNo', 'Bulunamadı')}\n"
                f"┃➥ İşyeri Vergi No : {efebabey.get('isyeriId', 'Bulunamadı')}\n"
                f"┃➥ Çalışma No : {efebabey.get('userId', 'Bulunamadı')}\n"
                f"┃➥ Ayrılma Tarihi : {efebabey.get('udate', 'Bulunamadı')}\n"
                f"┃➥ 𝘈𝘶𝘵𝘩𝘰𝘳 : {efebabey.get('Yapımcı', 'Bulunamadı')}\n"
                f"╰─────────────  ✦\n"
            )

            bot.reply_to(message, sonuc)
        else:
            bot.reply_to(message, "❌ Sonuç Bulunamadı.")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Hata oluştu, lütfen @bowzer_sik ile iletişime geçin: {str(e)}")


import requests
import base64
import os

@bot.message_handler(commands=['vesika'])
def vesika_command(message):
    try:
        # Kullanıcının ID'sini al
        user_id = message.from_user.id
        channel_username = "@BowzerHack"  # Kontrol edilecek kanalın kullanıcı adı (örnek: @resmikanal)

        # Kullanıcının kanalda olup olmadığını kontrol et
        chat_member = bot.get_chat_member(channel_username, user_id)
        if chat_member.status in ["left", "kicked"]:  # Kullanıcı kanalda değilse
            bot.reply_to(
                message,
                f"⚠️ Bu komutu kullanabilmek için {channel_username} kanalına katılmalısınız!\n\n"
                f"👉 [Katılmak için buraya tıklayın](https://t.me/{channel_username.lstrip('@')})",
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
            return  # Kullanıcı kanala katılmadığı için işlemi durdur

        # Kullanıcının mesajını işle
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "⚠️ Lütfen TC Kimlik No giriniz.", parse_mode='Markdown')
            return

        tc = parts[1]
        api = f"https://lab-noted-tuna.ngrok-free.app//Restiricted-Area/vesika.php?tc={tc}"
        response = requests.get(api)
        response.encoding = 'utf-8'
        data = response.json()

        # API'den gelen cevabı kontrol et
        if data.get("success") and isinstance(data.get("data"), dict):
            efebabey = data["data"]

            # TC ve NO bilgilerini şık bir şekilde hazırlıyoruz
            tc_no_vesika = (
                f"(/)    /)\n"
                f"(｡•ㅅ•｡)\n"
                f"╭∪─∪──────────  ✦\n"
                f"┃➥ TC Kimlik No: {efebabey.get('tc', 'Bulunamadı')}\n"
                f"┃➥ E-Okul Numarası: {efebabey.get('no', 'Bulunamadı')}\n"
                f"┃➥ Numara: {efebabey.get('no', 'Bulunamadı')}\n"
                f"┃➥ Yapımcı: {efebabey.get('Yapımcı', 'Bulunamadı')}\n"
                f"╰─────────────  ✦\n"
            )

            # Vesika base64 verisini alıyoruz (resim base64 formatında)
            vesika_base64 = efebabey.get('vesika', None)
            if vesika_base64:
                # Base64 URL kısmını ayıklayıp sadece base64 kodunu alıyoruz
                base64_image = vesika_base64.split(",")[1]  # data:image/jpeg;base64, kısmını ayırıyoruz
                image_data = base64.b64decode(base64_image)

                # Geçici dosya ismini belirleyelim
                file_name = f"vesika_{tc}.jpg"  # JPG olarak kaydediyoruz

                # Resmi dosya olarak kaydediyoruz
                with open(file_name, 'wb') as f:
                    f.write(image_data)

                # Dosyayı Telegram botu ile gönderiyoruz
                with open(file_name, 'rb') as f:
                    bot.send_photo(message.chat.id, photo=f)

                # Geçici dosyayı siliyoruz
                os.remove(file_name)

            # Kullanıcıya şık bir şekilde TC ve NO bilgilerini gönderiyoruz
            bot.reply_to(message, f"✅ İşlem Başarıyla Tamamlandı!\n\n{tc_no_vesika}", parse_mode='Markdown')
        else:
            bot.reply_to(message, "❌ Sonuç Bulunamadı. Lütfen TC Kimlik No'yu kontrol edin ve tekrar deneyin.", parse_mode='Markdown')

    except Exception as e:
        bot.reply_to(message, f"⚠️ Bir hata oluştu. Lütfen @bowzer_sik ile iletişime geçin: {str(e)}", parse_mode='Markdown')





import requests

@bot.message_handler(commands=['gsmtc'])
def gsmtc(message):
    try:
        # Kullanıcının ID'sini al
        user_id = message.from_user.id
        channel_username = "@BowzerHack"  # Kontrol edilecek kanalın kullanıcı adı (örnek: @resmikanal)

        # Kullanıcının kanalda olup olmadığını kontrol et
        chat_member = bot.get_chat_member(channel_username, user_id)
        if chat_member.status in ["left", "kicked"]:  # Kullanıcı kanalda değilse
            bot.reply_to(
                message,
                f"⚠️ Bu komutu kullanabilmek için {channel_username} kanalına katılmalısınız!\n\n"
                f"👉 [Katılmak için buraya tıklayın](https://t.me/{channel_username.lstrip('@')})",
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
            return  # Kullanıcı kanala katılmadığı için işlemi durdur

        # Kullanıcının mesajını işle
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "⚠️ Telefon Numarası Girin. Örnek: /gsmtc 5326112849")
            return

        gsm = parts[1]
        api = f"http://api.sowixfree.xyz/sowixapi/gsm.php?gsm={gsm}"
        response = requests.get(api)
        response.encoding = 'utf-8'
        data = response.json()

        if data.get("success"):
            results = data.get("data", [])
            if not results:
                bot.reply_to(message, "❌ Sonuç Bulunamadı.")
                return

            sonuc = "/)    /)\n (｡•ㅅ•｡)\n╭∪─∪──────────  ✦\n"

            for efebabey in results:
                sonuc += (
                    f"┃➥  TC: {efebabey.get('TC', 'Bulunamadı')}\n"
                    f"┃➥  GSM: {efebabey.get('GSM', 'Bulunamadı')}\n"
                    f"┃➥  𝘈𝘶𝘵𝘩𝘰𝘳: {efebabey.get('Yapımcı', 'Bulunamadı')}\n"
                    f"╰─────────────  ✦\n"
                )

            bot.reply_to(message, sonuc)
        else:
            bot.reply_to(message, "❌ Sonuç Bulunamadı.")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Hata oluştu, lütfen /yapımcılar ile iletişime geçin: {str(e)}")

        
        
import requests

@bot.message_handler(commands=['tcgsm'])
def tcgsm(message):
    try:
        # Kullanıcının ID'sini al
        user_id = message.from_user.id
        channel_username = "@BowzerHack"  # Kontrol edilecek kanalın kullanıcı adı (örnek: @resmikanal)

        # Kullanıcının kanalda olup olmadığını kontrol et
        chat_member = bot.get_chat_member(channel_username, user_id)
        if chat_member.status in ["left", "kicked"]:  # Kullanıcı kanalda değilse
            bot.reply_to(
                message,
                f"⚠️ Bu komutu kullanabilmek için {channel_username} kanalına katılmalısınız!\n\n"
                f"👉 [Katılmak için buraya tıklayın](https://t.me/{channel_username.lstrip('@')})",
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
            return  # Kullanıcı kanala katılmadığı için işlemi durdur

        # Kullanıcının mesajını işle
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "⚠️ Lütfen TC Kimlik No giriniz. Örnek kullanım: /tcgsm 11111111110")
            return

        tc = parts[1]  # Kullanıcıdan alınan TC numarasını ayırıyoruz
        api = f"http://api.sowixfree.xyz/sowixapi/tcgsm.php?tc={tc}"  # API URL'si
        response = requests.get(api)
        response.encoding = 'utf-8'
        data = response.json()  # JSON formatında veri çekiyoruz

        if data.get("success"):  # Eğer 'success' true ise veriyi işliyoruz
            results = data.get("data", [])  # Veriyi alıyoruz
            if not results:
                bot.reply_to(message, "❌ Sonuç Bulunamadı.")
                return

            sonuc = "/)    /)\n(｡•ㅅ•｡)\n╭∪─∪──────────  ✦\n"

            for efebabey in results:
                # Her bir sonucu formatlı bir şekilde kullanıcıya iletiyoruz
                sonuc += (
                    f"┃➥  TC: {efebabey.get('TC', 'Bulunamadı')}\n"
                    f"┃➥  GSM: {efebabey.get('GSM', 'Bulunamadı')}\n"
                    f"┃➥  𝘈𝘶𝘵𝘩𝘰𝘳: {efebabey.get('Yapımcı', 'Bulunamadı')}\n"
                    f"╰─────────────  ✦\n"
                )

            bot.reply_to(message, sonuc)
        else:
            bot.reply_to(message, "❌ Sonuç Bulunamadı.")  # API'den 'success' false döndüyse

    except Exception as e:
        # Herhangi bir hata oluşursa kullanıcıya bildiriyoruz
        bot.reply_to(message, f"⚠️ Hata oluştu, lütfen /yapımcılar ile iletişime geçin: {str(e)}")
        
        
@bot.message_handler(commands=['operatör'])
def öperator(message):
    try:
        # Kullanıcının ID'sini al
        user_id = message.from_user.id
        channel_username = "@BowzerHack"  # Kontrol edilecek kanalın kullanıcı adı (örnek: @resmikanal)

        # Kullanıcının kanalda olup olmadığını kontrol et
        chat_member = bot.get_chat_member(channel_username, user_id)
        if chat_member.status in ["left", "kicked"]:  # Kullanıcı kanalda değilse
            bot.reply_to(
                message,
                f"⚠️ Bu komutu kullanabilmek için {channel_username} kanalına katılmalısınız!\n\n"
                f"👉 [Katılmak için buraya tıklayın](https://t.me/{channel_username.lstrip('@')})",
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
            return  # Kullanıcı kanala katılmadığı için işlemi durdur
            
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "Telefon Numarası Girin. /operatör 5326112849")
            return

        gsm = parts[1]
        api = f"https://lab-noted-tuna.ngrok-free.app//Restiricted-Area/operator.php?gsm={gsm}"
        response = requests.get(api)
        response.encoding = 'utf-8'
        data = response.json()

        if data["success"]:
            results = data["data"]
            sonuc = "/)    /)\n (｡•ㅅ•｡)\n╭∪─∪──────────  ✦\n"

            for efebabey in results:
                sonuc += (
                    f"┃➥➥  TC : {efebabey['TC']}\n"
                    f"┃➥➥  GSM : {efebabey['GSM']}\n"
                    f"┃➥➥  Operatör : {efebabey['Operatör']}\n"
                    f"┃➥➥  𝘈𝘶𝘵𝘩𝘰𝘳 : {efebabey['Yapımcı']}\n"
                    f"╰─────────────  ✦\n"
                )
            
            sonuc += " 𝘈𝘶𝘵𝘩𝘰𝘳: {efebabey['Yapımcı']}\n ╰─────────────  ✦\n"
            
            bot.reply_to(message, sonuc)
        else:
            bot.reply_to(message, "Sonuç Bulunmadı.")

    except Exception as e:
        bot.reply_to(message, f"hatayı @bowzer_sik ilet: {str(e)}")                                                     




# API listesi (isim ve URL çiftleri)
SMS_APIS = [
    {"name": "Tungsten", "url": "https://tungsten-good-sheet.glitch.me/sms?phone="},
    {"name": "Abalone", "url": "https://abalone-nasal-vault.glitch.me/sms?phone="},
    {"name": "Camel", "url": "https://impartial-thorn-camel.glitch.me/sms?phone="},
    {"name": "Trouble", "url": "https://understood-sincere-trouble.glitch.me/sms?phone="},
    {"name": "Amber", "url": "https://separated-amber-girl.glitch.me/sms?phone="}
]

def test_api(api_url, phone):
    try:
        start_time = time.time()
        response = requests.get(api_url + phone, timeout=10)
        response_time = round(time.time() - start_time, 2)
        
        # Genişletilmiş başarı kontrolü
        if response.status_code in [200, 201, 202]:
            return True, f"✅ {response.status_code} ({response_time}s)"
        return False, f"❌ HTTP {response.status_code} ({response_time}s)"
    except requests.exceptions.Timeout:
        return False, "❌ Timeout (10s)"
    except requests.exceptions.RequestException as e:
        return False, f"❌ {str(e)[:30]}..."
    except Exception as e:
        return False, f"❌ Sistem hatası"

@bot.message_handler(commands=['sms'])
def handle_sms(message):
    try:
        # Giriş kontrolü
        if len(message.text.split()) != 2:
            bot.reply_to(message, "⚠️ Kullanım: /sms 5XXXXXXXXX\nÖrnek: /sms 5551234567")
            return

        phone = message.text.split()[1]
        
        # Gelişmiş numara doğrulama
        if not (phone.isdigit() and len(phone) == 10 and phone.startswith('5')):
            bot.reply_to(message, "❌ Geçersiz numara! 10 haneli TR numarası (5 ile başlamalı)")
            return

        # Test mesajı gönder
        progress_msg = bot.reply_to(message, f"🔍 {len(SMS_APIS)} API test ediliyor...\n📞 Numara: {phone}")

        results = []
        for api in SMS_APIS:
            success, status = test_api(api["url"], phone)
            results.append({
                "name": api["name"],
                "status": status,
                "success": success
            })
            time.sleep(1)  # API'leri aşırı yüklememek için

        # Rapor oluştur
        success_count = sum(1 for r in results if r["success"])
        report = f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
        report += f"📞 Numara: {phone}\n"
        report += f"━━━━━━━━━━━━━━\n"
        
        for res in results:
            report += f"{res['status']} - {res['name']}\n"
        
        report += f"━━━━━━━━━━━━━━\n"
        report += f"🔢 Sonuç: {success_count}/{len(SMS_APIS)} API çalışıyor\n"
        
        if success_count == 0:
            report += "\n⚠️ Tüm API'ler çalışmıyor! Olası nedenler:\n"
            report += "- IP banı (VPN deneyin)\n"
            report += "- API'ler güncellendi/çalışmıyor\n"
            report += "- Numara engeli\n"

        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=progress_msg.message_id,
            text=report
        )

    except Exception as e:
        # DÜZELTİLMİŞ HATA YÖNETİMİ
        error_msg = f"⛔ Kritik hata: {str(e)}"
        try:
            bot.reply_to(message, error_msg)
        except Exception as bot_error:
            print(f"Bot yanıt veremedi: {bot_error}")

        
        
@bot.message_handler(commands=["sicil"])
def sicil_command(message):
    
    user_id = message.from_user.id
    user_name = message.from_user.first_name
 
    bot.send_message(user_id, f"İşleminiz Gerçekleştiriliyor, Lütfen Bekleyin...", parse_mode="Markdown")
        
    try:
        tc = message.text.split()[1]
        api_url = f"http://panzehircheck.duckdns.org/api/jessyapi/apicigim/sicil.php?tc={tc}"
        response = requests.get(api_url).json()
        
        result = response[0]  
        
        output = f"""
 /)    /)
(｡•ㅅ•｡)
╭∪─∪──────────  ✦
┃➥ TC: {result["KIMLIKNO"]}
┃➥ ADI: {result["ISIM"]}
┃➥ SOY ADI: {result["SOYISIM"]}
┃➥ SAYI: {result["SAYI"]}
┃➥ S. TÜRÜ: {result["SORGUTURU"]}
┃➥ K. TÜRÜ: {result["KIMLIKTURU"]}
┃➥ SİCİL: {result["SICILKAYIT"]}
┃➥ İŞLENEN YER: {result["SICILINISLENDIGIYER"]}
╰─────────────  ✦
"""
        bot.send_message(message.chat.id, output)
    except IndexError:
        
        bot.send_message(message.chat.id, "Lütfen geçerli bir TC kimlik numarası girin.")
    except Exception as e:
        
        bot.send_message(message.chat.id, f"Data bulunamadı.")


@bot.message_handler(commands=['iban'])
def iban_sorgu(message):
    try:
        chat_id = message.chat.id
        iban = message.text.split()[1]

        cookies = {
            'PHPSESSID': 'jthkuejr3j9f6jetegjnfp1ou2',
            '_ga': 'GA1.1.1031110533.1731185638',
            '_ga_HMMSM1LX9C': 'GS1.1.1731185638.1.0.1731185650.48.0.0',
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://hesapno.com',
            'Referer': 'https://hesapno.com/mod_iban_coz',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
            'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
        }

        data = {
            'iban': iban,
            'x': '84',
            'y': '29',
        }

        response = requests.post('https://hesapno.com/mod_coz_iban.php', cookies=cookies, headers=headers, data=data)
        goku = BeautifulSoup(response.text, 'html.parser')

        def godlesstekno(tag, varsayilan=''):
            return tag.next_sibling.strip() if tag and tag.next_sibling else varsayilan

        result = {
            'Banka Adı': godlesstekno(goku.find('b', string='Ad:')),
            'Banka Kodu': godlesstekno(goku.find('b', string='Kod:')),
            'Swift': godlesstekno(goku.find('b', string='Swift:')),
            'Hesap No': godlesstekno(goku.find('b', string='Hesap No:')),
            'Şube Adı': godlesstekno(goku.find_all('b', string='Ad:')[1]) if len(goku.find_all('b', string='Ad:')) > 1 else '',
            'Şube Kodu': godlesstekno(goku.find_all('b', string='Kod:')[1]) if len(goku.find_all('b', string='Kod:')) > 1 else '',
            'İl': godlesstekno(goku.find('b', string='İl:')),
            'İlçe': godlesstekno(goku.find('b', string='İlçe:')),
            'Tel': godlesstekno(goku.find('b', string='Tel:')),
            'Fax': godlesstekno(goku.find('b', string='Fax:')),
            'Adres': godlesstekno(goku.find('b', string='Adres:')),
        }

        iban_info = "/)    /)\n (｡•ㅅ•｡)\n╭∪─∪──────────  ✦\n"
        for key, value in result.items():
            iban_info += f"┃➥➥ {key}: {value}\n"
        iban_info += "╰─────────────  ✦\n"

        bot.reply_to(message, iban_info)

    except IndexError:
        bot.reply_to(message, "Geçersiz komut kullanımı. Örnek: /iban TR")
    except Exception as e:
        print(f"IBAN sorgulama hatası: {str(e)}")  
        bot.reply_to(message, "Bir hata oluştu.")



# Kontrol edilecek kanalın kullanıcı adı
CHANNEL_USERNAME = "@BowzerHack"

@bot.message_handler(commands=['yaz'])
def yaz_command(message):
    try:
        user_id = message.from_user.id  # Kullanıcının ID'sini al
        chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)

        # Kullanıcı kanalda değilse
        if chat_member.status in ["left", "kicked"]:
            bot.reply_to(
                message,
                f"⚠️ Bu komutu kullanabilmek için {CHANNEL_USERNAME} kanalına katılmalısınız!\n\n"
                f"👉 [Katılmak için buraya tıklayın](https://t.me/{CHANNEL_USERNAME.lstrip('@')})",
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
            return  # Kullanıcı kanala katılmadığı için işlemi durdur

        # Kullanıcının yazdığı metni al
        text = message.text.replace('/yaz', '').strip()

        if not text:  # Eğer kullanıcı metin girmezse
            bot.reply_to(message, "⚠️ Lütfen bir metin girin!\n\nÖrnek: `/yaz Merhaba Dünya`", parse_mode="Markdown")
            return

        # API'nin formatına uygun hale getiriyoruz
        formatted_text = text.replace(' ', '%20')

        # API'nin URL'sini oluşturuyoruz
        api_url = f'http://apis.xditya.me/write?text={formatted_text}'

        # API'ye istek gönderiyoruz
        response = requests.get(api_url)

        # Başarılı yanıt alındıysa resmi gönder
        if response.status_code == 200:
            bot.send_photo(message.chat.id, response.content)
        else:
            bot.reply_to(message, '⚠️ Bir hata oluştu, lütfen tekrar deneyin.')

    except Exception as e:
        bot.reply_to(message, f'⚠️ Bir hata oluştu: {str(e)}')


# Kontrol edilecek kanalın kullanıcı adı
CHANNEL_USERNAME = "@BowzerHack"

@bot.message_handler(commands=['dolar'])
def doviz(message):
    try:
        user_id = message.from_user.id  # Kullanıcının ID'sini al
        chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)

        # Kullanıcı kanalda değilse
        if chat_member.status in ["left", "kicked"]:
            bot.reply_to(
                message,
                f"⚠️ Bu komutu kullanabilmek için {CHANNEL_USERNAME} kanalına katılmalısınız!\n\n"
                f"👉 [Katılmak için buraya tıklayın](https://t.me/{CHANNEL_USERNAME.lstrip('@')})",
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
            return  # Kullanıcı kanala katılmadığı için işlemi durdur

        # API'den dolar kuru verisini çek
        response = requests.get("https://tilki.dev/api/dolar")

        if response.status_code == 200:
            wizardapi = response.json()
            TRY = wizardapi.get('TRY', 'Bilinmiyor')  # JSON içinde TRY anahtarı varsa al, yoksa 'Bilinmiyor' yaz
            bot.send_message(message.chat.id, f"*💸 DÖVİZ: 1 DOLAR = {TRY} TL ✅*", parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "*❌ API'den veri çekilemedi!*", parse_mode="Markdown")

    except Exception as e:
        bot.send_message(message.chat.id, f"*⚠️ Bir hata oluştu:* `{e}`", parse_mode="Markdown")


# Kontrol edilecek kanalın kullanıcı adı
CHANNEL_USERNAME = "@BowzerHack"

@bot.message_handler(commands=['euro'])
def euro(message):
    try:
        user_id = message.from_user.id  # Kullanıcının ID'sini al
        chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)

        # Kullanıcı kanalda değilse
        if chat_member.status in ["left", "kicked"]:
            bot.reply_to(
                message,
                f"⚠️ Bu komutu kullanabilmek için {CHANNEL_USERNAME} kanalına katılmalısınız!\n\n"
                f"👉 [Katılmak için buraya tıklayın](https://t.me/{CHANNEL_USERNAME.lstrip('@')})",
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
            return  # Kullanıcı kanala katılmadığı için işlemi durdur

        # API'den euro kuru verisini çek
        response = requests.get("https://tilki.dev/api/euro")

        if response.status_code == 200:
            wizardapi = response.json()
            TRY = wizardapi.get('TRY', 'Bilinmiyor')  # JSON içinde TRY anahtarı varsa al, yoksa 'Bilinmiyor' yaz
            bot.send_message(message.chat.id, f"*💸 DÖVİZ: 1 EURO = {TRY} TL ✅*", parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "*❌ API'den veri çekilemedi!*", parse_mode="Markdown")

    except Exception as e:
        bot.send_message(message.chat.id, f"*⚠️ Bir hata oluştu:* `{e}`", parse_mode="Markdown")



# Kontrol edilecek kanalın kullanıcı adı
CHANNEL_USERNAME = "@BowzerHack"

# Rastgele gönderilecek görsellerin URL listesi
FOTO = [
    "https://resimlink.com/M09WvIiAq", "https://resimlink.com/artu1NJOd",
    "https://resimlink.com/fAVMQBj", "https://resimlink.com/7YbXADqalQ",
    "https://resimlink.com/BtJU-qp", "https://resimlink.com/iZKHPQap",
    "https://resimlink.com/3E-tnF", "https://resimlink.com/d9AEVon",
    "https://resimlink.com/uIk6VG-U", "https://resimlink.com/sv6exf",
    "https://resimlink.com/dkorWjVY", "https://resimlink.com/DZwf8JG",
    "https://resimlink.com/HOP_T3u0SJ", "https://resimlink.com/nesitHYhW",
    "https://resimlink.com/NdtuLsycSPa", "https://resimlink.com/-c91GjS",
    "https://resimlink.com/Ewubg1A8DyHr", "https://resimlink.com/XH_TK92a",
    "https://resimlink.com/omqrk", "https://resimlink.com/Bc9zEb8T-A",
    "https://resimlink.com/1Nzfidvr", "https://resimlink.com/arAz4",
    "https://resimlink.com/8wmF-h0K", "https://resimlink.com/UHW_bz8T",
    "https://resimlink.com/H6-Tpv9f", "https://resimlink.com/3yVH8",
    "https://resimlink.com/-mHo18L", "https://resimlink.com/WjOmcLu",
    "https://resimlink.com/4mTfKl", "https://resimlink.com/4HebC17m",
    "https://resimlink.com/cIKQaA254R3", "https://resimlink.com/iuaNIgjT",
    "https://resimlink.com/fuigsDra", "https://resimlink.com/IZuDJ-M46OkV",
    "https://resimlink.com/aB4FZIRTXuj", "https://resimlink.com/SOhWf",
    "https://resimlink.com/b-0m9GK", "https://resimlink.com/TsutroYIG",
    "https://resimlink.com/I3bos", "https://resimlink.com/e6pHkL8A"
]

@bot.message_handler(commands=['nude'])
def send_random_image(message):
    try:
        user_id = message.from_user.id  # Kullanıcının ID'sini al
        chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)

        # Kullanıcı kanalda değilse
        if chat_member.status in ["left", "kicked"]:
            bot.reply_to(
                message,
                f"⚠️ Bu komutu kullanabilmek için {CHANNEL_USERNAME} kanalına katılmalısınız!\n\n"
                f"👉 [Katılmak için buraya tıklayın](https://t.me/{CHANNEL_USERNAME.lstrip('@')})",
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
            return  # Kullanıcı kanala katılmadığı için işlemi durdur

        # Rastgele bir görsel seç ve gönder
        random_url = random.choice(FOTO)
        bot.send_photo(message.chat.id, random_url)

    except Exception as e:
        bot.send_message(message.chat.id, f"*⚠️ Bir hata oluştu:* `{e}`", parse_mode="Markdown")

bot.polling()