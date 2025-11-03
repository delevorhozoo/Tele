#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import telebot
import smtplib
import ssl
import time
import random
import os
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import subprocess
from telebot import types
import sys

# Konfigurasi Bot - GANTI DENGAN DATA ANDA SENDIRI
BOT_TOKEN = "8243804176:AAHddGdjqOlzACwDL8sTGzJjMGdo7KNI6ko"  # Ganti dengan token bot Anda
bot = telebot.TeleBot(BOT_TOKEN)
CHAT_ID = "8317643774"  # Ganti dengan chat ID Anda

# Konfigurasi email
sender_email = "your-email@gmail.com"  # Ganti dengan email Anda
sender_password = "your-app-password"  # Ganti dengan app password email
receiver_email = "feedback@tiktok.com"

# Template pesan report
body_template = """Halo Tim TikTok,

Saya ingin melaporkan akun @{username} karena telah melanggar aturan komunitas TikTok. 
Akun ini telah menampilkan konten yang tidak pantas dan melanggar pedoman komunitas.

Mohon agar akun ini ditinjau dan diambil tindakan yang sesuai.

Terima kasih,
Pengguna TikTok"""

# List username TikTok untuk report (ganti dengan target yang valid)
tiktok_username_list = ["example_user1", "example_user2", "example_user3"]

# Fungsi untuk install dependencies
def install_dependencies():
    try:
        import requests
        import telebot
        print("✓ Dependencies sudah terinstall")
    except ImportError as e:
        print(f"✗ Dependencies belum lengkap: {e}")
        print("Menginstall dependencies...")
        
        # Install pip jika belum ada
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "--version"])
        except:
            print("Installing pip...")
            if 'ANDROID_ROOT' in os.environ:  # Termux
                os.system("pkg install python-pip -y")
            else:  # Ubuntu/Linux
                os.system("sudo apt install python3-pip -y")
        
        # Install packages
        packages = ["requests", "pyTelegramBotAPI", "beautifulsoup4"]
        for package in packages:
            print(f"Installing {package}...")
            os.system(f"pip install {package}")
        
        print("✓ Semua dependencies berhasil diinstall")

# Fungsi untuk mendapatkan email sementara (versi sederhana)
def get_temp_email():
    try:
        # Menggunakan layanan temp-mail yang sederhana
        domains = ["tempmail.com", "mailinator.com", "guerrillamail.com"]
        domain = random.choice(domains)
        random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz1234567890', k=10))
        email = f"{random_string}@{domain}"
        print(f"Generated temp email: {email}")
        return email
    except Exception as e:
        print(f"Error generating temp email: {e}")
        return f"temp{random.randint(1000,9999)}@example.com"

# Fungsi untuk mengirim email
def send_email(subject, body, receiver_email, sender_email):
    try:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Gunakan SMTP yang sesuai
        if "gmail" in sender_email:
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
        else:
            smtp_server = "smtp.example.com"
            smtp_port = 587

        context = ssl.create_default_context()
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            if sender_password:  # Hanya login jika ada password
                server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        
        print(f"✓ Email berhasil dikirim ke {receiver_email}")
        return True
    except Exception as e:
        print(f"✗ Gagal mengirim email: {e}")
        return False

# Fungsi untuk mendapatkan informasi cuaca
def get_weather():
    try:
        # Menggunakan API cuaca gratis
        # Anda bisa mendapatkan API key gratis dari openweathermap.org
        api_key = "demo_key"  # Ganti dengan API key Anda
        location = "Jakarta"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            weather_desc = data['weather'][0]['description']
            temperature = data['main']['temp']
            return f"🌤 Cuaca di {location}: {weather_desc}, Suhu: {temperature}°C"
        else:
            return "❌ Tidak bisa mendapatkan info cuaca saat ini"
    except Exception as e:
        return f"❌ Error mendapatkan cuaca: {e}"

