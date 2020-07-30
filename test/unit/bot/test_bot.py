from unittest.mock import patch

from micebot.bot import on_ready
from test.unit.test_case import TestAsync


class TestBot(TestAsync):
    @patch("micebot.bot.exit")
    @patch("micebot.bot.Api.authenticate", return_value=True)
    async def test_should_not_exit_when_the_app_is_authenticated(
        self, authenticate, exit_function
    ):
        await on_ready()
        authenticate.assert_called_once()
        exit_function.assert_not_called()

    @patch("micebot.bot.exit")
    @patch("micebot.bot.Api.authenticate", return_value=False)
    async def test_should_exit_when_the_app_is_not_authenticated(
        self, authenticate, exit_function
    ):
        await on_ready()
        authenticate.assert_called_once()
        exit_function.assert_called_once()
