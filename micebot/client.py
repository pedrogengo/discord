from typing import List

from discord import Client, Message, Role

client = Client()

ROLE_PERMISSION = ['admin', 'renan']


def author_can_message(roles: List[Role]) -> bool:
    for role in roles:
        if role.name.lower() in ROLE_PERMISSION:
            return True
    return False


@client.event
async def on_ready():
    print("MiceBot is ready to receive commands. 🧀")


@client.event
async def on_message(message: Message):

    if message.author == client.user:
        return

    print(message.author.roles)

    if author_can_message(message.author.roles):
        print('AOBAA')
