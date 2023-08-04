# Обработчики нажатых, встроенных кнопок под сообщениями:
import asyncio
import pytz
import re
from data.loader import bot, dp, FSMContext, State, config
from database.database import collection, ObjectId
from states_scenes.scene import MySceneStates
from aiogram.types import CallbackQuery, ContentTypes, LabeledPrice, PreCheckoutQuery, Message
from aiogram.utils.exceptions import ChatNotFound
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
                if me.user.username == t_bot_user:
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
        db = collection.find_one({"user_id": call.from_user.id})
        if len(db['chats']) >= 1:
            lic = 'Лицензии нет'
            if db['lic'] != 'None': lic = db['lic']
            await bot.send_message(chat_id=call.message.chat.id, text=f'👤 Ваш профиль:\n\n<b>Пользователь:</b> #{db["inlineid"]} - {db["register_data"]}\n<b>Username:</b> @{call.from_user.username}\n<b>Имя:</b> {call.from_user.first_name}\n<b>Чатов:</b> {len(db["chats"])}\n<b>Лицензий:</b> {db["lic"]}',
                                        reply_markup=generate_add_button())
        else:
            await bot.send_message(chat_id=call.message.chat.id,
                                        text=t_start_text.format(bot_user=t_bot_user),
                                        reply_markup=generate_add_button())
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'texts_greeting')
async def text_greeting_show(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"chats": str(group_id)})

        index_of_chat = get_dict_index(db, group_id)

        text = 'Приветствуем, <b>{str("{member_name}")}</b>!\n\nПрежде чем размещать свои объявления, пожалуйста, ознакомься с правилами. Они доступны по команде /rules'

        await call.answer()
        if db["settings"][index_of_chat]['greeting'] != 'None': text = db["settings"][index_of_chat]['greeting']
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\n<b>Приветственное сообщение:</b>\n{text}',
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

        text = '<i>Правила отсутствуют</i>'

        await call.answer()
        if db["settings"][index_of_chat]['rules'] != 'None': text = db["settings"][index_of_chat]['rules']

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\n<b>Правила чата:</b>\n{text}',
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
        if call_main == 'greeting':
            await call.answer()
            await MySceneStates.greeting_change_text_scene.set()
            quatback = await bot.send_message(call.message.chat.id, '📋 Введите текст для приветствия новых участников чата:', reply_markup=generate_back_gretedittext())
        elif call_main == 'rules':
            await call.answer()
            await MySceneStates.rules_change_text_scene.set()
            quatback = await bot.send_message(call.message.chat.id, '📋 Введите текст правил чата:', reply_markup=generate_back_ruledittext())
        elif call_main == 'banwarning':
            await call.answer()
            await MySceneStates.banwarning_change_text_scene.set()
            quatback = await bot.send_message(call.message.chat.id, '📋 Введите текст, который будет отправлен после использования команды ban:', reply_markup=generate_back_banedittext())
        elif call_main == 'kickwarning':
            await call.answer()
            await MySceneStates.kickwarning_change_text_scene.set()
            quatback = await bot.send_message(call.message.chat.id, '📋 Введите текст, который будет отправлен после использования команды kick:', reply_markup=generate_back_kickedittext())
        elif call_main == 'unbantext':
            await call.answer()
            await MySceneStates.unbantext_change_text_scene.set()
            quatback = await bot.send_message(call.message.chat.id, '📋 Введите текст, который будет отправлен после использования команды unban:', reply_markup=generate_back_unbanedittext())
        elif call_main == 'afkw':
            await call.answer()
            await MySceneStates.afk_change_text_scene.set()
            quatback = await bot.send_message(call.message.chat.id, '📋 Введите текст, который будет уведомлять чат при неактивности:', reply_markup=generate_back_afkedittext())
        elif call_main == 'resourcesw':
            await call.answer()
            await MySceneStates.resourcesw_change_scene.set()
            quatback = await bot.send_message(call.message.chat.id, '📋 Введить новый текст предупреждения о нарушении:', reply_markup=generate_back_resedittext())
        elif call_main == 'repostesw':
            await call.answer()
            await MySceneStates.repostesw_change_scene.set()
            quatback = await bot.send_message(call.message.chat.id, '📋 Введить новый текст предупреждения о нарушении:', reply_markup=generate_back_repedittext())
        elif call_main == 'pingw':
            await call.answer()
            await MySceneStates.pingw_change_scene.set()
            quatback = await bot.send_message(call.message.chat.id, '📋 Введить новый текст предупреждения о нарушении:', reply_markup=generate_back_pingedittext())
        else:
            return await call.answer()
        collection.find_one_and_update({"user_id": call.from_user.id}, {"$set": {"chat_editing": group_id, "quatback": quatback.message_id}})
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda call: call.data == 'eback_resedittext', state=MySceneStates.resourcesw_change_scene)
async def answer_to_eback_resedittext(call: CallbackQuery, state: FSMContext):
    await state.finish()
    db = collection.find_one({"user_id": call.from_user.id})
    group_id = db['chat_editing']
    index_of_chat = get_dict_index(db, group_id)
    await call.answer()
    text = t_default_res
    if db['settings'][index_of_chat]['block_resources']['warning'] != 'None': text = db['settings'][index_of_chat]['block_resources']['warning']
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\n<b>Сообщение при нарушении:</b>\n{text}',
                                reply_markup=generate_block_resources_show(call.from_user.id, index_of_chat))

