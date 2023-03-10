import logging
import asyncio
from telethon import TelegramClient, events
import configparser
import telebot
from telebot import types
import time

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("config.ini")  # читаем конфиг

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

user = 'admin_telegram'
session_name = config.get(user, "my_phone")
# Здесь нужно указать API ID и API hash
api_id = config.get(user, "ipa_id")
api_hash = config.get(user, "ipa_hash")

# Берем токен из конфиг фаила
bot_token = config.get(user, "bot_token")
bot = telebot.TeleBot(bot_token)
my_id = 845800521

bot.send_message(my_id, "Скрипт сбора запущен")
logging.info(f'Сообщение в бота отпралено ')
#845800521

destination_channel = config.get(user, "destination_channel")  # Имя (или ID) целевого канала
forward_interval = 0  # Интервал пересылки сообщений в секундах

# Открытие файла
with open('channels.txt', 'r') as file:
    # Создание списка
    source_channel = []
    logging.info(f'Список source_channel создан')
    # Итерация по строкам файла
    for line in file:
        # Добавление элемента в список
        source_channel.append(line.strip())

# Создаем клиента Telethon
client = TelegramClient(session_name, api_id, api_hash)

logging.info(f'Клиент запущен')
for index, item in enumerate(source_channel):

    @client.on(events.NewMessage(chats=source_channel[int(index)]))
    async def forward_messages(event):
        message = event.message
        if message.media or message.text:
            logging.info(f'Received message with ID {message.id} from {source_channel[int(index)]}')
            await asyncio.sleep(forward_interval)
            try:
                forwarded_message = await client.send_message(destination_channel, message)

                logging.info(f'Forwarded message with ID {forwarded_message.id} to {destination_channel}')
            except Exception as e:
                logging.error(f'Error while forwarding message: {e}')
                errors = logging.error(f'Error while forwarding message: {e}')
                bot.send_message(my_id, errors)

async def main():
    await client.start()
    

    for index, item in enumerate(source_channel):
        logging.info(f'Started listening for messages in {item}')

    await client.run_until_disconnected()
    


if __name__ == '__main__':
    asyncio.run(main())

print(';lkjhgf')