#!/usr/bin/env python
# -*- coding: utf-8 -*-
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from load import bot, dp
from aiogram import types
from FormaAdmin import *
from keyboard import*
from database import*
from config import*
from Forma import*
import asyncio
from traits import*
import time
from FormaAdmin import*
from aiogram.types import InputMediaPhoto, InputMediaVideo




generator = Generator()
btn = Button()
db = Database()


@dp.callback_query_handler(lambda c: c.data == "buy_cinema")
async def process_buy_cinema(callback_query: types.CallbackQuery):
    # Удаляем предыдущее сообщение
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

    await bot.answer_callback_query(callback_query.id)

    await Forma.s1.set()


    await bot.send_message(
        callback_query.from_user.id,
        text="""*Қанша номерок алғыңыз келеді?
Цифрмен жазыңыз👇🏻

1000 тг 5 номер
2000 тг 10 номер
3000 тг 15 номер
4000 тг 20 номер
5000 тг 25 номер
6000 тг 30 номер
7000 тг 35 номер
8000 тг 40 номер
9000 тг 45 номер
10000 тг 50 номер
20000 тг 100 номер
40000 тг 200 номер
100000 тг 500 номер

Номерок көп болған сайын курсқа
доступ көбейеді, және көлік иесі болу мүмкіндігі жоғары🔥*""",
        parse_mode="Markdown",
        reply_markup=btn.digits_and_cancel()
    ) 
  

@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def get_file_id(message: types.Message):
    if message.document.mime_type == 'application/pdf':
        file_id = message.document.file_id
        await message.reply(f"File ID: {file_id}")


@dp.message_handler(commands=['get_last_message'])
async def get_last_message_handler(message: types.Message):
    try:
        # Use the current chat ID from the message
        chat_id = message.chat.id

        # Fetch the chat details
        chat_info = await bot.get_chat(chat_id)

        # Fetch the most recent messages using bot.get_updates workaround
        updates = await bot.get_updates(limit=1000)

        # Extract message from the update
        if updates and updates[0].message:
            last_msg = updates[0].message
            last_message_id = last_msg.message_id
            last_message_text = last_msg.text or "<No text content>"

            # Send the message ID and text to the user
            await message.answer(
                f"Chat Title: {chat_info.title}\n"
                f"Message ID: {last_message_id}\n"
                f"Text: {last_message_text}"
            )
        else:
            await message.answer("No recent messages found in this chat.")

    except Exception as e:
        await message.answer(f"An error occurred: {e}")


@dp.message_handler(commands=['admin'])
async def handler(message: types.Message):
    print(message.from_user.id)
    if message.from_user.id == admin or message.from_user.id == admin2 or message.from_user.id == admin3:
        await bot.send_message(
        message.from_user.id,
        text="😊 *Сәлеметсіз бе %s !\nСіздің статусыңыз 👤 Админ(-ка-)*"%message.from_user.first_name,
        parse_mode="Markdown",
        reply_markup=btn.admin()
    )

message_history = {
    800703982: {
        2: "Your last message here."
    }
}

user_message_history = {}

def store_message(user_id, message_id, text):
    if user_id not in user_message_history:
        user_message_history[user_id] = deque(maxlen=10)
    user_message_history[user_id].appendleft((message_id, text))

async def get_last_10_messages(user_id):
    return user_message_history.get(user_id, [])

@dp.message_handler(commands=['last'])
async def send_last_messages(message: types.Message):
    user_id = message.from_user.id
    last_messages = await get_last_10_messages(user_id)
    
    if last_messages:
        response = "\n".join([f"Message ID: {msg_id}, Text: {msg_text}" for msg_id, msg_text in last_messages])
    else:
        response = "No messages found."
    
    await bot.send_message(user_id, response)  
        
