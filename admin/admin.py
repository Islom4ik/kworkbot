from data.loader import bot, dp, FSMContext, State, Message, config
from data.configs import delete_message, resolve_username_to_user_id
from data.texts import *
from aiogram.types import CallbackQuery, ContentTypes
from database.database import collection, ObjectId
from states_scenes.scene import MySceneStates
from keyboards.inline_keyboards import *
import asyncio
import re

@dp.callback_query_handler(lambda call: call.data == 'admin_edit_money')
async def answer_to_admin_emoney(call: CallbackQuery):
    try:
        db = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
        prices = ''
        unsortedp = db['price']
        positions = sorted(unsortedp, key=lambda x: int(x['period']))
        for i in positions:
            prices += f'🔹 {i["period"]} дней – {i["price"]}₽\n'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       text=f'💎 <b>Прайс-лист:</b>\n{prices}\nВыберите действие:',
                                       reply_markup=generate_admin_price_edit_choice())
    except Exception as e:
        print('Error в answer_to_admin_emoney:' + f'{e}')

@dp.callback_query_handler(lambda call: call.data == 'admin_edit_limits')
async def answer_to_admin_elimit(call: CallbackQuery):
    try:
        db = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'✋ <b>Лимиты:</b>\n\n<b>Демо режим до:</b> {db["limit_to_users"]} юзеров',
                                    reply_markup=generate_admin_limit_edit_choice())
    except Exception as e:
        print('Error в answer_to_admin_elimit:' + f'{e}')

@dp.message_handler(commands=['admin'])
async def react_to_admin(ctx: Message):
    try:
        print('adadad')
        await ctx.delete()
        db = collection.find_one({'_id': ObjectId('64987b1eeed9918b13b0e8b4')})
        if ctx.from_user.id not in db['admins'] and ctx.from_user.id != int(config['MAIN_ADMIN_ID']): return await ctx.answer('🔒')
        await ctx.answer(f'Добро пожаловать в админку, <a href="tg://user?id={ctx.from_user.id}">{ctx.from_user.first_name}</a>', reply_markup=generate_admin_main_page())
    except Exception as e:
        print('Error в react_to_admin:' + f'{e}')

@dp.callback_query_handler(lambda call: call.data == 'admin_exit')
async def answer_to_admin_exit(call: CallbackQuery):
    try:
        await call.answer('😜 До новых встреч!')
        db = collection.find_one({"user_id": call.from_user.id})
        if len(db['chats']) >= 1:
            lic = 'Лицензии нет'
            if db['lic'] != 'None': lic = db['lic']
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'👤 Ваш профиль:\n\n<b>Пользователь:</b> #{db["inlineid"]} - {db["register_data"]}\n<b>Username:</b> @{call.from_user.username}\n<b>Имя:</b> {call.from_user.first_name}\n<b>Чатов:</b> {len(db["chats"])}\n<b>Лицензий:</b> {db["lic"]}',
                                        reply_markup=generate_add_button())
        else:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=t_start_text.format(bot_user=t_bot_user),
                                        reply_markup=generate_add_button())
    except Exception as e:
        print('Error в answer_to_admin_exit:' + f'{e}')

@dp.callback_query_handler(lambda call: call.data == 'admin_add')
async def answer_to_admin_add(call: CallbackQuery):
    try:
        await call.answer()
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(call.message.chat.id, '👮 Введите юзернейм или прямую сслку на пользователя:')
        await MySceneStates.add_admin.set()
    except Exception as e:
        print('Error в answer_to_admin_add:' + f'{e}')

@dp.callback_query_handler(lambda call: call.data == 'admin_post')
async def answer_to_admin_post(call: CallbackQuery):
    try:
        await call.answer()
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(call.message.chat.id, '💬 Отправьте сообщение, которое хотите отправить всем пользователям своего бота:')
        await MySceneStates.post_to_users.set()
    except Exception as e:
        print('Error в answer_to_admin_post:' + f'{e}')

@dp.callback_query_handler(lambda call: call.data == 'admin_bot_stats')
async def answer_to_admin_stats(call: CallbackQuery):
    try:
        db = collection.find_one({'_id': ObjectId('64987b1eeed9918b13b0e8b4')})
        await call.answer()
        await bot.edit_message_text(text=f'📊 Общая статистика бота:\n\n<b>Кол-во пользователей:</b> {len(db["users"])}\n<b>Кол-во чатов с ботом:</b> {len(db["groups"])}\n<b>Кол-во купленных лицензий за все время:</b> {db["lics_buyed"]}\n<b>Кол-во заработанных денег за все время:</b> {db["earned"]}₽\n<b>Кол-во чатов с лицензией:</b> {len(db["chat_with_lics"])}', chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=generate_admin_return())
    except Exception as e:
        print('Error в answer_to_admin_stats:' + f'{e}')


