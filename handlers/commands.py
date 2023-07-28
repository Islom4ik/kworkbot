# Обработчики команд:
import asyncio
import re
import time
import pytz
from data.loader import bot, dp, FSMContext, State, Message
from database.database import collection, ObjectId
from states_scenes.scene import MySceneStates
from keyboards.inline_keyboards import *
from time import sleep
from data.configs import *
from datetime import datetime
from data.texts import *

@dp.message_handler(commands=['start'])
async def start_help_command_handler(ctx: Message):
    try:
        if '/start settings_' in ctx.text:
            call_data = ctx.text.replace('/start ', '')
            call_datas = call_data.split('_')
            if ctx.from_user.id != int(call_datas[2]):
                await ctx.answer('⚠ Извините у вас не достаточно прав чтобы изменять настройки для данного чата')
                await asyncio.sleep(2)
            else:
                user_db = collection.find_one({"user_id": ctx.from_user.id})
                if user_db == None:
                    admindb = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
                    generate_user_data_id = admindb['users_count'] + 1
                    collection.insert_one(
                        {"user_id": ctx.from_user.id, "register_data": datetime.now().strftime("%d.%m.%Y"),
                         "inlineid": generate_user_data_id, "manual_msg": False, "manual_msg": False, "manual_s": False, "chats": [], "settings": [], "lic": 0})
                    collection.find_one_and_update({"_id": ObjectId('64987b1eeed9918b13b0e8b4')},
                                                   {"$set": {"users_count": generate_user_data_id},
                                                    "$push": {"users": ctx.from_user.id}})
                    user_db = collection.find_one({"user_id": ctx.from_user.id})
                if call_datas[1] not in user_db['chats']:
                    collection.find_one_and_update({"user_id": ctx.from_user.id}, {"$push": {"chats": call_datas[1], "settings": {"chat_id": call_datas[1], "updated_date": get_msk_unix(), "lic": False, "lic_end": 'None', "lic_buyed_date": 'None', "rules": 'None', "greeting": 'None', "warning_ban": 'None', "warning_kick": 'None', "unban_text": 'None', "warning_resources": 'None', "warning_repostes": 'None', "warning_ping": 'None', 'afk': 'None', 'system_notice': {'active': False}, 'block_repostes': {'active': False, 'warning': 'None'}, "block_ping": {'active': False, 'warning': 'None'},'block_resources': {'active': False, 'warning': 'None', "r_list": ["com" , "ru"]}}}})
                    collection.find_one_and_update({"_id": ObjectId('64987b1eeed9918b13b0e8b4')}, {"$push": {"groups": call_datas[1]}})
                db = collection.find_one({"chats": call_datas[1]})
                index_of_chat = get_dict_index(db, call_datas[1])
                if db['settings'][index_of_chat]['lic'] == True: return await ctx.answer(settings_start.format(group_id=call_datas[1], bot_user=bot_user, upd_time=update_time(db['settings'][index_of_chat]['updated_date'])), reply_markup=generate_settings(True))
                return await ctx.answer(t_settings.format(group_id=call_datas[1], bot_user=t_bot_user, upd_time=update_time(db['settings'][index_of_chat]['updated_date'])), reply_markup=generate_settings())


        if ctx.chat.type == 'group' or ctx.chat.type == 'supergroup':
            if ctx['from']['username'] == 'GroupAnonymousBot': return await ctx.answer('🤷‍♂ Извините, Аноним мы уважаем ваше решение но мы не можем идентифицировать создателя группы пока тот является анонимом...\n\nПопросим вас выключить анонимность на пару минут и следовать инструкция бота, но а позже вы сможете обратно включить анонимность и управлять ботом в личных сообщениях!')
            admins = await bot.get_chat_administrators(ctx.chat.id)
            creator_id = next((obj for obj in admins if obj["status"] == "creator"), None).user.id
            for me in admins:
                if me.user.username == t_bot_user:
                    if me.can_manage_chat == True and me.can_delete_messages == True and me.can_restrict_members == True and me.can_invite_users == True and me.can_promote_members == True:
                        return await ctx.answer(
                            '🤖 Вы выполнили корректные действия.\n\nНажмите кнопку "Настроить бота"',
                            reply_markup=generate_settings_button(f'{ctx.chat.id}_{creator_id}'))
                    else:
                        return await ctx.answer(
                            '🤖 Здравствуйте! Я бот-админ и могу администрировать данный чат.\n\nВыдайте мне все права администратора:\n- Управлять группой\n- Удаление сообщений\n- Изменение сообщений\n- Блокировать участников\n- Добовлять участников\n- Управлять пользователями\n- Добавление администраторов',
                            reply_markup=generate_check_admin_rights())
                    break
                else:
                    return await ctx.answer(
                        '🤖 Здравствуйте! Я бот-админ и могу администрировать данный чат.\n\nВыдайте мне все права администратора:\n- Управлять группой\n- Удаление сообщений\n- Изменение сообщений\n- Блокировать участников\n- Добовлять участников\n- Управлять пользователями\n- Добавление администраторов',
                        reply_markup=generate_check_admin_rights())
                    break

        db = collection.find_one({"user_id": ctx.from_user.id})
        if db == None:
            admindb = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
            generate_user_data_id = admindb['users_count'] + 1
            collection.insert_one({"user_id": ctx.from_user.id, "manual_s": False, "manual_msg": False, "register_data": datetime.now().strftime("%d.%m.%Y"),"inlineid": generate_user_data_id, "chats": [], "settings": [], "lic": 0})
            collection.find_one_and_update({"_id": ObjectId('64987b1eeed9918b13b0e8b4')},
                                           {"$set": {"users_count": generate_user_data_id},
                                            "$push": {"users": ctx.from_user.id}})
        await ctx.answer(
            'Здравствуйте! Я бот-админ и могу администрировать ваш групповой чат.\n\nДля того чтобы начать, добавьте меня в свой групповой чат:',
            reply_markup=generate_add_button())
    except Exception as e:
        print(e)

