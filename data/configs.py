import asyncio
from data.loader import pyrogram_client, ResolveUsername
from data.loader import bot
import re
from database.database import collection, ObjectId
from datetime import datetime

def add_time_to_unix(unix_time, time_string):
    time_in_seconds = 0

    if time_string.endswith('d'):
        days = int(time_string[:-1])
        time_in_seconds = days * 24 * 60 * 60
    elif time_string.endswith('h'):
        hours = int(time_string[:-1])
        time_in_seconds = hours * 60 * 60
    elif time_string.endswith('m'):
        minutes = int(time_string[:-1])
        time_in_seconds = minutes * 60
    elif time_string.endswith('s'):
        seconds = int(time_string[:-1])
        time_in_seconds = seconds

    new_unix_time = unix_time + time_in_seconds
    return new_unix_time

async def resolve_username_to_user_id(username: str) -> int | None:
    try:
        async with pyrogram_client:
            r = await pyrogram_client.invoke(ResolveUsername(username=username))
            if r.users:
                return [r.users[0].id, r.users[0].first_name]
            return None
    except Exception as e:
        print(e)


async def delete_message(timer_s, message_ids: list, chat_id):
    try:
        await asyncio.sleep(timer_s)
        for i in message_ids:
            try:
                await bot.delete_message(chat_id, i)
            except Exception as e:
                print(e)
            await asyncio.sleep(1)

    except Exception as e:
        print('error delete')

def contains_external_links(text: str, blocked_domains: list) -> bool:
    try:
        # Паттерн для поиска ссылок на запрещенные зоны
        pattern = r"(https?://)?([^\s]+\.(%s))" % "|".join(blocked_domains)
        # Проверяем, есть ли ссылки на запрещенные зоны в тексте
        if re.search(pattern, text):
            return True
        else:
            return False
    except Exception as e:
        print(e)


def check_mentions(text):
    try:
        pattern = r"(@\w+)"  # Регулярное выражение для проверки упоминаний
        matches = re.findall(pattern, text)

        if matches:
            return [True, matches[0]]  # Возвращаем список [True, @username]
        else:
            return [False, ""]  # Возвращаем список [False, ""]
    except Exception as e:
        print(e)


def time_diff(time1, time2):
    # Преобразование временных значений в объекты datetime
    fmt = "%H:%M:%S"
    datetime1 = datetime.strptime(time1, fmt)
    datetime2 = datetime.strptime(time2, fmt)

    # Вычисление разницы между временными значениями
    difference = datetime2 - datetime1

    # Перевод разницы в секунды
    seconds = difference.total_seconds()

    return int(seconds)

async def active():
    chat_ids = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})['groups']
    while True:
        for chat_id in chat_ids:
            try:
                db = collection.find_one({'chats': chat_id})
                index_of_chat = 0
                for index, item in enumerate(db['settings']):
                    if item.get("chat_id") == str(chat_id):
                        index_of_chat = index
                        break

                dif = time_diff(db['settings'][index_of_chat]['last_msg'], datetime.now().strftime('%H:%M:%S'))
                if dif >= 60:
                    text = 'Что-то все умолкли? Вы гдеее?'
                    if db['settings'][index_of_chat]['afk'] != 'None': text = db['settings'][index_of_chat]['afk']
                    await bot.send_message(chat_id, text=text)

                await asyncio.sleep(0.05)
            except Exception as e:
                print(e)

        await asyncio.sleep(5)

# loop = asyncio.get_event_loop()
# loop.create_task(active())








