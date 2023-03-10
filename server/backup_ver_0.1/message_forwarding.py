import logging
import asyncio
from telethon import TelegramClient, events
import configparser

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("config.ini")  # читаем конфиг

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Здесь нужно указать API ID и API hash
api_id = config.get("telegram", "ipa_id")
api_hash = config.get("telegram", "ipa_hash")

destination_channel = config.get("telegram", "destination_channel")  # Имя (или ID) целевого канала
forward_interval = 1  # Интервал пересылки сообщений в секундах

# Открытие файла
with open('channels.txt', 'r') as file:
    # Создание списка
    source_channel = []
    # Итерация по строкам файла
    for line in file:
        # Добавление элемента в список
        source_channel.append(line.strip())

# Создаем клиента Telethon
client = TelegramClient('session_name', api_id, api_hash)

for index, item in enumerate(source_channel):

    @client.on(events.NewMessage(chats=source_channel[int(index)]))
    async def forward_messages(event):
        message = event.message
        if message.media or message.text:
            logging.info(f'Received message with ID {message.id} from {source_channel[int(index)]}')
            await asyncio.sleep(forward_interval)
            try:
                forwarded_message = await client.forward_messages(destination_channel, message)
                logging.info(f'Forwarded message with ID {forwarded_message.id} to {destination_channel}')
            except Exception as e:
                logging.error(f'Error while forwarding message: {e}')

async def main():
    await client.start()
    

    for index, item in enumerate(source_channel):
        logging.info(f'Started listening for messages in {item}')

    await client.run_until_disconnected()
    


if __name__ == '__main__':
    asyncio.run(main())
