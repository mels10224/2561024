import configparser
import telebot
from telebot import types
import time
import shutil
import os
import logging
import os
import shutil
import win32com.client

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("config.ini")  # читаем конфиг

user = 'bot_telegram'

# Берем токен из конфиг фаила
bot_token = config.get(user, "bot_token")
bot = telebot.TeleBot(bot_token)
my_id = 845800521


menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
btnscreen = types.KeyboardButton('Добавить канал')
btnmouse = types.KeyboardButton('Создать backup')
btnfiles = types.KeyboardButton('Запустить сбор')
btnaddit = types.KeyboardButton('Скопировать бекапы на флешку')
btnmsgbox = types.KeyboardButton('📩Отправка уведомления')
btninfo = types.KeyboardButton('❗️Информация')
menu_keyboard.row(btnscreen, btnmouse)
menu_keyboard.row(btnfiles, btnaddit)
#menu_keyboard.row(btninfo, btnmsgbox)

menu_new_channel = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
cencel = types.KeyboardButton('Отмена')
menu_new_channel.row(cencel)

bot.send_message(my_id, "✅Сервер работает✅", reply_markup = menu_keyboard)
logging.info(f'Бот работает')

# Получаем сообшение
@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    # Проверяем от кого сообщение
    if message.from_user.id == my_id:
        bot.send_chat_action(my_id, 'typing')
        if message.text == "Добавить канал":
            bot.send_message(my_id, "Ввдите индификатор канала через @: ", reply_markup = menu_new_channel)
            if message.text == "Отмена":
                bot.send_message(my_id, "Назад", reply_markup = menu_keyboard)
            else:
                bot.register_next_step_handler(message, new_chennel)
        elif message.text == "Создать backup":
            bot.send_message(my_id, "Немного подождите")
            new_backup()
        elif message.text == "Запустить сбор":
            start_sbor()
        elif message.text == "Скопировать бекапы на флешку":
            copy_file()
    else:
        info_user(message)

def new_chennel(message):
    bot.send_chat_action(my_id, 'typing')
    try:
        my_string = message.text
        if "@" in my_string:
            with open('channels.txt', 'a') as chennels:
                chennels.write('\n' + str(message.text))

            bot.send_message(my_id, "Канал добавлен")
            logging.info(f'Канал добавлен')
        else:
            error_r()

    except:
        bot.send_message(my_id, "Ошибка! индификатор введен неверно", reply_markup = menu_keyboard)
        bot.register_next_step_handler(message, new_chennel)

def error_r ():
    bot.send_message(my_id, "ERROR", reply_markup = menu_keyboard)
    logging.error(f'Ошибка')

def start_sbor():
    try:
        os.startfile(r'' + 'message_forwarding.py')
        logging.info(f'Скрипт запушен')
    except Exception as e:
        bot.send_message(my_id, "Ошибка запуска")
        logging.error(f'Ошибка {e}')

def new_backup():
    #bot.send_chat_action(my_id, 'typing')
    try:

                                                    # Путь к папке, которую необходимо сохранить в бэкап
        source = config.get("backup", "source_files")
                                                    # Создаем имя директории для бэкапа, включающее текущую дату и время
        backup_name = 'backup_' + time.strftime('%Y%m%d_%H%M%S')
                                                    # Путь к папке, в которую будут сохранены бэкапы
        target_dir = config.get("backup", "file_copies")
                                                    # Создаем новую директорию для бэкапа
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
                                                    # Создаем полный путь к новой директории бэкапа
        target = os.path.join(target_dir, backup_name)
                                                    # Создаем бэкап папки
        shutil.copytree(source, target)
                                                    # Выводим сообщение о том, что бэкап создан успешно
        #print('Backup created at', target)
        logging.info(f'Backp created at {target}')
        bot.send_message(my_id, "Backup создан")
    except Exception as e:
        bot.send_message(my_id, "Ошибка! backup не создан")
        logging.error(f'Error while forwarding message: {e}')

def copy_file():

    # Путь к директории с файлами, которые нужно скопировать на флешку
    source_folder = r'C:\neuro\backup'

    # Путь к флешке, куда нужно скопировать файлы
    # Необходимо заменить "FLASH_DRIVE_NAME" на имя флешки, которое отображается в системе
    destination_folder = r'D:\backup'

    # Получение объекта WMI для отслеживания подключения USB-устройств
    wmi = win32com.client.GetObject("winmgmts:")
    usb_devices = wmi.InstancesOf("Win32_USBHub")

    # Ожидание подключения флешки
    def copy_folders(source, destination):
        shutil.copytree(source, destination)

# Мониторинг событий, связанных с флешкой
    while True:
        if os.path.exists("D:\\"):
            copy_folders(source_folder, destination_folder)
            break


def info_user(message):
    bot.send_chat_action(my_id, 'typing')
    alert = f"Кто-то пытался задать команду: \"{message.text}\"\n\n"
    alert += f"user id: {str(message.from_user.id)}\n"
    alert += f"first name: {str(message.from_user.first_name)}\n"
    alert += f"last name: {str(message.from_user.last_name)}\n"
    alert += f"username: @{str(message.from_user.username)}"
    bot.send_message(my_id, alert, reply_markup = menu_keyboard)
    bot.send_message(message.from_user.id, "Пошeл нахуй")
    logging.info(f'{alert}')

while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as E:
        print(E.args)
        time.sleep(2)
