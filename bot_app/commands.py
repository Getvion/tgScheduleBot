"""
Команды, по которым пользователь осуществляет запросы чат-боту.
"""

from aiogram import types

from bot_app.config import connection
from bot_app import messages

from bot_app import dp
import SQLCommands


# Первый запуск
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply(messages.GREETINGS)


# Показ кнопок для получения расписания
@dp.message_handler(commands=['schedule'])
async def buttons(message: types.Message):
    buttons = [
        [types.KeyboardButton(text=f"{messages.TODAY}")],
        [types.KeyboardButton(text=f"{messages.TOMOROW}")],
        [types.KeyboardButton(text=f"{messages.THIS_WEEK}")],
        [types.KeyboardButton(text=f"{messages.NEXT_WEEK}")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons, one_time_keyboard=True)
    await message.answer(text="Расписание на:", reply_markup=keyboard)


# Получение расписания на сегодня
@dp.message_handler(regexp=f"{messages.TODAY}")
async def getTodayLessons(message: types.Message):
    try:
        cursor = connection.cursor()
        cursor.execute(SQLCommands.allTodaySchedule)
        dbData = cursor.fetchall()

        if (dbData != []):
            return await message.answer(dbData)

        return await message.answer(messages.NO_TODAY)
    except:
        await message.answer(messages.SOMETHING_BROKEN)


# Получение расписания на завтра
@dp.message_handler(regexp=f"{messages.TOMOROW}")
async def getTomorowLessons(message: types.Message):
    try:
        cursor = connection.cursor()
        cursor.execute(SQLCommands.allTomorrowSchedule)
        dbData = cursor.fetchall()

        if (dbData != []):
            return await message.answer(dbData)

        return await message.answer(messages.NO_TOMORROW)
    except:
        await message.answer(messages.SOMETHING_BROKEN)


# Получение расписания на эту неделю
@dp.message_handler(regexp=f"{messages.THIS_WEEK}")
async def getThisWeekLessons(message: types.Message):
    try:
        cursor = connection.cursor()
        # todo добавить запрос на получение данных
        cursor.execute("")
        dbData = cursor.fetchall()

        if (dbData != []):
            return await message.answer(dbData)

        return await message.answer(messages.NO_THIS_WEEK)

    except:
        await message.answer(messages.SOMETHING_BROKEN)


# Получение расписания на следующую неделю
@dp.message_handler(regexp=f"{messages.NEXT_WEEK}")
async def getNextWeekLessons(message: types.Message):
    try:
        cursor = connection.cursor()

        # todo добавить запрос на получение данных
        cursor.execute("")
        dbData = cursor.fetchall()

        if (dbData != []):
            return await message.answer(dbData)

        return await message.answer(messages.NO_NEXT_WEEK)
    except:
        await message.answer(messages.SOMETHING_BROKEN)


# Любой текст, который не попал в остальные команды
@dp.message_handler()
async def allMessagesHandler(message: types.Message):
    cursor = connection.cursor()
    cursor.execute(SQLCommands.allPersonnelUser)

    dbData = cursor.fetchall()

    try:
        intUserWithId = dbData[int(message.text) - 1]
        userName = intUserWithId[1]

        await message.answer(intUserWithId)
        await message.answer(userName)
    except:
        await message.answer(f"Введите целое число от 1 до {len(dbData)}")

 
#TODO:
# 1. Команда по получению занятий сегодня. Сверяешь текущий день (date.today) c датами в бд, и распознаешь день недели, (date.weekday). 
# Если текущей даты нет, то выводишь что-то типа 'сегодня нет занятий. Радостно'. 
# В ином случае показываешь (пока-что) все занятия, назначенные на эту дату)
# 2. Команда по получению занятий на завтра (аналогично верхнему, но +1 день с проверкой на выходной)
# 3. Команда по получению всех занятий на неделю.
# Вот тут пока смутно понимаю, как это сделать. В голову приходит идея ориентироваться на данные о четности недели.
# То есть, по ближайшим датам понять, какая сейчас неделя (первая, или вторая), 
# и показать по запросу студента все занятия данной недели. 
# 4. Аналогично верхнему, но после определения текущей недели нужно выбрать нужную (если первая, то вторая, иначе первая), 
# и вывести все занятия уже для нее
