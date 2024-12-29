import pytest
import uuid

@pytest.fixture(scope="module")
def bot_name():
    return f"sample-bot-{uuid.uuid4()}"

@pytest.mark.create
def test_create_bot(bot_page, bot_name, bot_data):
    response = bot_page.create_bot(bot_name, bot_data["url"])
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == bot_name
    assert data['url'] == bot_data['url']
    assert data['intents'] == []

@pytest.mark.get
def test_get_bot(bot_page, bot_name):
    response = bot_page.get_bot(bot_name)
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == bot_name
    assert data['url'] == "http://example.com"
    assert data['intents'] == []

@pytest.mark.update
def test_update_bot(bot_page, bot_name):
    update_data = {
        "intents": ["play_sound", "tell_joke"]
    }
    response = bot_page.update_bot(bot_name, update_data["intents"])
    assert response.status_code == 200
    data = response.json()
    assert data['intents'] == update_data["intents"]

@pytest.mark.update
def test_patch_bot(bot_page, bot_name):
    patch_data = {
        "url": "http://example.com"
    }
    response = bot_page.patch_bot(bot_name, patch_data["url"])
    assert response.status_code == 200
    data = response.json()
    assert data['url'] == patch_data["url"]
    assert data['intents'] == ["play_sound", "tell_joke"]

@pytest.mark.delete
def test_delete_bot(bot_page, bot_name):
    response = bot_page.delete_bot(bot_name)
    assert response.status_code == 200

@pytest.mark.get
def test_bot_not_found(bot_page, bot_name):
    response = bot_page.get_bot(bot_name)
    assert response.status_code == 404
    data = response.json()
    assert data['error'] == 'Bot not found'

@pytest.mark.special
def test_create_bot_missing_url(bot_page, bot_name):
    response = bot_page.create_bot(bot_name, None)
    assert response.status_code == 400
    data = response.json()
    assert data['error'] == 'URL is required'

@pytest.mark.special
def test_update_bot_empty_intents(bot_page, bot_name):
    bot_page.create_bot(bot_name, "http://example.com")
    response = bot_page.update_bot(bot_name, [])
    assert response.status_code == 200
    data = response.json()
    assert data['intents'] == []

@pytest.mark.special
def test_update_bot_invalid_intents(bot_page, bot_name):
    bot_page.create_bot(bot_name, "http://example.com")
    response = bot_page.update_bot(bot_name, ["invalid_intent"])
    assert response.status_code == 400
    data = response.json()
    assert data['error'] == 'Invalid intent type'

@pytest.mark.special
def test_patch_bot_invalid_data(bot_page, bot_name):
    bot_page.create_bot(bot_name, "http://example.com")
    response = bot_page.patch_bot(bot_name, {"invalid": "data"})
    assert response.status_code == 400
    data = response.json()
    assert data['error'] == 'Invalid data format'

@pytest.mark.special
def test_concurrent_bot_creation(bot_page, bot_name):
    import threading

    def create_bot():
        return bot_page.create_bot(bot_name, "http://example.com")

    threads = [threading.Thread(target=create_bot) for _ in range(5)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    response = bot_page.get_bot(bot_name)
    assert response.status_code == 200

@pytest.mark.special
def test_bot_intents_case_sensitivity(bot_page, bot_name):
    bot_page.create_bot(bot_name, "http://example.com")
    bot_page.update_bot(bot_name, ["play_sound", "tell_joke"])
    response = bot_page.get_bot(bot_name)
    data = response.json()
    assert "play_sound" in data['intents']
    assert "tell_joke" in data['intents']
