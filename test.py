from unittest import TestCase
from app import app
from flask import session, json
from boggle import Boggle


class FlaskTests(TestCase):
    def setUp(self):
        """Setup to run before each test case."""
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.client = app.test_client()

    def tearDown(self):
        """Tear down after each test case."""
        pass

    def test_homepage(self):
        """Ensure homepage works and board is set in session."""
        with self.client as client:
            response = client.get('/')
            self.assertIn('board', session)
            self.assertEqual(response.status_code, 200)
            self.assertIn('game-board', response.get_data(as_text=True))

    def test_valid_word(self):
        """Test check a valid word."""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [['T', 'E', 'S', 'T', 'S'],
                                 ['T', 'E', 'S', 'T', 'S'],
                                 ['T', 'E', 'S', 'T', 'S'],
                                 ['T', 'E', 'S', 'T', 'S'],
                                 ['T', 'E', 'S', 'T', 'S']]
            response = client.get('/check-word?word=test')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test checking an invalid word."""
        with self.client as client:
            response = client.get('/check-word?word=xxxx')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'not-word')

    def test_word_not_on_board(self):
        """Test a word that cannot be formed on the board."""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [['A', 'B', 'C', 'D', 'E'],
                                 ['F', 'G', 'H', 'I', 'J'],
                                 ['K', 'L', 'M', 'N', 'O'],
                                 ['P', 'Q', 'R', 'S', 'T'],
                                 ['U', 'V', 'W', 'X', 'Y'],]
            response = client.get('/check-word?word=test')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'not-on-board')

    def test_post_score(self):
        """Test score posting and session update."""
        with self.client as client:
            response = client.post('/post-score', data=json.dumps({'score': 100}), content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertIn('highscore', session)
            self.assertIn('numplays', session)