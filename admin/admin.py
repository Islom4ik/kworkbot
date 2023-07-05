from data.loader import bot, dp, FSMContext, State, Message, config
from data.configs import delete_message, resolve_username_to_user_id
from aiogram.types import InputFile, CallbackQuery, ContentTypes, InputMediaPhoto
from database.database import collection, ObjectId
from states_scenes.scene import MySceneStates
from keyboards.inline_keyboards import generate_admin_main_page, generate_add_button, generate_admin_return
import asyncio
import re

@dp.message_handler(commands=['admin'])
async def react_to_admin(ctx: Message):
    try:
        db = collection.find_one({'_id': ObjectId('64987b1eeed9918b13b0e8b4')})
        if ctx.from_user.id not in db['admins'] and ctx.from_user.id != int(config['MAIN_ADMIN_ID']): return await ctx.answer('🔒')
        await ctx.answer_photo(InputFile('admin/admin_page.jpg'), f'Добро пожаловать в админку, <a href="tg://user?id={ctx.from_user.id}">{ctx.from_user.first_name}</a>', reply_markup=generate_admin_main_page())
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'admin_exit')
async def answer_to_admin_exit(call: CallbackQuery):
    try:
        await call.answer('😜 До новых встреч!')
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(call.message.chat.id, 'Здравствуйте! Я бот-админ и могу администрировать ваш групповой чат.\n\nДля того чтобы начать, добавьте меня в свой групповой чат:', reply_markup=generate_add_button())
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'admin_add')
async def answer_to_admin_exit(call: CallbackQuery):
    try:
        await call.answer()
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(call.message.chat.id, '👮 Введите юзернейм или прямую сслку на пользователя:')
        await MySceneStates.add_admin.set()
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'admin_post')
async def answer_to_admin_exit(call: CallbackQuery):
    try:
        await call.answer()
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(call.message.chat.id, '💬 Отправьте сообщение, которое хотите отправить всем пользователям своего бота:')
        await MySceneStates.post_to_users.set()
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'admin_bot_stats')
async def answer_to_admin_exit(call: CallbackQuery):
    try:
        db = collection.find_one({'_id': ObjectId('64987b1eeed9918b13b0e8b4')})
        await call.answer()
        await bot.edit_message_media(InputMediaPhoto(InputFile('admin/admin_stats.jpg'), caption=f'📊 Общая статистика бота:\n\n<b>Кол-во пользователей:</b> {len(db["users"])}\n<b>Кол-во чатов с ботом:</b> {len(db["groups"])}\n<b>Кол-во купленных лицензий:</b> {db["lics_buyed"]}\n<b>Кол-во заработанных денег:</b> {db["erned"]}') , call.message.chat.id, call.message.message_id, reply_markup=generate_admin_return())
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda call: call.data == 'admin_stats_back')
async def answer_to_admin_exit(call: CallbackQuery):
    try:
        await call.answer()
        await bot.edit_message_media(InputMediaPhoto(InputFile('admin/admin_page.jpg'), caption=f'Добро пожаловать в админку, <a href="tg://user?id={call.from_user.id}">{call.from_user.first_name}</a>') , call.message.chat.id, call.message.message_id, reply_markup=generate_admin_main_page())
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda call: call.data == 'admin_edit_money' or call.data == 'admin_edit_limits')
async def answer_to_admin_exit(call: CallbackQuery):
    try:
        await call.answer('Пока недоступно ✋', show_alert=True)
    except Exception as e:
        print(e)

@dp.message_handler(content_types=['text'], state=MySceneStates.add_admin)
async def blocked_resources_remove_scene(ctx: Message, state: FSMContext):
    try:
        user = ctx.text
        dicts_with_user_key = []

        pattern = r"https://t.me/([\w_]+)"

        if user[0] == '@':
            userid = await resolve_username_to_user_id(user.replace('@', ''))
            dicts_with_user_key.append(userid[0])
        elif re.search(pattern, user):
            usern = re.findall(pattern, user)[0]
            userid = await resolve_username_to_user_id(usern)
            dicts_with_user_key.append(userid[0])

        if len(dicts_with_user_key) == 0:
            trash = await ctx.answer('🪪 Пользователь не найден')
            await state.finish()
            await react_to_admin(ctx)
            return asyncio.create_task(delete_message(5, [trash.message_id, ctx.message_id], ctx.chat.id))

        db = collection.find_one({'_id': ObjectId('64987b1eeed9918b13b0e8b4')})
        for i in dicts_with_user_key:
            if i in db['admins']: continue
            collection.find_one_and_update({'_id': ObjectId('64987b1eeed9918b13b0e8b4')}, {'$push': {'admins': i}})

        await ctx.answer('✅ Вы успешно выдали доступ к админке!')
        await state.finish()
        await react_to_admin(ctx)
    except Exception as e:
        print(e)

@dp.message_handler(content_types=ContentTypes.ANY, state=MySceneStates.post_to_users)
async def blocked_resources_remove_scene(ctx: Message, state: FSMContext):
    try:
        db = collection.find_one({'_id': ObjectId('64987b1eeed9918b13b0e8b4')})
        msgidtoedit = await ctx.answer('🔄️ Ваше сообщение рассылается по всем пользователям')
        asyncio.create_task(message_to_users(ctx, db['users'], msgidtoedit.message_id))
        await state.finish()
        await react_to_admin(ctx)
    except Exception as e:
        print(e)

async def message_to_users(ctx: Message, users: list, id):
    try:
        for i in users:
            try:
                await bot.copy_message(i, from_chat_id=ctx.chat.id, message_id=ctx.message_id)
            except:
                print('')
            await asyncio.sleep(0.3)
        await bot.edit_message_text('Отправка завершена ✅', ctx.chat.id, id)
    except Exception as e:
        print(e)

@dp.message_handler(commands=['user_to_id'])
async def convert_to_id(ctx: Message):
    try:
        args = ctx.text.split(' ')
        if len(args) == 1: return await ctx.answer(
            'Пример: <i>/user_to_id @username</i>')
        if len(args) > 2: return await ctx.answer(
            f'Я принимаю только 1 аргумент, а в вашем тексте их <b>{len(args) - 1}</b>. Пример: <i>/user_to_id @username</i>')
        if args[1][0] != '@': return await ctx.answer(
            'Я принимаю только юзернейм. Пример: <i>/user_to_id @username</i>')

        try:
            global userid
            userid = await resolve_username_to_user_id(args[1].replace('@', ''))
            await ctx.answer(
                f'<b>👤 Пользователь:</b> <a href="tg://user?id={userid[0]}">{userid[1]}</a>\n\n<b>ID:</b> <code>{userid[0]}</code>')
        except:
            print('')

        if userid == None: return await ctx.answer('🔎 Пользователь не найден')
    except Exception as e:
        print(e)


