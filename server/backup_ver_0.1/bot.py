import configparser
import telebot
from telebot import types
import time

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("config.ini")  # читаем конфиг

# Берем токен из конфиг фаила
bot_token = config.get("telegram", "bot_token")
bot = telebot.TeleBot(bot_token)
my_id = 845800521

menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
btnscreen = types.KeyboardButton('Добавить канал')
btnmouse = types.KeyboardButton('🖱Управление мышкой')
btnfiles = types.KeyboardButton('📂Файлы и процессы')
btnaddit = types.KeyboardButton('❇️Дополнительно')
btnmsgbox = types.KeyboardButton('📩Отправка уведомления')
btninfo = types.KeyboardButton('❗️Информация')
menu_keyboard.row(btnscreen, btnmouse)
menu_keyboard.row(btnfiles, btnaddit)
menu_keyboard.row(btninfo, btnmsgbox)

# Получаем сообшение
@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    # Проверяем от кого сообщение
    if message.from_user.id == my_id:
        bot.send_chat_action(my_id, 'typing')
        if message.text == "Добавить канал":
            bot.send_message(my_id, "Ввдите индификатор канала через @: ")
            bot.register_next_step_handler(message, new_chennel)
    else:
        info_user(message)

def new_chennel(message):
    bot.send_chat_action(my_id, 'typing')
    try:
        with open('channels.txt', 'a') as chennels:
            chennels.write(str(message.text) + '\n')
    except:
        bot.send_message(my_id, "Ошибка! индификатор введен неверно")
        bot.register_next_step_handler(message, new_chennel)

def info_user(message):
    bot.send_chat_action(my_id, 'typing')
    alert = f"Кто-то пытался задать команду: \"{message.text}\"\n\n"
    alert += f"user id: {str(message.from_user.id)}\n"
    alert += f"first name: {str(message.from_user.first_name)}\n"
    alert += f"last name: {str(message.from_user.last_name)}\n"
    alert += f"username: @{str(message.from_user.username)}"
    bot.send_message(my_id, alert, reply_markup = menu_keyboard)

while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as E:
        print(E.args)
        time.sleep(2)

