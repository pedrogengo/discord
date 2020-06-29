from os import environ

from micebot.client import client

client.run(environ.get("DISCORD_TOKEN"))
