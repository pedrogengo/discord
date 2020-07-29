from discord.ext.commands import Bot, Context

from micebot.api import Api
from micebot.model.embed import embed, Field
from micebot.model.env import env
from micebot.model.model import OrderQuery


def register(bot: Bot, api: Api):
    @bot.command()
    async def orders(ctx: Context, limit: str = 5):

        response = api.list_orders(query=OrderQuery(limit=int(limit)))

        if response.total == 0:
            ...

        else:
            await ctx.message.delete()
            await ctx.channel.send(
                embed=embed(
                    title=f"Útimos itens resgatados",
                    description=f"Aqui estão os {limit} itens resgatados de um total de {response.total}.",
                )
            )
            for order in response.orders:
                await ctx.channel.send(
                    embed=embed(
                        title=order.uuid,
                        # description="Aqui estão os últimos itens resgatados.",
                        fields=[
                            [
                                Field(
                                    key="Entregue em",
                                    value=order.requested_at.strftime(
                                        env.datetime_formatter
                                    ),
                                    inline=False,
                                ),
                                Field(
                                    key="De / Para",
                                    value=f"{order.mod_display_name} / {order.owner_display_name}",
                                ),
                                Field(key="Código", value=order.product.code),
                                Field(key="UUID", value=order.product.uuid),
                            ]
                        ],
                    )
                )
