# Обработчики нажатых, встроенных кнопок под сообщениями:
import asyncio
import pytz
import re
from data.loader import bot, dp, FSMContext, State, config
from database.database import collection, ObjectId
from states_scenes.scene import MySceneStates
from aiogram.types import CallbackQuery, ContentTypes, LabeledPrice, PreCheckoutQuery, Message
from data.configs import *
from data.texts import *
from keyboards.inline_keyboards import *
from datetime import datetime

@dp.callback_query_handler(lambda call: call.data == 'check_admingr')
async def check_admin_rght(call: CallbackQuery):
    try:
        if call.message.chat.type == 'group' or call.message.chat.type == 'supergroup':
            admins = await bot.get_chat_administrators(call.message.chat.id)
            for me in admins:
                if me.user.username == "shieldsword_bot":
                    if me.can_manage_chat == True and me.can_delete_messages == True and me.can_restrict_members == True and me.can_invite_users == True and me.can_promote_members == True:
                        await bot.delete_message(call.message.chat.id, call.message.message_id)
                        admins = await bot.get_chat_administrators(call.message.chat.id)
                        creator_id = next((obj for obj in admins if obj["status"] == "creator"), None).user.id
                        await call.answer('Успех!', show_alert=False)
                        return await bot.send_message(call.message.chat.id,
                                                      '🤖 Вы выполнили корректные действия.\n\nНажмите кнопку "Настроить бота"',
                                                      reply_markup=generate_settings_button(
                                                          f'{call.message.chat.id}_{creator_id}'))
                    else:
                        return await call.answer(
                            'К сожалению ничего не изменилось 😶 Я все ещё без прав.\n\nВыдайте все права и попробуйте снова!',
                            show_alert=True)
                    break
                else:
                    return await call.answer(
                        'К сожалению ничего не изменилось 😶 Я все ещё без прав.\n\nВыдайте все права и попробуйте снова!',
                        show_alert=True)
                    break
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'settings_texts')
async def change_to_edit_page(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"chats": group_id})
        index_of_chat = get_dict_index(db, group_id)
        await call.answer()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db['settings'][index_of_chat]['updated_date'])),
                                    reply_markup=generate_edit_text_settings())
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'back_from_edit_limits')
async def answer_to_back_from_edits(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Добро пожаловать в админку, <a href="tg://user?id={call.from_user.id}">{call.from_user.first_name}</a>', reply_markup=generate_admin_main_page())

@dp.callback_query_handler(lambda call: call.data == 'back_to_chose')
async def react_to_back(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"chats": group_id})
        index_of_chat = get_dict_index(db, group_id)
        await call.answer()
        if db['settings'][index_of_chat]['lic'] == True: return await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db['settings'][index_of_chat]['updated_date'])),
                                    reply_markup=generate_settings(True))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db['settings'][index_of_chat]['updated_date'])),
                                    reply_markup=generate_settings())
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'done_btn')
async def react_to_done(call: CallbackQuery):
    try:
        await call.answer()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'⚙ Настройки чата завершена')
        asyncio.create_task(done_message(chat_id=call.message.chat.id))
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'texts_greeting')
async def text_greeting_show(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"chats": str(group_id)})

        index_of_chat = get_dict_index(db, group_id)

        text = db["settings"][index_of_chat]['greeting']

        await call.answer()
        if text == 'None':
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n<b>Приветственное сообщение:</b>\n\nПриветствуем, <b>{str("{member_name}")}</b>!\n\nПрежде чем размещать свои объявления, пожалуйста, ознакомься с правилами. Они доступны по команде /rules',
                                        reply_markup=generate_text_editing_page())
        else:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n<b>Приветственное сообщение:</b>\n\n{text}',
                                        reply_markup=generate_text_editing_page())
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'show_rules')
async def text_rules_show(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"chats": str(group_id)})

        index_of_chat = get_dict_index(db, group_id)

        text = db["settings"][index_of_chat]['rules']

        await call.answer()
        if text == 'None':
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n<b>Правила чата:</b>\n\n<i>Правила отсутствуют</i>',
                                        reply_markup=generate_rules_editing_page())
        else:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n<b>Правила чата:</b>\n\n{text}',
                                        reply_markup=generate_rules_editing_page())
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'show_warning')
async def text_warning_show(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"chats": str(group_id)})

        index_of_chat = get_dict_index(db, group_id)

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n<b>Сообщения о бане | кике | разбане\nНажмите на одну из кнопок, чтобы изменить сообщение о:</b>\n\n<b>BAN:</b>\n{db["settings"][index_of_chat]["warning_ban"]}\n\n<b>KICK:</b>\n{db["settings"][index_of_chat]["warning_kick"]}\n\n<b>UNBAN:</b>\n{db["settings"][index_of_chat]["unban_text"]}',
                                    reply_markup=generate_warning_editing_page())
    except Exception as e:
        print(e)




