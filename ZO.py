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
BOT_TOKEN = "8243804176:AAHddGdjqOlzACwDL8sTGzJjMGdo7KNI6ko"
bot = telebot.TeleBot(BOT_TOKEN)
CHAT_ID = "8317643774"

# Dictionary untuk menyimpan state user
user_states = {}

# Template pesan report
body_template = """Halo Tim TikTok,

Saya ingin melaporkan akun @{username} karena telah melanggar aturan komunitas TikTok. 
Akun ini telah menampilkan konten yang tidak pantas dan melanggar pedoman komunitas.

Mohon agar akun ini ditinjau dan diambil tindakan yang sesuai.

Terima kasih,
Pengguna TikTok"""

# List target email TikTok
tiktok_emails = [
    "feedback@tiktok.com",
    "legal@tiktok.com", 
    "privacy@tiktok.com",
    "abuse@tiktok.com",
    "info@tiktok.com"
]

# List username TikTok untuk report otomatis
tiktok_username_list = ["example_user1", "example_user2", "example_user3"]

# Counter untuk tracking pengiriman
email_counter = 0

# Path ke video Hozoo
VIDEO_PATH = "hozoo.mp4"

# Konfigurasi SMTP NYATA (GANTI DENGAN EMAIL ANDA)
REAL_EMAIL = "lkali8154@gmail.com"  # Ganti dengan email Gmail nyata
REAL_PASSWORD = "snle-msef-apmg-qwwj"  # Ganti dengan App Password Gmail

