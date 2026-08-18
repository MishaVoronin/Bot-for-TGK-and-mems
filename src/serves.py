from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv
import asyncio
import os

import src.models as models
import src.crud as crud

load_dotenv()

admin_chat_id = os.getenv("ADMIN_CHAT_ID")


async def start(db: AsyncSession, message: Message) -> None:
    await message.answer(
        """
Это бот предложки канала "Кусок домкрата".
Отправь сюда сообщение и оно отправится одмину
        """
    )


async def message(db: AsyncSession, message: Message) -> None:
    forward_meseg = await message.forward(chat_id=admin_chat_id)
    await crud.create_message(
        db,
        models.Message(
            message_id=forward_meseg.message_id,
            user_id=message.from_user.id,
        ),
    )
    answer = await message.answer("сообщение отправленно")
    await asyncio.sleep(1)
    await answer.delete()


async def answer(db: AsyncSession, message: Message) -> None:
    messeg_from_user: models.Message | None = await crud.get_mesage_by_id(
        db, message.reply_to_message.message_id
    )
    if messeg_from_user is None:
        await message.answer("отправитель не найден")
        return

    await message.copy_to(messeg_from_user.user_id)

    answer = await message.answer("сообщение отправленно")
    await asyncio.sleep(1)
    await answer.delete()
