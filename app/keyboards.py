import json

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

with open("data/config.json", "r", encoding='utf-8') as file:
    data = json.load(file)
    subscription = data["mailing list"]["subscription"]
    admins = data['Admins']

user_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='📩Получить рассылку')],
    [KeyboardButton(text='📰Новости'), KeyboardButton(text='ℹ️Инфо')]
],
                           resize_keyboard=True,
                           input_field_placeholder='Меню ниже')

admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🫡Изменить админов')],
    [KeyboardButton(text='✏️Изменить рассылку')]],
                           resize_keyboard=True)


edit_mailing_list = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='👩🏻‍🦳Подписки')],
    [KeyboardButton(text='🗂Ссылка на материалы')],
    [KeyboardButton(text='⏰Дата рассылки')]
],
                           resize_keyboard=True)


async def inline_subscribes():
    keyboard = InlineKeyboardBuilder()
    for user in subscription:
        keyboard.add(InlineKeyboardButton(text=user, url=subscription[user]))
    keyboard.add(InlineKeyboardButton(text='Проверить подписки', callback_data='check'))
    return keyboard.adjust(1).as_markup()