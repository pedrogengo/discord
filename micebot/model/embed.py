from typing import List

from attr import dataclass
from discord import Embed, Colour

from micebot.model.env import env


@dataclass
class Field:
    key: str
    value: str
    inline: bool = True


def embed(
    title: str,
    fields: List[List[Field]] = None,
    description: str = None,
    footer: str = None,
    color: Colour = Colour.lighter_grey(),
    thumbnail: bool = False,
) -> Embed:
    """
    Create an embed using generic settings.

    Added the default thumbnail and card color.

    Args:
        - title: the title of the embed.
        - description: the card description.
        - fields: the fields to be added (it is recommended less than 9) items.
        - footer: the optional footer for the embed.

    Returns:
        - the embed instance.
    """
    embed_content = Embed(title=title, description=description, colour=color)

    if thumbnail:
        embed_content.set_thumbnail(url=env.thumbnail_url)

    if fields:
        for field in fields:
            for field_line in field:
                embed_content.add_field(
                    name=field_line.key,
                    value=field_line.value,
                    inline=field_line.inline,
                )

    if footer:
        embed_content.set_footer(text=footer)
    return embed_content
