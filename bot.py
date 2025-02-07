import sys
import os
import asyncio
import threading
import serial
import time
from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.filters import Command
from aiogram import Router



from random import randint

API_TOKEN = '8111072355:AAFQibU8z_tFIUvETRueJv7fBJNBHsr2ZnI'  # Замените на ваш токен

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def send_message(text, id):
    
    await bot.send_message(id, text)