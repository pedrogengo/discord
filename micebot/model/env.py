from pydantic import BaseSettings


class Environment(BaseSettings):
    api_endpoint: str = "http://localhost:8000"
    discord_user: str = "ds_user"
    discord_pass: str = "ds_pass"
    discord_token: str = "NzM0NTY1MDE4ODkyMzY5OTYx.XxWYRQ.HrTqwfjW_nOrRsxDWqq0DwHpHPg"  # noqa
    command_prefix: str = "!mice "
    thumbnail_url: str = "https://raw.githubusercontent.com/micebot/assets/master/images/logo-64x64.png"  # noqa


env: Environment = Environment()