@dp.callback_query_handler(lambda call: call.data == 'formating')
async def format_btn_react(call: CallbackQuery):
    try:
        trash = await bot.send_message(call.message.chat.id, '💿 Для форматирования текста мы используем HTML форматирование и вы можете встроить HTML форматирование в ваш текст\n\nФичи:\n{member_name} - имя участника(участников) чата с которым связан контекст бота;\n\n{admin} - имя администратора с которым связанно действие бота(Можно использовать в сообщение о бане, кике, unban)')
        asyncio.create_task(delete_message(20, [trash.message_id], trash.chat.id))
        await call.answer()
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'show_afk')
async def text_afk_show(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"chats": str(group_id)})

        index_of_chat = get_dict_index(db, group_id)

        text = db["settings"][index_of_chat]['afk']

        await call.answer()
        if text == 'None':
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n<b>Уведомление при неактивности чата:</b>\n\nАууу... Что-то актива нет',
                                        reply_markup=generate_afk_editing_page())
        else:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n<b>Уведомление при неактивности чата:</b>\n\n{text}',
                                        reply_markup=generate_afk_editing_page())
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'back_to_show_page')
async def react_to_back_to_show(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"chats": group_id})
        index_of_chat = get_dict_index(db, group_id)
        await call.answer()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nВыберите текст, который хотите посмотреть:',
                                    reply_markup=generate_edit_text_settings())
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda call: 'edit' in call.data)
async def scenes_editor(call: CallbackQuery):
    try:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        call_main = call.data.split('_')[1]
        group_id_url = call.message.entities[0].url
        group_id = int("-" + re.sub(r"\D", "", group_id_url))
        collection.find_one_and_update({"user_id": call.from_user.id}, {"$set": {"chat_editing": group_id}})
        if call_main == 'greeting':
            await call.answer()
            await MySceneStates.greeting_change_text_scene.set()
            await bot.send_message(call.message.chat.id, '📋 Введите текст для приветствия новых участников чата:')
        elif call_main == 'rules':
            await call.answer()
            await MySceneStates.rules_change_text_scene.set()
            await bot.send_message(call.message.chat.id, '📋 Введите текст правил чата:')
        elif call_main == 'banwarning':
            await call.answer()
            await MySceneStates.banwarning_change_text_scene.set()
            await bot.send_message(call.message.chat.id, '📋 Введите текст, который будет отправлен после использования команды ban:')
        elif call_main == 'kickwarning':
            await call.answer()
            await MySceneStates.kickwarning_change_text_scene.set()
            await bot.send_message(call.message.chat.id, '📋 Введите текст, который будет отправлен после использования команды kick:')
        elif call_main == 'unbantext':
            await call.answer()
            await MySceneStates.unbantext_change_text_scene.set()
            await bot.send_message(call.message.chat.id, '📋 Введите текст, который будет отправлен после использования команды unban:')
        elif call_main == 'afk':
            await call.answer()
            await MySceneStates.afk_change_text_scene.set()
            await bot.send_message(call.message.chat.id, '📋 Введите текст, который будет уведомлять чат при неактивности:')
        elif call_main == 'resourcesw':
            await call.answer()
            await MySceneStates.resourcesw_change_scene.set()
            await bot.send_message(call.message.chat.id, '📋 Введить новый текст предупреждения о нарушении:')
        elif call_main == 'repostesw':
            await call.answer()
            await MySceneStates.repostesw_change_scene.set()
            await bot.send_message(call.message.chat.id, '📋 Введить новый текст предупреждения о нарушении:')
        elif call_main == 'pingw':
            await call.answer()
            await MySceneStates.pingw_change_scene.set()
            await bot.send_message(call.message.chat.id, '📋 Введить новый текст предупреждения о нарушении:')
        else:
            await call.answer()
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda call: call.data == 'settings_admins')
async def edit_admins_settings(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"chats": group_id})
        index_of_chat = get_dict_index(db, group_id)
        await call.answer()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nВыберите функцию:', reply_markup=generate_admins_settings())
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda call: call.data == 'back_to_admin_page')
async def back_to_admin_page(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"chats": group_id})
        index_of_chat = get_dict_index(db, group_id)
        await call.answer()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nВыберите функцию:', reply_markup=generate_admins_settings())
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda call: call.data == 'block_resources_show')
async def react_to_block_resources_show(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"user_id": call.from_user.id})

        index_of_chat = get_dict_index(db, group_id)
        await call.answer()
        text = '✋ {member_name}, у нас запрещено использовать ссылки!'
        if db['settings'][index_of_chat]['block_resources']['warning'] != 'None': text = db['settings'][index_of_chat]['block_resources']['warning']
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\n<b>Сообщение при нарушении:</b>\n{text}', reply_markup=generate_block_resources_show(call.from_user.id, index_of_chat))
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'block_repostes_show')
async def react_to_block_repostes_show(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"user_id": call.from_user.id})

        index_of_chat = get_dict_index(db, group_id)
        await call.answer()
        text = '✋ {member_name}, вы нарушаете наши правила! Репосты запрещены!'
        if db['settings'][index_of_chat]['block_repostes']['warning'] != 'None': text = db['settings'][index_of_chat]['block_repostes']['warning']
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\n<b>Запрет репостов:</b>\n{text}', reply_markup=generate_block_repostes_show(call.from_user.id, index_of_chat))
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda call: call.data == 'system_notice_show')
async def react_to_system_notice_show(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"user_id": call.from_user.id})

        index_of_chat = get_dict_index(db, group_id)
        await call.answer()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nАвто-удаление системных оповещение о подключении к чату нового пользователя или при покиданий пользователя:', reply_markup=generate_system_notice_show(call.from_user.id, index_of_chat))
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'block_ping_show')
async def react_to_block_ping_show(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"user_id": call.from_user.id})

        index_of_chat = get_dict_index(db, group_id)
        await call.answer()
        text = '✋ {member_name}, вы нарушаете наши правила! Пинг запрещен!'
        if db['settings'][index_of_chat]['block_ping']['warning'] != 'None': text = db['settings'][index_of_chat]['block_ping']['warning']
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\n<b>Запрет пинга:</b>\n{text}', reply_markup=generate_block_ping_show(call.from_user.id, index_of_chat))
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: 'activator' in call.data)
async def react_to_activator(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"user_id": call.from_user.id})

        index_of_chat = get_dict_index(db, group_id)

        call_data_identificator = call.data.split('_')[1]

        if call_data_identificator == 'resources':
            if db['settings'][index_of_chat]['block_resources']['active'] == False:
                collection.find_one_and_update({"user_id": call.from_user.id},
                                               {"$set": {f"settings.{index_of_chat}.block_resources.active": True, f"settings.{index_of_chat}.updated_date": get_msk_unix()}})
            else:
                collection.find_one_and_update({"user_id": call.from_user.id},
                                               {"$set": {f"settings.{index_of_chat}.block_resources.active": False, f"settings.{index_of_chat}.updated_date": get_msk_unix()}})
            await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                reply_markup=generate_block_resources_show(call.from_user.id, index_of_chat))
        elif call_data_identificator == 'repostes':
            if db['settings'][index_of_chat]['block_repostes']['active'] == False:
                collection.find_one_and_update({"user_id": call.from_user.id},
                                               {"$set": {f"settings.{index_of_chat}.block_repostes.active": True, f"settings.{index_of_chat}.updated_date": get_msk_unix()}})
            else:
                collection.find_one_and_update({"user_id": call.from_user.id},
                                               {"$set": {f"settings.{index_of_chat}.block_repostes.active": False, f"settings.{index_of_chat}.updated_date": get_msk_unix()}})
            await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                reply_markup=generate_block_repostes_show(call.from_user.id, index_of_chat))
        elif call_data_identificator == "sysnot":
            if db['settings'][index_of_chat]['system_notice']['active'] == False:
                collection.find_one_and_update({"user_id": call.from_user.id},
                                               {"$set": {f"settings.{index_of_chat}.system_notice.active": True, f"settings.{index_of_chat}.updated_date": get_msk_unix()}})
            else:
                collection.find_one_and_update({"user_id": call.from_user.id},
                                               {"$set": {f"settings.{index_of_chat}.system_notice.active": False, f"settings.{index_of_chat}.updated_date": get_msk_unix()}})
            await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                reply_markup=generate_system_notice_show(call.from_user.id, index_of_chat))
        else:
            if db['settings'][index_of_chat]['block_ping']['active'] == False:
                collection.find_one_and_update({"user_id": call.from_user.id},
                                               {"$set": {f"settings.{index_of_chat}.block_ping.active": True, f"settings.{index_of_chat}.updated_date": get_msk_unix()}})
            else:
                collection.find_one_and_update({"user_id": call.from_user.id},
                                               {"$set": {f"settings.{index_of_chat}.block_ping.active": False, f"settings.{index_of_chat}.updated_date": get_msk_unix()}})
            await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                reply_markup=generate_block_ping_show(call.from_user.id, index_of_chat))

        await call.answer()
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'blocked_resources')
async def show_blocked_resources(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"user_id": call.from_user.id})

        index_of_chat = get_dict_index(db, group_id)

        await call.answer()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nЗаблокированные ресурсы:\n<b>{", ".join(db["settings"][index_of_chat]["block_resources"]["r_list"])}</b>',
                                    reply_markup=generate_add_b_resources())
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda call: call.data == 'add_block_resources')
async def react_to_add_block_resources(call: CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    group_id_url = call.message.entities[0].url
    group_id = int("-" + re.sub(r"\D", "", group_id_url))
    collection.find_one_and_update({"user_id": call.from_user.id}, {"$set": {"chat_editing": group_id}})
    await bot.send_message(call.message.chat.id, '📋 Введите доменные расширения, которые хотите заблокировать через запятую\n\nПример 1: ru\nПример 2: ru, com, io')
    await MySceneStates.blocked_resources_add.set()

@dp.callback_query_handler(lambda call: call.data == 'remove_block_resources')
async def react_to_add_block_resources(call: CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    group_id_url = call.message.entities[0].url
    group_id = int("-" + re.sub(r"\D", "", group_id_url))
    collection.find_one_and_update({"user_id": call.from_user.id}, {"$set": {"chat_editing": group_id}})
    await bot.send_message(call.message.chat.id, '📋 Введите доменные расширения, которые хотите удалить из заблокированных через запятую\n\nПример 1: ru\nПример 2: ru, com, io')
    await MySceneStates.blocked_resources_remove.set()

@dp.callback_query_handler(lambda call: call.data == 'back_to_block_resources')
async def react_to_back_to_block_resources(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"chats": str(group_id)})

        index_of_chat = get_dict_index(db, group_id)

        await call.answer()
        text = '✋ {member_name}, у нас запрещено использовать ссылки!'
        if db['settings'][index_of_chat]['block_resources']['warning'] != 'None': text = db['settings'][index_of_chat]['block_resources']['warning']
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nСообщение при нарушении:\n{text}', reply_markup=generate_block_resources_show(call.from_user.id, index_of_chat))
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda call: call.data == 'my_profile')
async def show_profile(call: CallbackQuery):
    try:
        db = collection.find_one({"user_id": call.from_user.id})
        lic = 'Лицензии нет'
        if db['lic'] != 'None': lic = db['lic']
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'👤 Ваш профиль:\n\n<b>Пользователь:</b> #{db["inlineid"]} - {db["register_data"]}\n<b>Username:</b> @{call.from_user.username}\n<b>Имя:</b> {call.from_user.first_name}\n<b>Чатов:</b> {len(db["chats"])}\n<b>Лицензий:</b> {db["lic"]}', reply_markup=generate_money_top_up())
        await call.answer()
    except Exception as e:
        print(e)



