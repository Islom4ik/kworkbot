# Обработчики текстовых данных:
import asyncio
import json
from decimal import Decimal
from data.loader import bot, dp, FSMContext, State, Message, config
from database.database import collection, ObjectId
from states_scenes.scene import MySceneStates
from time import sleep
from keyboards.inline_keyboards import *
from data.configs import *
from aiogram import types
from handlers import commands
from admin import admin
from datetime import datetime
from data.texts import *


@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def new_chat_member_greatings(ctx: Message):
    try:
        if ctx['new_chat_member']['is_bot'] == True:
            if ctx['new_chat_member']['username'] == t_bot_user:
                is_valid_chat = collection.find_one_and_update({'settings': {"$elemMatch": {'chat_id': str(ctx.chat.id)}}}, {'$push': {'chats': str(ctx.chat.id)}})
                if is_valid_chat != None: return collection.find_one_and_update({'_id': ObjectId('64987b1eeed9918b13b0e8b4')}, {'$push': {'groups': str(ctx.chat.id)}})
        db = collection.find_one({"chats": f"{ctx.chat.id}"})
        if db == None: return
        index_of_chat = get_dict_index(db, ctx.chat.id)
        settings_of_chat = db['settings'][index_of_chat]
        if 'users' not in settings_of_chat: collection.find_one_and_update({"chats": f"{ctx.chat.id}"}, {"$set": {f'settings.{index_of_chat}.users': []}})

        if db['settings'][index_of_chat]['system_notice']['active'] == True:
            await ctx.delete()

        member_name = ctx["new_chat_member"]["first_name"]

        text = f"Приветствуем, <b>{member_name}</b>!\n\nПрежде чем размещать свои объявления, пожалуйста, ознакомься с правилами. Они доступны по команде /rules"
        if db['settings'][index_of_chat]['greeting'] != 'None':
            text = db['settings'][index_of_chat]['greeting'].replace("{member_name}", member_name)

        trash = await ctx.answer(text)
        collection.find_one_and_update({"chats": f"{ctx.chat.id}"}, {"$push": {f'settings.{index_of_chat}.users': {"id": ctx["new_chat_member"]["id"], 'l_msg': get_msk_unix()}}})
        asyncio.create_task(delete_message(30, [trash.message_id], ctx.chat.id))
    except Exception as e:
        print(e)

@dp.message_handler(content_types=[types.ContentType.LEFT_CHAT_MEMBER])
async def left_chat_member(ctx: Message):
    try:
        if ctx.left_chat_member.username == t_bot_user and ctx.left_chat_member.is_bot == True:
            collection.find_one_and_update({'_id': ObjectId('64987b1eeed9918b13b0e8b4')}, {'$pull': {'groups': str(ctx.chat.id)}})
            return collection.find_one_and_update({'chats': str(ctx.chat.id)}, {'$pull': {'chats': str(ctx.chat.id)}})
        db = collection.find_one({"chats": f"{ctx.chat.id}"})
        if db == None: return
        index_of_chat = get_dict_index(db, ctx.chat.id)
        settings_of_chat = db['settings'][index_of_chat]
        if 'users' not in settings_of_chat: collection.find_one_and_update({"chats": f"{ctx.chat.id}"}, {
            "$set": {f'settings.{index_of_chat}.users': []}})
        if db['settings'][index_of_chat]['system_notice']['active'] == True:
            await ctx.delete()
        collection.find_one_and_update({"chats": f"{ctx.chat.id}"},
                                       {"$pull": {f'settings.{index_of_chat}.users': {"id": ctx["left_chat_participant"]["id"]}}})
    except Exception as e:
        print(e)