@dp.message_handler(commands=['start', 'go'])
async def start_handler(message: types.Message):
    print(message.from_user.id)
      
    from datetime import datetime
    fileId = "AgACAgIAAxkBAAM2ZyqsMcOMY4neGp3t-X2yaduSDzYAApbwMRu60lFJHQ7Lqp4MY34BAAMCAAN5AAM2BA"

    user_id = message.from_user.id
    user_name = f"@{message.from_user.username}"
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    db.JustInsert(user_id, user_name, time_now)  
    
    if db.CheckUserPaid(message.from_user.id) == True:
        await bot.send_photo(
            message.from_user.id,
            fileId,
            caption="""*Сәлеметсізбе құттықтаймыз?!😍

Сіз Кенбаева Айжамалдың авторлық “Кондитер бол” курсына қатыса отыра, құны 30.000.000🍋тұратын LEXUS GX 460 автокөлігінің иесі болуға шешім қабылдадыңыз🔥

Курс құны : 1000 - ақ теңге😱
Және курсқа доступ көбейте отыра, Автокөлікке де мүмкіндігіңізді көбейте аласыз‼️
Яғни,👇🏻
2000 тг - 10 номерок алып курсқа
(1 ай доступ)
5000 тг - 25 номерок алып курсқа
(2 ай доступ)
10000 тг - 50 номерок алып курсқа (шексіз доступ) ие боласыз, әрі автокөлікке мүмкіндігіңіз артады👏🏻

“Кондитер бол” курсында 6 түрлі торт рецепттерінің онлайн-видео нұсқасы беріледі.
🔺Дубайский шоколад
🔺Дубайский чизкейк
🔺Нутелла торт
🔺Тары чизкейк
🔺Milka торт
🔺Баноффипай Тарталетки*""",
            parse_mode="Markdown",
            protect_content=True,
            reply_markup=btn.menu(),
        )
        return

    await bot.send_photo(
        message.from_user.id,
        fileId,
        caption="""*Сәлеметсізбе құттықтаймыз?!😍

Сіз Кенбаева Айжамалдың авторлық “Кондитер бол” курсына қатыса отыра, құны 30.000.000🍋тұратын LEXUS GX 460 автокөлігінің иесі болуға шешім қабылдадыңыз🔥

Курс құны : 1000 - ақ теңге😱
Және курсқа доступ көбейте отыра, Автокөлікке де мүмкіндігіңізді көбейте аласыз‼️
Яғни,👇🏻
2000 тг - 10 номерок алып курсқа
(1 ай доступ)
5000 тг - 25 номерок алып курсқа
(2 ай доступ)
10000 тг - 50 номерок алып курсқа (шексіз доступ) ие боласыз, әрі автокөлікке мүмкіндігіңіз артады👏🏻

“Кондитер бол” курсында 6 түрлі торт рецепттерінің онлайн-видео нұсқасы беріледі.
🔺Дубайский шоколад
🔺Дубайский чизкейк
🔺Нутелла торт
🔺Тары чизкейк
🔺Milka торт
🔺Баноффипай Тарталетки*""",        
        parse_mode="Markdown",
        protect_content=True,
        reply_markup=btn.buy_cinema(),
    )

    
             
@dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.VIDEO, types.ContentType.DOCUMENT])
async def media_handler(message: types.Message, state: FSMContext):
    file_id = None

    # Проверяем тип контента
    if message.content_type == 'photo':
        # Получаем file_id самого большого размера фото
        file_id = message.photo[-1].file_id
    elif message.content_type == 'video':
        # Получаем file_id видео
        file_id = message.video.file_id
    elif message.content_type == 'document':
        # Проверяем, является ли документ PDF файлом
        if message.document.mime_type == 'application/pdf':
            # Получаем file_id для PDF файла
            file_id = message.document.file_id
        else:
            # Если документ не PDF, отправляем сообщение об ошибке
            await bot.send_message(
                message.from_user.id,
                text="Ошибка: загрузите PDF файл.",
            )
            return

    if file_id:
        # Сохраняем file_id в состоянии
        async with state.proxy() as data:
            data['file_id'] = file_id

        # Отправляем file_id пользователю
        await bot.send_message(
            message.from_user.id,
            text=f"*FileID: {data['file_id']}*",
            parse_mode="Markdown",
        )
    else:
        await bot.send_message(
            message.from_user.id,
            text="Ошибка: неизвестный тип медиафайла.",
        )  
 

@dp.message_handler(Text(equals="🎥 Бейне курстар"), content_types=['text'])
async def handler(message: types.Message):

    file_id = "BAACAgIAAxkBAAIMsGYOfL6V-0jAR11JZUN9v2NrKV-8AALORQAC_NNxSKAE1UMhWlFeNAQ"     

    await bot.send_video(message.from_user.id, file_id, protect_content=True)

    await bot.send_message(
        message.from_user.id,
        text="""*Видео материялдағы сұрақтарға жауап беріңіз!\n Сұрақтар саны 5\nСұрақтар 1 ...*""",
        parse_mode="Markdown",
        reply_markup=btn.cancel()
    ) 

@dp.message_handler(commands=['help'])
@dp.message_handler(Text(equals="📲 Байланыс номері"), content_types=['text'])
async def handler(message: types.Message):

    await bot.send_message(
        message.from_user.id,
        text="""*https://wa.me/+77769001919*""",
        parse_mode="Markdown",
    ) 


