from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.message import Message
from load import dp, bot
from aiogram import types 
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import logging
from keyboard import*
from database import Database
import datetime
from main import*
import asyncio
from config import admin
from datetime import datetime
from traits import *
import time
from traits import*
from config import*
import os
from aiogram.types import InputMediaPhoto, InputMediaVideo

from test import PDFReaders



def calculate_sum(count):
    # Сопоставление количества номеров и суммы
    prices = {
        5: 1000,
        10: 2000,
        15: 3000,
        20: 4000,
        25: 5000,
        30: 6000,
        35: 7000,
        40: 8000,
        45: 9000,
        50: 10000,
        100: 20000,
        200: 40000,
        250: 50000,
        500: 100000
    }
    return prices.get(count, 0)



generator = Generator()
btn = Button()
db = Database()

# Dont touch!
#file_id = "BAACAgIAAxkBAAIBfmZVvFgHXNy6dEjDe2rDHuGlC3jrAALaTQAC1jOpSiMaJlO20CwKNQQ"  

c1 = "AgACAgIAAxkBAAMVZyYg7KuSuN_IPDYgM5ULXX7AzhkAAqzhMRvQzjBJDkg8df7HrdYBAAMCAAN5AAM2BA"
c2 = "AgACAgIAAxkBAAMXZyYg7ivtTtgaTt3uOn_SthmgAqQAAq3hMRvQzjBJKU9TV6vMYh4BAAMCAAN5AAM2BA"
c3 = "AgACAgIAAxkBAAMZZyYg8clEejb320N0ZrK_Jb5YAV8AAq7hMRvQzjBJhxNPNuDLOMkBAAMCAAN5AAM2BA"

# Ensure the directory exists
os.makedirs('./pdf/', exist_ok=True)

class Forma(StatesGroup):
    s1 = State()  
    s2 = State()
    s3 = State() 
    s4 = State()

@dp.message_handler(state='*', commands='🔕 Бас тарту')
@dp.message_handler(Text(equals='🔕 Бас тарту', ignore_case=True), state='*')
async def cancell_handler(message: types.Message, state: FSMContext):
    """
    :param message: Бастартылды
    :param state: Тоқтату
    :return: finish
    """
    
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Бас тарту!')
    
    await state.finish()
    await message.reply('Сіз тапсырыстан бас тарттыңыз.', reply_markup=btn.menu_not_paid())

@dp.message_handler(lambda message: not message.text.isdigit(), state=Forma.s1)
async def handler(message: types.Message):
    return await message.reply("Сандармен жазыңыз 🔢")

@dp.message_handler(lambda message: message.text.isdigit(), state=Forma.s1)
async def handler(message: types.Message, state: FSMContext):
    """
    state: number
    """
    try:
        await Forma.next()

        with open("/home/konditer/doc/offerta.pdf", 'rb') as doc:
            await bot.send_document(
            message.from_user.id,
            doc,
            caption="*📄 Оффертамен танысып алыңыз*",
            parse_mode="Markdown",
        )

        async with state.proxy() as data:
            data['count'] = int(message.text)

        # Вычисляем сумму с помощью функции calculate_sum
        total_sum = calculate_sum(data['count'])

        async with state.proxy() as data:
            data['sum'] = total_sum
        
        

        await bot.send_message(
            message.from_user.id,
            text="""*Инструкция:

Оплата жасау үшін сілтемеге өтіңіз: https://pay.kaspi.kz/pay/czlpep9g
Мұнде міндетті түрде 1000 теңге төлену керек. Басқа сумма төлеп қойсаңыз, бот оқымайды және ақшаңыз қайтпайды. Қателеспей төлеңіз!

1. Төлем жасап болған соң чекті ПДФ файл арқылы жіберіңіз

2. Төленетін сумма 1000, 2000, 5000 теңгенің біреуі болу керек

3. Төлем өткен соң бот сізге  нөмеріңізбен бейне сабақтарды жібереді

ПДФ файлымен чекті төменге жіберіңіз  👇*""",
            parse_mode="Markdown",
        ) 

        await bot.send_message(
            message.from_user.id,
            text="*Kaspi Pay - төлем жүйесін қолдана отыра 💳 төлем жасаңыз\nКурстың бағасы 💳 бағасы: %d теңге*"%total_sum,
            parse_mode="Markdown",
            reply_markup=btn.payment()
        ) 
        
    except Exception as e:
        print(e) 
        await Forma.s1.set()
        await bot.send_message(
            message.from_user.id,
            text="""*Қанша номер алғыңыз келеді?
Цифрмен жазыңыз👇🏻
Номерок көп болған сайын курсқа
доступ көбейеді, және көлік иесі болу мүмкіндігі жоғары*""",
            parse_mode="Markdown",
            reply_markup=btn.digits_and_cancel()
        )   

        await bot.send_message(
            admin,
            text="Error: %s"%str(e),
        )   