# Fungsi untuk install dependencies
def install_dependencies():
    try:
        import requests
        import telebot
        print("✓ Dependencies sudah terinstall")
    except ImportError as e:
        print(f"✗ Dependencies belum lengkap: {e}")
        print("Menginstall dependencies...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "--version"])
        except:
            print("Installing pip...")
            if 'ANDROID_ROOT' in os.environ:
                os.system("pkg install python-pip -y")
            else:
                os.system("sudo apt install python3-pip -y")
        
        packages = ["requests", "pyTelegramBotAPI"]
        for package in packages:
            print(f"Installing {package}...")
            os.system(f"pip install {package}")
        
        print("✓ Semua dependencies berhasil diinstall")

# Fungsi untuk membersihkan username
def clean_username(username):
    if username.startswith('@'):
        username = username[1:]
    cleaned = re.sub(r'[^a-zA-Z0-9_.]', '', username)
    return cleaned

# Fungsi untuk mendapatkan email sementara dari 1secmail.com 
def get_1secmail_email():
    try:
        url = "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            email_data = response.json()
            if email_data and len(email_data) > 0:
                email = email_data[0]
                print(f"✓ Generated 1secmail: {email}")
                return email
        return None
    except Exception as e:
        print(f"✗ Error getting 1secmail: {e}")
        return None

# Fungsi untuk mengirim email NYATA dengan SMTP Gmail
def send_real_email_gmail(subject, body, receiver_email, fake_sender_name):
    global email_counter
    
    try:
        # Konfigurasi SMTP Gmail
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        # Buat message
        message = MIMEMultipart()
        message["From"] = f"{fake_sender_name} <{REAL_EMAIL}>"
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
        
        # Context SSL
        context = ssl.create_default_context()
        
        # Kirim email dengan login Gmail nyata
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(REAL_EMAIL, REAL_PASSWORD)
            server.sendmail(REAL_EMAIL, receiver_email, message.as_string())
        
        email_counter += 1
        print(f"✓ Email #{email_counter} berhasil dikirim ke {receiver_email}")
        return True
        
    except Exception as e:
        print(f"✗ Gagal mengirim email ke {receiver_email}: {e}")
        return False

# Fungsi untuk mengirim email menggunakan HTTP API (Alternatif)
def send_email_via_http(subject, body, receiver_email, sender_name):
    try:
        # Gunakan layanan email via HTTP (contoh: EmailJS, SendGrid, dll)
        # Ini adalah fallback jika SMTP tidak bekerja
        
        print(f"📧 HTTP Send: {sender_name} -> {receiver_email}")
        print(f"📝 Subject: {subject}")
        
        # Simulasi pengiriman berhasil (untuk testing)
        # Dalam implementasi nyata, ganti dengan API email yang sesungguhnya
        time.sleep(1)
        
        global email_counter
        email_counter += 1
        return True
        
    except Exception as e:
        print(f"✗ Gagal HTTP send: {e}")
        return False

# Fungsi untuk mass report dengan multiple emails
def mass_report_tiktok(username_target, count=3):
    global email_counter
    
    success_count = 0
    failed_count = 0
    
    print(f"🚀 Starting mass report for @{username_target} (x{count})")
    
    for i in range(count):
        try:
            # Generate nama pengirim acak
            fake_names = [
                "User Concerned", "Community Member", "TikTok User", 
                "Content Reporter", "Safety Volunteer", "Platform User"
            ]
            fake_sender = random.choice(fake_names)
            
            # Pilih random target email
            target_email = random.choice(tiktok_emails)
            
            # Buat subject dan body
            subject_variants = [
                f"Report Violation - @{username_target}",
                f"Content Violation Report - @{username_target}",
                f"Community Guidelines Violation - @{username_target}",
                f"Inappropriate Content - @{username_target}",
                f"User Report - @{username_target}"
            ]
            subject = random.choice(subject_variants)
            body = body_template.format(username=username_target)
            
            # Coba kirim email dengan metode utama (SMTP Gmail)
            if REAL_EMAIL and REAL_PASSWORD:
                success = send_real_email_gmail(subject, body, target_email, fake_sender)
            else:
                # Fallback ke metode HTTP
                success = send_email_via_http(subject, body, target_email, fake_sender)
            
            if success:
                success_count += 1
            else:
                failed_count += 1
            
            # Delay kecil antara pengiriman
            time.sleep(2)
                
        except Exception as e:
            print(f"✗ Error in mass report iteration {i}: {e}")
            failed_count += 1
            continue
    
    return success_count, failed_count

# Fungsi untuk mendapatkan informasi cuaca
def get_weather():
    try:
        location = "Jakarta"
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
    # Kirim video Hozoo jika ada
    try:
        if os.path.exists(VIDEO_PATH):
            with open(VIDEO_PATH, 'rb') as video:
                bot.send_video(message.chat.id, video, caption="🎬 **Welcome to TikTok Report Bot**")
            print("✓ Video Hozoo berhasil dikirim")
        else:
            print("ℹ️ Video Hozoo tidak ditemukan, melanjutkan tanpa video...")
    except Exception as e:
        print(f"✗ Error sending video: {e}")
    
    # Cek konfigurasi email
    email_status = "❌ BELUM DIKONFIGURASI" if not REAL_EMAIL or REAL_EMAIL == "youremail@gmail.com" else "✅ AKTIF"
    
    welcome_text = f"""
🤖 **BOT TIKTOK MASS REPORT - REAL EMAIL**

**Fitur yang tersedia:**
/report - Report akun TikTok (3 emails)
/massreport - Mass report (5 emails)
/info - Info sistem & statistik
/weather - Info cuaca
/help - Bantuan

**Status Email:** {email_status}

**Cara Setup Email:**
1. Ganti REAL_EMAIL dan REAL_PASSWORD di script
2. Gunakan App Password Gmail (bukan password biasa)
3. Test dengan /report

Silakan pilih menu:
    """
    
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item1 = types.KeyboardButton('/report')
    item2 = types.KeyboardButton('/massreport') 
    item3 = types.KeyboardButton('/info')
    item4 = types.KeyboardButton('/weather')
    item5 = types.KeyboardButton('/help')
    markup.add(item1, item2, item3, item4, item5)

    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = f"""
📖 **BANTUAN BOT TIKTOK REPORT**

**CARA SETUP EMAIL (PENTING!):**
1. Buka Google Account → Security → 2-Step Verification → ON
2. Buka Security → App Passwords → Generate password untuk "Mail"
3. Ganti di script:
   REAL_EMAIL = "email-anda@gmail.com"
   REAL_PASSWORD = "app-password-dari-google"

**Commands:**
/start, /menu - Menu utama + Video Hozoo
/report - Report akun TikTok (3 emails)
/massreport - Mass report (5 emails)
/info - Info sistem & statistik
/weather - Info cuaca

**Format Username:**
@username atau username saja
    """
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['report'])
def report_command(message):
    # Cek konfigurasi email
    if not REAL_EMAIL or REAL_EMAIL == "youremail@gmail.com":
        bot.reply_to(message, 
                    "❌ **EMAIL BELUM DIKONFIGURASI**\n\n"
                    "Silakan setup email terlebih dahulu:\n"
                    "1. Ganti REAL_EMAIL dan REAL_PASSWORD di script\n"
                    "2. Gunakan App Password Gmail\n"
                    "3. Restart bot\n\n"
                    "Lihat /help untuk panduan detail.",
                    parse_mode='Markdown')
        return
    
    user_states[message.chat.id] = "awaiting_single_username"
    bot.reply_to(message, 
                "🔧 **SINGLE REPORT MODE**\n\n"
                "Ketik username TikTok yang ingin di-report:\n"
                "Akan dikirim 3 email sekaligus!\n"
                "Contoh: `@username` atau `username`",
                parse_mode='Markdown',
                reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(commands=['massreport'])
def massreport_command(message):
    # Cek konfigurasi email
    if not REAL_EMAIL or REAL_EMAIL == "youremail@gmail.com":
        bot.reply_to(message, 
                    "❌ **EMAIL BELUM DIKONFIGURASI**\n\n"
                    "Silakan setup email terlebih dahulu di script.",
                    parse_mode='Markdown')
        return
    
    user_states[message.chat.id] = "awaiting_mass_username" 
    bot.reply_to(message,
                "💣 **MASS REPORT MODE**\n\n"
                "Ketik username TikTok untuk MASS REPORT:\n"
                "Akan dikirim 5 email sekaligus!\n"
                "Contoh: `@username` atau `username`",
                parse_mode='Markdown',
                reply_markup=types.ReplyKeyboardRemove())

# Handler untuk input username single report
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "awaiting_single_username")
def handle_single_username(message):
    user_states[message.chat.id] = None
    process_single_report(message, message.text)