@dp.message_handler(Text(equals="📹 Курс беру"), content_types=['text'])
async def handler(message: types.Message):
    
    if message.from_user.id == admin or message.from_user.id == admin2 or message.from_user.id == admin3:
       # Первая группа медиафайлов
        media_group_1 = [
            InputMediaPhoto(media="AgACAgIAAxkBAAMeZyqoL2hcPlVl9zI4CuqW5m3R12sAAorwMRu60lFJ5hIbmqGY8gYBAAMCAAN5AAM2BA", protect_content=True),
            InputMediaVideo(media="BAACAgIAAxkBAAMOZyqe_nfopY8Q5-1w_WeTC7154m8AAjlnAAK60lFJ6L_NUPBTXrQ2BA", caption="*Дубайский чизкейк*", parse_mode="Markdown", protect_content=True),
            InputMediaPhoto(media="AgACAgIAAxkBAAMmZyqo72O6rOIDWCHVynSI-4-Ib8kAAo7wMRu60lFJNxy3QvbEieABAAMCAAN5AAM2BA", protect_content=True),
            InputMediaVideo(media="BAACAgIAAxkBAAMQZyqfeZNNl5pHS26pJUFDMqCBz-EAAjpnAAK60lFJkWKyJ47LKKc2BA", caption="*Баноффипай Тарталетки*", parse_mode="Markdown", protect_content=True),
            InputMediaPhoto(media="AgACAgIAAxkBAAMgZyqoVJ_aJdlmTsTeZNd_zSXrJnIAAovwMRu60lFJYJxv0s3qK2oBAAMCAAN5AAM2BA", protect_content=True),
            InputMediaVideo(media="BAACAgIAAxkBAAMSZyqfo_h18m4nswMZ1s39vYVw9zYAAjtnAAK60lFJvOXjvcm9ESM2BA", caption="*Дубайский шоколад*", parse_mode="Markdown", protect_content=True)
        ]

        # Вторая группа медиафайлов
        media_group_2 = [
            InputMediaPhoto(media="AgACAgIAAxkBAAMkZyqo0Z5XS8VdmQ5bGm1NkCq7U6oAAo3wMRu60lFJ22Wq-hMCB7ABAAMCAAN5AAM2BA", protect_content=True),
            InputMediaVideo(media="BAACAgIAAxkBAAMUZyqgEINrfKiWiimkNEzKijzyDZIAAj1nAAK60lFJbBRFB-tfEUQ2BA", caption="*Тарымен чизкейк*", parse_mode="Markdown", protect_content=True),
            InputMediaPhoto(media="AgACAgIAAxkBAAMaZyqndQUGGZtSINCdZxmGwXTSdBYAAofwMRu60lFJfbNFd-RW6JcBAAMCAAN5AAM2BA", protect_content=True),
            InputMediaVideo(media="BAACAgIAAxkBAAMWZyqgkGfWka-1f_eWUNiyI8f81rwAAj5nAAK60lFJVlhlilAwuYo2BA", caption="*Нутелла торт*", parse_mode="Markdown", protect_content=True),
            InputMediaPhoto(media="AgACAgIAAxkBAAMiZyqon452oco0ASVyHGqI1SRQXlkAAozwMRu60lFJv8e6Y5TV2dABAAMCAAN5AAM2BA", protect_content=True),
            InputMediaVideo(media="BAACAgIAAxkBAAMYZyqg2oywORWXAAEISx_bnPWMnHdqAAI_ZwACutJRSSPOQsKLE7CaNgQ", caption="*Milka торт*", parse_mode="Markdown", protect_content=True)
        ]

        # Отправляем первую группу медиафайлов
        await bot.send_media_group(
            chat_id=message.from_user.id,
            media=media_group_1,
            protect_content=True
        )

        # Отправляем вторую группу медиафайлов
        await bot.send_media_group(
            chat_id=message.from_user.id,
            media=media_group_2,
            protect_content=True
        )

        successful, failed = await ForwardMessage(file_id, user_ids, file_type, caption)
        await bot.send_message(admin, text=f"Сәтті жіберілді: {successful} қолданушыға\nҚателік болды: {failed} қолданушыға", reply_markup=btn.menu())
    


@dp.message_handler(Text(equals="💸 Money"), content_types=['text'])
async def handler(message: types.Message):
    
    if message.from_user.id == admin or message.from_user.id == admin2 or message.from_user.id == admin3:
        sum = db.get_money_sum()
        await bot.send_message(
                message.from_user.id,
                text="""*💳 Жалпы қаражат: %d*"""%sum,
                parse_mode="Markdown",
                reply_markup=btn.admin()
            )    

@dp.message_handler(Text(equals="📨 Хабарлама жіберу"), content_types=['text'])
async def handler(message: types.Message):
    if message.from_user.id == admin or message.from_user.id == admin2 or message.from_user.id == admin3:
        await FormaAdmin.s1.set()
        await bot.send_message(
                message.from_user.id,
                text="""*✏️ Хабарлама типін таңдаңыз*""",
                parse_mode="Markdown",
                reply_markup=btn.typeMsg()
            )     


@dp.message_handler(Text(equals="📨 Әкімшіге хабарлама"), content_types=['text'])
async def handler(message: types.Message):

    await bot.send_message(
        message.from_user.id,
        text="""*@senior_coffee_drinker +77769001919*\n""",
        parse_mode="Markdown",
    ) 

@dp.message_handler(commands=['buy'])
@dp.message_handler(Text(equals="📹 Қайтадан 📗 курс сатып алу"), content_types=['text'])
async def handler(message: types.Message):
    
    await Forma.s1.set()
    await bot.send_message(
            message.from_user.id,
            text="""Қанша номерок алғыңыз келеді?
Цифрмен жазыңыз👇🏻
Номерок көп болған сайын курсқа
доступ көбейеді, және көлік иесі болу мүмкіндігі жоғары🔥""",
            parse_mode="Markdown",
            reply_markup=btn.digits_and_cancel()
    )

"""
# Новый хендлер для обработки отправки PDF-файла
@dp.message_handler(content_types=types.ContentType.DOCUMENT, state='*')
async def pdf_received_handler(message: types.Message, state: FSMContext):
    # Проверяем, что отправленный файл — это PDF
    if message.document.mime_type == 'application/pdf':
        # Устанавливаем состояние Forma.s1
        await Forma.s1.set()
        # Отправляем сообщения, как при нажатии на кнопку "Қайтадан киноны сатып алу"
        await bot.send_message(
            message.from_user.id,
            text="*Билет саны көп болған сайын жүлдені ұту 📈 ықтималдығы соғырлым жоғары 😉👌*",
            parse_mode="Markdown",
        )
        await bot.send_message(
            message.from_user.id,
            text="*Қанша билет алғыңыз келеді? Билет саны көп болған сайын ұтыста жеңу ықтималдығы жоғары 😉*",
            parse_mode="Markdown",
            reply_markup=btn.digits_and_cancel()
        )
    else:
        # Если отправлен не PDF-файл, можно уведомить пользователя
        await message.reply("Тек, PDF файл жіберу керек!")
    
"""

