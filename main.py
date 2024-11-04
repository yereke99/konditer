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
        text="*Қанша билет алғыңыз келеді? Билет саны көп болған сайын ұтыста жеңу ықтималдығы жоғары 😉*",
        parse_mode="Markdown",
        reply_markup=btn.digits_and_cancel()
    ) 
  

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
    fileId = "BAACAgIAAxkBAAMbZyYiIKdnYAhaMDvwp6bckE-c6-4AAtFbAALQzjBJQEXId-9sVs42BA"

    user_id = message.from_user.id
    user_name = f"@{message.from_user.username}"
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    db.JustInsert(user_id, user_name, time_now)  
    
    if db.CheckUserPaid(message.from_user.id) == True:
        await bot.send_video(
            message.from_user.id,
            fileId,
            caption="""*Ассалаумағалейкум, бұл менің яғни Рамазан Амантайдың “Хотя бы кинода 3” фильмін жоғарғы сапада көруіңіз үшін ашылған ресми телеграм бот!✔️

“Хотя бы кинода 3” -  фильмін көргеніңіз үшін Алматы қаласынан 2 бөлмелі камфорт класстағы квартираны, 4 көлікті және 50 адамға 100 мың теңгеден сыйламақшымын! Киномды көру үшін “КИНОНЫ САТЫП АЛУ” кнопкасын басыңыз. 

Сәттілік жолдасыңыз болсын, қолдау білдіріп жатқаныңызға рахмет көрерменім!✊🏻*""",
            parse_mode="Markdown",
            protect_content=True,
            reply_markup=btn.menu(),
        )
        await bot.send_message(
            message.from_user.id,
            text="*Құрметті кино сүйер қауым бізді жоғалтып алмау үшін https://t.me/+69HQcxuN2uBlYzUy телеграмм каналаға және t.me/ramazan_amanatai_reserve_bot ботқа тіркеліп қойыңыздар*",
            parse_mode="Markdown",
        )
        return

    await bot.send_video(
        message.from_user.id,
        fileId,
        caption="""*Ассалаумағалейкум, бұл менің яғни Рамазан Амантайдың “Хотя бы кинода 3” фильмін жоғарғы сапада көруіңіз үшін ашылған ресми телеграм бот!✔️

“Хотя бы кинода 3” -  фильмін көргеніңіз үшін Алматы қаласынан 2 бөлмелі камфорт класстағы квартираны, 4 көлікті және 50 адамға 100 мың теңгеден сыйламақшымын! Киномды көру үшін “КИНОНЫ САТЫП АЛУ” кнопкасын басыңыз. 

Сәттілік жолдасыңыз болсын, қолдау білдіріп жатқаныңызға рахмет көрерменім!✊🏻*""",        
        parse_mode="Markdown",
        protect_content=True,
        reply_markup=btn.buy_cinema(),
    )

    await bot.send_message(
        message.from_user.id,
        text="*Құрметті кино сүйер қауым бізді жоғалтып алмау үшін https://t.me/+69HQcxuN2uBlYzUy телеграмм каналаға және t.me/ramazan_amanatai_reserve_bot ботқа тіркеліп қойыңыздар*",
        parse_mode="Markdown",
    )
    
             
@dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.VIDEO])
async def media_handler(message: types.Message, state: FSMContext):
    file_id = None

    # Проверяем тип контента
    if message.content_type == 'photo':
        # Получаем file_id самого большого размера фото
        file_id = message.photo[-1].file_id
    elif message.content_type == 'video':
        # Получаем file_id видео
        file_id = message.video.file_id

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
        text="""*https://wa.me/87086914391*""",
        parse_mode="Markdown",
    ) 


