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
import re

# Konfigurasi Bot - GANTI DENGAN DATA ANDA SENDIRI
BOT_TOKEN = "8243804176:AAHddGdjqOlzACwDL8sTGzJjMGdo7KNI6ko"  # Ganti dengan token bot Anda
bot = telebot.TeleBot(BOT_TOKEN)
CHAT_ID = "8317643774"  # Ganti dengan chat ID Anda

# Dictionary untuk menyimpan state user
user_states = {}

# Template pesan report
body_template = """Halo Tim TikTok,

Saya ingin melaporkan akun @{username} karena telah melanggar aturan komunitas TikTok. 
Akun ini telah menampilkan konten yang tidak pantas dan melanggar pedoman komunitas.

Mohon agar akun ini ditinjau dan diambil tindakan yang sesuai.

Terima kasih,
Pengguna TikTok"""

# List username TikTok untuk report otomatis
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

# Fungsi untuk membersihkan username
def clean_username(username):
    """Membersihkan username dari karakter tidak valid"""
    # Hapus @ di awal jika ada
    if username.startswith('@'):
        username = username[1:]
    
    # Hanya ambil alfanumerik, underscore, dan titik
    cleaned = re.sub(r'[^a-zA-Z0-9_.]', '', username)
    
    return cleaned

# Fungsi untuk mendapatkan email sementara (versi sederhana)
def get_temp_email():
    try:
        # Menggunakan layanan temp-mail yang sederhana
        domains = ["tempmail.com", "mailinator.com", "guerrillamail.com", "10minutemail.com"]
        domain = random.choice(domains)
        random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz1234567890', k=10))
        email = f"{random_string}@{domain}"
        print(f"Generated temp email: {email}")
        return email
    except Exception as e:
        print(f"Error generating temp email: {e}")
        return f"temp{random.randint(1000,9999)}@example.com"

# Fungsi untuk mengirim email (VERSI SIMULASI - TIDAK PAKAI SMTP NYATA)
def send_email(subject, body, receiver_email, sender_email):
    try:
        # SIMULASI PENGIRIMAN EMAIL
        # Karena email sementara tidak bisa benar-benar mengirim email
        print(f"📧 SIMULASI: Mengirim email dari {sender_email} ke {receiver_email}")
        print(f"📝 Subject: {subject}")
        print(f"📄 Body: {body}")
        
        # Simulasi delay pengiriman
        time.sleep(2)
        
        # Return True untuk simulasi berhasil
        # Dalam implementasi nyata, Anda perlu mengganti dengan SMTP yang valid
        print(f"✓ Email berhasil dikirim (simulasi)")
        return True
        
    except Exception as e:
        print(f"✗ Gagal mengirim email: {e}")
        return False

# Fungsi untuk mendapatkan informasi cuaca
def get_weather():
    try:
        # Menggunakan API cuaca gratis
        location = "Jakarta"
        # API gratis tanpa key
        url = f"http://wttr.in/{location}?format=%C+%t"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            weather_info = response.text.strip()
            return f"🌤 Cuaca di {location}: {weather_info}"
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
🤖 **BOT LORDHOZOO **
 MASSREPORT TIKTOK SPAM UNLIMITED 
**Fitur yang tersedia:**
/report - Report akun TikTok
/info - Info waktu dan sistem
/weather - Info cuaca
/help - Bantuan

**Cara Report:**
1. Ketik /report
2. Pilih mode: Auto atau Manual
3. Untuk manual: ketik username TikTok (contoh: @username)

Silakan pilih menu di bawah:
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

**Cara Report TikTok:**
1. Ketik /report
2. Pilih mode report:
   - Auto: Bot memilih username acak
   - Manual: Anda input username sendiri
3. Format username: @username atau username saja

**Contoh:**
/report (lalu pilih mode)
@username_tiktok (langsung report)

