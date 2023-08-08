# Встроенные кнопки под сообщения:
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import BotKicked, BotBlocked
from database.database import collection, ObjectId
from data.loader import bot
from data.texts import t_bot_user

def generate_add_button():
    markup = InlineKeyboardMarkup()
    add_bottogroup_btn = InlineKeyboardButton('➕ Добавить группу', url=f'https://t.me/{t_bot_user}?startgroup=true')
    my_groups_btn = InlineKeyboardButton('🗃️ Мои чаты', callback_data='show_my_chats')
    donate_btn = InlineKeyboardButton('💰 Поддержать донатом', callback_data='donate')
    markup.add(add_bottogroup_btn)
    markup.add(my_groups_btn)
    markup.add(donate_btn)
    return markup

def generate_mychats_button():
    markup = InlineKeyboardMarkup()
    my_groups_btn = InlineKeyboardButton('🗃️ Мои чаты', callback_data='show_my_chats')
    markup.add(my_groups_btn)
    return markup


def generate_settings_button(chat_id):
    markup = InlineKeyboardMarkup()
    settings_btn = InlineKeyboardButton('⚙ Настроить бота', url=f'https://t.me/{t_bot_user}?start=settings_{chat_id}')
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
    users_info_btn = InlineKeyboardButton('📊 Статистика участников', callback_data='chat_users_info')
    buy_lic_btn = InlineKeyboardButton('💎 Купить лицензию', callback_data='money_top_up')
    lic_info_btn = InlineKeyboardButton('ℹ Информация о лицензии', callback_data='lic_info')
    done_btn = InlineKeyboardButton('✅ Готово', callback_data='done_btn')
    markup.add(edit_admin_btn)
    markup.add(edit_texts_btn)
    markup.add(users_info_btn)
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

def generate_admins_settings():
    markup = InlineKeyboardMarkup()
    block_resources_show_btn = InlineKeyboardButton('🌐 Блок внешних ссылок', callback_data='block_resources_show')
    system_notice_show_btn = InlineKeyboardButton('📢 Удаление оповещений',
                                                  callback_data='system_notice_show')
    block_repostes_show_btn = InlineKeyboardButton('📩 Запрет репостов', callback_data='block_repostes_show')
    block_ping_show_btn = InlineKeyboardButton('🔕 Запрет пинга', callback_data='block_ping_show')
    format_btn = InlineKeyboardButton('💬 Форматирование', callback_data='formating')
    vorchun_btn = InlineKeyboardButton('🗣️ Ворчун', callback_data='vorchun_show')

    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_chose')
    markup.add(block_resources_show_btn, system_notice_show_btn)
    markup.add(block_repostes_show_btn, format_btn)
    markup.add(block_ping_show_btn, vorchun_btn)
    markup.add(back_btn)
    return markup

def generaate_users_toda_actions():
    markup = InlineKeyboardMarkup()
    remove_btn = InlineKeyboardButton('🗑️ Удаление из категорий', callback_data='delete_users_from_cat')
    filter_show_btn = InlineKeyboardButton('🔣 Фильтр символов', callback_data='filter_show')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_chose')
    markup.add(remove_btn)
    markup.add(filter_show_btn)
    markup.add(back_btn)
    return markup

def generaate_back_from_deletion():
    markup = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_from_deletion')
    markup.add(back_btn)
    return markup

def generaate_users_toda_categories():
    markup = InlineKeyboardMarkup()
    deleteds_btn = InlineKeyboardButton('👻 Удаленные аккаунты', callback_data='category_deleted')
    symbol_btn = InlineKeyboardButton('🔣 Участники попадающие под фильтр', callback_data='category_symbol')
    nonactive_7_btn = InlineKeyboardButton('🟠 Не активны более 7  д', callback_data='category_7')
    nonactive_14_btn = InlineKeyboardButton('🟠 Не активны более 14 д', callback_data='category_14')
    nonactive_30_btn = InlineKeyboardButton('🟠 Не активны более 30 д', callback_data='category_30')
    nonactive_60_btn = InlineKeyboardButton('🟠 Не активны более 60 д', callback_data='category_60')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_from_cat_chose')
    markup.add(deleteds_btn)
    markup.add(symbol_btn)
    markup.add(nonactive_7_btn)
    markup.add(nonactive_14_btn)
    markup.add(nonactive_30_btn)
    markup.add(nonactive_60_btn)
    markup.add(back_btn)
    return markup

