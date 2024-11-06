from aiogram import Bot, Dispatcher

import json

with open("data/config.json", "r") as file:
    API_TOKEN = json.load(file)["API_TOKEN"]


bot = Bot(token=API_TOKEN)
dp = Dispatcher()
