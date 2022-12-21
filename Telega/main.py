from aiogram import Bot, Dispatcher, executor, types

TOKEN_API = "5800671334:AAF9qT-B9bG97yTMzMW8t0ntEkvSB9BxBVU"

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(text=message.text)  # Ответить на сообщение


if __name__ == '__main__':
    executor.start_polling(dp)
