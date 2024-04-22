from flask import Flask, render_template, session, jsonify, request
from boggle import Boggle

class BoggleGame:
    def __init__(self, app):
        self.boggle = Boggle()
        self.app = app
        self.app.add_url_rule('/', 'homepage', self.show_homepage)
        self.app.add_url_rule('/check-word', 'check_word', self.check_word, methods=['GET'])
        self.app.add_url_rule('/post-score', 'post_score', self.post_score, methods=['POST'])

        def show_homepage(self):
            """Display initial game setup."""
            board = self.boggle.make_board()
            session['board'] = board
            return render_template('index.html', board=board)
        
        def check_word(self):
            """Check if the word is valid un the dictionary and on the board."""
            word = request.args.get('word')
            board = session.get('board')
            result = self.boggle.check_valid_word(board, word)
            return jsonify({'result': result})
        
        def post_score(self):
            """Handles posting scores and updates the session."""
            score = request.json['score']
            highscore = session.get('highscore', 0)
            numplays = session.get('numplays', 0)
            session['highscore'] = max(score, highscore)
            session['numplays'] = numplays + 1
            return jsonify(highscore=session['highscore'], numplays=session['numplays'])
        
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 's3c437k3y'
        game_manager = BoggleGame(app)