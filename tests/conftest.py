import pytest
from pages.bot_page import BotPage

@pytest.fixture(scope="module")
def bot_page():
    return BotPage()

@pytest.fixture(scope="module")
def bot_name():
    return "sample-bot"

@pytest.fixture(scope="module")
def bot_data():
    return {
        "url": "http://example.com"
    }

