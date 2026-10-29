import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.filters import Command

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# ================= НАСТРОЙКИ =================
BOT_TOKEN = '9150380238:AAF4tJqfU9Rs4MRfQatwA1z8_nWsGDw011U'

# ID чата
CHAT_ID = -1002542666027 
# ============================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- КЛАВИАТУРА С 5 КНОПКАМИ ---
def get_comment_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Чат 💬", url="https://t.me/+ur3bfgxx8SowYjc6")],
        [
            InlineKeyboardButton(text="VK Play Live 🎮", url="https://live.vkvideo.ru/soloa4"),
            InlineKeyboardButton(text="YouTube ▶️", url="https://www.youtube.com/@soloa4")
        ],
        [
            InlineKeyboardButton(text="Twitch 🟣", url="https://www.twitch.tv/soloa4"),
            InlineKeyboardButton(text="Лайв канал 📺", url="https://t.me/soloa4live")
        ]
    ])
    return keyboard

# --- ОТПРАВКА КОММЕНТАРИЯ ---
async def send_comment(reply_to_message_id=None):
    # НОВЫЙ ТЕКСТ
    text = (
        "не забывай ставить реакции на посты\n\n"
        "заглядывай в чат канала и на мои стримы, а ещё подписывайся на лайв-канал (там ничего интересного)"
    )
    
    # Загружаем картинку с мужиком
    try:
        photo = FSInputFile("meme.jpg") 
    except Exception as e:
        print(f"❌ ОШИБКА: Не найдена картинка meme.jpg. {e}")
        return

    # Отправляем как ОБЫЧНОЕ ФОТО (развернутое)
    try:
        await bot.send_photo(
            chat_id=CHAT_ID,
            photo=photo,
            caption=text,
            reply_markup=get_comment_keyboard(),
            parse_mode="HTML",
            reply_to_message_id=reply_to_message_id
        )
        print("✅ Комментарий успешно отправлен в группу!")
    except Exception as e:
        print(f"❌ ОШИБКА ОТПРАВКИ: {e}")

# --- ОТСЛЕЖИВАНИЕ НОВЫХ ПОСТОВ В ГРУППЕ ---
@dp.message()
async def handle_group_message(message: types.Message):
    # Проверяем, что сообщение пришло именно в нашу группу обсуждения
    if message.chat.id == CHAT_ID:
        # Ловим автоматическую пересылку из канала
        if message.is_automatic_forward:
            print(f"🔔 Telegram переслал новый пост в группу! ID: {message.message_id}")
            # Даем Telegram 2 секунды, чтобы пост точно появился
            await asyncio.sleep(2) 
            await send_comment(reply_to_message_id=message.message_id)

# --- РУЧНОЙ ЗАПУСК (ДЛЯ ТЕСТА) ---
@dp.message(Command("test"))
async def cmd_test(message: types.Message):
    print("⚙️ Получена команда /test")
    await message.answer("Отправляю тестовый комментарий...")
    await send_comment()

# --- ЗАПУСК БОТА ---
async def main():
    print("🚀 Бот запущен. Жду посты из канала в группе...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")