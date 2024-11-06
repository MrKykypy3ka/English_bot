import asyncio
import logging
from create_bot import dp, bot
from app.handlers import router

logging.basicConfig(level=logging.INFO)


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
