import random
import time
from flask import Flask, jsonify

app = Flask(__name__)

class Fish:
    def __init__(self, species):
        self.species = species
        self.health = 100
        self.hunger = 0
        self.x = random.randint(0, 100)
        self.y = random.randint(0, 100)

    def swim(self):
        self.x += random.randint(-5, 5)
        self.y += random.randint(-5, 5)
        self.hunger += 1
        self.health -= 1 if self.hunger > 50 else 0

    def eat(self):
        self.hunger = max(0, self.hunger - 30)
        self.health = min(100, self.health + 10)

fish = Fish(species="Goldfish")

@app.route('/status')
def get_status():
    return jsonify({
        "species": fish.species,
        "health": fish.health,
        "hunger": fish.hunger,
        "position": {"x": fish.x, "y": fish.y}
    })

@app.route('/swim')
def swim():
    fish.swim()
    return jsonify({"message": "Fish swam", "position": {"x": fish.x, "y": fish.y}})

@app.route('/eat')
def eat():
    fish.eat()
    return jsonify({"message": "Fish ate", "hunger": fish.hunger, "health": fish.health})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
