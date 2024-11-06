from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import json

with open("data\TOKEN.json", "r") as file:
    API_TOKEN = json.load(file)["API_TOKEN"]

storage = MemoryStorage()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
