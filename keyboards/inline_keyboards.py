# Встроенные кнопки под сообщения:
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.database import collection, ObjectId
from data.loader import bot

def generate_add_button():
    markup = InlineKeyboardMarkup()
    add_bottogroup_btn = InlineKeyboardButton('➕ Добавить бота в свой чат', url='https://t.me/shieldsword_bot?startgroup=true')
    my_profile_btn = InlineKeyboardButton('👤 Мой профиль', callback_data='my_profile')
    my_groups_btn = InlineKeyboardButton('🗃️ Мои чаты', callback_data='show_my_chats')
    markup.add(add_bottogroup_btn)
    markup.add(my_profile_btn)
    markup.add(my_groups_btn)
    return markup

def generate_mychats_button():
    markup = InlineKeyboardMarkup()
    my_groups_btn = InlineKeyboardButton('🗃️ Мои чаты', callback_data='show_my_chats')
    markup.add(my_groups_btn)
    return markup


def generate_settings_button(chat_id):
    markup = InlineKeyboardMarkup()
    settings_btn = InlineKeyboardButton('⚙ Настроить бота', url=f'https://t.me/shieldsword_bot?start=settings_{chat_id}')
    markup.add(settings_btn)
    return markup

def generate_check_admin_rights():
    markup = InlineKeyboardMarkup()
    check_btn = InlineKeyboardButton('📃 Проверить права', callback_data='check_admingr')
    markup.add(check_btn)
    return markup

def generate_rules_keyboard():
    markup = InlineKeyboardMarkup()
    rules_btn = InlineKeyboardButton('🪧 Правила чата', callback_data='rules')
    markup.add(rules_btn)
    return markup

def generate_settings(lic=False):
    markup = InlineKeyboardMarkup()
    edit_texts_btn = InlineKeyboardButton('✍ Изменение текста', callback_data='settings_texts')
    edit_admin_btn = InlineKeyboardButton('🧑‍⚖ Настройки администрирования', callback_data='settings_admins')
    buy_lic_btn = InlineKeyboardButton('💎 Купить лицензию', callback_data='money_top_up')
    lic_info_btn = InlineKeyboardButton('ℹ Информация о лицензии', callback_data='lic_info')
    done_btn = InlineKeyboardButton('✅ Готово', callback_data='done_btn')
    markup.add(edit_admin_btn)
    markup.add(edit_texts_btn)
    if lic == False: markup.add(buy_lic_btn)
    else: markup.add(lic_info_btn)
    markup.add(done_btn)
    return markup

def generate_edit_text_settings():
    markup = InlineKeyboardMarkup()
    texts_greeting_btn = InlineKeyboardButton('👋 Приветствие нового участника', callback_data='texts_greeting')
    show_rules = InlineKeyboardButton('🪧 Правила чата', callback_data='show_rules')
    warning_btn = InlineKeyboardButton('👮 Патруль', callback_data='show_warning')
    # afk_btn = InlineKeyboardButton('🔇 Если в чате никто не пишет __', callback_data='show_afk')
    format_btn = InlineKeyboardButton('💬 Форматирование', callback_data='formating')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_chose')
    markup.add(texts_greeting_btn)
    markup.add(show_rules)
    # markup.add(afk_btn)
    markup.add(warning_btn)
    markup.add(format_btn)
    markup.add(back_btn)
    return markup

def generate_text_editing_page():
    markup = InlineKeyboardMarkup()
    edit_greeting_btn = InlineKeyboardButton('✍ Изменить текст приветствия', callback_data='edit_greeting')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_show_page')
    markup.add(edit_greeting_btn)
    markup.add(back_btn)
    return markup

def generate_rules_editing_page():
    markup = InlineKeyboardMarkup()
    edit_rules_btn = InlineKeyboardButton('✍ Изменить правила', callback_data='edit_rules')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_show_page')
    markup.add(edit_rules_btn)
    markup.add(back_btn)
    return markup