@dp.message_handler(lambda message: not (message.document and message.document.mime_type == 'application/pdf'), state=Forma.s2, content_types=types.ContentType.DOCUMENT)
async def pdf_validator(message: types.Message, state: FSMContext):
    await message.reply(".pdf файл форматымен жіберіңіз!")
    await Forma.s2.set()

@dp.message_handler(state=Forma.s2, content_types=types.ContentType.DOCUMENT)
async def handler(message: types.Message, state: FSMContext):

    try:
        document = message.document

        # Generate a unique filename
        user_id = message.from_user.id
        timestamp = int(time.time())
        random_int = Generator.generate_random_int()
        file_name = f"{user_id}_{timestamp}_{random_int}.pdf"
        file_path = os.path.join('./pdf/', file_name)

        # Download the PDF file
        file_info = await bot.get_file(document.file_id)
        await bot.download_file(file_info.file_path, file_path)

        # Process the PDF file
        pdf_reader = PDFReaders(file_path)
        pdf_reader.open_pdf()
        #result = pdf_reader.extract_specific_info()
        result = pdf_reader.extract_detailed_info()
        pdf_reader.close_pdf()


        async with state.proxy() as data:
            data['data'] = message.text
            data['pdf_result'] = result
            data['fileName'] = file_name


        print(data['pdf_result'])
        if convert_currency_to_int(data['pdf_result'][3]) != data['sum']: 
            await bot.send_message(
                message.from_user.id,
                text="*Төленетін сумма қате!\nҚайталап көріңіз*",
                parse_mode="Markdown",
                reply_markup=btn.menu_not_paid()
            )  
            await state.finish() 
            return
        
        print(data['pdf_result'][3])

        if data['pdf_result'][11] == "Сатушының ЖСН/БСН 020319550979" or data['pdf_result'][11] == "ИИН/БИН продавца 020319550979":
        
            if db.CheckLoto(data['pdf_result'][7]) == True:
                await bot.send_message(
                    message.from_user.id,
                    text="*ЧЕК ТӨЛЕНІП ҚОЙЫЛҒАН!\nҚайталап көріңіз*",
                    parse_mode="Markdown",
                    reply_markup=btn.menu_not_paid()
                )  
                await state.finish() 
                return
            
            await Forma.next()
            await bot.send_message(
                message.from_user.id,
                text="*Сізбен кері 📲 байланысқа шығу үшін байланыс нөміріңізді қалдырыңыз! Төменде тұрған \n\n📱 Контактімен бөлісу кнопкасын басыныз\n\nЕШҚАШАН САНДАРМЕН ЖАЗБАЙМЫЗ ‼️*",
                parse_mode="Markdown",
                reply_markup=btn.send_contact()
            )
            return
        
        await bot.send_message(
                message.from_user.id,
                text="*Дұрыс емес счетқа төледіңіз!\nҚайталап көріңіз*",
                parse_mode="Markdown",
                reply_markup=btn.menu_not_paid()
            )  
        await state.finish() 

    except Exception as e:
        print(e)
        await bot.send_message(
            admin,
            text="Error: %s"%str(e),
        ) 
        await Forma.s2.set()
        await bot.send_message(
                message.from_user.id,
                text="Төлем жасаған соң чекті 📲 .pdf форматында жіберіңіз!\n\n*НАЗАР АУДАРЫҢЫЗ ЧЕКТІ МОДЕРАТОР ТЕКСЕРЕДІ\n\n ЕСКЕРТУ ❗️\nЖАЛҒАН ЧЕК ЖІБЕРУ НЕМЕСЕ БАСҚАДА ДҰЫРЫС ЕМЕС ЧЕКТЕР ЖІБЕРУ КУРС САБАҚТАРЫНА ҚАТЫСТЫРЫЛМАЙДЫ*",
                parse_mode="Markdown",
                reply_markup=btn.cancel()
            ) 
        
        
