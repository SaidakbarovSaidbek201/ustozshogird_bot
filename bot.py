import logging
import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards import start_keyboards
from config import API_TOKEN

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

bot = Bot(token=API_TOKEN)
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
    await message.answer("Assalomu aleykum mening ustoz-shogirt botga xush kelibsiz!!!", reply_markup=start_keyboards)

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