@dp.callback_query_handler(lambda call: call.data == 'eback_repedittext', state=MySceneStates.repostesw_change_scene)
async def answer_to_eback_repedittext(call: CallbackQuery, state: FSMContext):
    await state.finish()
    db = collection.find_one({"user_id": call.from_user.id})
    group_id = db['chat_editing']
    index_of_chat = get_dict_index(db, group_id)
    await call.answer()
    text = t_default_rep
    if db['settings'][index_of_chat]['block_repostes']['warning'] != 'None': text = db['settings'][index_of_chat]['block_repostes']['warning']
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\n<b>Сообщение при нарушении:</b>\n{text}',
                                reply_markup=generate_block_repostes_show(call.from_user.id, index_of_chat))

@dp.callback_query_handler(lambda call: call.data == 'eback_pingedittext', state=MySceneStates.pingw_change_scene)
async def answer_to_eback_pingedittext(call: CallbackQuery, state: FSMContext):
    await state.finish()
    db = collection.find_one({"user_id": call.from_user.id})
    group_id = db['chat_editing']
    index_of_chat = get_dict_index(db, group_id)
    await call.answer()
    text = t_default_ping
    if db['settings'][index_of_chat]['block_ping']['warning'] != 'None': text = db['settings'][index_of_chat]['block_ping']['warning']
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\n<b>Сообщение при нарушении:</b>\n{text}',
                                reply_markup=generate_block_ping_show(call.from_user.id, index_of_chat))

@dp.callback_query_handler(lambda call: call.data == 'eback_addblock', state=MySceneStates.blocked_resources_add)
async def answer_to_eback_addblock(call: CallbackQuery, state: FSMContext):
    await state.finish()
    db = collection.find_one({"user_id": call.from_user.id})
    group_id = db['chat_editing']
    index_of_chat = get_dict_index(db, group_id)
    await call.answer()
    blocked_reses = ", ".join(db["settings"][index_of_chat]["block_resources"]["r_list"])
    if len(db["settings"][index_of_chat]["block_resources"]["r_list"]) == 0: blocked_reses = 'Нету'
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nЗаблокированные ресурсы:\n<b>{blocked_reses}</b>',
                                reply_markup=generate_add_b_resources())

@dp.callback_query_handler(lambda call: call.data == 'eback_remblock', state=MySceneStates.blocked_resources_remove)
async def answer_to_eback_remblock(call: CallbackQuery, state: FSMContext):
    await state.finish()
    db = collection.find_one({"user_id": call.from_user.id})
    group_id = db['chat_editing']
    index_of_chat = get_dict_index(db, group_id)
    await call.answer()
    blocked_reses = ", ".join(db["settings"][index_of_chat]["block_resources"]["r_list"])
    if len(db["settings"][index_of_chat]["block_resources"]["r_list"]) == 0: blocked_reses = 'Нету'
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nЗаблокированные ресурсы:\n<b>{blocked_reses}</b>',
                                reply_markup=generate_add_b_resources())

