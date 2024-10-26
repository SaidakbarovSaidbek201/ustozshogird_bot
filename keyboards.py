from aiogram import types


# keyboardlar -> "Ish joyi kerak", "Hodim kerak"
start_keyboards = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        types.KeyboardButton(text="Ish joyi kerak"),
        types.KeyboardButton(text="Hodim kerak")
    ]
])


contact_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        types.KeyboardButton(text="Telefon raqamni yuborish", request_contact=True)
    ]
])

shaharlar_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        types.KeyboardButton(text="Toshkent"), types.KeyboardButton(text="Andijon"), types.KeyboardButton(text="Buxoro")
    ],
    [
        types.KeyboardButton(text="Farg`ona"), types.KeyboardButton(text="Jizzax"), types.KeyboardButton(text="Xorazm")
    ],
    [
        types.KeyboardButton(text="Namangan"), types.KeyboardButton(text="Navoiy"), types.KeyboardButton(text="Qashqadaryo")
    ],
    [
        types.KeyboardButton(text="Surxondaryo"), types.KeyboardButton(text="Samarqand"), types.KeyboardButton(text="Sirdaryo")
    ],
    [
        types.KeyboardButton(text="Qoraqalpog`iston")
    ]
])


oyliklar_kb = types.InlineKeyboardMarkup(inline_keyboard=[
    [
        types.InlineKeyboardButton(text="0$", callback_data="0$"),
        types.InlineKeyboardButton(text="100$ - 500$", callback_data="100$ - 500$")
    ],
    [
        types.InlineKeyboardButton(text="500$ - 1000$", callback_data="500$ - 1000$"),
        types.InlineKeyboardButton(text="1000$+", callback_data="1000$+")
    ]
])
