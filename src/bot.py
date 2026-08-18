import aiogram as io
import os
from dotenv import load_dotenv
from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import DbSessionMiddleware
import src.serves as serves

load_dotenv()

bot = io.Bot(token=os.getenv("BOT_TOKEN"))
dp = io.Dispatcher()

dp.message.middleware(DbSessionMiddleware())
dp.callback_query.middleware(DbSessionMiddleware())

admin_chat_id = int(os.getenv("ADMIN_CHAT_ID"))


@dp.message(Command("start"))
async def start(message: Message, db: AsyncSession) -> None:
    await serves.start(db, message)


@dp.message(F.chat.type == "private", F.chat.id != admin_chat_id)
async def messeg(message: Message, db: AsyncSession) -> None:
    await serves.message(db, message)


@dp.message(F.reply_to_message.from_user.id == bot.id, F.chat.id == admin_chat_id)
async def ansswer(message: Message, db: AsyncSession) -> None:
    await serves.answer(db, message)
