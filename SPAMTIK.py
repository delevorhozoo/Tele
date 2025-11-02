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
import subprocess  # Untuk menjalankan perintah eksternal
from telebot import types # Import untuk membuat tombol navigasi

# Konfigurasi Telegram Bot
BOT_TOKEN = "8243804176:AAHddGdjqOlzACwDL8sTGzJjMGdo7KNI6ko"  # Ganti dengan token bot lo
bot = telebot.TeleBot(BOT_TOKEN)
CHAT_ID = "8317643774"  # Ganti dengan chat ID lo

# Konfigurasi email
# Perlu diingat temp-mail biasanya punya batasan dan mungkin tidak berfungsi terus
# Disarankan menggunakan email sendiri jika ingin lebih reliable
sender_email = "temp-mail-generated@example.com"
sender_password = ""  # Tidak diperlukan untuk temp-mail, tapi diperlukan jika pakai email sendiri
receiver_email = "feedback@tiktok.com"

# Konfigurasi pesan
subject = "Report Akun TikTok"
body_template = """Halo Tim TikTok,
Saya ingin melaporkan akun @{username} karena telah melanggar aturan privasi dan konten dewasa (18+). 
Bukti pelanggaran dapat dilihat pada link berikut: https://i.ibb.co.com/8gGFbLV2/IMG-20251102-014928-678.jpg
Akun ini telah menampilkan konten yang tidak pantas dan melanggar privasi orang lain. Mohon agar akun ini segera diblokir.
Terima kasih,
Lordhozoo"""

# Konfigurasi TikTok
tiktok_username_list = ["akun1", "akun2", "akun3"]

# Path ke video Hozoo
VIDEO_PATH = "hozoo.mp4"

# Fungsi untuk mendapatkan email sementara (perlu implementasi parsing HTML)
def get_temp_email():
    try:
        url = "https://temp-mail.org/ko/change"
        response = requests.get(url)
        response.raise_for_status()
        # Ekstrak email dari response (perlu di-parse HTML)
        # Implementasi parsing HTML di sini (misalnya menggunakan BeautifulSoup)
        # Contoh sederhana (mungkin tidak akurat):
        email = "generated-email@example.com" # Ganti dengan hasil parsing HTML yang benar
        return email
    except requests.exceptions.RequestException as e:
        print(f"Gagal mendapatkan email sementara: {e}")
        return None

# Fungsi untuk mengirim email
def send_email(subject, body, receiver_email, sender_email):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            # Jika pakai email sendiri (bukan temp-mail), uncomment baris di bawah
            # server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print(f"Email berhasil dikirim ke {receiver_email} dari {sender_email}")
    except Exception as e:
        print(f"Gagal mengirim email ke {receiver_email} dari {sender_email}: {e}")

# Fungsi untuk mendapatkan informasi cuaca
def get_weather():
    try:
        # Ganti dengan API key dan lokasi lo
        api_key = "YOUR_WEATHER_API_KEY"
        location = "Jakarta"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        weather_desc = data['weather'][0]['description']
        temperature = data['main']['temp'] - 273.15 # Convert Kelvin to Celsius
        return f"Cuaca di {location}: {weather_desc}, Suhu: {temperature:.1f}°C"
    except Exception as e:
        return f"Gagal mendapatkan informasi cuaca: {e}"

# Handler untuk command /menu
@bot.message_handler(commands=['menu'])
def menu(message):
    # Kirim video
    try:
        video = open(VIDEO_PATH, 'rb')
        bot.send_video(message.chat.id, video, caption="Selamat Datang di Menu Bot!")
        video.close()
    except FileNotFoundError:
        bot.reply_to(message, "Video tidak ditemukan.")
    except Exception as e:
        bot.reply_to(message, f"Gagal mengirim video: {e}")

    # Buat tombol navigasi
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item1 = types.KeyboardButton('/report')
    item2 = types.KeyboardButton('/info')
    item3 = types.KeyboardButton('/weather')
    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, "Silakan pilih menu:", reply_markup=markup)

# Handler untuk command /report
@bot.message_handler(commands=['report'])
def report(message):
    # Proses pelaporan TikTok
    sender_email = get_temp_email()
    if sender_email:
        tiktok_username = random.choice(tiktok_username_list)
        body = body_template.format(username=tiktok_username)
        send_email(subject, body, receiver_email, sender_email)
        bot.reply_to(message, f"Berhasil melaporkan akun @{tiktok_username} menggunakan email {sender_email}")
    else:
        bot.reply_to(message, "Gagal mendapatkan email sementara.")

# Handler untuk command /info
@bot.message_handler(commands=['info'])
def info(message):
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    bot.reply_to(message, f"Waktu saat ini: {date_time}")

# Handler untuk command /weather
@bot.message_handler(commands=['weather'])
def weather(message):
    weather_info = get_weather()
    bot.reply_to(message, weather_info)

# Handler untuk pesan teks (untuk menampilkan username)
@bot.message_handler(func=lambda message: message.text.startswith('@'))
def get_username(message):
    username = message.text
    bot.reply_to(message, f"Username: {username}")

# Fungsi utama untuk menjalankan bot
def main():
    print("Bot sedang berjalan...")
    try:
        bot.polling()
    except Exception as e:
        print(f"Error: {e}")
        # Coba restart bot setelah beberapa detik
        time.sleep(10)
        main()

if __name__ == "__main__":
    # Cek apakah dijalankan di Termux
    if 'ANDROID_ROOT' in os.environ:
        print("Berjalan di Termux...")
        # Install module yang dibutuhkan jika belum ada
        try:
            import requests
            import telebot
            import smtplib
            import ssl
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            from datetime import datetime
            print("Semua module sudah terinstall.")
        except ImportError:
            print("Beberapa module belum terinstall. Menginstall...")
            os.system("pip install requests telebot pyTelegramBotAPI")
            print("Semua module berhasil diinstall.")
        main()
    else:
        print("Tidak terdeteksi Termux, pastikan Anda menjalankan skrip ini di Termux.")