@dp.message_handler(Text(equals="🎬 Киноны сатып алу"), content_types=['text'])
async def handler(message: types.Message):
    
    await Forma.s1.set()
    await bot.send_message(
            message.from_user.id,
            text="""*Қанша номерок алғыңыз келеді?
Цифрмен жазыңыз👇🏻
Номерок көп болған сайын курсқа
доступ көбейеді, және көлік иесі болу мүмкіндігі жоғары🔥*""",
            parse_mode="Markdown",
            reply_markup=btn.digits_and_cancel()
    ) 
    

@dp.message_handler(Text(equals="📑 Лото"), content_types=['text'])
async def send_just_excel(message: types.Message):
    if message.from_user.id == admin:
        db.create_loto_excel('./excell/loto.xlsx')
        await bot.send_document(message.from_user.id, open('./excell/loto.xlsx', 'rb'))

@dp.message_handler(Text(equals="👥 Қолданушылар саны"), content_types=['text'])
async def send_client_excel(message: types.Message):
    if message.from_user.id == admin or message.from_user.id == admin2 or message.from_user.id == admin3:
        db.create_client_excel('./excell/clients.xlsx')
        await bot.send_document(message.from_user.id, open('./excell/clients.xlsx', 'rb'))

@dp.message_handler(Text(equals="👇 Just Clicked"), content_types=['text'])
async def send_loto_excel(message: types.Message):
    if message.from_user.id == admin or message.from_user.id == admin2 or message.from_user.id == admin3:
        db.create_just_excel('./excell/just_users.xlsx')
        await bot.send_document(message.from_user.id, open('./excell/just_users.xlsx', 'rb'))
    


@dp.message_handler(Text(equals="📨 Хабарлама жіберу"), content_types=['text'])
async def handler(message: types.Message):

    await bot.send_message(
        message.from_user.id,
        text="""*@senior_coffee_drinker*""",
        parse_mode="Markdown",
        reply_markup=btn.admin()
    ) 

@dp.message_handler(commands=['mytickets'])
@dp.message_handler(Text(equals="🧧 Ұтыс билеттерім"), content_types=['text'])
async def handler(message: types.Message):

    id_user = message.from_user.id            # Get the user ID from the message
    loto_ids = db.FetchIdLotoByUser(id_user)  # Fetch the list of id_loto for this user
    
    if loto_ids:
        ids_formatted = ", ".join(map(str, loto_ids))  # Format the list as a comma-separated string
        response_text = f"Сіздің ұтыс билеттеріңіздің ID-лары: {ids_formatted}"
    else:
        response_text = "Сіздің ұтыс билетіңіз жоқ."

    await bot.send_message(
        message.from_user.id,
        text=response_text,
        parse_mode="Markdown",
        reply_markup=btn.menu()
    )


@dp.message_handler(commands=['subjects'])
@dp.message_handler(Text(equals="📹 Курс сабақтары"), content_types=['text'])
async def handler(message: types.Message):

    if message.from_user.id == admin or admin2:
        # Первая группа медиафайлов
        media_group_1 = [
            InputMediaPhoto(media="AgACAgIAAxkBAAMeZyqoL2hcPlVl9zI4CuqW5m3R12sAAorwMRu60lFJ5hIbmqGY8gYBAAMCAAN5AAM2BA", protect_content=True),
            InputMediaVideo(media="BAACAgIAAxkBAAMOZyqe_nfopY8Q5-1w_WeTC7154m8AAjlnAAK60lFJ6L_NUPBTXrQ2BA", caption="*Дубайский чизкейк*", parse_mode="Markdown", protect_content=True),
            InputMediaPhoto(media="AgACAgIAAxkBAAMmZyqo72O6rOIDWCHVynSI-4-Ib8kAAo7wMRu60lFJNxy3QvbEieABAAMCAAN5AAM2BA", protect_content=True),
            InputMediaVideo(media="BAACAgIAAxkBAAMQZyqfeZNNl5pHS26pJUFDMqCBz-EAAjpnAAK60lFJkWKyJ47LKKc2BA", caption="*Баноффипай Тарталетки*", parse_mode="Markdown", protect_content=True),
            InputMediaPhoto(media="AgACAgIAAxkBAAMgZyqoVJ_aJdlmTsTeZNd_zSXrJnIAAovwMRu60lFJYJxv0s3qK2oBAAMCAAN5AAM2BA", protect_content=True),
            InputMediaVideo(media="BAACAgIAAxkBAAMSZyqfo_h18m4nswMZ1s39vYVw9zYAAjtnAAK60lFJvOXjvcm9ESM2BA", caption="*Дубайский шоколад*", parse_mode="Markdown", protect_content=True)
        ]

        # Вторая группа медиафайлов
        media_group_2 = [
            InputMediaPhoto(media="AgACAgIAAxkBAAMkZyqo0Z5XS8VdmQ5bGm1NkCq7U6oAAo3wMRu60lFJ22Wq-hMCB7ABAAMCAAN5AAM2BA", protect_content=True),
            InputMediaVideo(media="BAACAgIAAxkBAAMUZyqgEINrfKiWiimkNEzKijzyDZIAAj1nAAK60lFJbBRFB-tfEUQ2BA", caption="*Тарымен чизкейк*", parse_mode="Markdown", protect_content=True),
            InputMediaPhoto(media="AgACAgIAAxkBAAMaZyqndQUGGZtSINCdZxmGwXTSdBYAAofwMRu60lFJfbNFd-RW6JcBAAMCAAN5AAM2BA", protect_content=True),
            InputMediaVideo(media="BAACAgIAAxkBAAMWZyqgkGfWka-1f_eWUNiyI8f81rwAAj5nAAK60lFJVlhlilAwuYo2BA", caption="*Нутелла торт*", parse_mode="Markdown", protect_content=True),
            InputMediaPhoto(media="AgACAgIAAxkBAAMiZyqon452oco0ASVyHGqI1SRQXlkAAozwMRu60lFJv8e6Y5TV2dABAAMCAAN5AAM2BA", protect_content=True),
            InputMediaVideo(media="BAACAgIAAxkBAAMYZyqg2oywORWXAAEISx_bnPWMnHdqAAI_ZwACutJRSSPOQsKLE7CaNgQ", caption="*Milka торт*", parse_mode="Markdown", protect_content=True)
        ]

        # Отправляем первую группу медиафайлов
        await bot.send_media_group(
            chat_id=message.from_user.id,
            media=media_group_1,
            protect_content=True
        )

        # Отправляем вторую группу медиафайлов
        await bot.send_media_group(
            chat_id=message.from_user.id,
            media=media_group_2,
            protect_content=True
        )
        return

    if db.CheckUserPaid(message.from_user.id):
        # Повторяем для платного пользователя
        await bot.send_media_group(
            chat_id=message.from_user.id,
            media=media_group_1,
            protect_content=True
        )

        await bot.send_media_group(
            chat_id=message.from_user.id,
            media=media_group_2,
            protect_content=True
        )
    else:
        await bot.send_message(
            message.from_user.id,
            text="Курсты сатып алыңыз!.",
            reply_markup=btn.buy_cinema()
        )
  


