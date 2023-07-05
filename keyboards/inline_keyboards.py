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

def generate_settings():
    markup = InlineKeyboardMarkup()
    edit_texts_btn = InlineKeyboardButton('✍ Изменение текста', callback_data='settings_texts')
    edit_admin_btn = InlineKeyboardButton('🧑‍⚖ Настройки администрирования', callback_data='settings_admins')
    done_btn = InlineKeyboardButton('✅ Готово', callback_data='done_btn')
    markup.add(edit_texts_btn)
    markup.add(edit_admin_btn)
    markup.add(done_btn)
    return markup

def generate_edit_text_settings():
    markup = InlineKeyboardMarkup()
    texts_greeting_btn = InlineKeyboardButton('👋 Приветствие нового участника', callback_data='texts_greeting')
    show_rules = InlineKeyboardButton('🪧 Правила чата', callback_data='show_rules')
    warning_btn = InlineKeyboardButton('👮 Уведомление при нарушений', callback_data='show_warning')
    afk_btn = InlineKeyboardButton('🔇 Если в чате никто не пишет __', callback_data='show_afk')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_chose')
    markup.add(texts_greeting_btn)
    markup.add(show_rules)
    markup.add(warning_btn)
    markup.add(afk_btn)
    markup.add(back_btn)
    return markup

def generate_text_editing_page():
    markup = InlineKeyboardMarkup()
    edit_greeting_btn = InlineKeyboardButton('✍ Изменить текст приветствия', callback_data='edit_greeting')
    format_btn = InlineKeyboardButton('💬 Форматирование', callback_data='formating')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_show_page')
    markup.add(edit_greeting_btn)
    markup.add(format_btn)
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
    edit_warning_btn = InlineKeyboardButton('✍ Изменить текст предупреждения', callback_data='edit_warning')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_show_page')
    markup.add(edit_warning_btn)
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
    block_repostes_show_btn = InlineKeyboardButton('📩 Запрет репостов', callback_data='block_repostes_show')
    block_ping_show_btn = InlineKeyboardButton('🔕 Запрет пинга', callback_data='block_ping_show')
    system_notice_show_btn = InlineKeyboardButton('📢 Авто-удаление системных оповещений', callback_data='system_notice_show')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_chose')
    markup.add(block_resources_show_btn)
    markup.add(block_repostes_show_btn)
    markup.add(block_ping_show_btn)
    markup.add(system_notice_show_btn)
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
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_admin_page')
    markup.add(activate_btn)
    markup.add(blocked_resources_btn)
    markup.add(back_btn)
    return markup



def generate_block_repostes_show(user_id, chat_index):
    markup = InlineKeyboardMarkup()
    db = collection.find_one({"user_id": user_id})
    status = '🔴 | Неактивированно'
    if db['settings'][chat_index]['block_repostes']['active'] == True:
        status = '🟢 | Активированно '

    activate_btn = InlineKeyboardButton(status, callback_data='activator_repostes')
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_admin_page')
    markup.add(activate_btn)
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
    back_btn = InlineKeyboardButton('⏪ Назад', callback_data='back_to_admin_page')
    markup.add(activate_btn)
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
