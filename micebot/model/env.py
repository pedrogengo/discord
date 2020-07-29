from pydantic import BaseSettings


class Environment(BaseSettings):
    api_endpoint: str = "http://localhost:8000"
    datetime_formatter: str = "%d/%m/%Y %H:%M:%S"
    discord_user: str = "ds_user"
    discord_pass: str = "ds_pass"
    discord_token: str = (
        "NzM0NTY1MDE4ODkyMzY5OTYx.XxTi_A.NgY6B4BYXUvx_HLJNmu9c2CEFhU"
    )
    command_prefix: str = "!mice "
    thumbnail_url: str = "https://raw.githubusercontent.com/micebot/assets/master/images/logo-64x64.png"  # noqa
    default_product_summary: str = "E-Book"
    delete_message_after: int = 30


env: Environment = Environment()
