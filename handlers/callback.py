# Обработчики нажатых, встроенных кнопок под сообщениями:
import asyncio

from data.loader import bot, dp, FSMContext, State
from database.database import collection, ObjectId
from states_scenes.scene import MySceneStates
from aiogram.types import CallbackQuery
from keyboards.inline_keyboards import generate_my_chats, generate_add_b_resources, generate_back_to_main, generate_system_notice_show, generate_add_button, generate_settings_button, generate_edit_text_settings, generate_settings, generate_text_editing_page, generate_rules_editing_page, generate_warning_editing_page, generate_afk_editing_page, generate_admins_settings, generate_block_repostes_show, generate_block_ping_show, generate_block_resources_show, generate_money_top_up
import re


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
                                                      '🤖 Здравствуйте! Я бот-админ и могу администрировать данный чат.\n\nДля того чтобы меня настроить, нажмите на кнопку настроить:',
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
        group_id = int("-" + re.sub(r"\D", "", group_id_url))
        await call.answer()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n\nВыберите текст, который хотите посмотреть:',
                                    reply_markup=generate_edit_text_settings())
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'back_to_chose')
async def react_to_back(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = int("-" + re.sub(r"\D", "", group_id_url))
        await call.answer()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)',
                                    reply_markup=generate_settings())
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'done_btn')
async def react_to_done(call: CallbackQuery):
    try:
        await call.answer()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'⚙ Настройки чата завершена')
        await asyncio.sleep(2)
        await bot.send_message(chat_id=call.message.chat.id, text='Здравствуйте! Я бот-админ и могу администрировать ваш групповой чат.\n\nДля того чтобы начать, добавьте меня в свой групповой чат:',
            reply_markup=generate_add_button())
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'texts_greeting')
async def text_greeting_show(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"chats": str(group_id)})

        index_of_chat = 0
        for index, item in enumerate(db['settings']):
            if item.get("chat_id") == group_id:
                index_of_chat = index
                break

        text = db["settings"][index_of_chat]['greeting']

        await call.answer()
        if text == 'None':
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n<b>Приветственное сообщение:</b>\n\nПриветствуем, <b>{str("{member_name}")}</b>!\n\nПрежде чем размещать свои объявления, пожалуйста, ознакомься с правилами. Они доступны по команде /rules',
                                        reply_markup=generate_text_editing_page())
        else:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n<b>Приветственное сообщение:</b>\n\n{text}',
                                        reply_markup=generate_text_editing_page())
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'show_rules')
async def text_rules_show(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"chats": str(group_id)})

        index_of_chat = 0
        for index, item in enumerate(db['settings']):
            if item.get("chat_id") == group_id:
                index_of_chat = index
                break

        text = db["settings"][index_of_chat]['rules']

        await call.answer()
        if text == 'None':
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n<b>Правила чата:</b>\n\n<i>Правила отсутствуют</i>',
                                        reply_markup=generate_rules_editing_page())
        else:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n<b>Правила чата:</b>\n\n{text}',
                                        reply_markup=generate_rules_editing_page())
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'show_warning')
async def text_warning_show(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"chats": str(group_id)})

        index_of_chat = 0
        for index, item in enumerate(db['settings']):
            if item.get("chat_id") == group_id:
                index_of_chat = index
                break

        text = db["settings"][index_of_chat]['warning']

        await call.answer()
        if text == 'None':
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n<b>Уведомление при нарушении:</b>\n\nВы нарушаете наши правила! Запрещены любые ссылки!',
                                        reply_markup=generate_warning_editing_page())
        else:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n<b>Уведомление при нарушении:</b>\n\n{text}',
                                        reply_markup=generate_warning_editing_page())
    except Exception as e:
        print(e)



@dp.callback_query_handler(lambda call: call.data == 'formating')
async def format_btn_react(call: CallbackQuery):
    try:
        await call.answer('💿 Для форматирования текста мы используем HTML форматирование и вы можете встроить HTML форматирование в ваш текст\n\nФичи:\n{member_name} - имя нового участника чата', show_alert=True)
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'show_afk')
async def text_afk_show(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"chats": str(group_id)})

        index_of_chat = 0
        for index, item in enumerate(db['settings']):
            if item.get("chat_id") == group_id:
                index_of_chat = index
                break

        text = db["settings"][index_of_chat]['afk']

        await call.answer()
        if text == 'None':
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n<b>Уведомление при неактивности чата:</b>\n\nАууу... Что-то актива нет',
                                        reply_markup=generate_afk_editing_page())
        else:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n<b>Уведомление при неактивности чата:</b>\n\n{text}',
                                        reply_markup=generate_afk_editing_page())
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'back_to_show_page')
async def react_to_back_to_show(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = int("-" + re.sub(r"\D", "", group_id_url))
        await call.answer()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n\nВыберите текст, который хотите посмотреть:',
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
        elif call_main == 'warning':
            await call.answer()
            await MySceneStates.warning_change_text_scene.set()
            await bot.send_message(call.message.chat.id, '📋 Введите текст, который будет уведомлять участников чата при нарушений:')
        elif call_main == 'afk':
            await call.answer()
            await MySceneStates.afk_change_text_scene.set()
            await bot.send_message(call.message.chat.id, '📋 Введите текст, который будет уведомлять чат при неактивности:')
        else:
            await call.answer()
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda call: call.data == 'settings_admins')
async def edit_admins_settings(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = int("-" + re.sub(r"\D", "", group_id_url))
        await call.answer()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n\nВыберите функцию:', reply_markup=generate_admins_settings())
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda call: call.data == 'back_to_admin_page')
async def back_to_admin_page(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = int("-" + re.sub(r"\D", "", group_id_url))
        await call.answer()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n\nВыберите функцию:', reply_markup=generate_admins_settings())
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda call: call.data == 'block_resources_show')
async def react_to_block_resources_show(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"user_id": call.from_user.id})

        index_of_chat = 0
        for index, item in enumerate(db['settings']):
            if item.get("chat_id") == group_id:
                index_of_chat = index
                break
        await call.answer()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n\nБлокировка ссылок на внешние ресурсы:', reply_markup=generate_block_resources_show(call.from_user.id, index_of_chat))
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'block_repostes_show')
async def react_to_block_repostes_show(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"user_id": call.from_user.id})

        index_of_chat = 0
        for index, item in enumerate(db['settings']):
            if item.get("chat_id") == group_id:
                index_of_chat = index
                break
        await call.answer()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n\nЗапрет репостов:', reply_markup=generate_block_repostes_show(call.from_user.id, index_of_chat))
    except Exception as e:
        print(e)\


