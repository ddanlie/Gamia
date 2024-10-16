from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    party_id = db.Column(db.BigInteger, nullable=True)
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
    name = db.Column(db.String(40), nullable=False)
    state = db.Column(db.Enum('Preparing', 'Playing', 'Finished', name='game_states'))  # Enum for game state
    party_code = db.Column(db.String(5), nullable=False)
    private = db.Column(db.Boolean, default=False)

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
        game1 = AllGames(type='Riddle', json_data=None)
        game2 = AllGames(type='Recycle', json_data=None)

        db.session.add(game1)
        db.session.add(game2)
        db.session.commit()



with app.app_context():
    db.drop_all()
     # games = AllGames.query.filter(AllGames.json_data == None).all()
    db.create_all()
    insert_default_games()







#Routes#################################################################################
@app.route('/api/fantom_user') 
def get_fantom_user():
    fantom_user = Users(name="user#", fantom=True)
    db.session.add(fantom_user)
    db.session.commit()
    fantom_user.name += f"{fantom_user.id:04d}"
    db.session.commit()

    user_data = {
        "id": fantom_user.name,
    }

    #debug, comment this later TODO
    db.session.delete(fantom_user)
    db.session.commit()
    #debug end

    return jsonify(user_data)


@app.route('/api/all_games') 
def get_all_games():
    games = AllGames.query.all()

    games_data = [
        {
            "id": game.id,
            "name": game.type
        }   
        for game in games
    ]

    return jsonify(games_data)



if __name__ == '__main__':
    app.run(debug=True)