@dp.callback_query_handler(lambda call: call.data == 'back_to_my_profil')
async def back_to_my_profil_reaction(call: CallbackQuery):
    try:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        db = collection.find_one({"user_id": call.from_user.id})
        lic = 'Лицензии нет'
        if db['lic'] != 'None': lic = db['lic']
        await bot.send_message(chat_id=call.message.chat.id,
                                    text=f'👤 Ваш профиль:\n\n<b>Пользователь:</b> #{db["inlineid"]} - {db["register_data"]}\n<b>Username:</b> @{call.from_user.username}\n<b>Имя:</b> {call.from_user.first_name}\n<b>Чатов:</b> {len(db["chats"])}\n<b>Лицензий:</b> {db["lic"]}', reply_markup=generate_money_top_up())
        await call.answer()
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'back_to_main_page')
async def show_profile(call: CallbackQuery):
    try:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Здравствуйте! Я бот-админ и могу администрировать ваш групповой чат.\n\nДля того чтобы начать, добавьте меня в свой групповой чат:', reply_markup=generate_add_button())
        await call.answer()
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'show_my_chats')
async def show_my_chats(call: CallbackQuery):
    try:
        db = collection.find_one_and_update({"user_id": call.from_user.id}, {'$set': {"current_pg": 0}})
        if len(db['chats']) == 0:
            return await call.answer('У вас нет чатов :(', show_alert=True)

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='🛢️ Выберите чат для настройки:', reply_markup=await generate_my_chats(user_id=db["user_id"]))
        await call.answer()
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'next_page')
async def react_to_next_page(call: CallbackQuery):
    try:
        db = collection.find_one({"user_id": call.from_user.id})
        current_page = db['current_pg'] + 1
        collection.find_one_and_update({"user_id": call.from_user.id}, {'$set': {'current_pg': current_page}})

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='🛢️ Выберите чат для настройки:', reply_markup=await generate_my_chats(current_page=current_page, user_id=db["user_id"]))
        await call.answer()
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda call: call.data == 'prev_page')
async def react_to_prev_page(call: CallbackQuery):
    try:
        db = collection.find_one({"user_id": call.from_user.id})
        current_page = db['current_pg'] - 1
        collection.find_one_and_update({"user_id": call.from_user.id}, {'$set': {'current_pg': current_page}})

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='🛢️ Выберите чат для настройки:', reply_markup=await generate_my_chats(current_page=current_page, user_id=db["user_id"]))
        await call.answer()
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda call: 'schat' in call.data)
async def react_to_settings_chats(call: CallbackQuery):
    try:
        chat_id = call.data.split('_')[1]
        db = collection.find_one({'chats': chat_id})
        index_of_chat = get_dict_index(db, chat_id)
        if db['settings'][index_of_chat]['lic'] == True: return await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text={t_settings.format(group_id=chat_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))},
                         reply_markup=generate_settings(True))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=t_settings.format(group_id=chat_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"])),
                         reply_markup=generate_settings())
        await call.answer()
    except Exception as e:
        print(e)



