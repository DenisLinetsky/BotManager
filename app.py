from flask import Flask, request, jsonify
import random


app = Flask(__name__)

bots_db = {}

class Bot:
    def __init__(self, name, url, intents=None):
        self.id = random.randint(1, 1000)
        self.name = name
        self.url = url
        self.intents = intents if intents is not None else []

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'intents': self.intents
        }

def find_bot(name):
    return next((bot for bot in bots_db.values() if bot.name == name), None)


@app.route('/bot/<name>', methods=['POST'])
def create_bot(name):
    data = request.get_json()
    if name in bots_db:
        return jsonify({'error': 'Bot with this name already exists'}), 400
    if not data or 'url' not in data or not data['url']:
        return jsonify({'error': 'URL is required'}), 400

    bot = Bot(name, data['url'])
    bots_db[name] = bot
    return jsonify(bot.to_dict()), 201

@app.route('/bot/<name>', methods=['GET'])
def get_bot(name):
    bot = find_bot(name)
    if bot:
        return jsonify(bot.to_dict())
    return jsonify({'error': 'Bot not found'}), 404

@app.route('/bot/<name>', methods=['PUT'])
def update_bot(name):
    bot = find_bot(name)
    if not bot:
        return jsonify({'error': 'Bot not found'}), 404
    data = request.get_json()
    valid_intents = ['play_sound', 'tell_joke', 'disconnect']
    if 'intents' in data and any(intent.lower() not in valid_intents for intent in data['intents']):
        return jsonify({'error': 'Invalid intent type'}), 400
    bot.intents = [intent.lower() for intent in data['intents']]
    return jsonify(bot.to_dict())


@app.route('/bot/<name>', methods=['PATCH'])
def patch_bot(name):
    bot = find_bot(name)
    if not bot:
        return jsonify({'error': 'Bot not found'}), 404
    data = request.get_json()
    if not isinstance(data, dict) or 'url' in data and not isinstance(data['url'], str):
        return jsonify({'error': 'Invalid data format'}), 400
    if 'url' in data:
        bot.url = data['url']
    if 'intents' in data:
        bot.intents = data['intents']
    return jsonify(bot.to_dict())


@app.route('/bot/<name>', methods=['DELETE'])
def delete_bot(name):
    bot = find_bot(name)
    if not bot:
        return jsonify({'error': 'Bot not found'}), 404
    del bots_db[name]
    return jsonify({'message': 'Bot deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