def generate_warning_editing_page():
    markup = InlineKeyboardMarkup()
    edit_banwarning_btn = InlineKeyboardButton('📝 Команда: /ban', callback_data='edit_banwarning')
    edit_kickwarning_btn = InlineKeyboardButton('📝 Команда: /kick', callback_data='edit_kickwarning')
    edit_unbantext_btn = InlineKeyboardButton('📝 Команда: /unban', callback_data='edit_unbantext')
    format_btn = InlineKeyboardButton('💬 Форматирование', callback_data='formating')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_show_page')
    markup.add(edit_banwarning_btn)
    markup.add(edit_kickwarning_btn)
    markup.add(edit_unbantext_btn)
    markup.add(format_btn)
    markup.add(back_btn)
    return markup

def generate_afk_editing_page():
    markup = InlineKeyboardMarkup()
    edit_afk_btn = InlineKeyboardButton('✍ Изменить текст неактивности', callback_data='edit_afk')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_show_page')
    markup.add(edit_afk_btn)
    markup.add(back_btn)
    return markup

def generate_admins_settings():
    markup = InlineKeyboardMarkup()
    block_resources_show_btn = InlineKeyboardButton('🌐 Блокировка ссылок на внешние ресурсы', callback_data='block_resources_show')
    system_notice_show_btn = InlineKeyboardButton('📢 Авто-удаление системных оповещений',
                                                  callback_data='system_notice_show')
    block_repostes_show_btn = InlineKeyboardButton('📩 Запрет репостов', callback_data='block_repostes_show')
    block_ping_show_btn = InlineKeyboardButton('🔕 Запрет пинга', callback_data='block_ping_show')
    format_btn = InlineKeyboardButton('💬 Форматирование', callback_data='formating')


    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_chose')
    markup.add(block_resources_show_btn)
    markup.add(block_repostes_show_btn)
    markup.add(block_ping_show_btn)
    markup.add(system_notice_show_btn)
    markup.add(format_btn)
    markup.add(back_btn)
    return markup

def generate_block_resources_show(user_id, chat_index):
    markup = InlineKeyboardMarkup()
    db = collection.find_one({"user_id": user_id})
    status = '🔴 | Неактивированно'
    if db['settings'][chat_index]['block_resources']['active'] == True:
        status = '🟢 | Активированно '

    activate_btn = InlineKeyboardButton(status, callback_data='activator_resources')
    blocked_resources_btn = InlineKeyboardButton('📃 Список запрещеных ресурсов', callback_data='blocked_resources')
    edit_resourcesw_btn = InlineKeyboardButton('📝 Изменить текст нарушения', callback_data='edit_resourcesw')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_admin_page')
    markup.add(activate_btn)
    markup.add(blocked_resources_btn)
    markup.add(edit_resourcesw_btn)
    markup.add(back_btn)
    return markup



def generate_block_repostes_show(user_id, chat_index):
    markup = InlineKeyboardMarkup()
    db = collection.find_one({"user_id": user_id})
    status = '🔴 | Неактивированно'
    if db['settings'][chat_index]['block_repostes']['active'] == True:
        status = '🟢 | Активированно '

    activate_btn = InlineKeyboardButton(status, callback_data='activator_repostes')
    edit_repostesw_btn = InlineKeyboardButton('📝 Изменить текст нарушения', callback_data='edit_repostesw')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_admin_page')
    markup.add(activate_btn)
    markup.add(edit_repostesw_btn)
    markup.add(back_btn)
    return markup

def generate_system_notice_show(user_id, chat_index):
    markup = InlineKeyboardMarkup()
    db = collection.find_one({"user_id": user_id})
    status = '🔴 | Неактивированно'
    if db['settings'][chat_index]['system_notice']['active'] == True:
        status = '🟢 | Активированно '

    activate_btn = InlineKeyboardButton(status, callback_data='activator_sysnot')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_admin_page')
    markup.add(activate_btn)
    markup.add(back_btn)
    return markup