@dp.callback_query_handler(lambda call: call.data == 'back_to_settings')
async def react_to_back_to_settings(call: CallbackQuery):
    group_id_url = call.message.entities[0].url
    group_id = "-" + re.sub(r"\D", "", group_id_url)
    db = collection.find_one({"chats": group_id})
    index_of_chat = get_dict_index(db, group_id)
    if db['settings'][index_of_chat]['lic'] == True: return await bot.edit_message_text(text=t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"])), message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=generate_settings(lic=True))
    await bot.edit_message_text(text=t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"])), message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=generate_settings())


@dp.callback_query_handler(lambda call: call.data == 'money_top_up')
async def react_to_money_top_up(call: CallbackQuery):
    try:
        db = collection.find_one({"user_id": call.from_user.id})
        if db['manual_msg'] == True or db['manual_s'] == True:
            if db['manual_s'] == True:
                return await call.answer('✋ Ваша заявка на проверке', show_alert=True)
            return await call.answer('❗ Вы не можете оплачивать лицензию одновременно с другой', show_alert=True)
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
        prices = ''
        unsortedp = db['price']
        positions = sorted(unsortedp, key=lambda x: int(x['period']))
        for i in positions:
            prices += f'💎 {i["period"]} дней – {i["price"]}₽\n'
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id,
                             text=f'<a href="https://{group_id}.id">🛒</a> <b>Прайс-лист лицензий:</b>\n{prices}', reply_markup=generate_payment_page())
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: 'buy' in call.data)
async def react_to_buy(call: CallbackQuery):
    try:
        db = collection.find_one({"user_id": call.from_user.id})
        if db['manual_msg'] == True or db['manual_s'] == True:
            if db['manual_s'] == True:
                await call.answer('✋ Ваша заявка на проверке', show_alert=True)
                return await react_to_back_to_settings(call)
            await call.answer('❗ Вы не можете оплачивать лицензию одновременно с другой',
                show_alert=True)
            return await react_to_back_to_settings(call)

        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        collection.find_one_and_update({"user_id": call.from_user.id}, {"$set": {"priceq": call.data.split('_')[1]}})
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<a href="https://{group_id}.id">💸</a> <b>Выберите способ оплаты:</b>', reply_markup=generate_payment_method())
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'lic_info')
async def answer_to_lic_info(call: CallbackQuery):
    group_id_url = call.message.entities[0].url
    group_id = "-" + re.sub(r"\D", "", group_id_url)
    db = collection.find_one({"chats": group_id})
    index_of_chat = get_dict_index(db, group_id)
    if db['settings'][index_of_chat]['lic'] == False:
        await call.answer('ℹ У вас нет лицензии на данный чат или срок действия лицензии окончен', show_alert=True)
        return await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=generate_settings())
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Информация о лицензии <a href="https://{group_id}.id">💎</a>:\n\n<b>Дата приобретения</b>: {db["settings"][index_of_chat]["lic_buyed_date"]}\n<b>Срок действия лицензии</b>: до {db["settings"][index_of_chat]["lic_end"][0]}\n<b>Приобретенный срок:</b> {db["settings"][index_of_chat]["lic_end"][2]} дней', reply_markup=generate_back_to_settings())

