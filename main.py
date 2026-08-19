from src.bot import dp, bot
import asyncio
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