@dp.message_handler(content_types=['text'], state=MySceneStates.greeting_change_text_scene)
async def greeting_scene(ctx: Message, state: FSMContext):
    try:
        db = collection.find_one({"user_id": ctx.from_user.id})
        group_id = db['chat_editing']
        index_of_chat = get_dict_index(db, group_id)
        collection.find_one_and_update({"user_id": ctx.from_user.id}, {"$set": {f"settings.{index_of_chat}.greeting": ctx.text, f"settings.{index_of_chat}.updated_date": get_msk_unix()}})
        db = collection.find_one({"user_id": ctx.from_user.id})
        try:
            await bot.delete_message(ctx.chat.id, db['quatback'])
        except:
            print('err - scene deletion (NOT Important)')
        await bot.send_message(ctx.chat.id, text=f'Успешное изменение ✅')
        await state.finish()
        text = 'Приветствуем, <b>{str("{member_name}")}</b>!\n\nПрежде чем размещать свои объявления, пожалуйста, ознакомься с правилами. Они доступны по команде /rules'
        if db["settings"][index_of_chat]['greeting'] != 'None': text = db["settings"][index_of_chat]['greeting']
        sleep(2)
        await bot.send_message(ctx.chat.id, text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\n<b>Приветственное сообщение:</b>\n{text}',
                                    reply_markup=generate_text_editing_page())
    except Exception as e:
        print(e)

@dp.message_handler(content_types=['text'], state=MySceneStates.rules_change_text_scene)
async def rules_scene(ctx: Message, state: FSMContext):
    try:
        db = collection.find_one({"user_id": ctx.from_user.id})
        group_id = db['chat_editing']
        index_of_chat = get_dict_index(db, group_id)
        collection.find_one_and_update({"user_id": ctx.from_user.id}, {"$set": {f"settings.{index_of_chat}.rules": ctx.text, f"settings.{index_of_chat}.updated_date": get_msk_unix()}})
        db = collection.find_one({"user_id": ctx.from_user.id})
        try:
            await bot.delete_message(ctx.chat.id, db['quatback'])
        except:
            print('err - scene deletion (NOT Important)')
        await bot.send_message(ctx.chat.id, text=f'Успешное изменение ✅')
        await state.finish()
        text = '<i>Правила отсутствуют</i>'
        if db["settings"][index_of_chat]['rules'] != 'None': text = db["settings"][index_of_chat]['rules']
        sleep(2)
        await bot.send_message(ctx.chat.id, text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\n<b>Правила чата:</b>\n{text}',
                                    reply_markup=generate_rules_editing_page())
    except Exception as e:
        print(e)

@dp.message_handler(content_types=['text'], state=MySceneStates.afk_change_text_scene)
async def afk_scene(ctx: Message, state: FSMContext):
    try:
        db = collection.find_one({"user_id": ctx.from_user.id})
        group_id = db['chat_editing']
        index_of_chat = get_dict_index(db, group_id)
        collection.find_one_and_update({"user_id": ctx.from_user.id}, {"$set": {f"settings.{index_of_chat}.afk.warning": ctx.text, f"settings.{index_of_chat}.updated_date": get_msk_unix()}})
        db = collection.find_one({"user_id": ctx.from_user.id})
        try:
            await bot.delete_message(ctx.chat.id, db['quatback'])
        except:
            print('err - scene deletion (NOT Important)')
        await bot.send_message(ctx.chat.id, text=f'Успешное изменение ✅')
        text = f'Текст сообщения отсутствует 🤷‍♂'
        timer = '60'
        if 'timer' not in db['settings'][index_of_chat]['afk']:
            collection.find_one_and_update({"user_id": ctx.from_user.id}, {"$set": {f'settings.{index_of_chat}.afk.timer': 'None'}})
        elif db['settings'][index_of_chat]['afk']['timer'] != 'None': timer = db['settings'][index_of_chat]['afk']['timer']
        if db['settings'][index_of_chat]['afk']['warning'] != 'None': text = db['settings'][index_of_chat]['afk']['warning']
        await state.finish()
        await asyncio.sleep(2)
        await bot.send_message(ctx.chat.id, text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\n<b>Ворчун:</b>\nЕсли в чате никто не пишет <b>{timer}</b> секунд, то выводит сообщение:\n\n{text}',
                                    reply_markup=generate_block_afk_show(db['user_id'], index_of_chat))
    except Exception as e:
        print(e)