@dp.message_handler(commands=['ban'])
async def handler_to_ban(ctx: Message):
    try:
        if ctx.chat.type == 'group' or ctx.chat.type == 'supergroup':
            trash = ''
            if ctx['from']['username'] == 'GroupAnonymousBot':
                trash = await ctx.answer(
                '🤷‍♂ Извините, Аноним мы уважаем ваше решение, но мы не можем идентифицировать вас и ваши прова пока вы являетесь анонимом...\n\nПопросим вас выключить анонимность на пару минут и использовать данную команду, а позже вы сможете обратно включить анонимность!')
                return asyncio.create_task(delete_message(15, [trash.message_id, ctx.message_id], trash.chat.id))
            admins = await bot.get_chat_administrators(ctx.chat.id)
            creator_id = next((obj for obj in admins if obj["status"] == "creator"), None).user.id
            isadmin = False
            for user in admins:
                if user.user.id == ctx.from_user.id and (user.status == 'creator' or user.status == 'administrator') and user.can_restrict_members == True:
                    isadmin = True

                    if ctx.reply_to_message:
                        await bot.ban_chat_member(ctx.reply_to_message.chat.id, ctx.reply_to_message.from_user.id)
                        banned = collection.find_one({"user_id": creator_id})
                        text = f'👨🏻‍⚖ Администратор <b>{ctx.from_user.first_name}</b> забанил <a href="tg://user?id={ctx.reply_to_message.from_user.id}">{ctx.reply_to_message.from_user.first_name}</a> за систематические нарушения правил!'
                        index = get_dict_index(banned, ctx.chat.id)
                        if banned['settings'][index]['warning_ban'] != 'None':
                            text = banned['settings'][index]['warning_ban'].replace('{member_name}', f'<a href="tg://user?id={ctx.reply_to_message.from_user.id}">{ctx.reply_to_message.from_user.first_name}</a>').replace('{admin}', f'<b>{ctx.from_user.first_name}</b>')

                        await ctx.answer(text)
                        break

                    args = ctx.text.split(' ')
                    if len(args) == 1:
                        trash = await ctx.answer('⚠ Введите пользователя, которого нужно забанить, следуя примеру ниже:\n\n<i>ban @username</i>')
                        asyncio.create_task(delete_message(8, [trash.message_id, ctx.message_id], ctx.chat.id))
                        break
                    args.pop(0)

                    collection.find_one_and_update({"user_id": creator_id}, {"$set": {"baned": []}})

                    dicts_with_user_key = []
                    for item in ctx.entities:
                        if 'user' in item:
                            dicts_with_user_key.append(item.user.id)
                            collection.find_one_and_update({"user_id": creator_id}, {"$push": {"baned": f'<a href="tg://user?id={item.user.id}">{item.user.first_name}</a>'}})

                    pattern = r"https://t.me/([\w_]+)"
                    for i in args:
                        if i[0] == '@':
                            userid = await resolve_username_to_user_id(i.replace('@', ''))
                            dicts_with_user_key.append(userid[0])
                            collection.find_one_and_update({"user_id": creator_id}, {
                                "$push": {"baned": f'<a href="tg://user?id={userid[0]}">{userid[1]}</a>'}})
                        elif re.search(pattern, i):
                            user = re.findall(pattern, i)[0]
                            userid = await resolve_username_to_user_id(user)
                            dicts_with_user_key.append(userid[0])
                            collection.find_one_and_update({"user_id": creator_id}, {
                                "$push": {"baned": f'<a href="tg://user?id={userid[0]}">{userid[1]}</a>'}})


                    if len(dicts_with_user_key) == 0:
                        trash = await ctx.answer('🪪 Пользователь не найден')
                        return asyncio.create_task(delete_message(5, [trash.message_id, ctx.message_id], ctx.chat.id))


                    for i in dicts_with_user_key:
                        await bot.ban_chat_member(ctx.chat.id, i)

                    banned = collection.find_one({"user_id": creator_id})
                    text = f'👨🏻‍⚖ Администратор <b>{ctx.from_user.first_name}</b> забанил {", ".join(banned["baned"])} за систематические нарушения правил!'
                    index = get_dict_index(banned, ctx.chat.id)
                    if banned['settings'][index]['warning_ban'] != 'None':
                        text = banned['settings'][index]['warning_ban'].replace('{member_name}', ", ".join(banned["baned"])).replace('{admin}', f'<b>{ctx.from_user.first_name}</b>')
                    await ctx.answer(text)
                    break

            if isadmin == False:
                trash = await ctx.answer('⚠ У вас не достаточно прав для использования данной команды')
                asyncio.create_task(delete_message(5, [trash.message_id], ctx.chat.id))

            asyncio.create_task(delete_message(5, [ctx.message_id], ctx.chat.id))

    except Exception as e:
        trash = ''
        if e.args[0] == 'Telegram says: [400 USERNAME_NOT_OCCUPIED] - The username is not occupied by anyone (caused by "contacts.ResolveUsername")':
            trash = await ctx.answer('🪪 Пользователь не найден')
        if e.args[0] == "Can't remove chat owner":
            trash = await ctx.answer('⚠ Вы не можете забанить основателя группы')
        if e.args[0] == "User is an administrator of the chat":
            trash = await ctx.answer('⚠ Вы не можете забанить администраторов чата\n\nЭто может сделать только создатель группы в ручную')
        if e.args[0] == 'Can\'t restrict self':
            trash = await ctx.answer('🤖 Ха-Ха-Ха... Я сам себя банить собрался?')
        print(e)
        asyncio.create_task(delete_message(8, [trash.message_id, ctx.message_id], ctx.chat.id))