@dp.message_handler(Text(equals="🎁 Сыйлықтар"), content_types=['text'])
async def handler(message: types.Message):
    print(message.from_user.id)
    if message.from_user.id == admin or message.from_user.id == admin2 or message.from_user.id == admin3:
        await bot.send_message(
        message.from_user.id,
        text="😊 *🎁 Сыйлықтар*",
        parse_mode="Markdown",
        reply_markup=btn.gift()
    )

@dp.message_handler(Text(equals="🎁 1-ші сыйлық"), content_types=['text'])
async def handler(message: types.Message):
    if message.from_user.id in [admin, admin2, admin3]:
        steps = [50, 25, 10, 1]
        
        # Fetch 100 entries initially
        entries = db.fetch_random_loto_car(100)
        if not entries:
            await bot.send_message(
                message.from_user.id,
                text="No data available.",
                reply_markup=btn.gift()
            )
            return
        
        # Send the first 100 entries as one message
        first_batch = entries[:100]
        text = "\n\n".join([f"ID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}" for row in first_batch])
        for chunk in split_message(text):
            sent_message = await bot.send_message(
                message.from_user.id,
                text=chunk,
                reply_markup=btn.gift()
            )
            await asyncio.sleep(2)
            await bot.delete_message(message.from_user.id, sent_message.message_id)
        
        # Process subsequent steps by selecting random subsets
        current_entries = entries
        for step in steps:
            current_entries = random.sample(current_entries, step)
            if step == 1:
                row = current_entries[0]
                text = f"🎁 100 000 теңге\n\nID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}"
                await send_pdf_with_caption(message.from_user.id, row[0], text)
            else:
                text = "\n\n".join([f"ID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}" for row in current_entries])
                for chunk in split_message(text):
                    sent_message = await bot.send_message(
                        message.from_user.id,
                        text=chunk,
                        reply_markup=btn.gift()
                    )
                    await asyncio.sleep(5)
                    await bot.delete_message(message.from_user.id, sent_message.message_id)
            
            await asyncio.sleep(0.5) 


@dp.message_handler(Text(equals="🎁 2-ші сыйлық"), content_types=['text'])
async def handler(message: types.Message):

    if message.from_user.id in [admin, admin2, admin3]:
        steps = [50, 25, 10, 1]
        
        # Fetch 100 entries initially
        entries = db.fetch_random_loto_car(100)
        if not entries:
            await bot.send_message(
                message.from_user.id,
                text="No data available.",
                reply_markup=btn.gift()
            )
            return
        
        # Send the first 100 entries as one message
        first_batch = entries[:100]
        text = "\n\n".join([f"ID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}" for row in first_batch])
        for chunk in split_message(text):
            sent_message = await bot.send_message(
                message.from_user.id,
                text=chunk,
                reply_markup=btn.gift()
            )
            await asyncio.sleep(2)
            await bot.delete_message(message.from_user.id, sent_message.message_id)
        
        # Process subsequent steps by selecting random subsets
        current_entries = entries
        for step in steps:
            current_entries = random.sample(current_entries, step)
            if step == 1:
                row = current_entries[0]
                text = f"🎁 100 000 теңге\n\nID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}"
                await send_pdf_with_caption(message.from_user.id, row[0], text)
            else:
                text = "\n\n".join([f"ID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}" for row in current_entries])
                for chunk in split_message(text):
                    sent_message = await bot.send_message(
                        message.from_user.id,
                        text=chunk,
                        reply_markup=btn.gift()
                    )
                    await asyncio.sleep(5)
                    await bot.delete_message(message.from_user.id, sent_message.message_id)
            
            await asyncio.sleep(0.5) 