@dp.callback_query_handler(lambda call: call.data == 'system_notice_show')
async def react_to_system_notice_show(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"user_id": call.from_user.id})

        index_of_chat = 0
        for index, item in enumerate(db['settings']):
            if item.get("chat_id") == group_id:
                index_of_chat = index
                break
        await call.answer()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n\nАвто-удаление системных оповещение о подключении к чату нового пользователя или при покиданий пользователя:', reply_markup=generate_system_notice_show(call.from_user.id, index_of_chat))
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'block_ping_show')
async def react_to_block_ping_show(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"user_id": call.from_user.id})

        index_of_chat = 0
        for index, item in enumerate(db['settings']):
            if item.get("chat_id") == group_id:
                index_of_chat = index
                break
        await call.answer()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n\nЗапрет пинга:', reply_markup=generate_block_ping_show(call.from_user.id, index_of_chat))
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: 'activator' in call.data)
async def react_to_activator(call: CallbackQuery):
    try:
        group_id_url = call.message.entities[0].url
        group_id = "-" + re.sub(r"\D", "", group_id_url)
        db = collection.find_one({"user_id": call.from_user.id})

        index_of_chat = 0
        for index, item in enumerate(db['settings']):
            if item.get("chat_id") == group_id:
                index_of_chat = index
                break

        call_data_identificator = call.data.split('_')[1]

        if call_data_identificator == 'resources':
            if db['settings'][index_of_chat]['block_resources']['active'] == False:
                collection.find_one_and_update({"user_id": call.from_user.id},
                                               {"$set": {f"settings.{index_of_chat}.block_resources.active": True}})
            else:
                collection.find_one_and_update({"user_id": call.from_user.id},
                                               {"$set": {f"settings.{index_of_chat}.block_resources.active": False}})
            await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                reply_markup=generate_block_resources_show(call.from_user.id, index_of_chat))
        elif call_data_identificator == 'repostes':
            if db['settings'][index_of_chat]['block_repostes']['active'] == False:
                collection.find_one_and_update({"user_id": call.from_user.id},
                                               {"$set": {f"settings.{index_of_chat}.block_repostes.active": True}})
            else:
                collection.find_one_and_update({"user_id": call.from_user.id},
                                               {"$set": {f"settings.{index_of_chat}.block_repostes.active": False}})
            await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                reply_markup=generate_block_repostes_show(call.from_user.id, index_of_chat))
        elif call_data_identificator == "sysnot":
            if db['settings'][index_of_chat]['system_notice']['active'] == False:
                collection.find_one_and_update({"user_id": call.from_user.id},
                                               {"$set": {f"settings.{index_of_chat}.system_notice.active": True}})
            else:
                collection.find_one_and_update({"user_id": call.from_user.id},
                                               {"$set": {f"settings.{index_of_chat}.system_notice.active": False}})
            await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                reply_markup=generate_system_notice_show(call.from_user.id, index_of_chat))
        else:
            if db['settings'][index_of_chat]['block_ping']['active'] == False:
                collection.find_one_and_update({"user_id": call.from_user.id},
                                               {"$set": {f"settings.{index_of_chat}.block_ping.active": True}})
            else:
                collection.find_one_and_update({"user_id": call.from_user.id},
                                               {"$set": {f"settings.{index_of_chat}.block_ping.active": False}})
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

        index_of_chat = 0
        for index, item in enumerate(db['settings']):
            if item.get("chat_id") == group_id:
                index_of_chat = index
                break

        await call.answer()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n\nЗапрещенные расширения доменных имен:\n\n<b>{", ".join(db["settings"][index_of_chat]["block_resources"]["r_list"])}</b>',
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

        index_of_chat = 0
        for index, item in enumerate(db['settings']):
            if item.get("chat_id") == group_id:
                index_of_chat = index
                break

        await call.answer()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'⚙ Настройки чата (<a href="https://{group_id}.id">{group_id}</a>)\n\nБлокировка ссылок на внешние ресурсы:', reply_markup=generate_block_resources_show(call.from_user.id, index_of_chat))
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
            await call.answer('У вас нет чатов :(', show_alert=True)

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
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'⚙ Настройки чата (<a href="https://{chat_id}.id">{chat_id}</a>):',
                         reply_markup=generate_settings())
        await call.answer()
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda call: call.data == 'money_top_up')
async def react_to_money_top_up(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Прайс-лист:\n30 дней - 30р\n90 дней - 90р\n180 дней - 180р\n365 дней - 350р')