@dp.message_handler(state=Forma.s3, content_types=types.ContentType.CONTACT)
async def handler(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['contact'] = message.contact.phone_number
    
    
    db.increase_money(data['sum'])

    if db.InsertClient(message.from_user.id, message.from_user.username,  data['contact'], datetime.now(), "paid", "true"):

        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for i in range(data['count']):
            gen = generator.generate_random_int()
            db.InsertLoto(
                message.from_user.id,
                gen,
                data['pdf_result'][7],
                message.from_user.username,
                data['fileName'],  
                data['contact'],
                time_now,
            )

        # Первая группа медиафайлов
        media_group_1 = [
            InputMediaPhoto(media="AgACAgIAAxkBAAEBJAFnRLiWe2sW6uzMSxdQR5Vv5BvsjgACkuIxG-J2KErj-vWtMknO6gEAAwIAA3kAAzYE", protect_content=True),
            InputMediaVideo(media="BAACAgIAAxkBAAMOZyqe_nfopY8Q5-1w_WeTC7154m8AAjlnAAK60lFJ6L_NUPBTXrQ2BA", caption="*Дубайский чизкейк*", parse_mode="Markdown", protect_content=True),
            InputMediaPhoto(media="AgACAgIAAxkBAAEBJANnRLieK-yegn4D4YTwfRiwsVLybAACk-IxG-J2KEr7BBNKvstEBwEAAwIAA3kAAzYE", protect_content=True),
            InputMediaVideo(media="BAACAgIAAxkBAAMQZyqfeZNNl5pHS26pJUFDMqCBz-EAAjpnAAK60lFJkWKyJ47LKKc2BA", caption="*Баноффипай Тарталетки*", parse_mode="Markdown", protect_content=True),
            InputMediaPhoto(media="AgACAgIAAxkBAAEBSLdnRygJHAxJWDkMQMZkSAGVc0HZuwACkOIxG-J2KEq4KuUTfT-0hwEAAwIAA3kAAzYE", protect_content=True),
            InputMediaVideo(media="BAACAgIAAxkBAAMSZyqfo_h18m4nswMZ1s39vYVw9zYAAjtnAAK60lFJvOXjvcm9ESM2BA", caption="*Дубайский шоколад*", parse_mode="Markdown", protect_content=True)
        ]

        # Вторая группа медиафайлов
        media_group_2 = [
            InputMediaPhoto(media="AgACAgIAAxkBAAEBJAVnRLiml_0Ps-gBE1SKEMqGud1XMwAClOIxG-J2KEo_QVeUpEFE_QEAAwIAA3kAAzYE", protect_content=True),
            InputMediaVideo(media="BAACAgIAAxkBAAMUZyqgEINrfKiWiimkNEzKijzyDZIAAj1nAAK60lFJbBRFB-tfEUQ2BA", caption="*Тарымен чизкейк*", parse_mode="Markdown", protect_content=True),
            InputMediaPhoto(media="AgACAgIAAxkBAAEBI_9nRLiO9Er8tsQ2SC1PPzRdEuJtwwACkeIxG-J2KErviLNZvNeEbAEAAwIAA3kAAzYE", protect_content=True),
            InputMediaVideo(media="BAACAgIAAxkBAAMWZyqgkGfWka-1f_eWUNiyI8f81rwAAj5nAAK60lFJVlhlilAwuYo2BA", caption="*Нутелла торт*", parse_mode="Markdown", protect_content=True),
            InputMediaPhoto(media="AgACAgIAAxkBAAEBJAdnRLisUDCzKv9zENjo9nz1kxZnoQACleIxG-J2KEqxP87JjThz1gEAAwIAA3kAAzYE", protect_content=True),
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

        await bot.send_message(
            message.from_user.id,
            text="*Құттықтаймыз сіз сәтті төлем жасадыңыз 👏\n\nКурс номерлерінің санын білу үшін \n🧧 Ұтыс билеттерім түймесін басыңыз 👇*",
            parse_mode="Markdown",
            reply_markup=btn.menu()
        )

        await state.finish()   
        return
    else:
        await bot.send_message(
            message.from_user.id,
            text="*Ой 🤨 бір нәрседен қате кетті\nҚайталап көріңіз*",
            parse_mode="Markdown",
            reply_markup=btn.menu_not_paid()
        )  
        await state.finish() 
    

