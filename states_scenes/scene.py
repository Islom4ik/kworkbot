# Состояния - сцены где бот будет получать различные данные с пользоватеоей
from data.loader import StatesGroup, State

class MySceneStates(StatesGroup):
    greeting_change_text_scene = State()
    rules_change_text_scene = State()
    banwarning_change_text_scene = State()
    kickwarning_change_text_scene = State()
    unbantext_change_text_scene = State()
    afk_change_text_scene = State()
    blocked_resources_add = State()
    blocked_resources_remove = State()
    get_reason = State()
    add_admin = State()
    post_to_users = State()
    resourcesw_change_scene = State()
    repostesw_change_scene = State()
    pingw_change_scene = State()
    addposition_period_scene = State()
    addposition_price_scene = State()
    posited_days_scene = State()
    posited_price_scene = State()
    aedit_limittousers_scene = State()