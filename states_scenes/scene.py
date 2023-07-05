# Состояния - сцены где бот будет получать различные данные с пользоватеоей
from data.loader import StatesGroup, State

class MySceneStates(StatesGroup):
    greeting_change_text_scene = State()
    rules_change_text_scene = State()
    warning_change_text_scene = State()
    afk_change_text_scene = State()
    blocked_resources_add = State()
    blocked_resources_remove = State()
    get_reason = State()
    add_admin = State()
    post_to_users = State()