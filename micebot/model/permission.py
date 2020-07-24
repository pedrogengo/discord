from typing import List

from discord import Role

ROLE_PERMISSION = ["admin"]


def can_use_command(roles: List[Role]) -> bool:
    for role in roles:
        if role.name.lower() in ROLE_PERMISSION:
            return True
    return False
