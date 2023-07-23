from data.loader import bot, dp, FSMContext, State, Message, config
from data.configs import delete_message, resolve_username_to_user_id
from aiogram.types import InputFile, CallbackQuery, ContentTypes, InputMediaPhoto
from database.database import collection, ObjectId
from states_scenes.scene import MySceneStates
from keyboards.inline_keyboards import generate_eidit_positions, generate_admin_return_main, generate_delete_positions, generate_admin_price_edit_choice, generate_admin_limit_edit_choice, generate_admin_main_page, generate_add_button, generate_admin_return
import asyncio
import re
import psutil

@dp.message_handler(commands=['admin'])
async def react_to_admin(ctx: Message):
    try:
        await ctx.delete()
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
async def answer_to_admin_add(call: CallbackQuery):
    try:
        await call.answer()
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(call.message.chat.id, '👮 Введите юзернейм или прямую сслку на пользователя:')
        await MySceneStates.add_admin.set()
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'admin_post')
async def answer_to_admin_post(call: CallbackQuery):
    try:
        await call.answer()
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(call.message.chat.id, '💬 Отправьте сообщение, которое хотите отправить всем пользователям своего бота:')
        await MySceneStates.post_to_users.set()
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'admin_bot_stats')
async def answer_to_admin_stats(call: CallbackQuery):
    try:
        db = collection.find_one({'_id': ObjectId('64987b1eeed9918b13b0e8b4')})
        cpu_percent = psutil.cpu_percent(percpu=True)
        net_stats = psutil.net_io_counters()
        memory_stats = psutil.virtual_memory()
        await call.answer()
        await bot.edit_message_media(InputMediaPhoto(InputFile('admin/admin_stats.jpg'), caption=f'📊 Общая статистика бота:\n\n<b>Кол-во пользователей:</b> {len(db["users"])}\n<b>Кол-во чатов с ботом:</b> {len(db["groups"])}\n<b>Кол-во купленных лицензий за все время:</b> {db["lics_buyed"]}\n<b>Кол-во заработанных денег за все время:</b> {db["earned"]}₽\n<b>Кол-во чатов с лицензией:</b> {len(db["chat_with_lics"])}\n\n<b>Статистика VPS:</b>\n\n<b>Оперативка:</b>\nИспользуется оперативной памяти: {memory_stats.used} байт\nПроцент использования оперативной памяти: {memory_stats.percent}%\n\n<b>Сеть:</b>\nВходящий трафик: {net_stats.bytes_recv} байт\nИсходящий трафик: {net_stats.bytes_sent} байт\n\n<b>Процессор:</b>\nПроцент использования ядра 1: {cpu_percent[0]}%\nПроцент использования ядра 2: {cpu_percent[1]}%'), call.message.chat.id, call.message.message_id, reply_markup=generate_admin_return())
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda call: call.data == 'admin_stats_back')
async def answer_to_admin_back(call: CallbackQuery):
    try:
        await call.answer()
        await bot.edit_message_media(InputMediaPhoto(InputFile('admin/admin_page.jpg'), caption=f'Добро пожаловать в админку, <a href="tg://user?id={call.from_user.id}">{call.from_user.first_name}</a>') , call.message.chat.id, call.message.message_id, reply_markup=generate_admin_main_page())
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda call: call.data == 'admin_edit_money')
async def answer_to_admin_emoney(call: CallbackQuery):
    try:
        db = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
        prices = ''
        unsortedp = db['price']
        positions = sorted(unsortedp, key=lambda x: int(x['period']))
        for i in positions:
            prices += f'🔹 {i["period"]} дней – {i["price"]}₽\n'
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption=f'💎 <b>Прайс-лист:</b>\n{prices}\nВыберите действие:',
                                       reply_markup=generate_admin_price_edit_choice())
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'admin_edit_limits')
async def answer_to_admin_elimits(call: CallbackQuery):
    try:
        db = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=f'✋ <b>Лимиты:</b>\n<b>Лимит количества пользователей на чат:</b> {db["limit_to_users"]}\n\nВыберите лимит который хотите изменить:', reply_markup=generate_admin_limit_edit_choice())
    except Exception as e:
        print(e)

# [{'period': '180', 'price': 180.0}, {'period': '365', 'price': 350.0}, {'period': '90', 'price': 90.0}, {'period': '30', 'price': 30.0}]
# collection.find_one_and_update({"_id": ObjectId('64987b1eeed9918b13b0e8b4')}, {"$set": {"price": [{'period': '180', 'price': 180.0}, {'period': '365', 'price': 350.0}, {'period': '90', 'price': 90.0}, {'period': '30', 'price': 30.0}]}})

