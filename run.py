import asyncio
import logging
from create_bot import dp, bot, send_newsletter_everyone
from app.handlers import router, scheduler
from functions import read_config

logging.basicConfig(level=logging.INFO)


async def main():
    dp.include_router(router)
    scheduler.start()
    if read_config()['newsletter']['date']:
        scheduler.add_job(send_newsletter_everyone, 'date', run_date=read_config()['newsletter']['date'])
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