@dp.callback_query_handler(lambda call: call.data == 'eback_gretedittext', state=MySceneStates.greeting_change_text_scene)
async def answer_to_eback_gretedittext(call: CallbackQuery, state: FSMContext):
    await state.finish()
    db = collection.find_one({"user_id": call.from_user.id})
    group_id = db['chat_editing']
    index_of_chat = get_dict_index(db, group_id)
    await call.answer()
    text = 'Приветствуем, <b>{str("{member_name}")}</b>!\n\nПрежде чем размещать свои объявления, пожалуйста, ознакомься с правилами. Они доступны по команде /rules'
    if db["settings"][index_of_chat]['greeting'] != 'None': text = db["settings"][index_of_chat]['greeting']
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\n<b>Приветственное сообщение:</b>\n{text}',
                                reply_markup=generate_text_editing_page())


@dp.callback_query_handler(lambda call: call.data == 'eback_ruledittext', state=MySceneStates.rules_change_text_scene)
async def answer_to_eback_ruledittext(call: CallbackQuery, state: FSMContext):
    await state.finish()
    db = collection.find_one({"user_id": call.from_user.id})
    group_id = db['chat_editing']
    index_of_chat = get_dict_index(db, group_id)
    await call.answer()
    text = '<i>Правила отсутствуют</i>'
    if db["settings"][index_of_chat]['rules'] != 'None': text = db["settings"][index_of_chat]['rules']
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\n<b>Правила чата:</b>\n{text}',
                                reply_markup=generate_rules_editing_page())

@dp.callback_query_handler(lambda call: call.data == 'eback_afkedittext', state=MySceneStates.afk_change_text_scene)
async def answer_to_eback_afkedittext(call: CallbackQuery, state: FSMContext):
    await state.finish()
    db = collection.find_one({"user_id": call.from_user.id})
    group_id = db['chat_editing']
    index_of_chat = get_dict_index(db, group_id)
    text = f'Текст сообщения отсутствует 🤷‍♂'
    if db['settings'][index_of_chat]['afk']['warning'] != 'None': text = db['settings'][index_of_chat]['afk']['warning']
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\n<b>Функция "Ворчун":</b>\nЕсли в чате никто не пишет минут, то выводит сообщение:\n{text}',
                                reply_markup=generate_block_afk_show(db['user_id'], index_of_chat))

