import logging
import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards import start_keyboards, contact_keyboard, shaharlar_kb, oyliklar_kb
from states import DataState
from config import ADMIN_CHAT_ID, API_TOKEN

# Setup logging
logging.basicConfig(level=logging.INFO)

# Connect to the SQLite database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create the users table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    name TEXT,
    surname TEXT,
    phone TEXT,
    username TEXT,
    user_id TEXT,
    place TEXT,
    info TEXT,
    time TEXT,
    money TEXT,
    moreinfo TEXT
)
''')
conn.commit()

bot = Bot(token=API_TOKEN, proxy="http://proxy.server:3128")
dp = Dispatcher(bot=bot, storage=MemoryStorage())

class Register(StatesGroup):
    name = State()
    surname = State()
    phone = State()
    place = State()
    info = State()
    tabletime = State()
    time = State()
    money = State()
    moreinfo = State()



@dp.message_handler(commands=['start'])  
async def salom_ber(message: types.Message):
    await message.answer(text=f"""Assalom alaykum {message.from_user.full_name}
UstozShogird kanalining NOrasmiy botiga xush kelibsiz!

/help yordam buyrugi orqali nimalarga qodir ekanligimni bilib oling!""", reply_markup=start_keyboards)


@dp.message_handler(commands=['help'])
async def yordam_ber(message: types.Message):
    await message.answer(text="""/start - Botni ishga tushirish\n/help - Yordam""")


@dp.message_handler(text="Ish joyi kerak")
async def ish_joyi_kerak(message: types.Message, state: DataState):
    await message.answer(text="""👨‍💻 Ish joyi topish uchun ariza berish

Hozir sizga birnecha savollar beriladi. 
Har biriga javob bering. 
Oxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.""")
    await state.update_data(status="Ish joyi kerak")
    await message.answer(text="🔖 Ism va Familiyangizni kiriting:")
    await DataState.ism_familiya.set()


@dp.message_handler(state=DataState.ism_familiya)
async def ism_familiya(message: types.Message, state: DataState):
    await state.update_data(ism_familiya=message.text)
    await message.answer(text="🧑 Yoshingizni kiriting:")
    await DataState.yosh.set()


@dp.message_handler(state=DataState.yosh)
async def yosh(message: types.Message, state: DataState):
    await state.update_data(yosh=message.text)
    await message.answer(text="📱 Qaysi texnologiyalardan foydalanishingiz kerak? (Masalan: Python, Java, C++)" )
    await DataState.texnologiya.set()


@dp.message_handler(state=DataState.texnologiya)
async def texnologiya(message: types.Message, state: DataState):
    await state.update_data(texnologiya=message.text)
    await message.answer(text="📞 Telefon raqamni yuboring:", reply_markup=contact_keyboard)
    await DataState.telefon.set()


@dp.message_handler(state=DataState.telefon, content_types=types.ContentType.CONTACT)  # contact
async def telefon(message: types.Message, state: DataState):
    await state.update_data(telefon=message.contact.phone_number)
    await message.answer(text="📍 Hududingizni tanlang:", reply_markup=shaharlar_kb)
    await DataState.hudud.set()


@dp.message_handler(state=DataState.hudud)
async def hudud(message: types.Message, state: DataState):
    await state.update_data(hudud=message.text)
    await message.answer(text="💸 Narx kiriting:", reply_markup=oyliklar_kb)
    await DataState.narx.set() 


@dp.callback_query_handler(state=DataState.narx)
async def narx(call: types.CallbackQuery, state: DataState):
    oylik = call.data
    await state.update_data(narx=oylik)
    await call.message.answer(text="👨‍💼 Kasbingizni kiriting: (Ishlaysizmi yoki o`qiysizmi?)")
    await DataState.kasb.set()


@dp.message_handler(state=DataState.kasb)
async def kasb(message: types.Message, state: DataState):
    await state.update_data(kasb=message.text)
    await message.answer(text="📅 Murojaat vaqtingizni kiriting:")
    await DataState.murojat_vaqti.set()


@dp.message_handler(state=DataState.murojat_vaqti)
async def murojat_vaqti(message: types.Message, state: DataState):
    await state.update_data(murojat_vaqti=message.text)
    await message.answer(text="🎯 Maqsadingizni qisqacha yozib bering:")
    await DataState.maqsad.set()


malumotlar = ''

@dp.message_handler(state=DataState.maqsad)
async def maqsad(message: types.Message, state: DataState):
    await state.update_data(maqsad=message.text)
    await message.answer(text="🤔 Ma'lumotlar to'g'rimi? (Ha / Yo`q)")
    all_data = await state.get_data()
    username = message.from_user.username if message.from_user.username else "Yo'q"
    global malumotlar
    malumotlar = f"""📝 Ma'lumotlar:
👨‍💼 Xodim: {all_data['ism_familiya']}
🕑 Yosh: {all_data['yosh']}
📚 Texnologiya: {all_data['texnologiya']} 
🇺🇿 Telegram: @{username}
📞 Aloqa: {all_data['telefon']} 
🌐 Hudud: {all_data['hudud']}
💰 Narxi: {all_data['narx']}
👨🏻‍💻 Kasbi: {all_data['kasb']}
🕰 Murojaat qilish vaqti: {all_data['murojat_vaqti']} 
🔎 Maqsad: {all_data['maqsad']} 
"""
    await message.answer(text=malumotlar)
    await DataState.ha_yoq.set()


@dp.message_handler(state=DataState.ha_yoq)
async def ha_yoq(message: types.Message, state: DataState):
    if message.text.lower() == "ha":
        all_data = await state.get_data()
        global malumotlar
        await bot.send_message(chat_id=ADMIN_CHAT_ID, text=malumotlar)
        await message.answer(text="✅ Arizangiz Adminga yuborildi.")
    else:
        await message.answer(text="❌ Arizangiz bekor qilindi.")
    await state.finish()

@dp.message_handler(lambda message: "Hodim kerak" in message.text)
async def royxatdan_otish(message: types.Message):
    await message.answer("Xodim topish uchun ariza berish. \nHozir sizga birnecha savollar beriladi.\nHar biriga javob bering.\nOxirida agar hammasi to'g'ri bo'lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.")
    await message.answer("🎓 Idora nomi?")
    await Register.name.set()

@dp.message_handler(state=Register.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📚 Texnologiya: Talab qilinadigan texnologiyalarni kiriting? (Masalan, Java, C++, C#)")
    await Register.surname.set()

@dp.message_handler(state=Register.surname)
async def process_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    contact = types.KeyboardButton(text="📞 Aloqa: ", request_contact=True)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(contact)
    await message.answer("📞 Aloqa: ", reply_markup=keyboard)
    await Register.phone.set()

@dp.message_handler(content_types=types.ContentType.CONTACT, state=Register.phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await Register.place.set()
    await message.answer("📍 Qaysi hududdansiz? Viloyat nomi, Toshkent shahar yoki Respublikani kiriting.")

@dp.message_handler(state=Register.place)
async def process_place(message: types.Message, state: FSMContext):
    await state.update_data(place=message.text)
    await message.answer("✍️ Mas'ul ism sharifi?")
    await Register.info.set()

@dp.message_handler(state=Register.info)
async def process_info(message: types.Message, state: FSMContext):
    await state.update_data(info=message.text)
    await message.answer("🕰 Murojaat qilish vaqti: Qaysi vaqtda murojaat qilish mumkin? Masalan, 9:00 - 18:00")
    await Register.tabletime.set()

@dp.message_handler(state=Register.tabletime)
async def process_tabletime(message: types.Message, state: FSMContext):
    await state.update_data(tabletime=message.text)
    await message.answer("🕰 Ish vaqtini kiriting?")
    await Register.time.set()

@dp.message_handler(state=Register.time)
async def process_time(message: types.Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.answer("💰 Maoshni kiriting?")
    await Register.money.set()

@dp.message_handler(state=Register.money)
async def process_money(message: types.Message, state: FSMContext):
    await state.update_data(money=message.text)
    await message.answer("‼️ Qo'shimcha ma'lumotlar?")
    await Register.moreinfo.set()

@dp.message_handler(lambda message: "Ha" in message.text)
async def order(message: types.Message, state: FSMContext):
    await("Javob adminga yuborildi!")


 
@dp.message_handler(lambda message: "Yoq" in message.text)
async def order(message: types.Message, state: FSMContext):
  await("Javob ochirildi!")

@dp.message_handler(state=Register.moreinfo)
async def process_moreinfo(message: types.Message, state: FSMContext):
    await state.update_data(moreinfo=message.text)

    data = await state.get_data()
    cursor.execute('INSERT INTO users (name, surname, phone, username, user_id, place, info, time, money, moreinfo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',(data['name'], data['surname'], data['phone'], message.from_user.username, message.from_user.id, data['place'], data['info'], data['tabletime'], data['time'], data['money'], data['moreinfo'])
    )
    conn.commit()
    await state.finish()


if __name__ == '__main__':
        executor.start_polling(dp, skip_updates=True)

