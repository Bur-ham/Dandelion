import os

from src.models.bot import Dandelion
from src.utils.functions import get_prefix

from src.utils.consts import TOKEN

bot = Dandelion(command_prefix=get_prefix)

if not os.path.exists('./database'):
    os.mkdir('./database')

@bot.check
async def check_global(_):
    await bot.wait_until_ready()
    return True

bot.run(TOKEN)