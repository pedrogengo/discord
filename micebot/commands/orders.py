from discord.ext.commands import Bot, Context

from micebot.api import Api
from micebot.model.embed import embed, Field
from micebot.model.env import env
from micebot.model.model import OrderQuery


def register(bot: Bot, api: Api):
    @bot.command(help='Exibe os últimos pedidos entregues.\
                 Traz as seguintes informações: data de entrega,\
                 nome do moderador e nome de quem recebeu a premiação')
    async def orders(ctx: Context, limit: str = 5):

        response = api.list_orders(query=OrderQuery(limit=int(limit)))

        if response.total == 0:
            """TODO: dar feedback se não tiver pedidos no BD."""

        else:
            await ctx.message.delete()
            await ctx.channel.send(
                embed=embed(
                    title="Útimos itens resgatados",
                    description=f"Aqui estão os {limit} itens resgatados "
                    f"de um total de {response.total}.",
                )
            )
            for order in response.orders:
                await ctx.channel.send(
                    embed=embed(
                        title=order.uuid,
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
                                    key="Entregue por",
                                    value=order.mod_display_name,
                                ),
                                Field(
                                    key="Entregue para",
                                    value=order.owner_display_name,
                                ),
                                Field(
                                    key=f"Código do {order.product.summary}",
                                    value=order.product.code,
                                ),
                            ]
                        ],
                    )
                )
