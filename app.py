import os
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

db = SQLAlchemy(app)
BASE_URL = '/api/v2/'

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    developer = db.Column(db.String(60), nullable=False)
    release_year = db.Column(db.String  (4), nullable=False)
    platform = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.String(1), nullable=False)


    def show(self):
        return {
            'id': self.id,
            'title': self.title,
            'developer': self.developer,
            'release' : self.release_year,
            'platform' : self.platform,
            'rating' : self.rating
        }
    

@app.route('/')
def home():
    return 'Welcome to my To-Do List'

@app.route(BASE_URL + 'create', methods=['POST'])
def addGame():
    if not request.json:
        abort(400, error = 'Missing body in request')
    if 'title' not in request.json:
        abort(400, error = 'Missing title in request')
    if 'developer' not in request.json:
        abort(400, error = 'Missing developer in request')
    if 'release' not in request.json:
        abort(400, error = 'Missing release in request')
    if 'platform' not in request.json:
        abort(400, error = 'Missing platform in request')
    if 'rating' not in request.json:
        abort(400, error = 'Missing rating in request')
    
    game = Game(title=(request.json['title']), developer=(request.json['developer']), status=False)
    db.session.add(game)
    db.session.commit()
    
    return jsonify({'Created game succesfully!': game.show()}), 201

@app.route(BASE_URL + 'create/<int:id>', methods=['POST'])
def addGameWithId(id):
    if game.query.get(id) is None:
        if not request.json:
            abort(400, error = 'Missing body in request')
        if 'title' not in request.json:
            abort(400, error = 'Missing title in request')
        if 'developer' not in request.json:
            abort(400, error = 'Missing developer in request')
        if 'release' not in request.json:
            abort(400, error = 'Missing release in request')
        if 'platform' not in request.json:
            abort(400, error = 'Missing platform in request')
        if 'rating' not in request.json:
            abort(400, error = 'Missing rating in request')
        
        game = Game(id=id,title=(request.json['title']), developer=(request.json['developer']), status=False)
        db.session.add(game)
        db.session.commit()
        
        return jsonify({'Created game succesfully!': game.show()}), 201
    else:
        return jsonify({'Id already in existace'}), 409

@app.route(BASE_URL + 'change/<int:id>', methods=['PATCH'])
def updateGame(id):
    game = game.query.get(id)
    if game is None:
        abort(404, error="game not found!")
        
    if 'title' and 'developer' not in request.json:
        abort(400, error = 'No body, nothing to change')
        
    if 'title' in request.json:
        game.title = request.json['title']
    if 'developer'in request.json:
        game.developer = request.json['developer']
    if 'release'in request.json:
        game.release = request.json['release']
    if 'platform'in request.json:
        game.platform = request.json['platform']
    if 'rating'in request.json:
        game.rating = request.json['rating']
        
    db.session.commit()
    return jsonify('game has been changed has been succesfully changed'), 200
    
@app.route(BASE_URL + 'games', methods=['GET'])
def getgames():
    allgames = Game.query.all()
    return jsonify({'These are all your games': [game.show() for game in allgames]}), 200

@app.route(BASE_URL + 'games/<int:id>', methods=['GET'])
def getGame(id):
    game = game.query.get(id)
    if game is None:
        abort(404, error="game not found!")
    return jsonify({'This is the game you asked for': game.show()}), 200

@app.route(BASE_URL + 'games/<int:id>', methods=['DELETE'])
def deleteGame(id):
    game = game.query.get(id)
    if game is None:
        abort(404, error="game not found!")
    db.session.delete(game)
    db.session.commit()
    
    return jsonify('game has been deleted'), 200


    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)