@dp.message_handler(Text(equals="🎁 3-ші сыйлық"), content_types=['text'])
async def handler(message: types.Message):

    if message.from_user.id in [admin, admin2, admin3]:
        steps = [50, 25, 10, 1]
        
        # Fetch 100 entries initially
        entries = db.fetch_random_loto_car(100)
        if not entries:
            await bot.send_message(
                message.from_user.id,
                text="No data available.",
                reply_markup=btn.gift()
            )
            return
        
        # Send the first 100 entries as one message
        first_batch = entries[:100]
        text = "\n\n".join([f"ID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}" for row in first_batch])
        for chunk in split_message(text):
            sent_message = await bot.send_message(
                message.from_user.id,
                text=chunk,
                reply_markup=btn.gift()
            )
            await asyncio.sleep(2)
            await bot.delete_message(message.from_user.id, sent_message.message_id)
        
        # Process subsequent steps by selecting random subsets
        current_entries = entries
        for step in steps:
            current_entries = random.sample(current_entries, step)
            if step == 1:
                row = current_entries[0]
                text = f"🎁 100 000 теңге\n\nID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}"
                await send_pdf_with_caption(message.from_user.id, row[0], text)
            else:
                text = "\n\n".join([f"ID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}" for row in current_entries])
                for chunk in split_message(text):
                    sent_message = await bot.send_message(
                        message.from_user.id,
                        text=chunk,
                        reply_markup=btn.gift()
                    )
                    await asyncio.sleep(5)
                    await bot.delete_message(message.from_user.id, sent_message.message_id)
            
            await asyncio.sleep(0.5)  

@dp.message_handler(Text(equals="🎁 4-ші сыйлық"), content_types=['text'])
async def handler(message: types.Message):

    if message.from_user.id in [admin, admin2, admin3]:
        steps = [50, 25, 10, 1]
        
        # Fetch 100 entries initially
        entries = db.fetch_random_loto_car(100)
        if not entries:
            await bot.send_message(
                message.from_user.id,
                text="No data available.",
                reply_markup=btn.gift()
            )
            return
        
        # Send the first 100 entries as one message
        first_batch = entries[:100]
        text = "\n\n".join([f"ID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}" for row in first_batch])
        for chunk in split_message(text):
            sent_message = await bot.send_message(
                message.from_user.id,
                text=chunk,
                reply_markup=btn.gift()
            )
            await asyncio.sleep(2)
            await bot.delete_message(message.from_user.id, sent_message.message_id)
        
        # Process subsequent steps by selecting random subsets
        current_entries = entries
        for step in steps:
            current_entries = random.sample(current_entries, step)
            if step == 1:
                row = current_entries[0]
                text = f"🎁 100 000 теңге\n\nID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}"
                await send_pdf_with_caption(message.from_user.id, row[0], text)
            else:
                text = "\n\n".join([f"ID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}" for row in current_entries])
                for chunk in split_message(text):
                    sent_message = await bot.send_message(
                        message.from_user.id,
                        text=chunk,
                        reply_markup=btn.gift()
                    )
                    await asyncio.sleep(5)
                    await bot.delete_message(message.from_user.id, sent_message.message_id)
            
            await asyncio.sleep(0.5) 

@dp.message_handler(Text(equals="🎁 5-ші сыйлық"), content_types=['text'])
async def handler(message: types.Message):

    if message.from_user.id in [admin, admin2, admin3]:
        steps = [50, 25, 10, 1]
        
        # Fetch 100 entries initially
        entries = db.fetch_random_loto_car(100)
        if not entries:
            await bot.send_message(
                message.from_user.id,
                text="No data available.",
                reply_markup=btn.gift()
            )
            return
        
        # Send the first 100 entries as one message
        first_batch = entries[:100]
        text = "\n\n".join([f"ID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}" for row in first_batch])
        for chunk in split_message(text):
            sent_message = await bot.send_message(
                message.from_user.id,
                text=chunk,
                reply_markup=btn.gift()
            )
            await asyncio.sleep(2)
            await bot.delete_message(message.from_user.id, sent_message.message_id)
        
        # Process subsequent steps by selecting random subsets
        current_entries = entries
        for step in steps:
            current_entries = random.sample(current_entries, step)
            if step == 1:
                row = current_entries[0]
                text = f"🎁 100 000 теңге\n\nID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}"
                await send_pdf_with_caption(message.from_user.id, row[0], text)
            else:
                text = "\n\n".join([f"ID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}" for row in current_entries])
                for chunk in split_message(text):
                    sent_message = await bot.send_message(
                        message.from_user.id,
                        text=chunk,
                        reply_markup=btn.gift()
                    )
                    await asyncio.sleep(5)
                    await bot.delete_message(message.from_user.id, sent_message.message_id)
            
            await asyncio.sleep(0.5)  

