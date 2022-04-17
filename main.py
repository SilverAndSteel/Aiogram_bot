import logging
from aiogram import Dispatcher, Bot, executor, types
import requests
import json
import configs


cities_id = {
    "Гомель": 627907,
    "Минск": 625144,
    "Брест": 629634,
    "Витебск": 620127,
    "Могилев": 625665,
    "Гродно": 627904,
}

logging.basicConfig(level=logging.INFO)
bot = Bot(token=configs.TOKEN)
dp = Dispatcher(bot)
url = "http://api.openweathermap.org/data/2.5/weather"
url_forecast = "http://api.openweathermap.org/data/2.5/forecast"
city = ""


@dp.message_handler(commands=['start', 'help'])
async def start_mes(message: types.Message):
    mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(text="Гомель")
    item2 = types.KeyboardButton(text="Минск")
    item3 = types.KeyboardButton(text="Брест")
    item4 = types.KeyboardButton(text="Гродно")
    item5 = types.KeyboardButton(text="Могилев")
    item6 = types.KeyboardButton(text="Витебск")
    mark.add(item1, item2, item3, item4, item5, item6)
    await message.answer(f"Hi!{message.from_user.username}\nI'm EchoBot!\nPowered by aiogram!", reply_markup=mark)

markup = types.InlineKeyboardMarkup(resize_keyboard=True).row(
    types.InlineKeyboardButton("Погода сейчас", callback_data="btn1"),
    types.InlineKeyboardButton("Погода на 5 дней", callback_data="btn2"))


@dp.message_handler(content_types=["text"])
async def weather(message: types.Message):
    global city
    city = message.text
    if message.text == "Гомель":
        await message.reply("Что вы хотите узнать?", reply_markup=markup)
    elif message.text == "Минск":
        await message.reply("Что вы хотите узнать?", reply_markup=markup)
    elif message.text == "Брест":
        await message.reply("Что вы хотите узнать?", reply_markup=markup)
    elif message.text == "Витебск":
        await message.reply("Что вы хотите узнать?", reply_markup=markup)
    elif message.text == "Гродно":
        await message.reply("Что вы хотите узнать?", reply_markup=markup)
    elif message.text == "Могилев":
        await message.reply("Что вы хотите узнать?", reply_markup=markup)



@dp.callback_query_handler(lambda call: call.data and call.data.startswith('btn'))
async def callback_inline(call):
    try:
        if call.message:
            if call.data == "btn1":
                req = requests.get(url, params={'id': cities_id[city], 'units': 'metric', 'APPID': configs.APIKEY,
                                                'lang': 'ru'})
                data = json.loads(req.text)
                await bot.send_message(call.from_user.id,
                                       f"Город {data['name']}\n{data['weather'][0]['description']}\n"
                                       f"Сейчас:  {data['main']['temp']}°C\n"
                                       f"Чувствуется как:   {data['main']['feels_like']}°C\n"
                                       f"Влажность:  {data['main']['humidity']}%\n"
                                       f"Ветер:  {round(data['wind']['speed'])} М/С")
            if call.data == "btn2":
                await bot.send_message(call.from_user.id,
                                       f"Погода на пять дней с 3-х часовым интервалом в городе {city}")
                req = requests.get(url_forecast,
                                   params={'id': cities_id[city],
                                           'units': 'metric', 'APPID': configs.APIKEY, 'lang': 'ru'})

                data = json.loads(req.text)
                for i in data['list']:
                    await bot.send_message(call.from_user.id,
                                           f"{i['dt_txt']} -- "
                                           f"Температура:  {round(i['main']['temp'])}°C -- "
                                           f"{i['weather'][0]['description']} -- "
                                           f"Влажность:  {i['main']['humidity']}% -- "
                                           f"Ветер:  {round(i['wind']['speed'])} М/С")
    except Exception as e:
        print(repr(e))
        pass


if __name__ == '__main__':
    executor.start_polling(dp)



