from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from config import *
import app.keyboards as kb


router = Router()


class Admin(StatesGroup):
    login = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(f'Привет!{message.from_user.id} {message.from_user.username}',
                        reply_markup=kb.user_keyboard)


@router.message(F.text.lower() == 'admin')
async def admin_menu(message: Message):
    if message.from_user.username in read_config()["Admins"]:
        await message.answer(f'Для изменения',
                            reply_markup=kb.admin_keyboard)
    else:
        await message.answer(f'Ты не админ😡')


@router.message(F.text == '🫡Изменить админов')
async def edit_admins(message: Message):
    if message.from_user.username in read_config()["Admins"]:
        await message.reply(f'Админы:'
                            f'Нажмите на админа чтобы его удалить.',
                            reply_markup=await kb.inline_admins())
    else:
        await message.answer(f'Ты не админ😡')


@router.message(F.text == '✏️Изменить рассылку')
async def edit_message_list(message: Message):
    if message.from_user.username in read_config()["Admins"]:
        await message.reply()
    else:
        await message.answer(f'Ты не админ😡')


@router.message(F.text == '📩Получить рассылку')
async def set_message_list(message: Message):
    await message.answer(f'Для получения материалов необходимо быть подписанным на следующие каналы:',
                        reply_markup=await kb.inline_subscribes())


@router.message(F.text == 'Выйти')
async def back(message: Message):
    await message.answer(text="Основное меню:", reply_markup=kb.user_keyboard)


@router.callback_query(F.data == 'check')
async def subscribe(callback: CallbackQuery):
    await callback.message.answer(f'Проверка подписок...')


@router.callback_query(F.data.startswith('user'))
async def del_admin(callback: CallbackQuery):
    data = read_config()
    data["Admins"].remove(callback.data.split(": ")[1])
    write_config(data)
    await callback.message.answer(f'Админ удёлён', reply_markup=await kb.inline_admins())


@router.callback_query(F.data == 'append')
async def write_admin(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Admin.login)
    await callback.message.answer("Введите логин нового админа:")


@router.message(Admin.login)
async def add_admin(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    data = read_config()
    login = await state.get_data()
    data["Admins"].append(login["login"])
    write_config(data)
    await state.clear()