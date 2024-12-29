BotManager

BotManager is a RESTful web server for managing bots. It supports the following HTTP methods: POST, PUT, GET, PATCH, DELETE. The server uses an in-memory database to represent bot objects. The project also includes tests for all bot functionalities using PyTest.

Features

Create Bot: Add a new bot with a unique name and URL.

Get Bot: Retrieve details of an existing bot.

Update Bot: Replace the intents of an existing bot.

Patch Bot: Update specific attributes of an existing bot.

Delete Bot: Remove an existing bot.

Bot Attributes

Each bot has the following attributes:

id: Random number.

name: Unique name.

url: External URL (not used by the application).

intents: Array of supported intents. Supported intent types include:

play_sound

tell_joke

disconnect

Running the Server

To start the Flask server, run:

python app.py

The server will be running on http://localhost:5000.

API Endpoints

Create Bot

http

POST /bot/{name}

Request Body:

json

{ "url": "http://example.com" }

Response:

json

{

"id": "17",

"name": "sample-bot",

"intents": [],

"url": "http://example.com"

}

Get Bot

http

GET /bot/{name}

Response:

json

{

"id": "17",

"name": "sample-bot",

"intents": [],

"url": "http://example.com"

}

Update Bot

http

PUT /bot/{name}

Request Body:

json

{

"intents": ["play_sound", "tell_joke"]

} Response:

json

{

"id": "17",

"name": "sample-bot",

"intents": ["play_sound", "tell_joke"]

}

Patch Bot

http

PATCH /bot/{name}

Request Body:

json

{

"url": "http://example.com"

}

Response:

json

{

"id": "17",

"name": "sample-bot",

"intents": ["play_sound", "tell_joke"],

"url": "http://example.com"

}

Delete Bot

http

DELETE /bot/{name}

Response:

200 OK

Running Tests

To run tests, use the following command:

sh

pytest --html=report.html

This will generate an HTML report of the test results.

Using PyTest Markers

PyTest markers allow you to categorize and selectively run tests. Here are the custom markers used in this project:

create: Tests related to creating bots.

update: Tests related to updating bots.

delete: Tests related to deleting bots.

get: Tests related to retrieving bots.

special: Tests for special scenarios and edge cases.

You can run tests based on these markers using the -m option. For example:

Run all tests marked as "create":

sh

pytest -m create

Run all tests marked as "special":

sh

pytest -m special

Run all tests:

sh

pytest