@dp.callback_query_handler(lambda call: call.data == 'eback_banedittext', state=MySceneStates.banwarning_change_text_scene)
@dp.callback_query_handler(lambda call: call.data == 'eback_kickedittext', state=MySceneStates.kickwarning_change_text_scene)
@dp.callback_query_handler(lambda call: call.data == 'eback_unbanedittext', state=MySceneStates.unbantext_change_text_scene)
async def answer_to_eback_patrul(call: CallbackQuery, state: FSMContext):
    await state.finish()
    db = collection.find_one({"user_id": call.from_user.id})
    group_id = db['chat_editing']
    index_of_chat = get_dict_index(db, group_id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n<b>Сообщения о бане | кике | разбане\nНажмите на одну из кнопок, чтобы изменить сообщение о:</b>\n\n<b>BAN:</b>\n{db["settings"][index_of_chat]["warning_ban"]}\n\n<b>KICK:</b>\n{db["settings"][index_of_chat]["warning_kick"]}\n\n<b>UNBAN:</b>\n{db["settings"][index_of_chat]["unban_text"]}',
                                reply_markup=generate_warning_editing_page())

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
        text = t_default_res
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
        text = t_default_rep
        if db['settings'][index_of_chat]['block_repostes']['warning'] != 'None': text = db['settings'][index_of_chat]['block_repostes']['warning']
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\n<b>Сообщение при нарушении:</b>\n{text}', reply_markup=generate_block_repostes_show(call.from_user.id, index_of_chat))
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
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nСкрытие системные оповещения о входе и выходе пользователей.', reply_markup=generate_system_notice_show(call.from_user.id, index_of_chat))
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
        text = t_default_ping
        if db['settings'][index_of_chat]['block_ping']['warning'] != 'None': text = db['settings'][index_of_chat]['block_ping']['warning']
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\n<b>Сообщение при нарушении:</b>\n{text}', reply_markup=generate_block_ping_show(call.from_user.id, index_of_chat))
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
        elif call_data_identificator == "afk":
            if db['settings'][index_of_chat]['afk']['active'] == False:
                collection.find_one_and_update({"user_id": call.from_user.id},
                                               {"$set": {f"settings.{index_of_chat}.afk.active": True, f"settings.{index_of_chat}.updated_date": get_msk_unix(), f"settings.{index_of_chat}.bot_send_afk": False}})
            else:
                collection.find_one_and_update({"user_id": call.from_user.id},
                                               {"$set": {f"settings.{index_of_chat}.afk.active": False, f"settings.{index_of_chat}.updated_date": get_msk_unix(), f"settings.{index_of_chat}.bot_send_afk": False}})
            await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                reply_markup=generate_block_afk_show(call.from_user.id, index_of_chat))
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
        blocked_reses = ", ".join(db["settings"][index_of_chat]["block_resources"]["r_list"])
        if len(db["settings"][index_of_chat]["block_resources"]["r_list"]) == 0: blocked_reses = 'Нету'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nЗаблокированные ресурсы:\n<b>{blocked_reses}</b>',
                                    reply_markup=generate_add_b_resources())
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda call: call.data == 'vorchun_show')
async def answer_to_vorchun_show(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"chats": group_id})
        index_of_chat = get_dict_index(db, group_id)
        text = f'Текст сообщения отсутствует 🤷‍♂'
        if db['settings'][index_of_chat]['afk']['warning'] != 'None': text = db['settings'][index_of_chat]['afk']['warning']
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\n<b>Функция "Ворчун":</b>\nЕсли в чате никто не пишет минут, то выводит сообщение:\n{text}', reply_markup=generate_block_afk_show(db['user_id'], index_of_chat))
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'add_block_resources')
async def react_to_add_block_resources(call: CallbackQuery):
    group_id_url = call.message.entities[0].url
    group_id = int("-" + re.sub(r"\D", "", group_id_url))
    db = collection.find_one({"user_id": call.from_user.id})
    index_of_chat = get_dict_index(db, group_id)
    blocks_list = 'Нету'
    if len(db["settings"][index_of_chat]['block_resources']['r_list']) != 0: blocks_list = ', '.join(db["settings"][index_of_chat]['block_resources']['r_list'])
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    quatback = await bot.send_message(call.message.chat.id, f'📋 Введите доменные расширения, которые хотите заблокировать через запятую\n\nПример 1: ru\nПример 2: ru, com, io\n\n<b>Ваш список запретов:</b> {blocks_list}', reply_markup=generate_back_addblock())
    collection.find_one_and_update({"user_id": call.from_user.id}, {"$set": {"chat_editing": group_id, "quatback": quatback.message_id}})
    await MySceneStates.blocked_resources_add.set()

@dp.callback_query_handler(lambda call: call.data == 'remove_block_resources')
async def react_to_add_block_resources(call: CallbackQuery):
    group_id_url = call.message.entities[0].url
    group_id = int("-" + re.sub(r"\D", "", group_id_url))
    db = collection.find_one({"user_id": call.from_user.id})
    index_of_chat = get_dict_index(db, group_id)
    blocks_list = 'Нету'
    if len(db["settings"][index_of_chat]['block_resources']['r_list']) == 0:
        return await call.answer('✋ У вас нет запретов в вашем списке, которых можно удалить!', show_alert=True)
    else:
        blocks_list = ', '.join(db["settings"][index_of_chat]['block_resources']['r_list'])
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    quatback = await bot.send_message(call.message.chat.id, f'📋 Введите доменные расширения, которые хотите удалить из заблокированных через запятую\n\nПример 1: ru\nПример 2: ru, com, io\n\n<b>Ваш список запретов:</b> {blocks_list}', reply_markup=generate_back_remblock())
    collection.find_one_and_update({"user_id": call.from_user.id}, {"$set": {"chat_editing": group_id, "quatback": quatback.message_id}})
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

# СТАРЫЕ ПУНКТЫ