# ОПЛАТА

@dp.callback_query_handler(lambda call: 'pay' in call.data)
async def react_to_pay(call: CallbackQuery):
    try:
        db = collection.find_one({"user_id": call.from_user.id})
        if db['manual_msg'] == True or db['manual_s'] == True:
            if db['manual_s'] == True:
                await call.answer('✋ Ваша заявка на проверке', show_alert=True)
                await react_to_back_to_settings(call)
            await call.answer('❗ Вы не можете оплачивать лицензию одновременно с другой', show_alert=True)
            return await react_to_back_to_settings(call)
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        chat = await bot.get_chat(group_id)
        if call.data.split('_')[1] == 'yoomoney':
            return await call.answer('Тут будет оплата invoke')
            db = collection.find_one({"user_id": call.from_user.id})
            admindb = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
            priceindex = get_price_index(db['priceq'])
            amount = int(str(admindb['price'][priceindex]['price']).replace('.', '') + '0')
            product = LabeledPrice(label='Product', amount=amount)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.send_invoice(
                chat_id=call.message.chat.id,
                title=f'Лицензия на {db["priceq"]} дней | Л̶и̶м̶и̶т̶ы̶ ̶н̶а̶ ̶ч̶а̶т̶ - {chat.title}',
                description='Купив лицензию, вы сможете избавиться от лимитов на чат',
                payload=f"{db['priceq']}_{group_id}",
                provider_token=config['PROVIDER'],
                currency='RUB',
                prices=[product],
                start_parameter=call.from_user.id,
                is_flexible=False,
                protect_content=True,
                photo_url='https://cdn.discordapp.com/attachments/992866546596712638/1131264970206744656/lic.jpg'
            )
            await call.answer()
        else:
            # return await call.answer('Пока не доступно 😶')
            db = collection.find_one({"user_id": call.from_user.id})
            admindb = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
            priceindex = get_price_index(db['priceq'])
            amount = admindb['price'][priceindex]['price']
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            manual_comentidc = admindb['manual_comentid'] + 1
            await bot.send_message(call.message.chat.id, text=f'<a href="https://{group_id}.id">💳</a> Ручная оплата:\n\nПереведите <b>{amount}₽</b> на указанные реквизиты 👇\n\n<b>{config["TYPE"]}</b>\n<code>{config["CARD_NUMBER"]}</code>\n<b>{config["CARD_OWNER"]}</b>\n\n❗ В КОМЕНТАРИЯХ УКАЖИТЕ НОМЕР: #{manual_comentidc}\n\nПосле перевода нажмите на кнопку "Я перевел"', reply_markup=generate_manual_payment())
            collection.find_one_and_update({"_id": ObjectId('64987b1eeed9918b13b0e8b4')}, {"$set": {"manual_comentid": manual_comentidc}})
            collection.find_one_and_update({"user_id": call.from_user.id}, {"$set": {"manual_codeid": manual_comentidc, "manual_msg": True}})
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: 'manualp' in call.data)
async def answer_to_manualp(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        if call.data.split('_')[1] == 'back':
            db = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
            prices = ''
            unsortedp = db['price']
            positions = sorted(unsortedp, key=lambda x: int(x['period']))
            for i in positions:
                prices += f'💎 {i["period"]} дней – {i["price"]}₽\n'
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'(<a href="https://{group_id}.id">🛒</a>) <b>Прайс-лист лицензий:</b>\n{prices}',
                                        reply_markup=generate_payment_page())
            collection.find_one_and_update({"user_id": call.from_user.id}, {"$set": {"manual_msg": False}})
        else:
            db = collection.find_one_and_update({"user_id": call.from_user.id}, {"$set": {"manual_s": True}})
            adb = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
            priceindx = get_price_index(db['priceq'])
            await bot.send_message(chat_id=config['MAIN_ADMIN_ID'], text=f'💸 Новый запрос на проверку ручной оплаты:\n\nЛицензия для чата: <a href="https://{group_id}.id">{group_id}</a>\nСрок лицензии: {db["priceq"]} дней\nЦена лицензии: {adb["price"][priceindx]["price"]}₽\n\n<b>Код который должен быть в коментариях:</b> <code>#{db["manual_codeid"]}</code>\n\nПользователь: <a href="https://t.me/{call.from_user.username}">{call.from_user.first_name}</a>', disable_web_page_preview=True, disable_notification=False)
            await call.answer('Ваша заявка отправлена на проверку ✅')
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            index_of_chat = get_dict_index(db, group_id)
            if db['settings'][index_of_chat]['lic'] == True: return await bot.edit_message_text(
                text=t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"])),
                message_id=call.message.message_id, chat_id=call.message.chat.id,
                reply_markup=generate_settings(lic=True))
            await bot.send_message(text=t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"])),
                                        chat_id=call.message.chat.id,
                                        reply_markup=generate_settings())
    except Exception as e:
        print(e)