@dp.callback_query_handler(lambda call: call.data == 'admin_stats_back')
async def answer_to_admin_back(call: CallbackQuery):
    try:
        await call.answer()
        await bot.edit_message_text(text=f'Добро пожаловать в админку, <a href="tg://user?id={call.from_user.id}">{call.from_user.first_name}</a>', chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=generate_admin_main_page())
    except Exception as e:
        print('Error в answer_to_admin_back:' + f'{e}')

@dp.callback_query_handler(lambda call: call.data == 'admin_deleteposition')
async def answer_to_admin_deleteposition(call: CallbackQuery):
    try:
        db = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
        if len(db['price']) == 0: return await bot.send_message(call.message.chat.id, call.message.message_id, text='⚠ Извините, но я не нашел ни одну позицию в базе данных')
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'⬇ <b>Выберите позицию которую хотите удалить:</b>', reply_markup=generate_delete_positions())
    except Exception as e:
        print('Error в answer_to_admin_deleteposition:' + f'{e}')

@dp.callback_query_handler(lambda call: call.data == 'admin_addposition')
async def answer_to_admin_admin_addposition(call: CallbackQuery):
    try:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await MySceneStates.addposition_period_scene.set()
        await bot.send_message(chat_id=call.message.chat.id, text='✍ Введите срок действия лицензии в днях:')
    except Exception as e:
        print('Error в answer_to_admin_admin_addposition:' + f'{e}')

@dp.callback_query_handler(lambda call: call.data == 'admin_editposition')
async def answer_to_admin_admin_editposition(call: CallbackQuery):
    try:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⬇ Выберите позицию которую хотите изменить:', reply_markup=generate_eidit_positions())
    except Exception as e:
        print('Error в answer_to_admin_admin_editposition:' + f'{e}')

@dp.callback_query_handler(lambda call: 'positedite' in call.data)
async def answer_to_admin_positedite(call: CallbackQuery):
    try:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        db = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
        index_of_possition = None
        for index, item in enumerate(db['price']):
            if item.get("period") == call.data.split("_")[1]:
                index_of_possition = index
                break
        await bot.send_message(chat_id=call.message.chat.id, text=f'⬇ Выберите то, что бы вы хотели изменить в этой позиции:\n\n<b>{db["price"][index_of_possition]["period"]}</b> дней - <b>{db["price"][index_of_possition]["price"]}</b>₽', reply_markup=generate_positedit())
        collection.find_one_and_update({"_id": ObjectId('64987b1eeed9918b13b0e8b4')},
                                          {"$set": {"positindx": index_of_possition, "positeddays": 'None', "positedprice": 'None'}})
    except Exception as e:
        print('Error в answer_to_admin_positedite:' + f'{e}')

@dp.callback_query_handler(lambda call: call.data == 'posited_days')
async def answer_to_admin_posited_days(call: CallbackQuery):
    try:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await MySceneStates.posited_days_scene.set()
        await bot.send_message(call.message.chat.id, text='✍ Введите срок действия лицензии в днях:')
    except Exception as e:
        print('Error в answer_to_admin_posited_days:' + f'{e}')

@dp.callback_query_handler(lambda call: call.data == 'posited_price')
async def answer_to_admin_posited_price(call: CallbackQuery):
    try:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await MySceneStates.posited_price_scene.set()
        await bot.send_message(call.message.chat.id, text='✍ Введите сумму которую заплатит пользователь при покупке(Значение должно быть в десятичном-float формате. Пример: 100.0 | 250.0):')
    except Exception as e:
        print('Error в answer_to_admin_posited_price:' + f'{e}')

@dp.callback_query_handler(lambda call: call.data == 'posited_cancel')
async def answer_to_admin_posited_cancel(call: CallbackQuery):
    try:
        db = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
        prices = ''
        unsortedp = db['price']
        positions = sorted(unsortedp, key=lambda x: int(x['period']))
        for i in positions:
            prices += f'🔹 {i["period"]} дней – {i["price"]}₽\n'
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id,
                             text=f'💎 <b>Прайс-лист:</b>\n{prices}\nВыберите действие:',
                             reply_markup=generate_admin_price_edit_choice())
    except Exception as e:
        print('Error в answer_to_admin_posited_cancel:' + f'{e}')