@dp.message_handler(commands=['unban'])
async def handler_to_unban(ctx: Message):
    try:
        if ctx.chat.type == 'group' or ctx.chat.type == 'supergroup':
            trash = ''
            if ctx['from']['username'] == 'GroupAnonymousBot':
                trash = await ctx.answer(
                '🤷‍♂ Извините, Аноним мы уважаем ваше решение, но мы не можем идентифицировать вас и ваши прова пока вы являетесь анонимом...\n\nПопросим вас выключить анонимность на пару минут и использовать данную команду, а позже вы сможете обратно включить анонимность!')
                return asyncio.create_task(delete_message(15, [trash.message_id, ctx.message_id], trash.chat.id))
            admins = await bot.get_chat_administrators(ctx.chat.id)
            isadmin = False
            for user in admins:
                if user.user.id == ctx.from_user.id and (user.status == 'creator' or user.status == 'administrator') and user.can_restrict_members == True:
                    isadmin = True
                    args = ctx.text.split(' ')
                    if args[1] == '@shieldsword_bot':
                        trash = await ctx.reply('Кхм-Кхм...')
                        return asyncio.create_task(delete_message(6, [trash.message_id, ctx.message_id], trash.chat.id))

                    if len(args) == 1:
                        trash = await ctx.answer('⚠ Введите пользователя, которого нужно разбанить, следуя примеру ниже:\n\n<i>unban @username</i>')
                        asyncio.create_task(delete_message(8, [trash.message_id, ctx.message_id], ctx.chat.id))
                        break
                    args.pop(0)

                    creator_id = next((obj for obj in admins if obj["status"] == "creator"), None).user.id
                    collection.find_one_and_update({"user_id": creator_id}, {"$set": {"unbaned": []}})

                    dicts_with_user_key = []
                    pattern = r"https://t.me/([\w_]+)"
                    for i in args:
                        if i[0] == '@':
                            userid = await resolve_username_to_user_id(i.replace('@', ''))
                            userc = ''
                            try:
                                userc = await bot.get_chat_member(chat_id=ctx.chat.id, user_id=userid[0])
                                if userc.status == 'kicked':
                                    dicts_with_user_key.append(userid[0])
                                    collection.find_one_and_update({"user_id": creator_id}, {
                                        "$push": {"unbaned": f'<a href="tg://user?id={userid[0]}">{userid[1]}</a>'}})
                                else:
                                    trash = await ctx.answer(
                                        f'⚠ Участник <a href="tg://user?id={userid[0]}">{userid[1]}</a> не заблокирован')
                                    asyncio.create_task(
                                        delete_message(10, [trash.message_id, ctx.message_id], ctx.chat.id))
                            except:
                                print('')
                        elif re.search(pattern, i):
                            user = re.findall(pattern, i)[0]
                            userid = await resolve_username_to_user_id(user)
                            try:
                                userc = await bot.get_chat_member(chat_id=ctx.chat.id, user_id=userid[0])
                                if userc.status == 'kicked':
                                    dicts_with_user_key.append(userid[0])
                                    collection.find_one_and_update({"user_id": creator_id}, {
                                        "$push": {"unbaned": f'<a href="tg://user?id={userid[0]}">{userid[1]}</a>'}})
                                else:
                                    trash = await ctx.answer(
                                        f'⚠ Участник <a href="tg://user?id={userid[0]}">{userid[1]}</a> не заблокирован')
                                    asyncio.create_task(
                                        delete_message(10, [trash.message_id, ctx.message_id], ctx.chat.id))
                            except:
                                print('')
                    if len(dicts_with_user_key) == 0:
                        trash = await ctx.answer('🪪 Пользователь не найден. Введите пользователя, которого нужно разбанить, следуя примеру ниже:\n\n<i>unban @username</i>')
                        return asyncio.create_task(delete_message(10, [trash.message_id, ctx.message_id], ctx.chat.id))


                    for i in dicts_with_user_key:
                        unban = await bot.unban_chat_member(ctx.chat.id, i, only_if_banned=False)

                    unbaned = collection.find_one({"user_id": creator_id})
                    text = f'👨🏻‍⚖ Администратор <b>{ctx.from_user.first_name}</b> разбанил {", ".join(unbaned["unbaned"])}'
                    index = get_dict_index(unbaned, ctx.chat.id)
                    if unbaned['settings'][index]['unban_text'] != 'None':
                        text = unbaned['settings'][index]['unban_text'].replace('{member_name}', ", ".join(unbaned["unbaned"])).replace('{admin}', f'<b>{ctx.from_user.first_name}</b>')

                    await ctx.answer(text)

                    break

            if isadmin == False:
                trash = await ctx.answer('⚠ У вас не достаточно прав для использования данной команды')
                asyncio.create_task(delete_message(5, [trash.message_id], ctx.chat.id))

            asyncio.create_task(delete_message(5, [ctx.message_id], ctx.chat.id))
    except Exception as e:
        trash = ''
        if e.args[
            0] == 'Telegram says: [400 USERNAME_NOT_OCCUPIED] - The username is not occupied by anyone (caused by "contacts.ResolveUsername")':
            trash = await ctx.answer('🪪 Пользователь не найден')
        print(e)
        asyncio.create_task(delete_message(5, [trash.message_id, ctx.message_id], ctx.chat.id))