@dp.callback_query_handler(lambda call: call.data == 'admin_deleteposition')
async def answer_to_admin_deleteposition(call: CallbackQuery):
    try:
        db = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
        if len(db['price']) == 0: return await bot.send_message(call.message.chat.id, call.message.message_id, text='⚠ Извините, но я не нашел ни одну позицию в базе данных')
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=f'⬇ <b>Выберите позицию которую хотите удалить:</b>', reply_markup=generate_delete_positions())
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'admin_addposition')
async def answer_to_admin_admin_addposition(call: CallbackQuery):
    try:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await MySceneStates.addposition_period_scene.set()
        await bot.send_message(chat_id=call.message.chat.id, text='✍ Введите срок действия лицензии в днях:')
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'admin_editposition')
async def answer_to_admin_admin_editposition(call: CallbackQuery):
    try:
        return await call.answer('😶 Пока не доступно', show_alert=True)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption='⬇ Выберите позицию которую хотите изменить:', reply_markup=generate_eidit_positions())
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: 'positdelete' in call.data)
async def react_to_admin_positdelete(call: CallbackQuery):
    try:
        db = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
        index_of_possition = None
        for index, item in enumerate(db['price']):
            if item.get("period") == call.data.split("_")[1]:
                index_of_possition = index
                break

        if len(db['price']) == 1: return await call.answer('✋ В базе должна оставаться хотя бы одна позиция')

        collection.find_one_and_update({"_id": ObjectId('64987b1eeed9918b13b0e8b4')}, {"$pull": {f'price': {"period": call.data.split("_")[1]}}})

        await call.answer('Успешное удаление позиции!')
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=generate_delete_positions())
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: call.data == 'back_to_edit_price')
async def answer_to_admin_back_to_edit_price(call: CallbackQuery):
    db = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
    prices = ''
    unsortedp = db['price']
    positions = sorted(unsortedp, key=lambda x: int(x['period']))
    for i in positions:
        prices += f'🔹 {i["period"]} дней – {i["price"]}₽\n'
    await call.answer()
    await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                   caption=f'💎 <b>Прайс-лист:</b>\n{prices}\nВыберите действие:',
                                   reply_markup=generate_admin_price_edit_choice())

@dp.callback_query_handler(lambda call: call.data == 'back_from_added_position')
async def answer_to_admin_back_from_added_position(call: CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    db = collection.find_one({'_id': ObjectId('64987b1eeed9918b13b0e8b4')})
    if call.from_user.id not in db['admins'] and call.from_user.id != int(
        config['MAIN_ADMIN_ID']): return await call.answer('🔒')
    await bot.send_photo(chat_id=call.message.chat.id, photo=InputFile('admin/admin_page.jpg'),
                           caption=f'Добро пожаловать в админку, <a href="tg://user?id={call.from_user.id}">{call.from_user.first_name}</a>',
                           reply_markup=generate_admin_main_page())

@dp.message_handler(content_types=['text'], state=MySceneStates.add_admin)
async def add_admin_scene(ctx: Message, state: FSMContext):
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

@dp.message_handler(content_types=['text'], state=MySceneStates.addposition_period_scene)
async def addposition_period_scene(ctx: Message, state: FSMContext):
    try:
        text = ctx.text.replace('d', '').replace('д', '').replace('дней', '')
        if text.isdigit() == False:
            await state.finish()
            await MySceneStates.addposition_period_scene.set()
            return await ctx.answer('✋ Значение должно быть числом\n\nВведите срок действия лицензии в днях:')

        db = collection.find_one({'_id': ObjectId('64987b1eeed9918b13b0e8b4')})
        check = None
        for index, item in enumerate(db['price']):
            if item.get("period") == text:
                check = index
                break

        if check != None:
            await ctx.answer('✋ В базе уже существует такая позиция с таким количеством дней\n\nВведите другое количество срока:')
            await state.finish()
            return await MySceneStates.addposition_period_scene.set()
        collection.find_one_and_update({'_id': ObjectId('64987b1eeed9918b13b0e8b4')}, {"$push": {"price": {"period": text}}})
        await MySceneStates.addposition_price_scene.set()
        await ctx.answer('✍ А теперь введите сумму которую заплатит пользователь при покупке(Значение должно быть в десятичном-float формате. Пример: 100.0 | 250.0):')
    except Exception as e:
        print(e)

def has_decimal_point(string):
    parts = string.split('.')
    return len(parts) == 2 and all(part.isdigit() for part in parts)

def remove_non_digits_and_dot(text):
    pattern = r'[^0-9.]'
    return re.sub(pattern, '', text)

@dp.message_handler(content_types=['text'], state=MySceneStates.addposition_price_scene)
async def addposition_price_scene(ctx: Message, state: FSMContext):
    try:
        trahstext = ctx.text.replace('₽', '').replace('р', '').replace('рублей', '')
        text = remove_non_digits_and_dot(trahstext)
        check = has_decimal_point(text)
        if check == False:
            await ctx.answer(
                '✋ Вы ввели значение в неправильном формате\n\nВведите сумму которую заплатит пользователь при покупке(Значение должно быть в десятичном-float формате. Пример: 100.0 | 250.0):')
            await state.finish()
            return await MySceneStates.addposition_price_scene.set()

        text_to_float = float(text)
        db = collection.find_one({'_id': ObjectId('64987b1eeed9918b13b0e8b4')})
        index_of_last_position = len(db["price"]) - 1

        collection.find_one_and_update({'_id': ObjectId('64987b1eeed9918b13b0e8b4')}, {"$set": {f"price.{index_of_last_position}.price": text_to_float}})
        await state.finish()
        await ctx.answer(f'Вы успешно добавили новую позицию:\n\n🆕 {db["price"][index_of_last_position]["period"]} дней - {text_to_float}₽', reply_markup=generate_admin_return_main())
    except Exception as e:
        print(e)

@dp.message_handler(content_types=ContentTypes.ANY, state=MySceneStates.post_to_users)
async def post_scene(ctx: Message, state: FSMContext):
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


