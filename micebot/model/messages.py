import enum

from discord.ext.commands import Context

from micebot.model.env import env


class Messages:
    @staticmethod
    async def remove_message_and_answer(context: Context, message: enum.Enum, **kwargs):
        await context.message.delete()
        await context.channel.send(
            message.value.format(**kwargs),
            delete_after=env.delete_message_after,
        )


class GenericMessage(enum.Enum):
    UNKNOWN_NETWORK_ERROR = (
        "Hey {mention}, ocorreu algum problema com a minha conexão. "
        "Talvez essa informação possa ajudar: {err_message}"
    )


class AddProductCommand(enum.Enum):
    NO_CODE_PROVIDED = (
        "Hey {mention}, para que eu possa inserir um novo "
        "produto para ser resgatado é necessário me dizer "
        "qual é o código. Exemplo: `{prefix} add <codigo> <descrição>`"
    )
    CODE_ALREADY_REGISTERED = (
        "Hey {mention}, o código que você está tentando inserir já está"
        "associado a outro produto."
    )


class EditProductCommand(enum.Enum):
    ...


class RemoveProductCommand(enum.Enum):
    INVALID = (
        "Hey {mention}, para que possa excluir um registro é "
        "necessário que você me informe o UUID do produto."
    )
    VALID = "Hey {mention}, acabei de remover o produto com UUID {uuid}."