@dp.callback_query_handler(lambda call: call.data == 'back_to_my_profil')
@dp.callback_query_handler(lambda call: call.data == 'my_profile')
async def show_profile(call: CallbackQuery):
    try:
        await show_start(call)
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'back_to_main_page')
async def show_start(call: CallbackQuery):
    try:
        db = collection.find_one({"user_id": call.from_user.id})
        if len(db['chats']) >= 1:
            lic = 'Лицензии нет'
            if db['lic'] != 'None': lic = db['lic']
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'👤 Ваш профиль:\n\n<b>Пользователь:</b> #{db["inlineid"]} - {db["register_data"]}\n<b>Username:</b> @{call.from_user.username}\n<b>Имя:</b> {call.from_user.first_name}\n<b>Чатов:</b> {len(db["chats"])}\n<b>Лицензий:</b> {db["lic"]}',
                reply_markup=generate_add_button())
        else:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=t_start_text.format(bot_user=t_bot_user),
                reply_markup=generate_add_button())
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'chat_users_info')
async def answer_to_chat_users_info(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"chats": group_id})
        index_of_chat = get_dict_index(db, group_id)
        deleted_acc = 0
        with_sym = 0
        nonactive_7 = 0
        nonactive_14 = 0
        nonactive_30 = 0
        nonactive_60 = 0
        for user in db['settings'][index_of_chat]['users']:
            try:
                user_info = await bot.get_chat(user['id'])
                if contains_external_links(user_info.first_name, db['settings'][index_of_chat]['blocked_syms']) == True or contains_external_links(user_info.last_name, db['settings'][index_of_chat]['blocked_syms']) == True:
                    with_sym += 1
            except ChatNotFound:
                deleted_acc += 1
                return
            if days_since_unix_time(user['l_msg']) > 60:
                nonactive_60 += 1
            elif days_since_unix_time(user['l_msg']) > 30 and days_since_unix_time(user['l_msg']) < 60:
                nonactive_30 += 1
            elif days_since_unix_time(user['l_msg']) > 14 and days_since_unix_time(user['l_msg']) < 30:
                nonactive_14 += 1
            elif days_since_unix_time(user['l_msg']) > 7 and days_since_unix_time(user['l_msg']) < 14:
                nonactive_7 += 1
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\n<b>Статистика участников чата:</b>\n<b>Удаленныйх акаунтов:</b> {deleted_acc} участников\n<b>Участники с фильт-символами:</b> {with_sym} участников\n\n<b>Категории не активности:</b>\n<b>Не активны более 7 дней:</b> {nonactive_7} участников\n<b>Не активны более 14 дней:</b> {nonactive_14} участников\n<b>Не активны более 30 дней:</b> {nonactive_30} участников\n<b>Не активны более 60 дней:</b> {nonactive_60} участников\n', reply_markup=generaate_users_toda_actions())
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'back_from_deletion')
async def answer_to_back_from_deletion(call: CallbackQuery):
    try:
        await answer_to_chat_users_info(call)
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'back_from_cat_chose')
async def answer_to_back_from_cat_chose(call: CallbackQuery):
    try:
        await answer_to_chat_users_info(call)
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: 'category' in call.data)
async def answer_to_catgory(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"chats": group_id})
        index_of_chat = get_dict_index(db, group_id)
        data = call.data.split('_')[1]
        if data == 'deleted':
            collection.find_one_and_update({"chats": group_id}, {"$set": {"category": 'deleted'}})
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nВыберите % удаления:', reply_markup=generaate_delete_percent())
        elif data == 'symbol':
            collection.find_one_and_update({"chats": group_id}, {"$set": {"category": 'symbol'}})
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nВыберите % удаления:', reply_markup=generaate_delete_percent())
        elif data == '7':
            collection.find_one_and_update({"chats": group_id}, {"$set": {"category": '7'}})
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nВыберите % удаления:', reply_markup=generaate_delete_percent())
        elif data == '14':
            collection.find_one_and_update({"chats": group_id}, {"$set": {"category": '14'}})
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nВыберите % удаления:', reply_markup=generaate_delete_percent())
        elif data == '30':
            collection.find_one_and_update({"chats": group_id}, {"$set": {"category": '30'}})
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nВыберите % удаления:', reply_markup=generaate_delete_percent())
        elif data == '60':
            collection.find_one_and_update({"chats": group_id}, {"$set": {"category": '60'}})
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nВыберите % удаления:', reply_markup=generaate_delete_percent())
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: 'catdelete' in call.data)
async def answer_to_catdelete_percentage(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"chats": group_id})
        index_of_chat = get_dict_index(db, group_id)
        data = call.data.split('_')[1]
        users_syms = []
        users_deleted = []
        users_7 = []
        users_14 = []
        users_30 = []
        users_60 = []

        msg = await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nИдет удаление...')
        for user in db['settings'][index_of_chat]['users']:
            try:
                user_info = await bot.get_chat(user['id'])
                if contains_external_links(user_info.first_name, db['settings'][index_of_chat]['blocked_syms']) == True or contains_external_links(user_info.last_name, db['settings'][index_of_chat]['blocked_syms']) == True:
                    users_syms.append(user['id'])
            except ChatNotFound:
                users_deleted.append(user['id'])
                return
            if days_since_unix_time(user['l_msg']) > 60:
                users_60.append(user['id'])
            elif days_since_unix_time(user['l_msg']) > 30 and days_since_unix_time(user['l_msg']) < 60:
                users_30.append(user['id'])
            elif days_since_unix_time(user['l_msg']) > 14 and days_since_unix_time(user['l_msg']) < 30:
                users_14.append(user['id'])
            elif days_since_unix_time(user['l_msg']) > 7 and days_since_unix_time(user['l_msg']) < 14:
                users_7.append(user['id'])

        if db['category'] == 'deleted':
            if len(users_deleted) == 0: return await bot.edit_message_text(chat_id=call.message.chat.id,
                                                                     message_id=msg.message_id,
                                                                     text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nУдалены <b>0</b> участников чата ✅', reply_markup=generaate_back_from_deletion())
            count_to_delete = (int(data) * len(users_deleted)) // 100
            arr_with_users = trim_array(users_deleted, count_to_delete)
            for i in arr_with_users:
                try:
                    await bot.kick_chat_member(chat_id=group_id, user_id=i)
                    await bot.unban_chat_member(chat_id=group_id, user_id=i)
                    index_of_user = get_chat_user_dict_index(db, i, index_of_chat)
                    collection.find_one_and_update({'chats': group_id},
                                                   {"$pull": {f'settings.{index_of_chat}.users.{index_of_user}.id': i}})
                except Exception as e:
                    print(e)
            return await bot.edit_message_text(chat_id=call.message.chat.id,
                                         message_id=msg.message_id,
                                         text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nУдалены <b>{len(arr_with_users)}</b> участников чата ✅', reply_markup=generaate_back_from_deletion())
        elif db['category'] == 'symbol':
            if len(users_syms) == 0: return await bot.edit_message_text(chat_id=call.message.chat.id,
                                                                     message_id=msg.message_id,
                                                                     text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nУдалены <b>0</b> участников чата ✅', reply_markup=generaate_back_from_deletion())
            count_to_delete = (int(data) * len(users_syms)) // 100
            arr_with_users = trim_array(users_syms, count_to_delete)
            for i in arr_with_users:
                try:
                    await bot.kick_chat_member(chat_id=group_id, user_id=i)
                    await bot.unban_chat_member(chat_id=group_id, user_id=i)
                    index_of_user = get_chat_user_dict_index(db, i, index_of_chat)
                    collection.find_one_and_update({'chats': group_id},
                                                   {"$pull": {f'settings.{index_of_chat}.users.{index_of_user}.id': i}})
                except Exception as e:
                    print(e)
            return await bot.edit_message_text(chat_id=call.message.chat.id,
                                         message_id=msg.message_id,
                                         text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nУдалены <b>{len(arr_with_users)}</b> участников чата ✅',
                                         reply_markup=generaate_back_from_deletion())
        elif db['category'] == '7':
            if len(users_7) == 0: return await bot.edit_message_text(chat_id=call.message.chat.id,
                                                                     message_id=msg.message_id,
                                                                     text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nУдалены <b>0</b> участников чата ✅', reply_markup=generaate_back_from_deletion())
            count_to_delete = (int(data) * len(users_7)) // 100
            arr_with_users = trim_array(users_7, count_to_delete)
            for i in arr_with_users:
                try:
                    await bot.kick_chat_member(chat_id=group_id, user_id=i)
                    await bot.unban_chat_member(chat_id=group_id, user_id=i)
                    index_of_user = get_chat_user_dict_index(db, i, index_of_chat)
                    collection.find_one_and_update({'chats': group_id},
                                                   {"$pull": {f'settings.{index_of_chat}.users.{index_of_user}.id': i}})
                except Exception as e:
                    print(e)
            return await bot.edit_message_text(chat_id=call.message.chat.id,
                                         message_id=msg.message_id,
                                         text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nУдалены <b>{len(arr_with_users)}</b> участников чата ✅',
                                         reply_markup=generaate_back_from_deletion())
        elif db['category'] == '14':
            if len(users_14) == 0: return await bot.edit_message_text(chat_id=call.message.chat.id,
                                                                     message_id=msg.message_id,
                                                                     text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nУдалены <b>0</b> участников чата ✅', reply_markup=generaate_back_from_deletion())
            count_to_delete = (int(data) * len(users_14)) // 100
            arr_with_users = trim_array(users_14, count_to_delete)
            for i in arr_with_users:
                try:
                    await bot.kick_chat_member(chat_id=group_id, user_id=i)
                    await bot.unban_chat_member(chat_id=group_id, user_id=i)
                    index_of_user = get_chat_user_dict_index(db, i, index_of_chat)
                    collection.find_one_and_update({'chats': group_id},
                                                   {"$pull": {f'settings.{index_of_chat}.users.{index_of_user}.id': i}})
                except Exception as e:
                    print(e)
            return await bot.edit_message_text(chat_id=call.message.chat.id,
                                         message_id=msg.message_id,
                                         text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nУдалены <b>{len(arr_with_users)}</b> участников чата ✅',
                                         reply_markup=generaate_back_from_deletion())
        elif db['category'] == '30':
            if len(users_30) == 0: return await bot.edit_message_text(chat_id=call.message.chat.id,
                                                                     message_id=msg.message_id,
                                                                     text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nУдалены <b>0</b> участников чата ✅', reply_markup=generaate_back_from_deletion())
            count_to_delete = (int(data) * len(users_30)) // 100
            arr_with_users = trim_array(users_30, count_to_delete)
            for i in arr_with_users:
                try:
                    await bot.kick_chat_member(chat_id=group_id, user_id=i)
                    await bot.unban_chat_member(chat_id=group_id, user_id=i)
                    index_of_user = get_chat_user_dict_index(db, i, index_of_chat)
                    collection.find_one_and_update({'chats': group_id},
                                                   {"$pull": {f'settings.{index_of_chat}.users.{index_of_user}.id': i}})
                except Exception as e:
                    print(e)
            return await bot.edit_message_text(chat_id=call.message.chat.id,
                                         message_id=msg.message_id,
                                         text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nУдалены <b>{len(arr_with_users)}</b> участников чата ✅',
                                         reply_markup=generaate_back_from_deletion())
        elif db['category'] == '60':
            if len(users_60) == 0: return await bot.edit_message_text(chat_id=call.message.chat.id,
                                                                     message_id=msg.message_id,
                                                                     text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nУдалены <b>0</b> участников чата ✅', reply_markup=generaate_back_from_deletion())
            count_to_delete = (int(data) * len(users_60)) // 100
            arr_with_users = trim_array(users_60, count_to_delete)
            for i in arr_with_users:
                try:
                    await bot.kick_chat_member(chat_id=group_id, user_id=i)
                    await bot.unban_chat_member(chat_id=group_id, user_id=i)
                    index_of_user = get_chat_user_dict_index(db, i, index_of_chat)
                    collection.find_one_and_update({'chats': group_id}, {"$pull": {f'settings.{index_of_chat}.users.{index_of_user}.id': i}})
                except Exception as e:
                    print(e)

            return await bot.edit_message_text(chat_id=call.message.chat.id,
                                         message_id=msg.message_id,
                                         text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\nУдалены <b>{len(arr_with_users)}</b> участников чата ✅',
                                         reply_markup=generaate_back_from_deletion())
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'back_from_percent')
async def answer_to_back_from_percent(call: CallbackQuery):
    try:
        await answer_to_delete_users_from_cat(call)
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'delete_users_from_cat')
async def answer_to_delete_users_from_cat(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"chats": group_id})
        index_of_chat = get_dict_index(db, group_id)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{t_settings.format(group_id=group_id, bot_user=t_bot_user, upd_time=update_time(db["settings"][index_of_chat]["updated_date"]))}\n\n<b>Выберите категорию с которой хотите удалить участников:</b>', reply_markup=generaate_users_toda_categories())
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
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<a href="https://{group_id}.id">🛒</a> <b>Прайс-лист лицензий:</b>\n{prices}', reply_markup=generate_payment_page())
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