@dp.callback_query_handler(lambda call: call.data == 'posited_accept')
async def answer_to_admin_posited_accept(call: CallbackQuery):
    try:
        db = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
        if db['positeddays'] == "None" and db['positedprice'] == "None": return await call.answer('Вы ещё ничего не изменили 😶',
                                                                              show_alert=True)
        if db['positeddays'] != 'None': collection.find_one_and_update({"_id": ObjectId('64987b1eeed9918b13b0e8b4')}, {
            "$set": {f'price.{db["positindx"]}.period': db['positeddays']}})
        if db['positedprice'] != 'None': collection.find_one_and_update({"_id": ObjectId('64987b1eeed9918b13b0e8b4')}, {
            "$set": {f'price.{db["positindx"]}.price': db['positedprice']}})
        await call.answer('Успешное изменение ✅')
        db = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
        prices = ''
        unsortedp = db['price']
        positions = sorted(unsortedp, key=lambda x: int(x['period']))
        for i in positions:
            prices += f'🔹 {i["period"]} дней – {i["price"]}₽\n'
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id,
                             text=f'💎 <b>Прайс-лист:</b>\n{prices}\nВыберите действие:',
                             reply_markup=generate_admin_price_edit_choice())
    except Exception as e:
        print('Error в answer_to_admin_posited_accept:' + f'{e}')


@dp.callback_query_handler(lambda call: call.data == 'aedit_limittousers')
async def answer_to_admin_aedit_limittousers(call: CallbackQuery):
    try:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await MySceneStates.aedit_limittousers_scene.set()
        await bot.send_message(call.message.chat.id, text='✍ Введите лимит пользователей на чаты, в которых отсутсвует лицензия:')
    except Exception as e:
        print('Error в answer_to_admin_aedit_limittousers:' + f'{e}')

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
        print('Error в react_to_admin_positdelete:' + f'{e}')

@dp.callback_query_handler(lambda call: call.data == 'back_to_edit_price')
async def answer_to_admin_back_to_edit_price(call: CallbackQuery):
    db = collection.find_one({"_id": ObjectId('64987b1eeed9918b13b0e8b4')})
    prices = ''
    unsortedp = db['price']
    positions = sorted(unsortedp, key=lambda x: int(x['period']))
    for i in positions:
        prices += f'🔹 {i["period"]} дней – {i["price"]}₽\n'
    await call.answer()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                   text=f'💎 <b>Прайс-лист:</b>\n{prices}\nВыберите действие:',
                                   reply_markup=generate_admin_price_edit_choice())