@dp.message_handler(content_types=['text'], state=MySceneStates.blocked_resources_add)
async def blocked_resources_add_scene(ctx: Message, state: FSMContext):
    try:
        domains_array = ctx.text.replace(' ', '').split(',')
        db = collection.find_one({"user_id": ctx.from_user.id})
        group_id = db['chat_editing']
        index_of_chat = get_dict_index(db, group_id)

        # if domains_array in db['settings'][index_of_chat]['block_resources']['r_list']: return await ctx.answer('⚠ В вашем списке запрещенных доменных расширений уже имеются некоторые введенные вами расширения.\n\nВведите доменные расширения, которые хотите заблокировать через запятую:')

        for i in domains_array:
            try:
                if i in db['settings'][index_of_chat]['block_resources']['r_list']: return await ctx.answer(
                    '✋ Вы пытаетесь добавить уже существующий запрет, введите запрет, которого нет в вашем списке:')
                collection.find_one_and_update({"user_id": ctx.from_user.id},
                                               {'$push': {f'settings.{index_of_chat}.block_resources.r_list': i}, '$set': {f"settings.{index_of_chat}.updated_date": get_msk_unix()}})
            except Exception as e:
                print(e)
        db = collection.find_one({"user_id": ctx.from_user.id})
        try:
            await bot.delete_message(ctx.chat.id, db['quatback'])
        except:
            print('err - scene deletion (NOT Important)')
        await bot.send_message(ctx.chat.id, text=f'Успешное изменение ✅')
        await state.finish()
        blocked_reses = ", ".join(db["settings"][index_of_chat]["block_resources"]["r_list"])
        if len(db["settings"][index_of_chat]["block_resources"]["r_list"]) == 0: blocked_reses = 'Нету'
        await asyncio.sleep(2)
        await bot.send_message(ctx.chat.id, text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nЗаблокированные ресурсы:\n<b>{", ".join(db["settings"][index_of_chat]["block_resources"]["r_list"])}</b>', reply_markup=generate_add_b_resources())
    except Exception as e:
        print(e)

@dp.message_handler(content_types=['text'], state=MySceneStates.blocked_resources_remove)
async def blocked_resources_remove_scene(ctx: Message, state: FSMContext):
    try:
        domains_array = ctx.text.replace(' ', '').split(',')
        db = collection.find_one({"user_id": ctx.from_user.id})
        group_id = db['chat_editing']
        index_of_chat = get_dict_index(db, group_id)

        for i in domains_array:
            try:
                if i not in db['settings'][index_of_chat]['block_resources']['r_list']: return await ctx.answer('✋ Вы пытаетесь удалить несуществующий запрет, введите запрет, который есть в вашем списке:')
                collection.find_one_and_update({"user_id": ctx.from_user.id},
                                               {'$pull': {f'settings.{index_of_chat}.block_resources.r_list': i}, "$set": {f"settings.{index_of_chat}.updated_date": get_msk_unix()}})
            except Exception as e:
                print(e)
        db = collection.find_one({"user_id": ctx.from_user.id})
        try:
            await bot.delete_message(ctx.chat.id, db['quatback'])
        except:
            print('err - scene deletion (NOT Important)')
        await bot.send_message(ctx.chat.id, text=f'Успешное изменение ✅')
        await state.finish()
        blocked_reses = ", ".join(db["settings"][index_of_chat]["block_resources"]["r_list"])
        if len(db["settings"][index_of_chat]["block_resources"]["r_list"]) == 0: blocked_reses = 'Нету'
        await asyncio.sleep(2)
        await bot.send_message(ctx.chat.id, text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nЗаблокированные ресурсы:\n<b>{", ".join(db["settings"][index_of_chat]["block_resources"]["r_list"])}</b>', reply_markup=generate_add_b_resources())
    except Exception as e:
        print(e)


@dp.message_handler(content_types=['text'], state=MySceneStates.blocked_syms_add)
async def blocked_syms_add_scene(ctx: Message, state: FSMContext):
    try:
        syms_array = ctx.text.replace(' ', '').split(',')
        db = collection.find_one({"user_id": ctx.from_user.id})
        group_id = db['chat_editing']
        index_of_chat = get_dict_index(db, group_id)

        for i in syms_array:
            try:
                if i in db['settings'][index_of_chat]['blocked_syms']: return await ctx.answer(
                    '✋ Вы пытаетесь добавить уже существующий фильтр, введите символ, которого нет в вашем списке:')
                collection.find_one_and_update({"user_id": ctx.from_user.id},
                                               {'$push': {f'settings.{index_of_chat}.blocked_syms': i}, '$set': {f"settings.{index_of_chat}.updated_date": get_msk_unix()}})
            except Exception as e:
                print(e)
        db = collection.find_one({"user_id": ctx.from_user.id})
        try:
            await bot.delete_message(ctx.chat.id, db['quatback'])
        except:
            print('err - scene deletion (NOT Important)')
        await bot.send_message(ctx.chat.id, text=f'Успешное изменение ✅')
        await state.finish()
        list = 'Нету'
        if len(db["settings"][index_of_chat]["blocked_syms"]) != 0: list = ", ".join(db["settings"][index_of_chat]["blocked_syms"])
        await asyncio.sleep(1)
        await bot.send_message(ctx.chat.id, text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\n<b>Ваш список символов:</b>\n{list}\n\n<b>Выберите действие:</b>', reply_markup=generate_add_b_syms())
    except Exception as e:
        print(e)

@dp.message_handler(content_types=['text'], state=MySceneStates.blocked_syms_remove)
async def blocked_syms_remove_scene(ctx: Message, state: FSMContext):
    try:
        syms_array = ctx.text.replace(' ', '').split(',')
        db = collection.find_one({"user_id": ctx.from_user.id})
        group_id = db['chat_editing']
        index_of_chat = get_dict_index(db, group_id)

        for i in syms_array:
            try:
                if i not in db['settings'][index_of_chat]['blocked_syms']: return await ctx.answer('✋ Вы пытаетесь удалить несуществующий фильтр, введите символ, который есть в вашем списке:')
                collection.find_one_and_update({"user_id": ctx.from_user.id},
                                               {'$pull': {f'settings.{index_of_chat}.blocked_syms': i}, "$set": {f"settings.{index_of_chat}.updated_date": get_msk_unix()}})
            except Exception as e:
                print(e)
        db = collection.find_one({"user_id": ctx.from_user.id})
        try:
            await bot.delete_message(ctx.chat.id, db['quatback'])
        except:
            print('err - scene deletion (NOT Important)')
        await bot.send_message(ctx.chat.id, text=f'Успешное изменение ✅')
        await state.finish()
        list = 'Нету'
        if len(db["settings"][index_of_chat]["blocked_syms"]) != 0: list = ", ".join(db["settings"][index_of_chat]["blocked_syms"])
        await asyncio.sleep(1)
        await bot.send_message(ctx.chat.id, text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\n<b>Ваш список символов:</b>\n{list}\n\n<b>Выберите действие:</b>', reply_markup=generate_add_b_syms())
    except Exception as e:
        print(e)


@dp.message_handler(content_types=['text'], state=MySceneStates.banwarning_change_text_scene)
async def banwarning_change_text(ctx: Message, state: FSMContext):
    try:
        db = collection.find_one({"user_id": ctx.from_user.id})
        group_id = db['chat_editing']
        index_of_chat = get_dict_index(db, group_id)

        collection.find_one_and_update({"user_id": ctx.from_user.id},
                                       {'$set': {f'settings.{index_of_chat}.warning_ban': ctx.text, f"settings.{index_of_chat}.updated_date": get_msk_unix()}})
        try:
            await bot.delete_message(ctx.chat.id, db['quatback'])
        except:
            print('err - scene deletion (NOT Important)')
        await bot.send_message(ctx.chat.id, text=f'Успешное изменение ✅')
        db = collection.find_one({"user_id": ctx.from_user.id})
        await state.finish()
        ban = t_ban
        kick = t_kick
        unban = t_unban
        if db["settings"][index_of_chat]["warning_ban"] != 'None': ban = db["settings"][index_of_chat]["warning_ban"]
        if db["settings"][index_of_chat]["warning_kick"] != 'None': kick = db["settings"][index_of_chat]["warning_kick"]
        if db["settings"][index_of_chat]["unban_text"] != 'None': unban = db["settings"][index_of_chat]["unban_text"]
        await asyncio.sleep(2)
        await bot.send_message(chat_id=ctx.chat.id,
                               text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n<b>Сообщения, которые будут выводиться по вводу команд: /kick , /ban , /unban</b>\n\n<b>/ban</b>\n{ban}\n\n<b>/kick</b>\n{kick}\n\n<b>/unban</b>\n{unban}',
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
                                       {'$set': {f'settings.{index_of_chat}.warning_kick': ctx.text, f"settings.{index_of_chat}.updated_date": get_msk_unix()}})
        try:
            await bot.delete_message(ctx.chat.id, db['quatback'])
        except:
            print('err - scene deletion (NOT Important)')
        await bot.send_message(ctx.chat.id, text=f'Успешное изменение ✅')
        db = collection.find_one({"user_id": ctx.from_user.id})
        await state.finish()
        ban = t_ban
        kick = t_kick
        unban = t_unban
        if db["settings"][index_of_chat]["warning_ban"] != 'None': ban = db["settings"][index_of_chat]["warning_ban"]
        if db["settings"][index_of_chat]["warning_kick"] != 'None': kick = db["settings"][index_of_chat]["warning_kick"]
        if db["settings"][index_of_chat]["unban_text"] != 'None': unban = db["settings"][index_of_chat]["unban_text"]
        await asyncio.sleep(2)
        await bot.send_message(chat_id=ctx.chat.id,
                               text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n<b>Сообщения, которые будут выводиться по вводу команд: /kick , /ban , /unban</b>\n\n<b>/ban</b>\n{ban}\n\n<b>/kick</b>\n{kick}\n\n<b>/unban</b>\n{unban}',
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
                                       {'$set': {f'settings.{index_of_chat}.unban_text': ctx.text, f"settings.{index_of_chat}.updated_date": get_msk_unix()}})
        try:
            await bot.delete_message(ctx.chat.id, db['quatback'])
        except:
            print('err - scene deletion (NOT Important)')
        await bot.send_message(ctx.chat.id, text=f'Успешное изменение ✅')
        db = collection.find_one({"user_id": ctx.from_user.id})
        await state.finish()
        ban = t_ban
        kick = t_kick
        unban = t_unban
        if db["settings"][index_of_chat]["warning_ban"] != 'None': ban = db["settings"][index_of_chat]["warning_ban"]
        if db["settings"][index_of_chat]["warning_kick"] != 'None': kick = db["settings"][index_of_chat]["warning_kick"]
        if db["settings"][index_of_chat]["unban_text"] != 'None': unban = db["settings"][index_of_chat]["unban_text"]
        await asyncio.sleep(2)
        await bot.send_message(chat_id=ctx.chat.id,
                               text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n<b>Сообщения, которые будут выводиться по вводу команд: /kick , /ban , /unban</b>\n\n<b>/ban</b>\n{ban}\n\n<b>/kick</b>\n{kick}\n\n<b>/unban</b>\n{unban}',
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
                                       {'$set': {f'settings.{index_of_chat}.block_resources.warning': ctx.text, f"settings.{index_of_chat}.updated_date": get_msk_unix()}})
        db = collection.find_one({"user_id": ctx.from_user.id})
        try:
            await bot.delete_message(ctx.chat.id, db['quatback'])
        except:
            print('err - scene deletion (NOT Important)')
        await bot.send_message(ctx.chat.id, text=f'Успешное изменение ✅')
        await state.finish()
        await asyncio.sleep(2)
        await bot.send_message(chat_id=ctx.chat.id,
                                    text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\n<b>Сообщение при нарушении:</b>\n{ctx.text}',
                                    reply_markup=generate_block_resources_show(ctx.from_user.id, index_of_chat))
    except Exception as e:
        print(e)

@dp.message_handler(content_types=['text'], state=MySceneStates.repostesw_change_scene)
async def repostesw_change_text(ctx: Message, state: FSMContext):
    try:
        db = collection.find_one({"user_id": ctx.from_user.id})
        group_id = db['chat_editing']
        index_of_chat = get_dict_index(db, group_id)

        collection.find_one_and_update({"user_id": ctx.from_user.id},
                                       {'$set': {f'settings.{index_of_chat}.block_repostes.warning': ctx.text, f"settings.{index_of_chat}.updated_date": get_msk_unix()}})
        db = collection.find_one({"user_id": ctx.from_user.id})
        try:
            await bot.delete_message(ctx.chat.id, db['quatback'])
        except:
            print('err - scene deletion (NOT Important)')
        await bot.send_message(ctx.chat.id, text=f'Успешное изменение ✅')
        await state.finish()
        await asyncio.sleep(2)
        await bot.send_message(chat_id=ctx.chat.id,
                                    text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\n<b>Сообщение при нарушении:</b>\n{ctx.text}',
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
                                       {'$set': {f'settings.{index_of_chat}.block_ping.warning': ctx.text, f"settings.{index_of_chat}.updated_date": get_msk_unix()}})
        db = collection.find_one({"user_id": ctx.from_user.id})
        try:
            await bot.delete_message(ctx.chat.id, db['quatback'])
        except:
            print('err - scene deletion (NOT Important)')
        await bot.send_message(ctx.chat.id, text=f'Успешное изменение ✅')
        await state.finish()
        await asyncio.sleep(2)
        await bot.send_message(chat_id=ctx.chat.id,
                                    text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\n<b>Сообщение при нарушении:</b>\n{ctx.text}',
                                    reply_markup=generate_block_ping_show(ctx.from_user.id, index_of_chat))
    except Exception as e:
        print(e)


@dp.message_handler(content_types=['text'], state=MySceneStates.donate_money_scene)
async def donate_money_set(ctx: Message, state: FSMContext):
    try:
        sum = ctx.text
        if sum.isdigit() == False: return await ctx.answer('✋ Введите целое число:')
        todigit = int(sum)
        if todigit < 100: return await ctx.answer('✋ Минимальная сумма оплаты <b>100</b>₽, введите сумму ещё раз:')
        if todigit > 100000000: return await ctx.answer('✋ Сумма доната не может быть больше <b>1 млн</b>, введите сумму ещё раз:')
        withdecimate = todigit * 100
        collection.find_one_and_update({"user_id": ctx.from_user.id},
                                       {'$set': {'donate_money': withdecimate}})
        db = collection.find_one({"user_id": ctx.from_user.id})
        try:
            await bot.delete_message(ctx.chat.id, db['quatback'])
        except:
            print('err - scene deletion (NOT Important)')
        await state.finish()
        await bot.send_message(chat_id=ctx.chat.id,
                                    text=f'💸 <b>Выберите способ оплаты:</b>',
                                    reply_markup=generate_dpayment_method())
    except Exception as e:
        print(e)

@dp.message_handler(content_types=['text'], state=MySceneStates.vorchun_timer_scene)
async def vorchun_timer_scene(ctx: Message, state: FSMContext):
    try:
        timer = ctx.text
        if timer.isdigit() == False: return await ctx.answer('✋ Значение должно быть целым числом, введите значение ещё раз:')
        todigit = int(timer)
        if todigit <= 0: return await ctx.answer('✋ Значение не может быть <b>0</b> или отрецательным, введите значение ещё раз:')
        if todigit > 100000000000000000: return await ctx.answer('✋ Значение слишком большое, введите значение ещё раз:')
        db = collection.find_one({"user_id": ctx.from_user.id})
        group_id = db['chat_editing']
        index_of_chat = get_dict_index(db, group_id)
        collection.find_one_and_update({"user_id": ctx.from_user.id},
                                       {'$set': {f'settings.{index_of_chat}.afk.timer': todigit}})
        db = collection.find_one({"user_id": ctx.from_user.id})
        try:
            await bot.delete_message(ctx.chat.id, db['quatback'])
        except:
            print('err - scene deletion (NOT Important)')

        text = f'Текст сообщения отсутствует 🤷‍♂'
        timer = '60'
        if 'timer' not in db['settings'][index_of_chat]['afk']:
            collection.find_one_and_update({"user_id": ctx.from_user.id}, {"$set": {f'settings.{index_of_chat}.afk.timer': 'None'}})
        elif db['settings'][index_of_chat]['afk']['timer'] != 'None': timer = db['settings'][index_of_chat]['afk']['timer']
        if db['settings'][index_of_chat]['afk']['warning'] != 'None': text = db['settings'][index_of_chat]['afk']['warning']
        await state.finish()
        await bot.send_message(ctx.chat.id, text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\n<b>Ворчун:</b>\nЕсли в чате никто не пишет <b>{timer}</b> секунд, то выводит сообщение:\n\n{text}',
                               reply_markup=generate_block_afk_show(db['user_id'], index_of_chat))
    except Exception as e:
        print(e)

@dp.message_handler(content_types=['text', 'photo', types.ContentTypes.AUDIO, types.ContentTypes.VIDEO, types.ContentTypes.VOICE, types.ContentTypes.VIDEO_NOTE])
async def message_staff(ctx: Message):
    try:
        # print(collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')}))
        if ctx.chat.type == 'group' or ctx.chat.type == 'supergroup':
            db = collection.find_one({"chats": f'{ctx.chat.id}'})
            if db == None: return
            index_of_chat = get_dict_index(db, ctx.chat.id)
            settings_of_chat = db['settings'][index_of_chat]
            if 'users' not in settings_of_chat: collection.find_one_and_update({"chats": f"{ctx.chat.id}"}, {
                "$set": {f'settings.{index_of_chat}.users': []}})
            users_count = await bot.get_chat_members_count(ctx.chat.id)
            db = collection.find_one_and_update({'chats': f'{ctx.chat.id}'}, {
                "$set": {f"settings.{index_of_chat}.last_msg": datetime.now().strftime('%H:%M:%S'),
                         f"settings.{index_of_chat}.users_count": users_count, f"settings.{index_of_chat}.bot_send_afk": False}})
            get_user = get_chat_user_dict_index(db, ctx.from_user.id, index_of_chat)
            if get_user == None: collection.find_one_and_update({'chats': f'{ctx.chat.id}'}, {"$push": {f'settings.{index_of_chat}.users': {"id": ctx.from_user.id, 'l_msg': get_msk_unix()}}})
            else: collection.find_one_and_update({'chats': f'{ctx.chat.id}'}, {"$set": {f'settings.{index_of_chat}.users.{get_user}.l_msg': get_msk_unix()}})
            adb = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
            if users_count > adb['limit_to_users'] and db['settings'][index_of_chat]['lic'] == False:
                if 'lic_warn' not in db['settings'][index_of_chat]: collection.find_one_and_update({'chats': f'{ctx.chat.id}'}, {
                "$set": {f"settings.{index_of_chat}.lic_warn": False}})
                db = collection.find_one({'chats': f'{ctx.chat.id}'})
                if db['settings'][index_of_chat]['lic_warn'] == False:
                    await bot.send_message(db['user_id'],
                                           f'Вы превысили Бесплатный лимит подписчиков на группу. Чтобы продолжить использовать бота, необходимо приобрести лицензию на чат в настройках чата - <b>{ctx.chat.title}</b>',
                                           reply_markup=generate_mychats_button(), disable_notification=False)
                    return collection.find_one_and_update({'chats': f'{ctx.chat.id}'}, {
                        "$set": {f"settings.{index_of_chat}.lic_warn": True}})
            # and db['user_id'] not in adb['admins'] and db['user_id'] != int(config['MAIN_ADMIN_ID'])
            if db['settings'][index_of_chat]['block_repostes']['active'] == True:
                if ctx.forward_from or ctx.forward_from_chat:
                    await ctx.delete()
                    warning_text = f'✋ <a href="tg://user?id={ctx.from_user.id}">{ctx.from_user.first_name}</a>, вы нарушаете наши правила! Репосты запрещены!'
                    if db['settings'][index_of_chat]['block_repostes']['warning'] != 'None':
                        warning_text = db['settings'][index_of_chat]['block_repostes']['warning'].replace("{member_name}", ctx.from_user.first_name)
                    return await ctx.answer(warning_text)

            if db['settings'][index_of_chat]['block_ping']['active'] == True:
                if ctx.text:
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
                if ctx.caption:
                    mentions = check_mentions(ctx.caption)
                    entitle_user_index = get_user_dict_index(ctx.caption)
                    if mentions[0] == True or entitle_user_index != None:
                        if mentions[1] == f'@{ctx.from_user.username}': return
                        if entitle_user_index != None:
                            if ctx.caption_entities[entitle_user_index].user.id == ctx.from_user.id: return

                        await ctx.delete()
                        warning_text = f'✋ <a href="tg://user?id={ctx.from_user.id}">{ctx.from_user.first_name}</a>, вы нарушаете наши правила! Пинг запрещен!'
                        if db['settings'][index_of_chat]['block_ping']['warning'] != 'None':
                            warning_text = db['settings'][index_of_chat]['block_ping']['warning'].replace("{member_name}", ctx.from_user.first_name)
                        return await ctx.answer(warning_text)


            if db['settings'][index_of_chat]['block_resources']['active'] == True:
                if ctx.text:
                    if len(db['settings'][index_of_chat]['block_resources']['r_list']) == 0: return
                    if contains_external_links(ctx.text, db['settings'][index_of_chat]['block_resources']['r_list']):
                        await ctx.delete()
                        warning_text = f'✋ <a href="tg://user?id={ctx.from_user.id}">{ctx.from_user.first_name}</a>, вы нарушаете наши правила! Запрещены любые ссылки!'
                        if db['settings'][index_of_chat]['block_resources']['warning'] != 'None':
                            warning_text = db['settings'][index_of_chat]['block_resources']['warning'].replace("{member_name}", ctx.from_user.first_name)
                        return await ctx.answer(warning_text)
                if ctx.caption:
                    if len(db['settings'][index_of_chat]['block_resources']['r_list']) == 0: return
                    if contains_external_links(ctx.caption, db['settings'][index_of_chat]['block_resources']['r_list']):
                        await ctx.delete()
                        warning_text = f'✋ <a href="tg://user?id={ctx.from_user.id}">{ctx.from_user.first_name}</a>, вы нарушаете наши правила! Запрещены любые ссылки!'
                        if db['settings'][index_of_chat]['block_resources']['warning'] != 'None':
                            warning_text = db['settings'][index_of_chat]['block_resources']['warning'].replace("{member_name}", ctx.from_user.first_name)
                        return await ctx.answer(warning_text)


    except Exception as e:
        print(e)