@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    trash = await bot.send_message(pre_checkout_query.from_user.id, '🔄️ Транскрипция...')
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message='Произошла ошибка при подтверждении транскрипции ⚠')
    await bot.delete_message(pre_checkout_query.from_user.id, trash.message_id)

@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def process_successful_payment(ctx: Message):
    db = collection.find_one({"user_id": ctx.from_user.id})
    index_of_chat = get_dict_index(db, ctx.successful_payment.invoice_payload.split('_')[1])
    adb = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
    liccount = db['lic'] + 1
    liccountgeneral = adb['lics_buyed'] + 1
    alics = adb['active_lic'] + 1
    earnup = float(str(ctx.successful_payment.total_amount)[:-2] + "." + str(ctx.successful_payment.total_amount)[-2:])
    earned = adb['earned'] + earnup
    enddate = calculate_end_date(int(ctx.successful_payment.invoice_payload.split('_')[0]))
    current_datetime = datetime.now(pytz.utc)
    moscow_tz = pytz.timezone('Europe/Moscow')
    current_datetime_moscow = current_datetime.astimezone(moscow_tz)
    formatted_datetime = current_datetime_moscow.strftime("%H:%M %d.%m.%Y")
    collection.find_one_and_update({"user_id": ctx.from_user.id}, {"$set": {"lic": liccount, f"settings.{index_of_chat}.lic": True, f"settings.{index_of_chat}.lic_end": [enddate[0], enddate[1], ctx.successful_payment.invoice_payload.split('_')[0]], f"settings.{index_of_chat}.lic_buyed_date": formatted_datetime}})
    collection.find_one_and_update({"_id": ObjectId('64987b1eeed9918b13b0e8b4')}, {"$set": {"lics_buyed": liccountgeneral, "earned": earned, "active_lic": alics}, "$push": {"chat_with_lics": ctx.successful_payment.invoice_payload.split('_')[1]}})
    await ctx.answer('😇 Свяжитесь с @GrSoul, если возникнут проблемы')
    await ctx.answer(text=f"Успешная оплата ✅\n\nИнформация о лицензии в настройках чата(<a href='https://{ctx.successful_payment.invoice_payload.split('_')[1]}.id'>{ctx.successful_payment.invoice_payload.split('_')[1]}</a>)", reply_markup=generate_back_to_settings())