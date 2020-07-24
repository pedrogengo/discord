from discord.ext.commands import Bot, Context

from micebot.api import Api
from micebot.model.embed import embed, Field
from micebot.model.env import env
from micebot.model.model import ProductCreation, ProductQuery, ProductEdit

DEFAULT_FOOTER = "Essa mensagem será removida após 30 segundos."
DELETE_MESSAGE_AFTER = 30  # seconds


def register(bot: Bot, api: Api):
    @bot.command()
    async def add(ctx: Context, code: str = None, summary: str = "E-Book"):

        if not code:
            # TODO: Help message quando não passar o código.
            return

        product = api.add_product(
            product=ProductCreation(code=code, summary=summary)
        )

        if product:
            await ctx.message.delete()
            await ctx.channel.send(
                embed=embed(
                    title="Novo Item",
                    description="Acabei de adicionar um novo item para ser resgatado.",  # noqa
                    fields=[
                        [
                            Field(
                                key="UUID", value=product.uuid, inline=False
                            ),
                            Field(key="código", value=product.code),
                            Field(key="descrição", value=product.summary),
                        ]
                    ],
                    footer=DEFAULT_FOOTER,
                ),
                delete_after=DELETE_MESSAGE_AFTER,
            )

    @bot.command()
    async def edit(ctx: Context, uuid: str, code: str, summary: str = None):
        ...

    @bot.command()
    async def delete(ctx: Context, uuid: str):
        ...

    @bot.command()
    async def ls(ctx: Context, taken: str = "!taken"):

        if taken not in ["all", "taken", "!taken"]:
            return

        taken = taken == "taken"
        products = api.list_products(ProductQuery(taken=taken, desc=True))
        products_len = len(products)

        if products_len == 0:
            await ctx.message.delete()
            await ctx.channel.send(
                f"Nenhum produto cadastrado ainda. Para inserir um novo item, "
                f"utilize o comando `{env.command_prefix} add <code> <summary>`.",  # noqa
                delete_after=DELETE_MESSAGE_AFTER,
            )

        if products_len <= 8:
            await ctx.message.delete()
            await ctx.channel.send(
                embed=embed(
                    title="Últimos Itens",
                    description=f"""
                    Aqui estão os últimos itens registrados para serem resgatados. Você pode utilizar os comandos:
                    
                    `{env.command_prefix} rm <uuid>` - para remover um item.
                    `{env.command_prefix} edit <uuid> <code> <summary>` - para editar um item.                    
                    """,
                    fields=[
                        [
                            Field(key="UUID", value=product.uuid),
                            Field(key="código", value=product.code),
                            Field(key="descrição", value=product.summary),
                        ]
                        for product in products
                    ],
                )
            )

        else:
            await ctx.message.delete()
            message = f"Todos os itens registrados **({'Resgatados' if taken else 'Ainda não Resgatado'})**:\n\n"
            index = 0
            for product in products:
                message += f"**código**: {product.code}\n"
                message += f"**descrição**: {product.summary}\n"
                message += f"**uuid**: {product.uuid}\n"
                message += (
                    f"**resgatado**: {'sim' if product.taken else 'não'}\n"
                )
                message += f"**resgatado em**: {'-' if not product.taken else product.taken_at.strftime('%d/%m/%Y %H:%M:%S') }\n"
                message += "--------------------------\n"
                index += 1

                if index == 4:
                    await ctx.channel.send(message)
                    index = 0
                    message = ""

            if len(message) > 0:
                await ctx.channel.send(message)
