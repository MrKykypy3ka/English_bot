import json

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from config import read_config

user_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='📩Получить рассылку')],
    [KeyboardButton(text='📰Новости'), KeyboardButton(text='ℹ️Инфо')]
],
                           resize_keyboard=True,
                           input_field_placeholder='Меню ниже')

admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🫡Изменить админов')],
    [KeyboardButton(text='✏️Изменить рассылку')],
    [KeyboardButton(text='Выйти')]],
                           resize_keyboard=True)


edit_mailing_list = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='👩🏻‍🦳Подписки')],
    [KeyboardButton(text='🗂Ссылка на материалы')],
    [KeyboardButton(text='⏰Дата рассылки')]
],
                           resize_keyboard=True)


async def inline_subscribes():
    keyboard = InlineKeyboardBuilder()
    for user in read_config()["mailing list"]:
        keyboard.add(InlineKeyboardButton(text=user, url=read_config()["mailing list"][user]))
    keyboard.add(InlineKeyboardButton(text='Проверить подписки', callback_data='check'))
    return keyboard.adjust(1).as_markup()


async def inline_admins():
    keyboard = InlineKeyboardBuilder()
    for user in read_config()["Admins"]:
        keyboard.add(InlineKeyboardButton(text=user, callback_data=f'user: {user}'))
    keyboard.add(InlineKeyboardButton(text='Добавить', callback_data='append'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='back'))
    return keyboard.adjust(1).as_markup()