def generate_block_ping_show(user_id, chat_index):
    markup = InlineKeyboardMarkup()
    db = collection.find_one({"user_id": user_id})
    status = '🔴 | Неактивированно'
    if db['settings'][chat_index]['block_ping']['active'] == True:
        status = '🟢 | Активированно '

    activate_btn = InlineKeyboardButton(status, callback_data='activator_ping')
    edit_pingw_btn = InlineKeyboardButton('📝 Изменить текст нарушения', callback_data='edit_pingw')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_admin_page')
    markup.add(activate_btn)
    markup.add(edit_pingw_btn)
    markup.add(back_btn)
    return markup

def generate_money_top_up():
    markup = InlineKeyboardMarkup()
    money_top_up_btn = InlineKeyboardButton('💰 Отправить донат', callback_data='money_top_up')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_main_page')
    markup.add(money_top_up_btn)
    markup.add(back_btn)
    return markup

def generate_back_to_main():
    markup = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_main_page')
    markup.add(back_btn)
    return markup

def generate_add_b_resources():
    markup = InlineKeyboardMarkup()
    add_btn = InlineKeyboardButton('➕ Расширить список', callback_data='add_block_resources')
    delete_btn = InlineKeyboardButton('🗑️ Удалить расширение', callback_data='remove_block_resources')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_block_resources')
    markup.add(add_btn)
    markup.add(delete_btn)
    markup.add(back_btn)
    return markup

async def generate_my_chats(user_id, current_page=0, buttons_per_page=6):
    try:
        db = collection.find_one({"user_id": user_id})
        inline_buttons = []
        for i in db['chats']:
            chat = await bot.get_chat(i)
            inline_buttons.append(InlineKeyboardButton(text=f'{chat.title}', callback_data=f'schat_{chat.id}'))


        pages = [inline_buttons[i:i + buttons_per_page] for i in range(0, len(inline_buttons), buttons_per_page)]
        current_page = current_page % len(pages)
        markup = InlineKeyboardMarkup().add(*pages[current_page])

        prev_btn = 'N'
        next_btn = 'N'
        if len(pages) > 1:
            if current_page > 0:
                prev_btn = InlineKeyboardButton('◀ Назад', callback_data='prev_page')
            if current_page < len(pages) - 1:
                next_btn = (InlineKeyboardButton('Вперед ▶', callback_data='next_page'))

        if next_btn != 'N' and prev_btn != 'N':
            markup.add(prev_btn, next_btn)
        elif next_btn != 'N':
            markup.add(next_btn)
        elif prev_btn != 'N':
            markup.add(prev_btn)


        markup.add(InlineKeyboardButton('⏪ Назад в меню', callback_data='back_to_main_page'))
        return markup
    except Exception as e:
        print(e)

def generate_admin_main_page():
    markup = InlineKeyboardMarkup()
    stats_btn = InlineKeyboardButton('📊 Статистика бота 📊', callback_data='admin_bot_stats')
    edit_money_btn = InlineKeyboardButton('🪙 Изменить цены', callback_data='admin_edit_money')
    edit_limits_btn = InlineKeyboardButton('✋ Изменить лимиты', callback_data='admin_edit_limits')
    post_btn = InlineKeyboardButton('📢 Отправить объявление всем пользователям', callback_data='admin_post')
    add_admin_btn = InlineKeyboardButton('🔓 Дать доступ к админке', callback_data='admin_add')
    leave_admin_btn = InlineKeyboardButton('↩ Выйти с админки', callback_data='admin_exit')
    markup.add(stats_btn)
    markup.add(edit_money_btn, edit_limits_btn)
    markup.add(post_btn)
    markup.add(add_admin_btn)
    markup.add(leave_admin_btn)
    return markup

def generate_admin_return():
    markup = InlineKeyboardMarkup()
    admin_stats_back_btn = InlineKeyboardButton('⏪ Назад', callback_data='admin_stats_back')
    markup.add(admin_stats_back_btn)
    return markup

def generate_admin_return_main():
    markup = InlineKeyboardMarkup()
    admin_stats_back_btn = InlineKeyboardButton('⏪ Назад в админку', callback_data='back_from_added_position')
    markup.add(admin_stats_back_btn)
    return markup


