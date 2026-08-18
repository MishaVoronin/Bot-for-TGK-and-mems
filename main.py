from src.bot import dp, bot
import asyncio
import os
import sys


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