@dp.message_handler(Text(equals="🎞 Кино беру"), content_types=['text'])
async def handler(message: types.Message):
    
    if message.from_user.id == admin or message.from_user.id == admin2 or message.from_user.id == admin3:
        #file_id = "BAACAgIAAxkBAAHqn9lmzCTjZas-7lUDgSY-FAABVIBF21cAAjpVAAIxrGFKi6XARXI2nR41BA"
        #file_id = "BAACAgIAAxkBAAIBfmZVvFgHXNy6dEjDe2rDHuGlC3jrAALaTQAC1jOpSiMaJlO20CwKNQQ"
        first_cinema = "AgACAgIAAxkBAAID4GcjW6EeTHiQ7VJy2DcwPVpuJmabAALR4jEbeqEYSZhgzh3T2zCkAQADAgADeQADNgQ"
        second_cinema = "BAACAgIAAxkBAAMJZyYe7_WEAS_hyBFZjzgQDO7qnAkAAlBbAAKOvjFJsU2nPCIK1Wg2BA"   

        #user_ids = db.gatherC() 
        user_ids = [800703982, 6391833468]
        file_type = 'video'
        caption = """Құрметті 🎞  кино сүйер қауым\n\nСанаулы күннен соң сіздерге сатып алған кино билеттеріңіздің арасынан Mercedes авто 🚙 көлік сыйға берілетін болады және 15 адамның қарызын жауып беретін боламыз\nКино билеттеріңізді көру үшін төмендегі \n🧧 Ұтыс билеттерім - түймесін баса отыра көре аласыздар!\n\nСыйлықты ұтып алу мүмкіндігін арттыру үшін \n🎬 Қайтадан киноны - сатып алу түймесін баса отыра тағыда кино билетін ала аласыздар! Оған дәлел ретінде бірінші көлікті ұтып алған Ахметов Ғалым дәлел 10 билет алған\n\nКино билеттер барлығы РАНДОМНО ТҮРДЕ ОЙНАТЫЛАДЫ ЯҒНИ СИСТЕМА ӨЗІ ТАҢДАЙДЫ ❗️"""

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
        text="""*@senior_coffee_drinker*\n\nhttps://wa.me/77086914391""",
        parse_mode="Markdown",
    ) 


@dp.message_handler(Text(equals="🎬 Қайтадан киноны сатып алу"), content_types=['text'])
async def handler(message: types.Message):
    
    await Forma.s1.set()
    await bot.send_message(
            message.from_user.id,
            text="*Қанша билет алғыңыз келеді 😉?*",
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
            text="*Қанша билет алғыңыз келеді? Билет саны көп болған сайын ұтыста жеңу ықтималдығы жоғары 😉*",
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


@dp.message_handler(commands=['cinema'])
@dp.message_handler(Text(equals="🎞 Movie"), content_types=['text'])
async def handler(message: types.Message):

    if message.from_user.id == admin:
        cinema_capture = "AgACAgIAAxkBAAMLZyYfyW99I3vVDWIvAAHlhHep7QWgAAKl4TEb0M4wSQ24B5FVHE2jAQADAgADeQADNgQ"
        cinema = "BAACAgIAAxkBAAMJZyYe7_WEAS_hyBFZjzgQDO7qnAkAAlBbAAKOvjFJsU2nPCIK1Wg2BA"

        # Создаем список медиафайлов для отправки
        media = [
            InputMediaPhoto(
                media=cinema_capture,
                parse_mode="Markdown",
                protect_content=True
            ),
            InputMediaVideo(
                media=cinema,
                caption="*Хотя Бы Кинода 3*",  # Если нужно добавить подпись
                parse_mode="Markdown",
                protect_content=True
            ),
        ]

        # Отправляем медиафайлы как альбом
        await bot.send_media_group(
            chat_id=message.from_user.id,
            media=media,
            protect_content=True
        )
        return

    if db.CheckUserPaid(message.from_user.id) == True:
        cinema_capture = "AgACAgIAAxkBAAMLZyYfyW99I3vVDWIvAAHlhHep7QWgAAKl4TEb0M4wSQ24B5FVHE2jAQADAgADeQADNgQ"
        cinema = "BAACAgIAAxkBAAMJZyYe7_WEAS_hyBFZjzgQDO7qnAkAAlBbAAKOvjFJsU2nPCIK1Wg2BA"

        # Создаем список медиафайлов для отправки
        media = [
            InputMediaPhoto(
                media=cinema_capture,
                parse_mode="Markdown",
                protect_content=True
            ),
            InputMediaVideo(
                media=cinema,
                caption="*Хотя Бы Кинода 3*",  # Если нужно добавить подпись
                parse_mode="Markdown",
                protect_content=True
            ),
        ]

        # Отправляем медиафайлы как альбом
        await bot.send_media_group(
            chat_id=message.from_user.id,
            media=media,
            protect_content=True
        )
    
    await bot.send_message(
        message.from_user.id,
        text="Кино сатып алыңыз.",
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





