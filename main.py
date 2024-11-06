import logging
from aiogram import executor
from create_bot import dp
from handlers import client, other

logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    print('Бот в сети')

client.register_handlers_client(dp)
other.register_handlers_others(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
