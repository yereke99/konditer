#!/usr/bin/env python
# -*- coding: utf-8 -*-
from aiogram import types
import datetime
from load import bot
from database import Database

class Button:
    def __init__(self) -> None:
        pass

    def _create_keyboard(self, btns):

        button = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        for btn in btns:
            button.add(btn)

        return button
    
    def payment(self):

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("💳 Төлем жасау", url="https://pay.kaspi.kz/pay/czlpep9g"))
        
        return keyboard
    
    def buy_cinema(self):

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("📗 💳 Курс сатып алу", callback_data="buy_cinema"))
        
        return keyboard
    
    
    def menu(self):
        return self._create_keyboard([
            "🧧 Ұтыс билеттерім",
            "📹 Курс сабақтары",
            "📹 Қайтадан 📗 курс сатып алу",
            "📨 Әкімшіге хабарлама",
            "📲 Байланыс номері",  
        ])

    def again(self):
        return self._create_keyboard([
            "📹 Қайтадан 📗 курс сатып алу"
        ])
       

    def loto(self):
        return self._create_keyboard([
            "🧧 Ұтыс билеттерім"
       ])
    
    def digits_and_cancel(self):
        # Используем ключи словаря prices для генерации кнопок
        prices = {
            1: 50,
            10: 500,
            20: 1000,
            30: 1500,
            40: 2000,
            50: 2500,
            80: 4000,
            100: 5000,
            200: 10000,
            500: 25000
        }
        buttons = [str(key) for key in prices.keys()]  # Преобразуем ключи в строки
        buttons.append("🔕 Бас тарту")  # Добавляем кнопку отмены
        return self._create_keyboard(buttons)

    def tg_link(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("📗 💳 Курс сатып алу", url="https://t.me/konditerbol_bot"))
        
        return keyboard


    def menu_not_paid(self):

        return self._create_keyboard([
            #"🎬 Киноны сатып алу",
            "📨 Әкімшіге хабарлама",  
            "📲 Байланыс номері", 
        ])
    
    def admin(self):

        return self._create_keyboard([
            "💸 Money",
            "👇 Just Clicked",
            "👥 Қолданушылар саны",
            "📑 Лото",
            "📨 Хабарлама жіберу",
            "📹 Курс беру",
            "🎁 Сыйлықтар",
        ])
    
    def gift(self):

        return self._create_keyboard([
            "🎁 1-ші сыйлық",
            "🎁 2-ші сыйлық",
            "🎁 3-ші сыйлық",
            "🎁 4-ші сыйлық",
            "🎁 5-ші сыйлық",
            "🎁 6-шы сыйлық",
            "🎁 7-ші сыйлық",
            "🎁 8-ші сыйлық",
            "🎁 9-шы сыйлық",
            "🎁 10-шы сыйлық",
            "🎁 11-ші сыйлық",
            "🎁 12-ші сыйлық",
            "🎁 13-ші сыйлық",
            "◀️ Кері",
        ])

    def typeMsg(self):

        return self._create_keyboard([
            "🖋 Текстік хабарлама",
            "🖼 Картинкалық хабарлама",
            "🗣 Аудио хабарлама",
            "📹 Бейне хабарлама",
            "🔕 Бас тарту",
        ])
    
    def typeUsers(self):

        return self._create_keyboard([
            "📑 Жалпы қолданушыларға",
            "💳 Төлем 🟢 жасаған 📊 қолданушаларға",
            "🔕 Бас тарту",
        ])
    
    
    def message(self):

        return self._create_keyboard([
            "📩 Жеке хабарлама",
            "📑 Жалпы қолданушыларға",
            "👇 Just Clicked",
            "💳 Төлем 🟢 жасаған 📊 қолданушаларға",
            "💳 Төлем 🔴 жасамаған 📊 қолданушаларға",
            "⬅️ Кері",
        ])
    
    def study(self):

        return self._create_keyboard([
            "💽 Бейне сабақтарды енгізу",
            "📋 Сабақтар тізімі",
            "⬅️  Кері",
        ])
    
    def cancel(self):

        return self._create_keyboard([
            "🔕 Бас тарту",
        ])
    
    def offerta(self):

        return self._create_keyboard([
            "🟢 Келісімімді беремін",
            "🔴 Жоқ, келіспеймін",
            "🔕 Бас тарту",
        ])
    
    def agreement(self):

        return self._create_keyboard([
            "🟢 Әрине",
            "🔴 Жоқ сенімді емеспін",
            "🔕 Бас тарту",
        ])
    
    def send_contact(self):

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(types.KeyboardButton("📱 Контактімен бөлісу", request_contact=True))

        return keyboard