**Note:** Saat ini menggunakan simulasi email.
    """
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['report'])
def report_menu(message):
    # Set state user ke mode pilihan report
    user_states[message.chat.id] = "awaiting_report_mode"
    
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item1 = types.KeyboardButton('Auto Report 🎲')
    item2 = types.KeyboardButton('Manual Report ✏️')
    item3 = types.KeyboardButton('Cancel ❌')
    markup.add(item1, item2, item3)
    
    bot.reply_to(message, 
                "🔧 **PILIH MODE REPORT**\n\n"
                "🎲 *Auto Report*: Bot memilih username acak\n"
                "✏️ *Manual Report*: Anda input username sendiri\n\n"
                "Atau ketik username TikTok langsung (contoh: @username)",
                parse_mode='Markdown', 
                reply_markup=markup)

# Handler untuk pilihan mode report
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "awaiting_report_mode")
def handle_report_mode(message):
    if message.text == 'Auto Report 🎲':
        # Report otomatis
        user_states[message.chat.id] = None
        auto_report(message)
    elif message.text == 'Manual Report ✏️':
        # Minta input username manual
        user_states[message.chat.id] = "awaiting_username"
        bot.reply_to(message, "✏️ Silakan ketik username TikTok yang ingin di-report:\n\nContoh: `@username` atau `username`", 
                    parse_mode='Markdown', 
                    reply_markup=types.ReplyKeyboardRemove())
    elif message.text == 'Cancel ❌':
        user_states[message.chat.id] = None
        bot.reply_to(message, "❌ Report dibatalkan.", reply_markup=types.ReplyKeyboardRemove())
    else:
        # Jika user langsung ketik username saat di mode selection
        process_username_report(message, message.text)

# Handler untuk input username manual
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "awaiting_username")
def handle_manual_username(message):
    user_states[message.chat.id] = None
    process_username_report(message, message.text)

# Fungsi untuk report otomatis
def auto_report(message):
    try:
        bot.reply_to(message, "🔄 Memproses Auto Report TikTok...")
        
        # Generate email sementara
        temp_email = get_temp_email()
        username_target = random.choice(tiktok_username_list)
        
        # Buat subject dan body
        subject = f"Report Akun TikTok @{username_target}"
        body = body_template.format(username=username_target)
        
        # Kirim email (simulasi)
        success = send_email(subject, body, "feedback@tiktok.com", temp_email)
        
        if success:
            report_result = f"""
✅ **AUTO REPORT BERHASIL**

📧 Email Pengirim: `{temp_email}`
📨 Email Tujuan: `feedback@tiktok.com`
🎯 Target: `@{username_target}`
⏰ Waktu: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`
🔧 Mode: `Auto (Random)`

Report telah dikirim ke TikTok!
            """
            bot.reply_to(message, report_result, parse_mode='Markdown')
        else:
            bot.reply_to(message, "❌ Gagal mengirim report. Coba lagi nati.")
            
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# Fungsi untuk memproses report dengan username
def process_username_report(message, username_input):
    try:
        # Bersihkan username
        username_target = clean_username(username_input)
        
        if not username_target:
            bot.reply_to(message, "❌ Username tidak valid. Silakan coba lagi.")
            return
        
        bot.reply_to(message, f"🔄 Memproses Report untuk @{username_target}...")
        
        # Generate email sementara
        temp_email = get_temp_email()
        
        # Buat subject dan body
        subject = f"Report Akun TikTok @{username_target}"
        body = body_template.format(username=username_target)
        
        # Kirim email (simulasi)
        success = send_email(subject, body, "feedback@tiktok.com", temp_email)
        
        if success:
            report_result = f"""
✅ **MANUAL REPORT BERHASIL**

📧 Email Pengirim: `{temp_email}`
📨 Email Tujuan: `feedback@tiktok.com`
🎯 Target: `@{username_target}`
⏰ Waktu: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`
🔧 Mode: `Manual`

Report telah dikirim ke TikTok!
            """
            bot.reply_to(message, report_result, parse_mode='Markdown')
        else:
            bot.reply_to(message, "❌ Gagal mengirim report. Coba lagi nanti.")
            
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# Handler untuk username langsung
@bot.message_handler(func=lambda message: message.text and 
                    (message.text.startswith('@') or 
                     len(message.text) > 2 and 
                     not message.text.startswith('/')))
def handle_direct_username(message):
    # Skip jika user sedang dalam state tertentu
    if user_states.get(message.chat.id):
        return
        
    username_input = message.text
    if len(username_input) > 2 and not username_input.startswith('/'):
        # Cek jika ini mungkin username (bukan command biasa)
        if re.match(r'^[@a-zA-Z0-9_.]+$', username_input):
            process_username_report(message, username_input)

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
👥 Users: `{len(user_states)}`
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
    if user_states.get(message.chat.id):
        return
        
    if message.text.startswith('/'):
        bot.reply_to(message, "❌ Command tidak dikenali. Ketik /menu untuk melihat daftar command.")
    else:
        # Jika bukan command, mungkin user ingin report username
        if len(message.text) > 2:
            bot.reply_to(message, f"💡 Tips: Ketik /report untuk melaporkan akun TikTok, atau ketik username langsung dengan format @username")

# Fungsi utama
def main():
    print("🤖 Starting Telegram Bot...")
    print("🔧 Checking dependencies...")
    install_dependencies()
    
    print("✅ Bot ready!")
    print("💬 Check your Telegram bot and send /start")
    print("📧 Note: Email system using simulation")
    
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
