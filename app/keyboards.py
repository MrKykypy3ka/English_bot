import json

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from functions import read_config

user_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='📩Получить рассылку')],
    [KeyboardButton(text='📰Новости'), KeyboardButton(text='ℹ️Инфо')]
],
                           resize_keyboard=True,
                           input_field_placeholder='Меню ниже')

admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🫡Изменить админов')],
    [KeyboardButton(text='✏️Изменить рассылку')],
    [KeyboardButton(text='️👨‍👩‍👦‍👦Отправить рассылку всем (в случае если произошёл сбой)')],
    # [KeyboardButton(text='Отправить рассылку конкретному человеку')],
    [KeyboardButton(text='Выйти')]],
                           resize_keyboard=True)


async def inline_subscribes():
    keyboard = InlineKeyboardBuilder()
    subscription = read_config()["newsletter"]['subscription']
    for user in subscription:
        keyboard.add(InlineKeyboardButton(text=user, url=subscription[user]))
    keyboard.add(InlineKeyboardButton(text='Проверить подписки и подписаться на рассылку', callback_data='check'))
    return keyboard.adjust(1).as_markup()


async def inline_admins():
    keyboard = InlineKeyboardBuilder()
    for user in read_config()["Admins"]:
        keyboard.add(InlineKeyboardButton(text=user, callback_data=f'user: {user}'))
    keyboard.add(InlineKeyboardButton(text='Добавить', callback_data='append'))
    return keyboard.adjust(1).as_markup()