def generate_payment_page():
    markup = InlineKeyboardMarkup(row_width=1)
    db = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
    unsortedp = db['price']
    positions = sorted(unsortedp, key=lambda x: int(x['period']))
    btns = []
    for i in positions:
        btns.append(InlineKeyboardButton(f'🛒 Купить - {i["period"]} дней', callback_data=f'buy_{i["period"]}'))
    back_btn = InlineKeyboardButton('⏪ Назад в настройки', callback_data='back_to_settings')
    markup.add(*btns)
    markup.add(back_btn)
    return markup

def generate_delete_positions():
    markup = InlineKeyboardMarkup(row_width=1)
    db = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
    unsortedp = db['price']
    positions = sorted(unsortedp, key=lambda x: int(x['period']))
    btns = []
    for i in positions:
        btns.append(InlineKeyboardButton(f'🗑️ {i["period"]} дней - {i["price"]}₽', callback_data=f'positdelete_{i["period"]}'))
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_edit_price')
    markup.add(*btns)
    markup.add(back_btn)
    return markup

def generate_eidit_positions():
    markup = InlineKeyboardMarkup(row_width=1)
    db = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
    unsortedp = db['price']
    positions = sorted(unsortedp, key=lambda x: int(x['period']))
    btns = []
    for i in positions:
        btns.append(InlineKeyboardButton(f'📝 {i["period"]} дней - {i["price"]}₽', callback_data=f'positedite_{i["period"]}'))
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_edit_price')
    markup.add(*btns)
    markup.add(back_btn)
    return markup

def generate_payment_method():
    markup = InlineKeyboardMarkup()
    manual_btn = InlineKeyboardButton('💳 Ручной перевод', callback_data='pay_manual')
    yoomoney_btn = InlineKeyboardButton('💳 ЮMoney', callback_data='pay_yoomoney')
    back_btn = InlineKeyboardButton('⏪ Назад в настройки', callback_data='back_to_settings')
    markup.add(manual_btn)
    markup.add(yoomoney_btn)
    markup.add(back_btn)
    return markup

def generate_back_to_settings():
    markup = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton('⏪ Назад в настройки', callback_data='back_to_settings')
    markup.add(back_btn)
    return markup

def generate_back_to_profil():
    markup = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton('⏪ Открыть профиль', callback_data='back_to_my_profil')
    markup.add(back_btn)
    return markup

def generate_admin_limit_edit_choice():
    markup = InlineKeyboardMarkup()
    limit_to_users_edit_btn = InlineKeyboardButton('📝 Лимит пользователей на чат', callback_data='aedit_limittousers')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_from_edit_limits')
    markup.add(limit_to_users_edit_btn)
    markup.add(back_btn)
    return markup

def generate_admin_price_edit_choice():
    markup = InlineKeyboardMarkup()
    admin_addposition_btn = InlineKeyboardButton('➕ Добавить новую позицию', callback_data='admin_addposition')
    admin_editposition_btn = InlineKeyboardButton('✍ Изменить существующую позицию', callback_data='admin_editposition')
    admin_deleteposition_btn = InlineKeyboardButton('🗑️ Удалить позицию', callback_data='admin_deleteposition')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_from_edit_limits')
    markup.add(admin_addposition_btn)
    markup.add(admin_editposition_btn)
    markup.add(admin_deleteposition_btn)
    markup.add(back_btn)
    return markup

def generate_positedit():
    markup = InlineKeyboardMarkup()
    edit_days = InlineKeyboardButton('🔹 Изменить срок', callback_data='posited_days')
    edit_price = InlineKeyboardButton('🔹 Изменить цену', callback_data='posited_price')
    cancel_editing = InlineKeyboardButton('🔴 Отменить изменение', callback_data='posited_cancel')
    accept_editing = InlineKeyboardButton('🟢 Применить изменения', callback_data='posited_accept')
    markup.add(edit_days)
    markup.add(edit_price)
    markup.add(cancel_editing)
    markup.add(accept_editing)
    return markup