@dp.callback_query_handler(lambda call: call.data == 'back_from_added_position')
async def answer_to_admin_back_from_added_position(call: CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    db = collection.find_one({'_id': ObjectId('64987b1eeed9918b13b0e8b4')})
    if call.from_user.id not in db['admins'] and call.from_user.id != int(
        config['MAIN_ADMIN_ID']): return await call.answer('🔒')
    await bot.send_message(chat_id=call.message.chat.id,
                           text=f'Добро пожаловать в админку, <a href="tg://user?id={call.from_user.id}">{call.from_user.first_name}</a>',
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
        else:
            await ctx.answer('👮 Введите юзернейм пользователя через @ или прямую ссылку на пользователя:')
            await state.finish()
            return await MySceneStates.add_admin.set()

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
        if e.args[0] == "'NoneType' object is not subscriptable":
            await ctx.answer('Пользователь не найден 🤷‍♂')
            await ctx.answer(text=f'Добро пожаловать в админку, <a href="tg://user?id={ctx.from_user.id}">{ctx.from_user.first_name}</a>',
                                   reply_markup=generate_admin_main_page())

@dp.message_handler(content_types=['text'], state=MySceneStates.aedit_limittousers_scene)
async def aedit_limittousers_scene(ctx: Message, state: FSMContext):
    try:
        text = ctx.text
        if text.isdigit() == False or (len(text) >= 2 and text[0] == '0'): return await ctx.answer('✋ Значение должно быть целым числом, введите ещё раз:')
        toint = int(ctx.text)
        collection.find_one_and_update({'_id': ObjectId('64987b1eeed9918b13b0e8b4')}, {"$set": {"limit_to_users": toint}})
        await ctx.answer('Успешное изменение ✅')
        await state.finish()
        db = collection.find_one({'_id': ObjectId('64987b1eeed9918b13b0e8b4')})
        await ctx.answer(text=f'✋ <b>Лимиты:</b>\n<b>Лимит количества пользователей на чат:</b> {db["limit_to_users"]}\n\nВыберите лимит который хотите изменить:', reply_markup=generate_admin_limit_edit_choice())
    except Exception as e:
        print('Error в aedit_limittousers_scene:' + f'{e}')

@dp.message_handler(content_types=['text'], state=MySceneStates.posited_days_scene)
async def posited_days_scene(ctx: Message, state: FSMContext):
    try:
        text = ctx.text.replace('d', '').replace('д', '').replace('дней', '')
        if text.isdigit() == False:
            await state.finish()
            await MySceneStates.posited_days_scene.set()
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
            return await MySceneStates.posited_days_scene.set()
        collection.find_one_and_update({'_id': ObjectId('64987b1eeed9918b13b0e8b4')}, {"$set": {"positeddays": text}})
        db = collection.find_one({'_id': ObjectId('64987b1eeed9918b13b0e8b4')})
        await state.finish()
        if db["positedprice"] == 'None': return await ctx.answer(text=f'⬇ Выберите то, что бы вы хотели изменить в этой позиции:\n\n<b>{db["positeddays"]}</b> дней - <b>{db["price"][db["positindx"]]["price"]}</b>₽',
                               reply_markup=generate_positedit())
        await ctx.answer(text=f'⬇ Выберите то, что бы вы хотели изменить в этой позиции:\n\n<b>{db["positeddays"]}</b> дней - <b>{db["positedprice"]}</b>₽',
                               reply_markup=generate_positedit())
    except Exception as e:
        print('Error в posited_days_scene:' + f'{e}')

@dp.message_handler(content_types=['text'], state=MySceneStates.posited_price_scene)
async def posited_price_scene(ctx: Message, state: FSMContext):
    try:
        trahstext = ctx.text.replace('₽', '').replace('р', '').replace('рублей', '')
        text = remove_non_digits_and_dot(trahstext)
        check = has_decimal_point(text)
        if check == False:
            await ctx.answer(
                '✋ Вы ввели значение в неправильном формате\n\nВведите сумму которую заплатит пользователь при покупке(Значение должно быть в десятичном-float формате. Пример: 100.0 | 250.0):')
            await state.finish()
            return await MySceneStates.posited_price_scene.set()

        text_to_float = float(text)

        collection.find_one_and_update({'_id': ObjectId('64987b1eeed9918b13b0e8b4')},
                                       {"$set": {'positedprice': text_to_float}})
        await state.finish()
        db = collection.find_one({'_id': ObjectId('64987b1eeed9918b13b0e8b4')})
        if db["positeddays"] == 'None': return await ctx.answer(text=f'⬇ Выберите то, что бы вы хотели изменить в этой позиции:\n\n<b>{db["price"][db["positindx"]]["period"]}</b> дней - <b>{db["positedprice"]}</b>₽',
                               reply_markup=generate_positedit())
        await ctx.answer(text=f'⬇ Выберите то, что бы вы хотели изменить в этой позиции:\n\n<b>{db["positeddays"]}</b> дней - <b>{db["positedprice"]}</b>₽',
            reply_markup=generate_positedit())
    except Exception as e:
        print('Error в posited_price_scene:' + f'{e}')

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
        print('Error в addposition_period_scene:' + f'{e}')

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
        print('Error в addposition_price_scene:' + f'{e}')

@dp.message_handler(content_types=ContentTypes.ANY, state=MySceneStates.post_to_users)
async def post_scene(ctx: Message, state: FSMContext):
    try:
        db = collection.find_one({'_id': ObjectId('64987b1eeed9918b13b0e8b4')})
        msgidtoedit = await ctx.answer('🔄️ Ваше сообщение рассылается по всем пользователям')
        asyncio.create_task(message_to_users(ctx, db['users'], msgidtoedit.message_id))
        await state.finish()
        await ctx.answer(text=f'Добро пожаловать в админку, <a href="tg://user?id={ctx.from_user.id}">{ctx.from_user.first_name}</a>',
                               reply_markup=generate_admin_main_page())
    except Exception as e:
        print('Error в post_scene:' + f'{e}')

async def message_to_users(ctx, users: list, id):
    try:
        for i in users:
            try:
                if i == ctx.chat.id: continue
                await bot.copy_message(i, from_chat_id=ctx.chat.id, message_id=ctx.message_id)
                await asyncio.sleep(0.4)
            except:
                print('msg_t_users - user blocked the bot')
        await bot.edit_message_text('Отправка завершена ✅', ctx.chat.id, id)
    except Exception as e:
        print('Error в message_to_users:' + f'{e}')

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
        print('Error в convert_to_id:' + f'{e}')


