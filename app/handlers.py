from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from config import *
import app.keyboards as kb
from datetime import date, datetime


router = Router()


class Admin(StatesGroup):
    login = State()


class MailingList(StatesGroup):
    subscription = State()
    link = State()
    data = State()


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
        await message.answer(f'Админы:\n'
                            f'Нажмите на админа чтобы его удалить.',
                            reply_markup=await kb.inline_admins())
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
    user_id = callback.from_user.id
    print(user_id)
    try:
        for chanel in read_config()["mailing list"]["subscription"]:
            member = await callback.message.bot.get_chat_member(chat_id=chanel, user_id=user_id)
            print(member.status)
            if member.status in ["member", "administrator", "creator"]:
                await callback.message.answer("Вы подписаны на канал!")
            else:
                await callback.message.answer("Вы не подписаны на канал. Пожалуйста, подпишитесь для доступа.")
    except TelegramBadRequest as e:
        print(e)
        await callback.message.answer("e")


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
    await message.answer(f'Админ добавлен', reply_markup=await kb.inline_admins())


@router.message(F.text == '✏️Изменить рассылку')
async def edit_message_list(message: Message, state: FSMContext):
    if message.from_user.username in read_config()["Admins"]:
        await state.set_state(MailingList.subscription)
        await message.answer(f"""Введите каналы на которые нужно подписаться через пробел:\n
Формат ввода: название канала: ссылка, название канала: ссылка, название канала: ссылка""")
    else:
        await message.answer(f'Ты не админ😡')


@router.message(MailingList.subscription)
async def write_link(message: Message, state: FSMContext):
    await state.update_data(subscription=message.text)
    await state.set_state(MailingList.link)
    await message.answer("Введите ссылку на материалы:")


@router.message(MailingList.link)
async def write_link(message: Message, state: FSMContext):
    await state.update_data(link=message.text)
    await state.set_state(MailingList.data)
    await message.answer("""Введите дату рассылки:\n
формат даты: Год.Месяц.День""")


@router.message(MailingList.data)
async def add_admin(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    config = read_config()
    data = await state.get_data()
    try:
        temp = dict()
        for elem in data['subscription'].split(', '):
            s = elem.split(': ')
            temp[s[0]] = s[1]
        config["mailing list"]["subscription"] = temp
        config["mailing list"]["link"] = data['link']
        today = date.today()
        custom_date = date(*list(map(int, data['date'].split('.'))))
        if custom_date < today:
            raise
        config["mailing list"]["date"] = str(custom_date)
        write_config(config)
        await message.answer(f'Рассылка настроена', reply_markup=kb.admin_keyboard)
    except Exception:
        await message.answer('Некорректные данные')
    await state.clear()
