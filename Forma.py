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

        async with state.proxy() as data:
            data['count'] = int(message.text)

        sum = 2000 * data['count']

        async with state.proxy() as data:
            data['sum'] = sum
        
        media = [
            InputMediaPhoto(
                media=c1,
                caption="""*Инструкция:

Оплата жасау үшін сілтемеге өтіңіз: https://pay.kaspi.kz/pay/0wdcrpat
Мұнде міндетті түрде 2000 теңге төлену керек. Басқа сумма төлеп қойсаңыз, бот оқымайды және ақшаңыз қайтпайды. Қателеспей төлеңіз!

1. Төлем жасап болған соң чекті ПДФ файл арқылы жіберіңіз( фотода көрсетілгендей)

2. Төленетін сумма 2000 теңгенің біреуі болу керек

3. Төлем өткен соң бот сізге киноға билет нөмеріңізбен, киноларды жібереді

ПДФ файлымен чекті төменге жіберіңіз  👇*""",
                parse_mode="Markdown",
                protect_content=True
            ),
            InputMediaPhoto(
                media=c2,
                parse_mode="Markdown",
                protect_content=True
            ),
            InputMediaPhoto(
                media=c3,
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
            text="*Kaspi Pay - төлем жүйесін қолдана отыра 💳 төлем жасаңыз\nКиноның 💳 бағасы: %d теңге*"%sum,
            parse_mode="Markdown",
            reply_markup=btn.payment()
        ) 
        
    except Exception as e:
        print(e) 
        await Forma.s1.set()
        await bot.send_message(
            message.from_user.id,
            text="*Қанша билет алғыңыз келеді? Билет саны көп болған сайын ұтыста жеңу ықтималдығы жоғары 😉*",
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
        pdf_reader = PDFReader(file_path)
        pdf_reader.open_pdf()
        result = pdf_reader.extract_specific_info()
        pdf_reader.close_pdf()


        async with state.proxy() as data:
            data['data'] = message.text
            data['pdf_result'] = result
            data['fileName'] = file_name

        print(data['pdf_result'])
        if convert_currency_to_int(data['pdf_result'][2]) != data['sum']: 
            await bot.send_message(
                message.from_user.id,
                text="*Төленетін сумма қате!\nҚайталап көріңіз*",
                parse_mode="Markdown",
                reply_markup=btn.menu_not_paid()
            )  
            await state.finish() 
            return
        
        print(data['pdf_result'][4])

        if data['pdf_result'][4] == "Сатушының ЖСН/БСН 011225600097" or data['pdf_result'][4] == "ИИН/БИН продавца 011225600097":
        
            if db.CheckLoto(data['pdf_result'][3]) == True:
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
                text="Төлем жасаған соң чекті 📲 .pdf форматында жіберіңіз!\n\n*НАЗАР АУДАРЫҢЫЗ ЧЕКТІ МОДЕРАТОР ТЕКСЕРЕДІ\n\n ЕСКЕРТУ ❗️\nЖАЛҒАН ЧЕК ЖІБЕРУ НЕМЕСЕ БАСҚАДА ДҰЫРЫС ЕМЕС ЧЕКТЕР ЖІБЕРУ АВТОМАТТЫ ТҮРДЕ ҰТЫС ОЙЫННАН ШЫҒАРЫЛАДЫ*",
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
                data['pdf_result'][3],
                message.from_user.username,
                data['fileName'],  
                data['contact'],
                time_now,
            )

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
            text="*Құттықтаймыз сіз сәтті төлем жасадыңыз 👏\n\nҰтыс билеттерінің санын білу үшін \n🧧 Ұтыс билеттерім түймесін басыңыз 👇*",
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
    

