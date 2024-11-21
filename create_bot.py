from aiogram import Bot, Dispatcher
from functions import read_user, read_config
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


async def check_subscriptions(user_id):
    try:
        subscription = read_config()["newsletter"]["subscription"]
        for chanel in subscription:
            member = await bot.get_chat_member(chat_id="@" + chanel, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        return True
    except Exception as e:
        print(e)


async def send_newsletter_everyone():
    users = read_user()
    for user_id in users:
        try:
            if await check_subscriptions(user_id):
                malling_list = read_config()['newsletter']
                await bot.send_message(text=f"""Здравствуйте! Ловите материалы:
{malling_list['link']}
Спасибо за участие! 💜""", chat_id=user_id)
            else:
                await bot.send_message(text="Извините, но вы не подписаны на каналы😒",
                                       chat_id=user_id)
                await bot.send_message(text=f"{user_id} не получил рассылку из-за того что не подписан на канал",
                                       chat_id='1425132540')
        except Exception as e:
            print(e)


async def send_newsletter_one(user_id):
    try:
        if await check_subscriptions(user_id):
            malling_list = read_config()['newsletter']
            await bot.send_message(text=f"""Здравствуйте! Ловите материалы:
{malling_list['link']}
Спасибо за участие! 💜""", chat_id=user_id)
        else:
            await bot.send_message(text="Извините, но вы не подписаны на каналы😒",
                                   chat_id=user_id)
            await bot.send_message(text=f"{user_id} не получил рассылку из-за того что не подписан на канал",
                                   chat_id='1425132540')
    except Exception:
        print(e)
