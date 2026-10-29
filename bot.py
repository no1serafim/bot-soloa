import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.filters import Command
from aiohttp import web
import os

logging.basicConfig(level=logging.INFO)

# ================= НАСТРОЙКИ =================
BOT_TOKEN = '9150380238:AAF4tJqfU9Rs4MRfQatwA1z8_nWsGDw011U'
CHAT_ID = -1002542666027 
# ============================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

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

async def send_comment(reply_to_message_id=None):
    text = (
        "не забывай ставить реакции на посты\n\n"
        "заглядывай в чат канала и на мои стримы, а ещё подписывайся на лайв-канал (там ничего интересного)"
    )
    
    try:
        photo = FSInputFile("meme.jpg") 
    except Exception as e:
        print(f"❌ ОШИБКА: Не найдена картинка meme.jpg. {e}")
        return

    try:
        await bot.send_photo(
            chat_id=CHAT_ID,
            photo=photo,
            caption=text,
            reply_markup=get_comment_keyboard(),
            parse_mode="HTML",
            reply_to_message_id=reply_to_message_id
        )
        print("✅ Комментарий успешно отправлен!")
    except Exception as e:
        print(f"❌ ОШИБКА ОТПРАВКИ: {e}")

@dp.message()
async def handle_group_message(message: types.Message):
    if message.chat.id == CHAT_ID:
        if message.is_automatic_forward:
            print(f"🔔 Новый пост! ID: {message.message_id}")
            await asyncio.sleep(2) 
            await send_comment(reply_to_message_id=message.message_id)

@dp.message(Command("test"))
async def cmd_test(message: types.Message):
    await message.answer("Тест...")
    await send_comment()

# --- ЗАГЛУШКА ДЛЯ RENDER ---
async def handle_web(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_web)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"🌐 Веб-сервер запущен на порту {port}")

# --- БУДИЛЬНИК ДЛЯ RENDER ---
async def keep_alive():
    # Ждем 10 минут, чтобы дать серверу запуститься
    await asyncio.sleep(600) 
    while True:
        try:
            # ВАЖНО: Замени эту ссылку на свою из Render!
            url = "https://bot-soloa.onrender.com" 
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    print(f"🔔 Будильник: статус {response.status}")
        except Exception as e:
            print(f"Будильник не сработал: {e}")
        await asyncio.sleep(600) # Следующий пинок через 10 минут

# --- ГЛАВНЫЙ ЗАПУСК ---
async def main():
    asyncio.create_task(start_web_server())
    asyncio.create_task(keep_alive()) # Запускаем будильник
    print("🚀 Бот запущен и работает...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")
