# Обработчики текстовых данных:
import asyncio
from data.loader import bot, dp, FSMContext, State, Message, config
from database.database import collection, ObjectId
from states_scenes.scene import MySceneStates
from time import sleep
from keyboards.inline_keyboards import generate_block_repostes_show, generate_block_ping_show, generate_block_repostes_show, generate_admins_settings, generate_rules_keyboard, generate_edit_text_settings, generate_warning_editing_page
from data.configs import get_user_dict_index, resolve_username_to_user_id, contains_external_links, check_mentions, delete_message, get_dict_index
from aiogram import types
from handlers import commands
from admin import admin
from datetime import datetime


@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def new_chat_member_greatings(ctx: Message):
    try:
        if ctx['new_chat_member']['is_bot'] == True: return
        db = collection.find_one({"chats": f"{ctx.chat.id}"})
        index_of_chat = get_dict_index(db, ctx.chat.id)

        if db['settings'][index_of_chat]['system_notice']['active'] == True:
            await ctx.delete()

        member_name = ctx["new_chat_member"]["first_name"]

        trash = ''
        if db['settings'][index_of_chat]['greeting'] == 'None':
            trash = await ctx.answer(f"Приветствуем, <b>{member_name}</b>!\n\nПрежде чем размещать свои объявления, пожалуйста, ознакомься с правилами. Они доступны по команде /rules")
        else:
            text_from_db = db['settings'][index_of_chat]['greeting']
            text = ''
            if '{member_name}' in text_from_db:
                text = text_from_db.replace("{member_name}", member_name)
            else:
                text = text_from_db

            trash = await ctx.answer(text)

        asyncio.create_task(delete_message(30, [trash.message_id], ctx.chat.id))
    except Exception as e:
        print(e)

@dp.message_handler(content_types=[types.ContentType.LEFT_CHAT_MEMBER])
async def left_chat_member(ctx: Message):
    try:
        db = collection.find_one({"chats": f"{ctx.chat.id}"})
        index_of_chat = get_dict_index(db, ctx.chat.id)

        if db['settings'][index_of_chat]['system_notice']['active'] == True:
            await ctx.delete()
    except Exception as e:
        print(e)


@dp.message_handler(content_types=['text'], state=MySceneStates.greeting_change_text_scene)
async def greeting_scene(ctx: Message, state: FSMContext):
    try:
        db = collection.find_one({"user_id": ctx.from_user.id})
        group_id = db['chat_editing']
        index_of_chat = get_dict_index(db, group_id)
        collection.find_one_and_update({"user_id": ctx.from_user.id}, {"$set": {f"settings.{index_of_chat}.greeting": ctx.text}})
        await bot.send_message(ctx.chat.id, text=f'Успешное изменение ✅')
        await state.finish()
        sleep(2)
        await bot.send_message(ctx.chat.id, text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n\nВыберите текст, который хотите посмотреть:',
                                    reply_markup=generate_edit_text_settings())
    except Exception as e:
        print(e)

@dp.message_handler(content_types=['text'], state=MySceneStates.rules_change_text_scene)
async def rules_scene(ctx: Message, state: FSMContext):
    try:
        db = collection.find_one({"user_id": ctx.from_user.id})
        group_id = db['chat_editing']
        index_of_chat = get_dict_index(db, group_id)
        collection.find_one_and_update({"user_id": ctx.from_user.id}, {"$set": {f"settings.{index_of_chat}.rules": ctx.text}})
        await bot.send_message(ctx.chat.id, text=f'Успешное изменение ✅')
        await state.finish()
        sleep(2)
        await bot.send_message(ctx.chat.id, text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n\nВыберите текст, который хотите посмотреть:',
                                    reply_markup=generate_edit_text_settings())
    except Exception as e:
        print(e)

@dp.message_handler(content_types=['text'], state=MySceneStates.afk_change_text_scene)
async def afk_scene(ctx: Message, state: FSMContext):
    try:
        db = collection.find_one({"user_id": ctx.from_user.id})
        group_id = db['chat_editing']
        index_of_chat = get_dict_index(db, group_id)
        collection.find_one_and_update({"user_id": ctx.from_user.id}, {"$set": {f"settings.{index_of_chat}.afk": ctx.text}})
        await bot.send_message(ctx.chat.id, text=f'Успешное изменение ✅')
        await state.finish()
        sleep(2)
        await bot.send_message(ctx.chat.id, text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n\nВыберите текст, который хотите посмотреть:',
                                    reply_markup=generate_edit_text_settings())
    except Exception as e:
        print(e)