@dp.message_handler(commands=['kick'])
async def handler_to_kick(ctx: Message):
    try:
        if ctx.chat.type == 'group' or ctx.chat.type == 'supergroup':
            trash = ''
            if ctx['from']['username'] == 'GroupAnonymousBot':
                trash = await ctx.answer(
                '🤷‍♂ Извините, Аноним мы уважаем ваше решение, но мы не можем идентифицировать вас и ваши прова пока вы являетесь анонимом...\n\nПопросим вас выключить анонимность на пару минут и использовать данную команду, а позже вы сможете обратно включить анонимность!')
                return asyncio.create_task(delete_message(15, [trash.message_id, ctx.message_id], trash.chat.id))
            admins = await bot.get_chat_administrators(ctx.chat.id)
            isadmin = False
            for user in admins:
                if user.user.id == ctx.from_user.id and (
                        user.status == 'creator' or user.status == 'administrator') and user.can_restrict_members == True:
                    isadmin = True

                    if ctx.reply_to_message:
                        await bot.kick_chat_member(ctx.reply_to_message.chat.id, ctx.reply_to_message.from_user.id)
                        await bot.unban_chat_member(ctx.reply_to_message.chat.id, ctx.reply_to_message.from_user.id)
                        await ctx.answer(
                            f'👨🏻‍⚖ Администратор <b>{ctx.from_user.first_name}</b> кикнул <a href="tg://user?id={ctx.reply_to_message.from_user.id}">{ctx.reply_to_message.from_user.first_name}</a> за систематические нарушения правил!')

                        break


                    args = ctx.text.split(' ')
                    if len(args) == 1:
                        trash = await ctx.answer(
                            '⚠ Введите пользователя, которого нужно кикнуть, следуя примеру ниже:\n\n<i>kick @username</i>')
                        asyncio.create_task(delete_message(8, [trash.message_id, ctx.message_id], ctx.chat.id))
                        break
                    args.pop(0)

                    creator_id = next((obj for obj in admins if obj["status"] == "creator"), None).user.id
                    collection.find_one_and_update({"user_id": creator_id}, {"$set": {"kicked": []}})

                    dicts_with_user_key = []
                    for item in ctx.entities:
                        if 'user' in item:
                            dicts_with_user_key.append(item.user.id)
                            collection.find_one_and_update({"user_id": creator_id}, {"$push": {
                                "kicked": f'<a href="tg://user?id={item.user.id}">{item.user.first_name}</a>'}})

                    pattern = r"https://t.me/([\w_]+)"
                    for i in args:
                        if i[0] == '@':
                            userid = await resolve_username_to_user_id(i.replace('@', ''))
                            dicts_with_user_key.append(userid[0])
                            collection.find_one_and_update({"user_id": creator_id}, {
                                "$push": {"kicked": f'<a href="tg://user?id={userid[0]}">{userid[1]}</a>'}})
                        elif re.search(pattern, i):
                            user = re.findall(pattern, i)[0]
                            userid = await resolve_username_to_user_id(user)
                            dicts_with_user_key.append(userid[0])
                            collection.find_one_and_update({"user_id": creator_id}, {
                                "$push": {"kicked": f'<a href="tg://user?id={userid[0]}">{userid[1]}</a>'}})

                    if len(dicts_with_user_key) == 0:
                        trash = await ctx.answer('🪪 Пользователь не найден')
                        return asyncio.create_task(delete_message(5, [trash.message_id, ctx.message_id], ctx.chat.id))

                    for i in dicts_with_user_key:
                        await bot.kick_chat_member(ctx.chat.id, i)
                        await bot.unban_chat_member(ctx.chat.id, i)

                    kicked = collection.find_one({"user_id": creator_id})
                    text = f'👨🏻‍⚖ Администратор <b>{ctx.from_user.first_name}</b> кикнул {", ".join(kicked["kicked"])} за систематические нарушения правил!'
                    index = get_dict_index(kicked, ctx.chat.id)
                    if kicked['settings'][index]['warning_kick'] != 'None':
                        text = kicked['settings'][index]['warning_kick'].replace('{member_name}', ", ".join(kicked["kicked"])).replace('{admin}', f'<b>{ctx.from_user.first_name}</b>')

                    await ctx.answer(text)
                    break

            if isadmin == False:
                trash = await ctx.answer('⚠ У вас не достаточно прав для использования данной команды')
                asyncio.create_task(delete_message(5, [trash.message_id], ctx.chat.id))

            asyncio.create_task(delete_message(5, [ctx.message_id], ctx.chat.id))
    except Exception as e:
        trash = ''
        if e.args[
            0] == 'Telegram says: [400 USERNAME_NOT_OCCUPIED] - The username is not occupied by anyone (caused by "contacts.ResolveUsername")':
            trash = await ctx.answer('🪪 Пользователь не найден')
        if e.args[0] == "Can't remove chat owner":
            trash = await ctx.answer('⚠ Вы не можете забанить основателя группы')
        if e.args[0] == "User is an administrator of the chat":
            trash = await ctx.answer(
                '⚠ Вы не можете забанить администраторов чата\n\nЭто может сделать только создатель группы в ручную')
        print(e)
        asyncio.create_task(delete_message(5, [trash.message_id, ctx.message_id], ctx.chat.id))

