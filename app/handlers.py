import json

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

import app.keyboards as kb

with open("data/config.json", "r") as file:
    admins = json.load(file)["Admins"]


router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(f'Привет!{message.from_user.id} {message.from_user.username}',
                        reply_markup=kb.user_keyboard)


@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Это команда /help')


@router.message(F.text.lower() == 'admin')
async def how_are_you(message: Message):
    if message.from_user.username in admins:
        await message.answer(f'Для изменения',
                            reply_markup=kb.admin_keyboard)
    else:
        await message.answer(f'Ты не админ😡')


@router.message(F.text == '🫡Изменить админов')
async def how_are_you(message: Message):
    if message.from_user.username in admins:
        await message.reply(f'',
                            reply_markup=kb.settings)
    else:
        await message.answer(f'Ты не админ😡')


@router.message(F.text == '📩Получить рассылку')
async def how_are_you(message: Message):
    await message.answer(f'Для получения материалов необходимо быть подписанным на следующие каналы:',
                        reply_markup=await kb.inline_subscribes())

@router.callback_query(F.data == 'check')
async def check_subccrube(callback: CallbackQuery):
    await callback.message.answer(f'Проверка подписок...')