# Handler untuk input username mass report  
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "awaiting_mass_username")
def handle_mass_username(message):
    user_states[message.chat.id] = None
    process_mass_report(message, message.text)

# Fungsi untuk single report
def process_single_report(message, username_input):
    try:
        username_target = clean_username(username_input)
        
        if not username_target:
            bot.reply_to(message, "❌ Username tidak valid. Silakan coba lagi.")
            return
        
        bot.reply_to(message, f"🔄 Memproses SINGLE REPORT untuk @{username_target}...")
        
        # Kirim 3 emails untuk single report
        success_count, failed_count = mass_report_tiktok(username_target, count=3)
        
        report_result = f"""
✅ **SINGLE REPORT COMPLETED**

🎯 Target: `@{username_target}`
📧 Emails Sent: `{success_count}`
❌ Failed: `{failed_count}`
⏰ Time: `{datetime.now().strftime('%H:%M:%S')}`
📊 Total Sent: `{email_counter}`

Reports telah dikirim ke TikTok menggunakan REAL EMAIL!
        """
        bot.reply_to(message, report_result, parse_mode='Markdown')
            
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# Fungsi untuk mass report
def process_mass_report(message, username_input):
    try:
        username_target = clean_username(username_input)
        
        if not username_target:
            bot.reply_to(message, "❌ Username tidak valid. Silakan coba lagi.")
            return
        
        bot.reply_to(message, f"💣 Memproses MASS REPORT untuk @{username_target}...")
        
        # Kirim 5 emails untuk mass report
        success_count, failed_count = mass_report_tiktok(username_target, count=5)
        
        report_result = f"""
💣 **MASS REPORT COMPLETED**

🎯 Target: `@{username_target}`
📧 Emails Sent: `{success_count}`
❌ Failed: `{failed_count}`
⏰ Time: `{datetime.now().strftime('%H:%M:%S')}`
📊 Total Sent: `{email_counter}`

Mass reports telah dikirim ke TikTok!
        """
        bot.reply_to(message, report_result, parse_mode='Markdown')
            
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# Handler untuk username langsung
@bot.message_handler(func=lambda message: message.text and 
                    (message.text.startswith('@') or 
                     (len(message.text) > 2 and 
                     not message.text.startswith('/') and
                     re.match(r'^[@a-zA-Z0-9_.]+$', message.text))))
def handle_direct_username(message):
    if user_states.get(message.chat.id):
        return
        
    username_input = message.text
    process_single_report(message, username_input)

@bot.message_handler(commands=['info'])
def info(message):
    try:
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        system_info = get_system_info()
        
        email_status = "❌ BELUM DIKONFIGURASI" if not REAL_EMAIL or REAL_EMAIL == "youremail@gmail.com" else "✅ AKTIF"
        
        info_text = f"""
📊 **SYSTEM INFO & STATS**

⏰ Waktu: `{date_time}`
{system_info}
📧 Email Status: `{email_status}`
📨 Emails Sent: `{email_counter}`
👥 Active Users: `{len(user_states)}`

**Fitur:**
✅ Real Email (Gmail SMTP)
✅ Video Hozoo Integration  
✅ Mass Report Mode
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

# Fungsi utama
def main():
    print("🤖 Starting TikTok Mass Report Bot...")
    print("🔧 Checking dependencies...")
    install_dependencies()
    
    # Cek konfigurasi email
    if not REAL_EMAIL or REAL_EMAIL == "youremail@gmail.com":
        print("❌ PERINGATAN: Email belum dikonfigurasi!")
        print("📧 Silakan ganti REAL_EMAIL dan REAL_PASSWORD di script")
        print("🔐 Gunakan App Password Gmail (bukan password biasa)")
    else:
        print("✅ Email configuration: READY")
    
    print("🎬 Video Hozoo: READY" if os.path.exists(VIDEO_PATH) else "🎬 Video Hozoo: NOT FOUND")
    print("💬 Bot ready! Check your Telegram and send /start")
    
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"❌ Bot error: {e}")
        print("🔄 Restarting in 5 seconds...")
        time.sleep(5)
        main()

if __name__ == "__main__":
    print("=" * 60)
    print("TIKTOK MASS REPORT BOT - REAL GMAIL SMTP")
    print("Powered by Real Email + Video Hozoo")
    print("Compatible with Termux, Ubuntu, Linux")
    print("=" * 60)
    
    main()
