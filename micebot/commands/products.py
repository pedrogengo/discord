from discord import Colour
from discord.ext.commands import Bot, Context

from micebot.api import (
    Api,
    CodeAlreadyRegistered,
    UnknownNetworkError,
    ProductNotFound,
)
from micebot.model.embed import embed, Field
from micebot.model.env import env
from micebot.model.messages import (
    RemoveProductCommand,
    Messages,
    AddProductCommand,
    GenericMessage,
)
from micebot.model.model import (
    ProductCreation,
    ProductEdit,
    ProductDelete, ProductQuery,
)

DEFAULT_FOOTER = "Essa mensagem será removida após 30 segundos."


def register(bot: Bot, api: Api):
    @bot.command()
    async def add(
        ctx: Context,
        code: str = None,
        summary: str = env.default_product_summary,
    ):

        if not code:
            await Messages.remove_message_and_answer(
                context=ctx,
                message=AddProductCommand.NO_CODE_PROVIDED,
                mention=ctx.author.mention,
                prefix=env.command_prefix,
            )
            return

        try:
            product = api.add_product(
                product=ProductCreation(code=code, summary=summary)
            )

            desc = "Acabei de adicionar um novo item para ser resgatado."
            fields = [
                [
                    Field(key="UUID", value=product.uuid, inline=False),
                    Field(key="código", value=product.code),
                    Field(key="descrição", value=product.summary),
                    Field(
                        key="criado em",
                        value=product.created_at.strftime(
                            env.datetime_formatter
                        ),
                        inline=False,
                    ),
                ]
            ]
            await ctx.message.delete()
            await ctx.channel.send(
                embed=embed(
                    title="Novo Item",
                    description=desc,
                    fields=fields,
                    footer=DEFAULT_FOOTER,
                ),
                delete_after=env.delete_message_after,
            )

        except CodeAlreadyRegistered:
            await Messages.remove_message_and_answer(
                context=ctx,
                message=AddProductCommand.CODE_ALREADY_REGISTERED,
                mention=ctx.author.mention,
            )
        except UnknownNetworkError as e:
            await Messages.remove_message_and_answer(
                context=ctx,
                message=GenericMessage.UNKNOWN_NETWORK_ERROR,
                err_message=str(e),
            )

    @bot.command()
    async def edit(
        ctx: Context, uuid: str = None, code: str = None, summary: str = None
    ):

        if not uuid:
            ...

        if not code:
            ...

        try:
            updated_product = api.edit_product(
                product=ProductEdit(uuid=uuid, code=code, summary=summary)
            )
            if updated_product:
                desc = f"Acabei de atualizar os dados do produto."
                fields = [
                    [
                        Field(
                            key="UUID",
                            value=updated_product.uuid,
                            inline=False,
                        ),
                        Field(key="código", value=updated_product.code),
                        Field(key="descrição", value=updated_product.summary),
                        Field(
                            key="criado em",
                            value=updated_product.created_at.strftime(
                                env.datetime_formatter
                            ),
                            inline=False,
                        ),
                        Field(
                            key="atualizado em",
                            value=updated_product.updated_at.strftime(
                                env.datetime_formatter
                            ),
                        ),
                    ]
                ]
                await ctx.message.delete()
                await ctx.channel.send(
                    embed=embed(
                        title="Atualização Bem Sucedida",
                        description=desc,
                        fields=fields,
                        footer=DEFAULT_FOOTER,
                    ),
                    delete_after=env.delete_message_after,
                )

        except ProductNotFound:
            ...

        except CodeAlreadyRegistered:
            ...

        except UnknownNetworkError:
            ...

        ...

    @bot.command()
    async def remove(ctx: Context, uuid: str = None):
        if not uuid:
            await Messages.remove_message_and_answer(
                context=ctx,
                message=RemoveProductCommand.INVALID,
                mention=ctx.author.mention,
            )
            return

        response = api.delete_product(product=ProductDelete(uuid=uuid))

        if response.deleted:
            await Messages.remove_message_and_answer(
                context=ctx,
                message=RemoveProductCommand.VALID,
                mention=ctx.author.mention,
                uuid=uuid,
            )

    @bot.command()
    async def ls(ctx: Context, limit: str = '5'):

        products = api.list_products(ProductQuery(
            taken=False,
            desc=True,
            limit=int(limit)
        ))

        await ctx.message.delete()
        await ctx.channel.send(
            embed=embed(
                title='Detalhamento',
                description='Esses são os dados que tenho até o momento:',
                thumbnail=True,
                color=Colour.green(),
                fields=[
                    [
                        Field(key="Total", value=str(products.total.all)),
                        Field(key="Disponíveis", value=str(products.total.available)),
                        Field(key="Resgatados", value=str(products.total.taken)),

                    ]
                ]
            )
        )

        for product in products.products:
            await ctx.channel.send(
                embed=embed(
                    title=product.code,
                    fields=[
                        [
                            Field(key="UUID", value=product.uuid, inline=False),
                            Field(key="descrição", value=product.summary),
                            Field(
                                key="criado em",
                                value=product.created_at.strftime(
                                    env.datetime_formatter
                                ),
                                inline=False,
                            )
                        ]
                        ]
            ))

        await ctx.channel.send(
            embed=embed(
                title='Final do Relatório.',
                color=Colour.green()
            )
        )