from flask import Flask, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json, random, string

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(40), nullable=True)
    name = db.Column(db.String(40), nullable=False)
    current_game_id = db.Column(db.BigInteger, db.ForeignKey('playedgame.id'), nullable=True)
    fantom = db.Column(db.Boolean, default=False)
    ready_for_game = db.Column(db.Boolean, default=False)
    host = db.Column(db.Boolean, default=False)

    current_played_game = db.relationship('PlayedGame', backref='users')

    def __repr__(self):
        return f'User {self.username}'


class AllGames(db.Model):
    __tablename__ = 'allgames'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum('Riddle', 'Recycle', name='game_types'))
    json_data = db.Column(db.String(5000), nullable=True)



class PlayedGame(db.Model):
    __tablename__ = 'playedgame'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.BigInteger, db.ForeignKey('allgames.id'))
    state = db.Column(db.Enum('Preparing', 'Playing', 'Finished', name='game_states'))  # Enum for game state
    party_code = db.Column(db.String(5), nullable=False)
    private = db.Column(db.Boolean, default=False)
    temp_json_data = db.Column(db.String(5000), nullable=True)

    game_type = db.relationship('AllGames', backref='played_games')

    def __repr__(self):
        return f'PlayedGame {self.name}'


class GameStatistics(db.Model):
    __tablename__ = 'gamestatistics'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    played_game_id = db.Column(db.BigInteger, db.ForeignKey('playedgame.id'))
    points_earned = db.Column(db.BigInteger, nullable=False)

    user = db.relationship('Users', backref='statistics')
    played_game = db.relationship('PlayedGame', backref='statistics')

    def __repr__(self):
        return f'GameStatistics {self.points_earned}'



def insert_default_games():
    if AllGames.query.count() == 0:
        game1 = AllGames(type='Riddle', json_data=json.dumps({'src': 'RiddleGameDemonstration.png'}))
        game2 = AllGames(type='Recycle', json_data=json.dumps({'src': 'RecycleGameDemonstration.png'}))

        db.session.add(game1)
        db.session.add(game2)

        db.session.commit()


def generate_game_code():
    return ''.join(random.choices(string.ascii_uppercase, k=5))

with app.app_context():
    db.drop_all()
     # games = AllGames.query.filter(AllGames.json_data == None).all()
    db.create_all()
    insert_default_games()







#Routes#################################################################################
@app.route('/api/fantom_user') 
def get_fantom_user():
    id = request.cookies.get('userId')

    if id != None:
        fantom_user = Users.query.get(id)
    else:
        fantom_user = Users(name='user#', fantom=True)
        db.session.add(fantom_user)
        db.session.commit()
        fantom_user.name += f"{fantom_user.id:04d}"
        db.session.commit()

    user_data = {
        'id': fantom_user.id,
        'name': fantom_user.name,
        'current_game_id': fantom_user.current_game_id,
    }

    response = jsonify(user_data)
    #cookie is set by client
    response.set_cookie('userId', value=str(user_data['id']))


    return response


@app.route('/api/all_games') 
def get_all_games():
    games = AllGames.query.all()

    games_data = [
        {
            'id': str(game.id),
            'name': game.type,
        }   
        for game in games
    ]

    return jsonify(games_data)


@app.route('/api/game_info') 
def get_game_info():
    game = AllGames.query.get(request.args['id'])
    if game == None:
        return jsonify({}), 404
    
    src = url_for('static', filename=f'{json.loads(game.json_data)["src"]}', _external=True)
    data = {
        'routeName': game.type, 
        'src': src,
    }
    return jsonify(data)

    

@app.route('/api/played_game') 
def get_played_game(): 
    game = PlayedGame.query.get(request.args['id'])
    if game == None:
        return jsonify({}), 404
    data = {
        "id": game.id,
        "game_id": game.game_id,
        "state": game.state,
        "party_code": game.party_code,
        "private": game.private,
        "data": game.temp_json_data
    }
    return jsonify(data)
       


@app.route('/api/create_game_for', methods=["POST"]) 
def post_create_game_for():    
    data = request.get_json() 
    host_id = data['userId']
    new_game_id = data['gameId']
    is_private = data['private']
    host = Users.query.get(host_id)

    if not host:
        return jsonify({}), 404
    
    #if user already has game - not allow to create game
    if(host.current_game_id != None):
        return jsonify({}), 404
    #if user has game with status: preparing - give host to someone else or delete game
    game = PlayedGame.query.get(host.current_game_id)
    if(game):
        return jsonify({}), 200

    #some day - check if party code is not unique
    new_game = PlayedGame(
        game_id=new_game_id, 
        state="Preparing",
        party_code=generate_game_code(),
        private=is_private)

    db.session.add(new_game)
    db.session.commit()

    host.current_game_id = new_game.id
    host.ready_for_game = False
    host.host = True

    db.session.add(host)
    db.session.commit()

    return jsonify({}), 200


@app.route('/api/game_players') 
def get_game_players(): 
    game = PlayedGame.query.get(request.args['id'])
    if game == None:
        return jsonify({}), 404
    users = game.users
    data = [{
        'id': user.id,
        'name': user.name,
        'current_game_id': user.current_game_id,
        'ready_for_game': user.ready_for_game,
        'host': user.host,
    } for user in users]

    return jsonify(data)


@app.route('/api/disconnect_player') 
def post_disconnect_player(): 
    player = Users.query.get(request.args['id'])
    if player == None:
        return jsonify({}), 404



    return jsonify({}), 200


if __name__ == '__main__':
    app.run(debug=True)
