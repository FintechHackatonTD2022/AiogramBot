import aiogram


async def start(message: aiogram.types.Message):
    await message.answer('Привет этот бот выполняет манипуляции с картами')
