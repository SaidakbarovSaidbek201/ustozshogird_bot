from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

start_keyboards = ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboards.add(KeyboardButton('Hodim kerak'), KeyboardButton('Ish joyi kerak'))