from fastapi import FastAPI
from pydantic import BaseModel

import os
from dotenv import load_dotenv
import telebot
import requests
from binance.client import Client

load_dotenv()

telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')

bot = telebot.TeleBot(telegram_token)
client = Client()

def get_top_coins():
    response = requests.get('https://api.binance.com/api/v3/ticker/24hr')
    data = response.json()
    volumes = [(coin['symbol'], float(coin['volume']), float(coin['lastPrice']), coin['symbol'][-4:]=="USDT") for coin in data]
    volumes_sorted = sorted(volumes, key=lambda x: x[1]*x[2], reverse=True)
    top_coins = [coin for coin in volumes_sorted if coin[0].endswith('USDT')][:10]
    return top_coins

@bot.message_handler(commands=['top'])
def send_top_coins(message):
    top_coins = get_top_coins()
    text = "Top 10 monedas con mayor volumen de negociación en las últimas 24 horas:\n"
    for i, coin in enumerate(top_coins):
        text += f"{i+1}. {coin[0]} ({coin[2]} USDT)\n"
    bot.reply_to(message, text)

bot.polling()
