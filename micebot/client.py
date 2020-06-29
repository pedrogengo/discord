from discord import Client, Message

client = Client()


@client.event
async def on_ready():
    print("MiceBot is ready to receive commands. 🧀")


@client.event
async def on_message(message: Message):
    print(f"Received message: {message} from {message.author}.")