timezone = pytz.timezone('Europe/Moscow')

# @dp.message_handler(commands=['mute'])
# async def handler_to_ban(ctx: Message):
#     try:
#         if ctx.chat.type == 'group' or ctx.chat.type == 'supergroup':
#             admins = await bot.get_chat_administrators(ctx.chat.id)
#             isadmin = False
#             for user in admins:
#                 if user.user.id == ctx.from_user.id and (user.status == 'creator' or user.status == 'administrator') and user.can_restrict_members == True:
#                     isadmin = True
#
#                     args = ctx.text.split(' ')
#                     if len(args) > 4:
#                         trash = await ctx.answer(
#                             '⚠ Вы ввели неправильную структуру команды. Ниже приведена правильная структура команды:\n\n<i>mute @username until reason</i>\n\nuntil(365d|1h|1m|30s) -> Время, через которое будет снят мут. (необязательно указывать дату снятия мута, если хотите замутить пользователя навсегда)\nreason -> Причина мута')
#                         asyncio.create_task(delete_message(15, [trash.message_id, ctx.message_id], ctx.chat.id))
#                         break
#
#                     if ctx.reply_to_message:
#                         rargs = ctx.text.split(' ')
#                         if len(rargs) > 3:
#                             trash = await ctx.answer(
#                                 '⚠ Вы ввели неправильную структуру команды. Если вы отвечаете на сообщение пользователя которого нужно замутить, то структура команды:\n\n<i>mute until\n\nuntil(365d|1h|1m|30s) -> Время, через которое будет снят мут. (необязательно указывать дату снятия мута, если хотите замутить пользователя навсегда)</i>')
#                             asyncio.create_task(delete_message(15, [trash.message_id, ctx.message_id], ctx.chat.id))
#                             break
#                         elif len(rargs) == 3:
#                             if re.search(r"[dhms]", rargs[1]):
#                                 await bot.restrict_chat_member(ctx.reply_to_message.chat.id,
#                                                                ctx.reply_to_message.from_user.id, can_send_messages=False, can_send_media_messages=False, can_send_other_messages=False, until_date=add_time_to_unix(int(datetime.now(timezone).timestamp()), rargs[1]))
#
#                                 await ctx.answer(
#                                     f'👨🏻‍⚖ Администратор <b>{ctx.from_user.first_name}</b> замутил <a href="tg://user?id={ctx.reply_to_message.from_user.id}">{ctx.reply_to_message.from_user.first_name}</a> по причине:\n<i>{"".join(args)}</i>')
#                                 break
#                         else:
#                             await bot.restrict_chat_member(ctx.reply_to_message.chat.id,
#                                                           ctx.reply_to_message.from_user.id,)
#                             await ctx.answer(
#                                 f'👨🏻‍⚖ Администратор <b>{ctx.from_user.first_name}</b> замутил <a href="tg://user?id={ctx.reply_to_message.from_user.id}">{ctx.reply_to_message.from_user.first_name}</a>')
#                             break
#
#                     creator_id = next((obj for obj in admins if obj["status"] == "creator"), None).user.id
#                     collection.find_one_and_update({"user_id": creator_id}, {"$set": {"baned": []}})
#
#                     dicts_with_user_key = []
#                     for item in ctx.entities:
#                         if 'user' in item:
#                             dicts_with_user_key.append(item.user.id)
#                             collection.find_one_and_update({"user_id": creator_id}, {"$push": {"baned": f'<a href="tg://user?id={item.user.id}">{item.user.first_name}</a>'}})
#
#                     pattern = r"https://t.me/([\w_]+)"
#                     for i in args:
#                         if i[0] == '@':
#                             userid = await resolve_username_to_user_id(i.replace('@', ''))
#                             dicts_with_user_key.append(userid[0])
#                             collection.find_one_and_update({"user_id": creator_id}, {
#                                 "$push": {"baned": f'<a href="tg://user?id={userid[0]}">{userid[1]}</a>'}})
#                         elif re.search(pattern, i):
#                             user = re.findall(pattern, i)[0]
#                             userid = await resolve_username_to_user_id(user)
#                             dicts_with_user_key.append(userid[0])
#                             collection.find_one_and_update({"user_id": creator_id}, {
#                                 "$push": {"baned": f'<a href="tg://user?id={userid[0]}">{userid[1]}</a>'}})
#
#
#                     if len(dicts_with_user_key) == 0:
#                         trash = await ctx.answer('🪪 Пользователь не найден')
#                         return asyncio.create_task(delete_message(5, [trash.message_id, ctx.message_id], ctx.chat.id))
#
#
#                     for i in dicts_with_user_key:
#                         await bot.ban_chat_member(ctx.chat.id, i)
#
#                     banned = collection.find_one({"user_id": creator_id})
#                     await ctx.answer(f'👨🏻‍⚖ Администратор <b>{ctx.from_user.first_name}</b> забанил {", ".join(banned["baned"])} за систематические нарушения правил!')
#                     break
#
#             if isadmin == False:
#                 trash = await ctx.answer('⚠ У вас не достаточно прав для использования данной команды')
#                 asyncio.create_task(delete_message(5, [trash.message_id], ctx.chat.id))
#
#             asyncio.create_task(delete_message(5, [ctx.message_id], ctx.chat.id))
#
#     except Exception as e:
#         trash = ''
#         if e.args[0] == 'Telegram says: [400 USERNAME_NOT_OCCUPIED] - The username is not occupied by anyone (caused by "contacts.ResolveUsername")':
#             trash = await ctx.answer('🪪 Пользователь не найден')
#         if e.args[0] == "Can't remove chat owner":
#             trash = await ctx.answer('⚠ Вы не можете забанить основателя группы')
#         if e.args[0] == "User is an administrator of the chat":
#             trash = await ctx.answer('⚠ Вы не можете забанить администраторов чата\n\nЭто может сделать только создатель группы в ручную')
#         if e.args[0] == 'Can\'t restrict self':
#             trash = await ctx.answer('🤖 Ха-Ха-Ха... Я сам себя банить собрался?')
#         print(e)
#         asyncio.create_task(delete_message(5, [trash.message_id, ctx.message_id], ctx.chat.id))

