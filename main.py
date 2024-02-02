import asyncio
import logging
import datetime
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters.command import Command, CommandStart
from config_reader import config
import parser

bot = Bot(token=config.bot_token.get_secret_value())


logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="Markdown")
dp = Dispatcher()

chat_id_to_send_messages = None

async def run_parser():
    global chat_id_to_send_messages
    while True:
        new_info = parser.parserpy()
        for i in new_info:
            msg_msg = "\n".join(i)
            full_message = f'{msg_msg}\n'
            if chat_id_to_send_messages:
                await bot.send_message(chat_id_to_send_messages, full_message, parse_mode='Markdown')
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Текущее время:", current_time)
        await asyncio.sleep(5)  # Пауза перед следующим запуском парсера

@dp.message(CommandStart())
async def start_message(message: types.Message):
    global chat_id_to_send_messages
    chat_id_to_send_messages = message.chat.id
    await message.reply("Стартуем шеф")
    await run_parser()


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())