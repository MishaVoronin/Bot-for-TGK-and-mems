from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models import Message

async def create_message(db: AsyncSession, message: Message) -> Message:
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message

async def get_mesage_by_id(db: AsyncSession, id: int) -> Message | None:
    result = await db.execute(select(Message).where(Message.message_id == id))
    return result.scalar_one_or_none()