@dp.message_handler(Text(equals="🎁 6-шы сыйлық"), content_types=['text'])
async def handler(message: types.Message):

    if message.from_user.id in [admin, admin2, admin3]:
        steps = [50, 25, 10, 1]
        
        # Fetch 100 entries initially
        entries = db.fetch_random_loto_car(100)
        if not entries:
            await bot.send_message(
                message.from_user.id,
                text="No data available.",
                reply_markup=btn.gift()
            )
            return
        
        # Send the first 100 entries as one message
        first_batch = entries[:100]
        text = "\n\n".join([f"ID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}" for row in first_batch])
        for chunk in split_message(text):
            sent_message = await bot.send_message(
                message.from_user.id,
                text=chunk,
                reply_markup=btn.gift()
            )
            await asyncio.sleep(2)
            await bot.delete_message(message.from_user.id, sent_message.message_id)
        
        # Process subsequent steps by selecting random subsets
        current_entries = entries
        for step in steps:
            current_entries = random.sample(current_entries, step)
            if step == 1:
                row = current_entries[0]
                text = f"🎁 100 000 теңге\n\nID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}"
                await send_pdf_with_caption(message.from_user.id, row[0], text)
            else:
                text = "\n\n".join([f"ID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}" for row in current_entries])
                for chunk in split_message(text):
                    sent_message = await bot.send_message(
                        message.from_user.id,
                        text=chunk,
                        reply_markup=btn.gift()
                    )
                    await asyncio.sleep(5)
                    await bot.delete_message(message.from_user.id, sent_message.message_id)
            
            await asyncio.sleep(0.5)  

@dp.message_handler(Text(equals="🎁 7-ші сыйлық"), content_types=['text'])
async def handler(message: types.Message):

    if message.from_user.id in [admin, admin2, admin3]:
        steps = [50, 25, 10, 1]
        
        # Fetch 100 entries initially
        entries = db.fetch_random_loto_car(100)
        if not entries:
            await bot.send_message(
                message.from_user.id,
                text="No data available.",
                reply_markup=btn.gift()
            )
            return
        
        # Send the first 100 entries as one message
        first_batch = entries[:100]
        text = "\n\n".join([f"ID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}" for row in first_batch])
        for chunk in split_message(text):
            sent_message = await bot.send_message(
                message.from_user.id,
                text=chunk,
                reply_markup=btn.gift()
            )
            await asyncio.sleep(2)
            await bot.delete_message(message.from_user.id, sent_message.message_id)
        
        # Process subsequent steps by selecting random subsets
        current_entries = entries
        for step in steps:
            current_entries = random.sample(current_entries, step)
            if step == 1:
                row = current_entries[0]
                text = f"🎁 100 000 теңге\n\nID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}"
                await send_pdf_with_caption(message.from_user.id, row[0], text)
            else:
                text = "\n\n".join([f"ID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}" for row in current_entries])
                for chunk in split_message(text):
                    sent_message = await bot.send_message(
                        message.from_user.id,
                        text=chunk,
                        reply_markup=btn.gift()
                    )
                    await asyncio.sleep(5)
                    await bot.delete_message(message.from_user.id, sent_message.message_id)
            
            await asyncio.sleep(0.5)  



@dp.message_handler(Text(equals="🎁 8-ші сыйлық"), content_types=['text'])
async def handler(message: types.Message):

    if message.from_user.id in [admin, admin2, admin3]:
        steps = [50, 25, 10, 1]
        
        # Fetch 100 entries initially
        entries = db.fetch_random_loto_car(100)
        if not entries:
            await bot.send_message(
                message.from_user.id,
                text="No data available.",
                reply_markup=btn.gift()
            )
            return
        
        # Send the first 100 entries as one message
        first_batch = entries[:100]
        text = "\n\n".join([f"ID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}" for row in first_batch])
        for chunk in split_message(text):
            sent_message = await bot.send_message(
                message.from_user.id,
                text=chunk,
                reply_markup=btn.gift()
            )
            await asyncio.sleep(2)
            await bot.delete_message(message.from_user.id, sent_message.message_id)
        
        # Process subsequent steps by selecting random subsets
        current_entries = entries
        for step in steps:
            current_entries = random.sample(current_entries, step)
            if step == 1:
                row = current_entries[0]
                text = f"🎁 100 000 теңге\n\nID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}"
                await send_pdf_with_caption(message.from_user.id, row[0], text)
            else:
                text = "\n\n".join([f"ID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}" for row in current_entries])
                for chunk in split_message(text):
                    sent_message = await bot.send_message(
                        message.from_user.id,
                        text=chunk,
                        reply_markup=btn.gift()
                    )
                    await asyncio.sleep(5)
                    await bot.delete_message(message.from_user.id, sent_message.message_id)
            
            await asyncio.sleep(0.5)  