@dp.message_handler(commands=['rules'])
async def answer_to_rules(ctx: Message):
    try:
        if ctx.chat.type == 'group' or ctx.chat.type == 'supergroup':
            db = collection.find_one({"chats": f"{ctx.chat.id}"})
            index_of_chat = get_dict_index(db, ctx.chat.id)

            trash = ''

            if db['settings'][index_of_chat]['rules'] == 'None':
                admins = await bot.get_chat_administrators(ctx.chat.id)
                creator_id = next((obj for obj in admins if obj["status"] == "creator"), None).user.id
                trash = await ctx.answer(
                    "⚠ Правила чата отсутствуют!\n\nДля того чтобы изменить правила, перейдите в настройки бота через команду /settings или по кнопке ниже:",
                    reply_markup=generate_settings_button(f"{ctx.chat.id}_{creator_id}"))
            else:
                trash = await ctx.answer(db['settings'][index_of_chat]['rules'])

            asyncio.create_task(delete_message(150, [trash.message_id, ctx.message_id], ctx.chat.id))
    except Exception as e:
        print(e)

@dp.message_handler(commands=['settings'])
async def answer_to_settings(ctx: Message):
    try:
        if ctx.chat.type == 'group' or ctx.chat.type == 'supergroup':
            trash = ''
            if ctx['from']['username'] == 'GroupAnonymousBot':
                trash = await ctx.answer(
                '🤷‍♂ Извините, Аноним мы уважаем ваше решение, но мы не можем идентифицировать создателя группы пока вы являетесь анонимом...\n\nПопросим вас выключить анонимность на пару минут и использовать команду, а позже вы сможете обратно включить анонимность!')
                return asyncio.create_task(delete_message(15, [trash.message_id, ctx.message_id], trash.chat.id))
            admins = await bot.get_chat_administrators(ctx.chat.id)
            creator_id = next((obj for obj in admins if obj["status"] == "creator"), None).user.id
            trash = await ctx.answer('Для того чтобы изменить настройки, перейдите в бота по кнопке ниже:',
                             reply_markup=generate_settings_button(f"{ctx.chat.id}_{creator_id}"))
            asyncio.create_task(delete_message(6, [trash.message_id, ctx.message_id], ctx.chat.id))
    except Exception as e:
        print(e)