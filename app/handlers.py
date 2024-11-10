import re
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from functions import *
import app.keyboards as kb
from datetime import datetime, timedelta

from create_bot import send_newsletter_everyone, send_newsletter_one

router = Router()
scheduler = AsyncIOScheduler()


class Admin(StatesGroup):
    login = State()


class Newsletter(StatesGroup):
    subscription = State()
    link = State()
    data = State()


class People(StatesGroup):
    login = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(
        f"""Привет {message.from_user.username}! На связи бот @engncity
Чтобы получить материалы, Вам нужно подписаться на меня и моих коллег.""",
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
    await message.answer(f"""Для получения материалов необходимо быть подписанным на следующие каналы:
    
❗Не забудьте нажать кнопку «Проверить подписки»""",
                         reply_markup=await kb.inline_subscribes())


@router.message(F.text == '📰Новости')
async def set_message_list(message: Message):
    y, mo, d, h, mi, s = re.split(r"[- :]", read_config()['newsletter']['date'])
    if datetime(*list(map(int, [y, mo, d, h, mi, s]))) > datetime.now():
        await message.answer(f"""Следующая рассылка запланирована на {d}.{mo}.{y} в {h}:{mi}""",
                             reply_markup=kb.user_keyboard)
    else:
        await message.answer(f"""Рассылка ещё не запланирована.""",
                             reply_markup=kb.user_keyboard)


@router.message(F.text == 'ℹ️Инфо')
async def set_message_list(message: Message):
    await message.answer(f"""
Английский для взрослых и подростков ✨

Здесь Вы сможете найти:
🟣 Дополнительные материалы для себя, будь Вы преподавателем или учащимся

Основной канал - @engncity:
🟣 Вдохновение
🟣 Разглагольствования о жизни и преподавании

По всем вопросам обращаться: @lilith_slip""",
                         reply_markup=kb.user_keyboard)


@router.message(F.text == 'Выйти')
async def back(message: Message):
    await message.answer(text="Основное меню:", reply_markup=kb.user_keyboard)


@router.callback_query(F.data == 'check')
async def subscribe(callback: CallbackQuery):
    try:
        if await check_subscriptions(callback):
            y, mo, d, h, mi, s = re.split(r"[- :]", read_config()['newsletter']['date'])
            write_user(callback.from_user.id)
            await callback.message.answer(
                f"""Спасибо за подписки 💜
Бот пришлет материалы {d}.{mo}.{y} в {h}:{mi}

❗️Не отменяйте подписки, иначе бот не пришлет Вам материалы """)
        else:
            await callback.message.answer("Вы не подписаны на каналы. Пожалуйста, подпишитесь для доступа к рассылке.")
    except TelegramBadRequest as e:
        print(e)


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
        await state.set_state(Newsletter.subscription)
        await message.answer(f"""Введите ссылки на каналы через пробел на которые нужно подписаться:\n""")
    else:
        await message.answer(f'Ты не админ😡')


@router.message(Newsletter.subscription)
async def write_link(message: Message, state: FSMContext):
    await state.update_data(subscription=message.text)
    await state.set_state(Newsletter.link)
    await message.answer("Введите ссылку на материалы:")


@router.message(Newsletter.link)
async def write_link(message: Message, state: FSMContext):
    await state.update_data(link=message.text)
    await state.set_state(Newsletter.data)
    await message.answer("""Введите дату рассылки:\n
формат даты: Год Месяц День Час Минуты""")


@router.message(Newsletter.data)
async def edit_message_list(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    config = read_config()
    data = await state.get_data()
    try:
        temp = dict()
        for elem in data['subscription'].split(' '):
            name = elem[elem.rfind('/') + 1:]
            temp[name] = elem
        config["newsletter"]["subscription"] = temp
        config["newsletter"]["link"] = data['link']
        today = datetime.now()
        y, mo, d, h, mi = list(map(int, (data['date']).split(' ')))
        custom_date = datetime(y, mo, d, h, mi)
        if custom_date < today:
            raise
        config["newsletter"]["date"] = str(custom_date)
        write_config(config)
        print(data['date'])
        with open("data/users.txt", "r", encoding='utf-8') as f:
            users = list(map(str.strip, f.readlines()))
            for user_id in users:
                await message.bot.send_message(text=f"""УРА! Готовы новые материалы для рассылки!
Подпишись на новую рассылку которая запланирована на:
{d}.{mo}.{y} в {h}:{mi}""",
                                               chat_id=user_id)
        with open("data/users.txt", "w", encoding='utf-8') as f:
            f.write('')

        scheduler.remove_all_jobs()
        scheduler.add_job(send_newsletter_everyone, 'date', run_date=str(custom_date))
        await message.answer(f'Рассылка настроена', reply_markup=kb.admin_keyboard)
    except Exception as e:
        print(e)
        await message.answer('Некорректные данные')
    await state.clear()


@router.message(F.text == '️👨‍👩‍👦‍👦Отправить рассылку всем (в случае если произошёл сбой)')
async def sand_all(message: Message):
    scheduler.add_job(send_newsletter_everyone, 'date', run_date=str(datetime.now() + timedelta(seconds=5)))
    await message.answer(f"""Через 5 секунд придёт рассылка""")


# @router.message(F.text == 'Отправить рассылку конкретному человеку')
# async def sand_all(message: Message, state: FSMContext):
#     await state.set_state(People.login)
#     await message.answer("Введите логин человека, которому нужно отправить рассылку:")


@router.message(People.login)
async def send_newsletter(message: Message, state: FSMContext):
    scheduler.add_job(send_newsletter_one, 'date',
                      run_date=str(datetime.now() + timedelta(seconds=5)),
                      args=[message.text])
    await message.answer(f"""Через 5 секунд придёт рассылка""")
    await state.clear()


@router.message()
async def handle_unmatched_message(message: Message):
    await message.answer("Извините, я не понимаю это сообщение.", reply_markup=kb.user_keyboard)
