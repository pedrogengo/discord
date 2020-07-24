from datetime import datetime

from discord import Embed
from discord.ext.commands import Bot, Context

from micebot.api import Api
from micebot.model.model import OrderQuery


def register(bot: Bot, api: Api):
    @bot.command()
    async def orders(ctx: Context, query: str = None):
        if not query:
            await ctx.message.delete()
            await ctx.channel.send(
                f'🐭 {ctx.author.mention} parece que você esqueceu de especificar '
                'como gostaria de visualizar a listagem de itens entregues. Tente '
                'utilizar o comando dessa forma: `!mice orders all` para exibir todos '
                'os itens entregues desde o começo (de forma mais detalhada) ou '
                '`!mice orders latest` para exibir somente os últimos 8.'
                '\n\n⚠️ Apagarei essa mensagem daqui 20 segundos.',
                delete_after=20
            )
            return

        if query == "latest":
            response = api.list_latest_orders()
            if response.total == 0:
                await ctx.channel.send("Nenhum item foi distribuído ainda!")
                return

            embed = Embed(
                title="Últimas Entregas",
                description=f'🐭 {ctx.author.mention} estou exibindo os '
                            f'últimos 8 itens que registrei mas ao todo já '
                            f'entreguei **{response.total}** itens.'
            )
            for order in response.orders:
                embed.add_field(name="código", value=order.product.code)
                embed.add_field(
                    name="De/Para",
                    value=f"{order.mod_display_name}/{order.owner_display_name}",
                )
                embed.add_field(
                    name="Requisitado em",
                    value=f'{order.requested_at.strftime("%d/%m/%Y %H:%M:%S")}',
                )

            await ctx.message.delete()
            await ctx.channel.send(embed=embed)
            return

        if query == "all":
            response = api.list_orders(query=OrderQuery(limit=200))
            if response.total == 0:
                await ctx.channel.send("Nenhum item foi distribuído ainda!")
                return

            message = (
                f"🐭 {ctx.author.mention}, aqui está a listagem de itens "
                f"entregues que eu registrei.\nAté o momento "
                f"**{response.total}** itens foram entregues:\n\n"
            )

            index = 0
            await ctx.message.delete()
            for order in response.orders:
                message += f"**Código**: {order.product.code}\n"
                message += f'**Criado em**: {order.product.created_at.strftime("%d/%m/%Y %H:%M:%S")}\n'
                message += f"**Descrição**: {order.product.summary}\n"
                message += f'**Entregue pelo Moderador**: {order.mod_display_name}\n'
                message += f'**ID do Moderador**: {order.mod_id}\n'
                message += f"**Entregue para**: {order.owner_display_name}\n"
                message += f'**Solicitado em**: {order.requested_at.strftime("%d/%m/%Y %H:%M:%S")}\n'
                message += f"{'-'* 15}\n"

                index += 1
                if index == 5:
                    await ctx.channel.send(message)
                    index = 0