def generaate_delete_percent():
    markup = InlineKeyboardMarkup()
    delete_10_btn = InlineKeyboardButton('🔹 Удалить 10%', callback_data='catdelete_10')
    delete_20_btn = InlineKeyboardButton('🔹 Удалить 20%', callback_data='catdelete_20')
    delete_30_btn = InlineKeyboardButton('🔹 Удалить 30%', callback_data='catdelete_30')
    delete_40_btn = InlineKeyboardButton('🔹 Удалить 40%', callback_data='catdelete_40')
    delete_50_btn = InlineKeyboardButton('🔹 Удалить 50%', callback_data='catdelete_50')
    delete_100_btn = InlineKeyboardButton('💯 Удалить 100%', callback_data='catdelete_100')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_from_percent')
    markup.add(delete_10_btn)
    markup.add(delete_20_btn)
    markup.add(delete_30_btn)
    markup.add(delete_40_btn)
    markup.add(delete_50_btn)
    markup.add(delete_100_btn)
    markup.add(back_btn)
    return markup

def generate_block_resources_show(user_id, chat_index):
    markup = InlineKeyboardMarkup()
    db = collection.find_one({"user_id": user_id})
    status = '🔴 | Выключено'
    if db['settings'][chat_index]['block_resources']['active'] == True:
        status = '🟢 | Включено '

    activate_btn = InlineKeyboardButton(status, callback_data='activator_resources')
    blocked_resources_btn = InlineKeyboardButton('📋 Список ресурсов', callback_data='blocked_resources')
    edit_resourcesw_btn = InlineKeyboardButton('📝 Изменить текст', callback_data='edit_resourcesw')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_admin_page')
    markup.add(activate_btn)
    markup.add(blocked_resources_btn)
    markup.add(edit_resourcesw_btn)
    markup.add(back_btn)
    return markup



def generate_block_repostes_show(user_id, chat_index):
    markup = InlineKeyboardMarkup()
    db = collection.find_one({"user_id": user_id})
    status = '🔴 | Выключено'
    if db['settings'][chat_index]['block_repostes']['active'] == True:
        status = '🟢 | Включено '

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
    status = '🔴 | Выключено'
    if db['settings'][chat_index]['system_notice']['active'] == True:
        status = '🟢 | Включено '

    activate_btn = InlineKeyboardButton(status, callback_data='activator_sysnot')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_admin_page')
    markup.add(activate_btn)
    markup.add(back_btn)
    return markup


def generate_block_ping_show(user_id, chat_index):
    markup = InlineKeyboardMarkup()
    db = collection.find_one({"user_id": user_id})
    status = '🔴 | Выключено'
    if db['settings'][chat_index]['block_ping']['active'] == True:
        status = '🟢 | Включено '

    activate_btn = InlineKeyboardButton(status, callback_data='activator_ping')
    edit_pingw_btn = InlineKeyboardButton('📝 Изменить текст нарушения', callback_data='edit_pingw')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_admin_page')
    markup.add(activate_btn)
    markup.add(edit_pingw_btn)
    markup.add(back_btn)
    return markup

def generate_block_afk_show(user_id, chat_index):
    markup = InlineKeyboardMarkup()
    db = collection.find_one({"user_id": user_id})
    status = '🔴 | Выключено'
    if db['settings'][chat_index]['afk']['active'] == True:
        status = '🟢 | Включено '

    activate_btn = InlineKeyboardButton(status, callback_data='activator_afk')
    edit_pingw_btn = InlineKeyboardButton('📝 Изменить текст', callback_data='edit_afkw')
    edit_time_btn = InlineKeyboardButton('⏳ Изменить таймер', callback_data='edit_afktimer')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_admin_page')
    markup.add(activate_btn)
    markup.add(edit_pingw_btn)
    markup.add(edit_time_btn)
    markup.add(back_btn)
    return markup

def generate_back_to_main():
    markup = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_main_page')
    markup.add(back_btn)
    return markup

def generate_add_b_resources():
    markup = InlineKeyboardMarkup()
    add_btn = InlineKeyboardButton('➕ Добавить запрет', callback_data='add_block_resources')
    delete_btn = InlineKeyboardButton('🗑️ Удалить', callback_data='remove_block_resources')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_block_resources')
    markup.add(add_btn)
    markup.add(delete_btn)
    markup.add(back_btn)
    return markup

def generate_add_b_syms():
    markup = InlineKeyboardMarkup()
    add_btn = InlineKeyboardButton('➕ Добавить фильтр', callback_data='add_block_sym')
    delete_btn = InlineKeyboardButton('🗑️ Удалить', callback_data='remove_block_sym')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_from_block_syms')
    markup.add(add_btn)
    markup.add(delete_btn)
    markup.add(back_btn)
    return markup

async def generate_my_chats(user_id, current_page=0, buttons_per_page=6):
    try:
        db = collection.find_one({"user_id": user_id})
        inline_buttons = []
        for i in db['chats']:
            try:
                chat = await bot.get_chat(i)
                inline_buttons.append(InlineKeyboardButton(text=f'{chat.title}', callback_data=f'schat_{chat.id}'))
            except BotKicked:
                continue

        markup = ''
        if len(inline_buttons) != 0:
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
        else:
            markup = InlineKeyboardMarkup()
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