# Fungsi untuk mendapatkan info sistem
def get_system_info():
    try:
        system_info = []
        system_info.append(f"🖥 Platform: {sys.platform}")
        system_info.append(f"🐍 Python: {sys.version.split()[0]}")
        
        if 'ANDROID_ROOT' in os.environ:
            system_info.append("📱 Environment: Termux")
        else:
            system_info.append("💻 Environment: Desktop/Linux")
            
        return "\n".join(system_info)
    except Exception as e:
        return f"Error getting system info: {e}"

# Handler commands
@bot.message_handler(commands=['start', 'menu'])
def menu(message):
    welcome_text = """
🤖 **BOT MULTI-FUNGSI**

**Fitur yang tersedia:**
/report - Report akun TikTok
/info - Info waktu dan sistem
/weather - Info cuaca
/help - Bantuan

Silakan pilih menu di bawah atau ketik command:
    """
    
    # Buat tombol navigasi
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item1 = types.KeyboardButton('/report')
    item2 = types.KeyboardButton('/info')
    item3 = types.KeyboardButton('/weather')
    item4 = types.KeyboardButton('/help')
    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
📖 **BANTUAN BOT**

**Commands:**
/start atau /menu - Menu utama
/report - Report akun TikTok ke email resmi
/info - Info waktu dan sistem
/weather - Info cuaca terkini
/help - Menampilkan bantuan ini

**Cara penggunaan:**
1. Untuk report TikTok, gunakan /report
2. Bot akan otomatis generate email dan mengirim report
3. Tunggu konfirmasi dari bot

**Note:** Fitur report menggunakan email sementara dan mungkin memiliki limitasi.
    """
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['report'])
def report(message):
    try:
        bot.reply_to(message, "🔄 Memproses report TikTok...")
        
        # Generate email sementara
        temp_email = get_temp_email()
        username_target = random.choice(tiktok_username_list)
        
        # Buat subject dan body
        subject = f"Report Akun TikTok @{username_target}"
        body = body_template.format(username=username_target)
        
        # Kirim email
        success = send_email(subject, body, receiver_email, temp_email)
        
        if success:
            report_result = f"""
✅ **REPORT BERHASIL**

📧 Email Pengirim: `{temp_email}`
📨 Email Tujuan: `{receiver_email}`
🎯 Target: `@{username_target}`
⏰ Waktu: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`

Report telah dikirim ke TikTok!
            """
            bot.reply_to(message, report_result, parse_mode='Markdown')
        else:
            bot.reply_to(message, "❌ Gagal mengirim report. Coba lagi nanti.")
            
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

@bot.message_handler(commands=['info'])
def info(message):
    try:
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        system_info = get_system_info()
        
        info_text = f"""
🕐 **INFO SISTEM**

⏰ Waktu: `{date_time}`
{system_info}
📊 Status: `Bot berjalan normal`
        """
        bot.reply_to(message, info_text, parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

@bot.message_handler(commands=['weather'])
def weather_command(message):
    try:
        bot.reply_to(message, "🌤 Mendapatkan info cuaca...")
        weather_info = get_weather()
        bot.reply_to(message, weather_info)
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text.startswith('@'):
        bot.reply_to(message, f"🔍 Username: {message.text}")
    else:
        bot.reply_to(message, "❌ Command tidak dikenali. Ketik /menu untuk melihat daftar command.")

# Fungsi utama
def main():
    print("🤖 Starting Telegram Bot...")
    print("🔧 Checking dependencies...")
    install_dependencies()
    
    print("✅ Bot ready!")
    print("💬 Check your Telegram bot and send /start")
    
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"❌ Bot error: {e}")
        print("🔄 Restarting in 10 seconds...")
        time.sleep(10)
        main()

if __name__ == "__main__":
    # Banner
    print("=" * 50)
    print("TELEGRAM BOT MULTI-FUNCTION")
    print("Compatible with Termux, Ubuntu, Linux")
    print("=" * 50)
    
    main()