@dp.message_handler(Text(equals="🎁 9-шы сыйлық"), content_types=['text'])
async def handler(message: types.Message):

    if message.from_user.id in [admin, admin2, admin3]:
        steps = [50, 25, 10, 1]
        
        # Fetch 100 entries initially
        entries = db.fetch_random_loto_car(100)
        if not entries:
            await bot.send_message(
                message.from_user.id,
                text="No data available.",
                reply_markup=btn.gift()
            )
            return
        
        # Send the first 100 entries as one message
        first_batch = entries[:100]
        text = "\n\n".join([f"ID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}" for row in first_batch])
        for chunk in split_message(text):
            sent_message = await bot.send_message(
                message.from_user.id,
                text=chunk,
                reply_markup=btn.gift()
            )
            await asyncio.sleep(2)
            await bot.delete_message(message.from_user.id, sent_message.message_id)
        
        # Process subsequent steps by selecting random subsets
        current_entries = entries
        for step in steps:
            current_entries = random.sample(current_entries, step)
            if step == 1:
                row = current_entries[0]
                text = f"🎁 100 000 теңге\n\nID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}"
                await send_pdf_with_caption(message.from_user.id, row[0], text)
            else:
                text = "\n\n".join([f"ID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}" for row in current_entries])
                for chunk in split_message(text):
                    sent_message = await bot.send_message(
                        message.from_user.id,
                        text=chunk,
                        reply_markup=btn.gift()
                    )
                    await asyncio.sleep(5)
                    await bot.delete_message(message.from_user.id, sent_message.message_id)
            
            await asyncio.sleep(0.5)  

@dp.message_handler(Text(equals="🎁 10-шы сыйлық"), content_types=['text'])
async def handler(message: types.Message):

    if message.from_user.id in [admin, admin2, admin3]:
        steps = [50, 25, 10, 1]
        
        # Fetch 100 entries initially
        entries = db.fetch_random_loto_car(100)
        if not entries:
            await bot.send_message(
                message.from_user.id,
                text="No data available.",
                reply_markup=btn.gift()
            )
            return
        
        # Send the first 100 entries as one message
        first_batch = entries[:100]
        text = "\n\n".join([f"ID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}" for row in first_batch])
        for chunk in split_message(text):
            sent_message = await bot.send_message(
                message.from_user.id,
                text=chunk,
                reply_markup=btn.gift()
            )
            await asyncio.sleep(2)
            await bot.delete_message(message.from_user.id, sent_message.message_id)
        
        # Process subsequent steps by selecting random subsets
        current_entries = entries
        for step in steps:
            current_entries = random.sample(current_entries, step)
            if step == 1:
                row = current_entries[0]
                text = f"🎁 100 000 теңге\n\nID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}"
                await send_pdf_with_caption(message.from_user.id, row[0], text)
            else:
                text = "\n\n".join([f"ID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}" for row in current_entries])
                for chunk in split_message(text):
                    sent_message = await bot.send_message(
                        message.from_user.id,
                        text=chunk,
                        reply_markup=btn.gift()
                    )
                    await asyncio.sleep(5)
                    await bot.delete_message(message.from_user.id, sent_message.message_id)
            
            await asyncio.sleep(0.5) 

@dp.message_handler(Text(equals="◀️ Кері"), content_types=['text'])
async def handler(message: types.Message):

    if message.from_user.id == admin or message.from_user.id == admin2:
        await bot.send_message(
        message.from_user.id,
        text="😊 *Сәлеметсіз бе %s !\nСіздің статусыңыз 👤 Админ(-ка-)*"%message.from_user.first_name,
        parse_mode="Markdown",
        reply_markup=btn.admin()
    )

async def send_pdf_with_caption(user_id, id_loto, caption):
    loto_info = db.fetch_loto_by_id(id_loto)
    if not loto_info:
        await bot.send_message(user_id, text="PDF not found.")
        return

    receipt = loto_info[3]  # Adjusted index for receipt column
    pdf_path = f"/home/cinema/pdf/{receipt}"
    
    if os.path.exists(pdf_path):
        await bot.send_document(
            user_id,
            document=open(pdf_path, 'rb'),
            caption=caption,
            reply_markup=btn.gift()
        )
    else:
        await bot.send_message(user_id, text="PDF file not found.")



#
@dp.message_handler(Text(equals="🎁 🚗 Көлік"), content_types=['text'])
async def handler(message: types.Message):
    if message.from_user.id in [admin, admin2, admin3]:
        steps = [50, 25, 10, 1]
        
        # Fetch 100 entries initially
        entries = db.fetch_random_loto_car(100)
        if not entries:
            await bot.send_message(
                message.from_user.id,
                text="No data available.",
                reply_markup=btn.gift()
            )
            return
        
        # Send the first 100 entries as one message
        first_batch = entries[:100]
        text = "\n\n".join([f"ID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}" for row in first_batch])
        for chunk in split_message(text):
            sent_message = await bot.send_message(
                message.from_user.id,
                text=chunk,
                reply_markup=btn.gift()
            )
            await asyncio.sleep(2)
            await bot.delete_message(message.from_user.id, sent_message.message_id)
        
        # Process subsequent steps by selecting random subsets
        current_entries = entries
        for step in steps:
            current_entries = random.sample(current_entries, step)
            if step == 1:
                row = current_entries[0]
                text = f"🎁 🚗 Көлік\n\nID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}"
                await send_pdf_with_caption(message.from_user.id, row[0], text)
            else:
                text = "\n\n".join([f"ID Loto: {row[0]}\nContact: {row[1]}\nData Pay: {row[2]}" for row in current_entries])
                for chunk in split_message(text):
                    sent_message = await bot.send_message(
                        message.from_user.id,
                        text=chunk,
                        reply_markup=btn.gift()
                    )
                    await asyncio.sleep(5)
                    await bot.delete_message(message.from_user.id, sent_message.message_id)
            
            await asyncio.sleep(0.5)