@dp.message_handler(content_types=['text'], state=MySceneStates.blocked_resources_add)
async def blocked_resources_add_scene(ctx: Message, state: FSMContext):
    try:
        domains_array = ctx.text.replace('.', '').replace(' ', '').split(',')
        db = collection.find_one({"user_id": ctx.from_user.id})
        group_id = db['chat_editing']
        index_of_chat = get_dict_index(db, group_id)

        # if domains_array in db['settings'][index_of_chat]['block_resources']['r_list']: return await ctx.answer('⚠ В вашем списке запрещенных доменных расширений уже имеются некоторые введенные вами расширения.\n\nВведите доменные расширения, которые хотите заблокировать через запятую:')

        for i in domains_array:
            try:
                collection.find_one_and_update({"user_id": ctx.from_user.id},
                                               {'$push': {f'settings.{index_of_chat}.block_resources.r_list': i}})
            except Exception as e:
                print(e)

        await bot.send_message(ctx.chat.id, text=f'Успешное изменение ✅')
        await state.finish()
        await asyncio.sleep(2)
        await bot.send_message(ctx.chat.id, text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n\nВыберите функцию:', reply_markup=generate_admins_settings())
    except Exception as e:
        print(e)

@dp.message_handler(content_types=['text'], state=MySceneStates.blocked_resources_remove)
async def blocked_resources_remove_scene(ctx: Message, state: FSMContext):
    try:
        domains_array = ctx.text.replace('.', '').replace(' ', '').split(',')
        db = collection.find_one({"user_id": ctx.from_user.id})
        group_id = db['chat_editing']
        index_of_chat = get_dict_index(db, group_id)

        for i in domains_array:
            try:
                collection.find_one_and_update({"user_id": ctx.from_user.id},
                                               {'$pull': {f'settings.{index_of_chat}.block_resources.r_list': i}})
            except Exception as e:
                print(e)

        await bot.send_message(ctx.chat.id, text=f'Успешное изменение ✅')
        await state.finish()
        await asyncio.sleep(2)
        await bot.send_message(ctx.chat.id, text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n\nВыберите функцию:', reply_markup=generate_admins_settings())
    except Exception as e:
        print(e)

@dp.message_handler(content_types=['text'], state=MySceneStates.banwarning_change_text_scene)
async def banwarning_change_text(ctx: Message, state: FSMContext):
    try:
        db = collection.find_one({"user_id": ctx.from_user.id})
        group_id = db['chat_editing']
        index_of_chat = get_dict_index(db, group_id)

        collection.find_one_and_update({"user_id": ctx.from_user.id},
                                       {'$set': {f'settings.{index_of_chat}.warning_ban': ctx.text}})

        await bot.send_message(ctx.chat.id, text=f'Успешное изменение ✅')
        db = collection.find_one({"user_id": ctx.from_user.id})
        await state.finish()
        await asyncio.sleep(2)
        await bot.send_message(chat_id=ctx.chat.id,
                               text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n<b>Сообщения о бане | кике | разбане\nНажмите на одну из кнопок, чтобы изменить сообщение о:</b>\n\n<b>BAN:</b>\n{db["settings"][index_of_chat]["warning_ban"]}\n\n<b>KICK:</b>\n{db["settings"][index_of_chat]["warning_kick"]}\n\n<b>UNBAN:</b>\n{db["settings"][index_of_chat]["unban_text"]}',
                               reply_markup=generate_warning_editing_page())
    except Exception as e:
        print(e)

@dp.message_handler(content_types=['text'], state=MySceneStates.kickwarning_change_text_scene)
async def kickwarning_change_text(ctx: Message, state: FSMContext):
    try:
        db = collection.find_one({"user_id": ctx.from_user.id})
        group_id = db['chat_editing']
        index_of_chat = get_dict_index(db, group_id)

        collection.find_one_and_update({"user_id": ctx.from_user.id},
                                       {'$set': {f'settings.{index_of_chat}.warning_kick': ctx.text}})

        await bot.send_message(ctx.chat.id, text=f'Успешное изменение ✅')
        db = collection.find_one({"user_id": ctx.from_user.id})
        await state.finish()
        await asyncio.sleep(2)
        await bot.send_message(chat_id=ctx.chat.id,
                               text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n<b>Сообщения о бане | кике | разбане\nНажмите на одну из кнопок, чтобы изменить сообщение о:</b>\n\n<b>BAN:</b>\n{db["settings"][index_of_chat]["warning_ban"]}\n\n<b>KICK:</b>\n{db["settings"][index_of_chat]["warning_kick"]}\n\n<b>UNBAN:</b>\n{db["settings"][index_of_chat]["unban_text"]}',
                               reply_markup=generate_warning_editing_page())
    except Exception as e:
        print(e)

@dp.message_handler(content_types=['text'], state=MySceneStates.unbantext_change_text_scene)
async def unban_change_text(ctx: Message, state: FSMContext):
    try:
        db = collection.find_one({"user_id": ctx.from_user.id})
        group_id = db['chat_editing']
        index_of_chat = get_dict_index(db, group_id)

        collection.find_one_and_update({"user_id": ctx.from_user.id},
                                       {'$set': {f'settings.{index_of_chat}.unban_text': ctx.text}})

        await bot.send_message(ctx.chat.id, text=f'Успешное изменение ✅')
        db = collection.find_one({"user_id": ctx.from_user.id})
        await state.finish()
        await asyncio.sleep(2)
        await bot.send_message(chat_id=ctx.chat.id,
                               text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n<b>Сообщения о бане | кике | разбане\nНажмите на одну из кнопок, чтобы изменить сообщение о:</b>\n\n<b>BAN:</b>\n{db["settings"][index_of_chat]["warning_ban"]}\n\n<b>KICK:</b>\n{db["settings"][index_of_chat]["warning_kick"]}\n\n<b>UNBAN:</b>\n{db["settings"][index_of_chat]["unban_text"]}',
                               reply_markup=generate_warning_editing_page())
    except Exception as e:
        print(e)


@dp.message_handler(content_types=['text'], state=MySceneStates.resourcesw_change_scene)
async def resourcesw_change_text(ctx: Message, state: FSMContext):
    try:
        db = collection.find_one({"user_id": ctx.from_user.id})
        group_id = db['chat_editing']
        index_of_chat = get_dict_index(db, group_id)

        collection.find_one_and_update({"user_id": ctx.from_user.id},
                                       {'$set': {f'settings.{index_of_chat}.block_resources.warning': ctx.text}})

        await bot.send_message(ctx.chat.id, text=f'Успешное изменение ✅')
        await state.finish()
        await asyncio.sleep(2)
        await bot.send_message(chat_id=ctx.chat.id,
                                    text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n\n<b>Блокировка ссылок на внешние ресурсы:</b>\n{ctx.text}',
                                    reply_markup=generate_block_repostes_show(ctx.from_user.id, index_of_chat))
    except Exception as e:
        print(e)

@dp.message_handler(content_types=['text'], state=MySceneStates.repostesw_change_scene)
async def repostesw_change_text(ctx: Message, state: FSMContext):
    try:
        db = collection.find_one({"user_id": ctx.from_user.id})
        group_id = db['chat_editing']
        index_of_chat = get_dict_index(db, group_id)

        collection.find_one_and_update({"user_id": ctx.from_user.id},
                                       {'$set': {f'settings.{index_of_chat}.block_repostes.warning': ctx.text}})

        await bot.send_message(ctx.chat.id, text=f'Успешное изменение ✅')
        await state.finish()
        await asyncio.sleep(2)
        await bot.send_message(chat_id=ctx.chat.id,
                                    text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n\n<b>Запрет репостов:</b>\n{ctx.text}',
                                    reply_markup=generate_block_repostes_show(ctx.from_user.id, index_of_chat))
    except Exception as e:
        print(e)

@dp.message_handler(content_types=['text'], state=MySceneStates.pingw_change_scene)
async def pingw_change_text(ctx: Message, state: FSMContext):
    try:
        db = collection.find_one({"user_id": ctx.from_user.id})
        group_id = db['chat_editing']
        index_of_chat = get_dict_index(db, group_id)

        collection.find_one_and_update({"user_id": ctx.from_user.id},
                                       {'$set': {f'settings.{index_of_chat}.block_ping.warning': ctx.text}})

        await bot.send_message(ctx.chat.id, text=f'Успешное изменение ✅')
        await state.finish()
        await asyncio.sleep(2)
        await bot.send_message(chat_id=ctx.chat.id,
                                    text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n\n<b>Запрет пинга:</b>\n{ctx.text}',
                                    reply_markup=generate_block_ping_show(ctx.from_user.id, index_of_chat))
    except Exception as e:
        print(e)


@dp.message_handler(content_types=['text'])
async def message_staff(ctx: Message):
    try:
        if ctx.chat.type == 'group' or ctx.chat.type == 'supergroup':
            db = collection.find_one({"chats": f'{ctx.chat.id}'})
            if db == None: return
            index_of_chat = get_dict_index(db, ctx.chat.id)

            users_count = await bot.get_chat_members_count(ctx.chat.id)
            collection.find_one_and_update({'chats': f'{ctx.chat.id}'}, {
                "$set": {f"settings.{index_of_chat}.last_msg": datetime.now().strftime('%H:%M:%S'),
                         f"settings.{index_of_chat}.users_count": users_count}})
            adb = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})

            if users_count > adb['limit_to_users'] and db['user_id'] not in adb['admins'] and db['user_id'] != int(config['MAIN_ADMIN_ID']):
                return await bot.send_message(db['user_id'], 'Вы превысили Бесплатный лимит подписчиков на группу. Чтобы продолжить использовать бота, необходимо приобрести лицензию.', disable_notification=False)

            if db['settings'][index_of_chat]['block_repostes']['active'] == True:
                if ctx.forward_from:
                    await ctx.delete()
                    warning_text = f'✋ <a href="tg://user?id={ctx.from_user.id}">{ctx.from_user.first_name}</a>, вы нарушаете наши правила! Репосты запрещены!'
                    if db['settings'][index_of_chat]['block_repostes']['warning'] != 'None':
                        warning_text = db['settings'][index_of_chat]['block_repostes']['warning'].replace("{member_name}", ctx.from_user.first_name)
                    return await ctx.answer(warning_text)

            if db['settings'][index_of_chat]['block_ping']['active'] == True:
                mentions = check_mentions(ctx.text)
                entitle_user_index = get_user_dict_index(ctx.entities)
                if mentions[0] == True or entitle_user_index != None:
                    if mentions[1] == f'@{ctx.from_user.username}': return
                    if entitle_user_index != None:
                        if ctx.entities[entitle_user_index].user.id == ctx.from_user.id: return

                    await ctx.delete()
                    warning_text = f'✋ <a href="tg://user?id={ctx.from_user.id}">{ctx.from_user.first_name}</a>, вы нарушаете наши правила! Пинг запрещен!'
                    if db['settings'][index_of_chat]['block_ping']['warning'] != 'None':
                        warning_text = db['settings'][index_of_chat]['block_ping']['warning'].replace("{member_name}", ctx.from_user.first_name)
                    return await ctx.answer(warning_text)

            if db['settings'][index_of_chat]['block_resources']['active'] == True:
                if len(db['settings'][index_of_chat]['block_resources']['r_list']) == 0: return
                if contains_external_links(ctx.text, db['settings'][index_of_chat]['block_resources']['r_list']):
                    await ctx.delete()
                    warning_text = f'✋ <a href="tg://user?id={ctx.from_user.id}">{ctx.from_user.first_name}</a>, вы нарушаете наши правила! Запрещены любые ссылки!'
                    if db['settings'][index_of_chat]['block_resources']['warning'] != 'None':
                        warning_text = db['settings'][index_of_chat]['block_resources']['warning'].replace("{member_name}", ctx.from_user.first_name)
                    return await ctx.answer(warning_text)

    except Exception as e:
        print(e)
