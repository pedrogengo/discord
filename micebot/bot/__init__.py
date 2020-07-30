from discord.ext.commands import Bot

from micebot.api import Api
from micebot.commands.orders import register as register_order_commands
from micebot.commands.products import register as register_product_commands
from micebot.model.env import env

api = Api(
    endpoint=env.api_endpoint,
    username=env.discord_user,
    password=env.discord_pass,
)

bot = Bot(command_prefix=env.command_prefix)

register_product_commands(bot=bot, api=api)
register_order_commands(bot=bot, api=api)


@bot.event
async def on_ready():
    print("Stabilizing connection to the API, wait...")
    if api.authenticate():
        print("MiceBot is ready to receive commands. 🧀")
    else:
        print("Fail to connect to API, check logs.")
        exit(1)
