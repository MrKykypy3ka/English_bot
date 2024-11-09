from aiogram import Bot, Dispatcher

import json

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import read_user, read_config

with open("data/config.json", "r") as file:
    API_TOKEN = json.load(file)["API_TOKEN"]


bot = Bot(token=API_TOKEN)
dp = Dispatcher()


async def send_scheduled_broadcast():
    users = read_user()
    for user_id in users:
        try:
            malling_list = read_config()['mailing list']
            await bot.send_message(
f"""Здравствуйте! Ловите материалы:
{malling_list['link']}
Спасибо за участие! 💜""")
        except Exception as e:
            print(f"Не удалось отправить сообщение {user_id}: {e}")