def generate_dpayment_method():
    markup = InlineKeyboardMarkup()
    manual_btn = InlineKeyboardButton('💳 Ручной перевод', callback_data='donpay_manual')
    yoomoney_btn = InlineKeyboardButton('💳 ЮMoney', callback_data='donpay_yoomoney')
    back_btn = InlineKeyboardButton('⏪ Отменить', callback_data='back_from_donate_method')
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
    limit_to_users_edit_btn = InlineKeyboardButton('📝 Изменить ограничение', callback_data='aedit_limittousers')
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

def generate_manual_payment():
    markup = InlineKeyboardMarkup()
    manualp_sendtoacc = InlineKeyboardButton('✅ Я перевел', callback_data='manualp_sendtoacc')
    manualp_back = InlineKeyboardButton('⏪ Назад', callback_data='manualp_back')
    markup.add(manualp_sendtoacc)
    markup.add(manualp_back)
    return markup

def generate_dmanual_payment():
    markup = InlineKeyboardMarkup()
    manualp_sendtoacc = InlineKeyboardButton('✅ Готово', callback_data='dmanul_done')
    manualp_back = InlineKeyboardButton('⏪ Назад', callback_data='dmanul_back')
    markup.add(manualp_sendtoacc)
    markup.add(manualp_back)
    return markup

def generate_back_resedittext():
    markup = InlineKeyboardMarkup()
    back = InlineKeyboardButton('⏪ Назад', callback_data='eback_resedittext')
    markup.add(back)
    return markup

def generate_back_repedittext():
    markup = InlineKeyboardMarkup()
    back = InlineKeyboardButton('⏪ Назад', callback_data='eback_repedittext')
    markup.add(back)
    return markup

def generate_back_pingedittext():
    markup = InlineKeyboardMarkup()
    back = InlineKeyboardButton('⏪ Назад', callback_data='eback_pingedittext')
    markup.add(back)
    return markup

def generate_back_addblock():
    markup = InlineKeyboardMarkup()
    back = InlineKeyboardButton('⏪ Назад', callback_data='eback_addblock')
    markup.add(back)
    return markup

def generate_back_remblock():
    markup = InlineKeyboardMarkup()
    back = InlineKeyboardButton('⏪ Назад', callback_data='eback_remblock')
    markup.add(back)
    return markup

def generate_back_ruledittext():
    markup = InlineKeyboardMarkup()
    back = InlineKeyboardButton('⏪ Назад', callback_data='eback_ruledittext')
    markup.add(back)
    return markup

def generate_back_gretedittext():
    markup = InlineKeyboardMarkup()
    back = InlineKeyboardButton('⏪ Назад', callback_data='eback_gretedittext')
    markup.add(back)
    return markup

def generate_back_banedittext():
    markup = InlineKeyboardMarkup()
    back = InlineKeyboardButton('⏪ Назад', callback_data='eback_banedittext')
    markup.add(back)
    return markup

def generate_back_kickedittext():
    markup = InlineKeyboardMarkup()
    back = InlineKeyboardButton('⏪ Назад', callback_data='eback_kickedittext')
    markup.add(back)
    return markup

def generate_back_unbanedittext():
    markup = InlineKeyboardMarkup()
    back = InlineKeyboardButton('⏪ Назад', callback_data='eback_unbanedittext')
    markup.add(back)
    return markup

def generate_back_afkedittext():
    markup = InlineKeyboardMarkup()
    back = InlineKeyboardButton('⏪ Назад', callback_data='eback_afkedittext')
    markup.add(back)
    return markup

def generate_back_donatemoney():
    markup = InlineKeyboardMarkup()
    back = InlineKeyboardButton('⏪ Назад', callback_data='eback_donatemoney')
    markup.add(back)
    return markup

def generate_back_addsyms():
    markup = InlineKeyboardMarkup()
    back = InlineKeyboardButton('⏪ Назад', callback_data='eback_addsyms')
    markup.add(back)
    return markup

def generate_back_removesyms():
    markup = InlineKeyboardMarkup()
    back = InlineKeyboardButton('⏪ Назад', callback_data='eback_removesyms')
    markup.add(back)
    return markup

def generate_back_vtimer():
    markup = InlineKeyboardMarkup()
    back = InlineKeyboardButton('⏪ Назад', callback_data='eback_vtimer')
    markup.add(back)
    return markup


def generate_manual_payment_admin_actions():
    markup = InlineKeyboardMarkup()
    accept = InlineKeyboardButton('Проверил ✅', callback_data='mmpay_acadmin')
    decline = InlineKeyboardButton('Не пришло 🤷‍♂', callback_data='mmpay_decadmin')
    markup.add(accept)
    markup.add(decline)
    return markup


def generate_back_to_main():
    markup = InlineKeyboardMarkup()
    back = InlineKeyboardButton('⏪ Назад', callback_data='back_to_main_page')
    markup.add(back)
    return markup

def generate_donate_payment_button():
    markup = InlineKeyboardMarkup()
    pay = InlineKeyboardButton('Помочь', pay=True)
    markup.add(pay)
    return markup