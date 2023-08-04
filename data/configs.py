import asyncio
from data.loader import pyrogram_client, ResolveUsername
from data.loader import bot
from data.texts import *
from database.database import collection, ObjectId
from datetime import datetime, timedelta, timezone
import time
import pytz
import re
from keyboards.inline_keyboards import generate_add_button

def get_msk_unix():
    tz_msk = timezone(timedelta(hours=3))
    current_time_msk = datetime.now(tz_msk)
    unix_time_msk = int(current_time_msk.timestamp())
    return unix_time_msk

def update_time(unix_time):
    dt_utc = datetime.fromtimestamp(unix_time, timezone.utc)
    dt_msk = dt_utc + timedelta(hours=3)
    formatted_time = dt_msk.strftime("%d.%m.%Y в %H:%M")
    return formatted_time

def calculate_end_date(days):
    tz_moscow = pytz.timezone('Europe/Moscow')

    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%d.%m.%Y")

    start_date = datetime.strptime(formatted_date, "%d.%m.%Y")

    start_date = tz_moscow.localize(start_date)

    end_date = start_date + timedelta(days=days)

    formatted_date_with_time = end_date.strftime("%H:%M %d.%m.%Y")


    # ЮНИКС тайм
    new_datetime = current_datetime + timedelta(days=days)
    unix_time = int(time.mktime(new_datetime.timetuple()))

    return [formatted_date_with_time, unix_time]

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

def get_dict_index(database, groupid: str):
    index_of_chat = 0
    for index, item in enumerate(database['settings']):
        if item.get("chat_id") == str(groupid):
            index_of_chat = index
            break
    return index_of_chat

def get_user_dict_index(dict):
    index_dict = None
    for index, obj in enumerate(dict):
        if "type" in obj and obj["type"] == 'text_mention':
            index_dict = index
    return index_dict

def get_chat_user_dict_index(db, user_id, indexofchat):
    index_dict = None
    for index, item in enumerate(db['settings'][indexofchat]['users']):
        if item.get("id") == user_id:
            index_dict = index
            break
    return index_dict

def days_since_unix_time(unix_time):
    current_time_unix = get_msk_unix()
    time_difference_seconds = current_time_unix - unix_time
    days_difference = int(time_difference_seconds / (60 * 60 * 24))
    return days_difference

def get_price_index(days):
    index_of_price = 0
    db = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
    for index, item in enumerate(db['price']):
        if item.get("period") == str(days):
            index_of_price = index
            break
    return index_of_price

async def resolve_username_to_user_id(username: str):
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

def contains_external_links(text: str, blocked_domains: list):
    try:
        for substring in blocked_domains:
            if substring in text:
                return True
        return False
    except Exception as e:
        print(e)

def trim_array(arr, num_elements_to_keep):
    if len(arr) > num_elements_to_keep:
        arr = arr[:num_elements_to_keep]
    return arr

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
                index_of_chat = get_dict_index(db, chat_id)

                if db['settings'][index_of_chat]['afk']['active'] == False: continue
                if db['settings'][index_of_chat]['bot_send_afk'] == True: continue
                dif = time_diff(db['settings'][index_of_chat]['last_msg'], datetime.now().strftime('%H:%M:%S'))
                if dif >= 60:
                    text = f'{t_start_text.format(bot_user=t_bot_user)}\n\n<b>Функция:</b> "Ворчун"'
                    if db['settings'][index_of_chat]['afk']['warning'] != 'None': text = db['settings'][index_of_chat]['afk']['warning']
                    await bot.send_message(chat_id, text=text)
                    collection.find_one_and_update({'chats': chat_id}, {"$set": {f'settings.{index_of_chat}.bot_send_afk': True}})

                await asyncio.sleep(0.05)
            except Exception as e:
                print(e)

        await asyncio.sleep(5)

loop = asyncio.get_event_loop()
loop.create_task(active())








