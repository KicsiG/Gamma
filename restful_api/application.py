#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import time

from flask import Flask, redirect, request, render_template, jsonify


class Data:
    def __init__(self):
        self.active_game = {}
        self.previous_games = {}

    @property
    def is_active_game(self):
        if self.active_game:
            return True

        return False

    @property
    def get_active_game(self):
        return self.active_game

    @property
    def get_active_game_start(self):
        return self.active_game.get('round_id')

    @property
    def get_previous_games(self):
        return self.previous_games

    def add_round(self, round_id):
        self.active_game.setdefault('round_id', round_id)
        self.active_game.setdefault('players', [])
        self.active_game.setdefault('votes', [])

    def get_round(self, round_id):
        return self.previous_games.get(round_id)

    @property
    def get_round_id(self):
        return self.active_game.get('round_id')

    def check_name(self, name):
        if self.active_game.get('players'):
            if name in self.active_game.get('players') or not name:
                return (
                    'Your chosen name is not unique. '
                    'Please select an other one.'
                )

        return ''

    @classmethod
    def check_number(cls, number):
        try:
            number = int(number)

            if number <= 0:
                raise ValueError
        except ValueError:
            return 'Please give a positive integer.'

        return ''

    def add_vote(self, name, number):
        self.active_game['players'].append(name)
        self.active_game['votes'].append(int(number))

    @property
    def get_winner_data(self):
        winner = None
        winner_number = None
        temporary = {}

        for name, number in zip(
                self.active_game.get('players'),
                self.active_game.get('votes')
        ):
            temporary.setdefault(number, [])
            temporary[number].append(name)

        for key, value in sorted(temporary.items()):
            if len(value) == 1:
                winner, = value
                winner_number = key

                break

        del temporary

        return winner, winner_number

    def close_round(self):
        round_id = self.get_round_id
        winner, winner_number = self.get_winner_data

        del self.active_game['round_id']

        self.previous_games.setdefault(
            round_id,
            self.active_game.copy()
        )
        self.previous_games[round_id].setdefault(
            'start',
            round_id
        )
        self.previous_games[round_id].setdefault(
            'end',
            int(time.time())
        )
        self.previous_games[round_id].setdefault(
            'winner',
            winner
        )
        self.previous_games[round_id].setdefault(
            'winner_number',
            winner_number
        )

        self.active_game.clear()

        return round_id


app = Flask(__name__)
data = Data()


@app.errorhandler(404)
def page_not_found(message):
    return render_template('error.html'), message


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form.get('yes') == 'Yes':
            return redirect('/start')

        else:
            return redirect('/sorry')

    if request.method == 'GET':
        return render_template('index.html')


@app.route('/sorry', methods=['GET'])
def sorry():
    return render_template('sorry.html')


@app.route('/start')
def start():
    if not data.is_active_game:
        data.add_round(int(time.time()))

        auto_close = threading.Thread(target=close_automatically)
        auto_close.start()

    return redirect('/submit')


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if not data.is_active_game:
        return redirect('/')

    if request.method == 'GET':
        return render_template('submit.html')

    if request.method == 'POST':
        name = request.form.get('name')
        number = request.form.get('number')

        user_error = data.check_name(name)
        number_error = data.check_number(number)

        if user_error or number_error:
            return render_template(
                'submit.html',
                user_error=user_error,
                number_error=number_error
            )

        else:
            data.add_vote(name, number)

        return redirect('/thanks')


@app.route('/thanks')
def thanks():
    if not data.is_active_game:
        return redirect('/')

    return render_template('thanks.html')


@app.route('/close')
def close():
    if not data.is_active_game:
        return jsonify(data.get_active_game)

    round_id = data.close_round()

    return jsonify({'round_id': round_id})


@app.route('/current_round')
def get_current_round():
    return jsonify(data.get_active_game)


@app.route('/get_all_rounds')
def get_all_rounds():
    return jsonify(data.get_previous_games)


@app.route('/list_all_rounds')
def list_all_rounds():
    previous_games = data.get_previous_games

    if not previous_games:
        return jsonify(data.get_previous_games)

    response = {}

    for key in previous_games:
        response.setdefault(key, {})
        response[key].setdefault(
            'start',
            previous_games[key].get('start')
        )
        response[key].setdefault(
            'end',
            previous_games[key].get('end')
        )
        response[key].setdefault(
            'number_of_praticipants',
            len(previous_games[key].get('players'))
        )

    return jsonify(response)


@app.errorhandler(404)
@app.route('/round/<int:round_id>')
def query_winner_and_winner_number(round_id):
    if not data.get_previous_games:
        return jsonify(data.get_previous_games)

    game_round = data.get_round(round_id)

    if not game_round:
        return jsonify({})

    response = {}
    response.setdefault(
        'winner',
        game_round.get('winner')
    )
    response.setdefault(
        'winner_number',
        game_round.get('winner_number')
    )

    return jsonify(response)


@app.route('/round2')
def query_winner_and_winner_number2():
    if not data.get_previous_games:
        return jsonify(data.get_previous_games)

    query_parameters = request.args

    try:
        round_id = int(query_parameters.get('round_id'))
    except ValueError:
        return jsonify({})

    game_round = data.get_round(round_id)

    if not game_round:
        return jsonify({})

    response = {}
    response.setdefault('winner', game_round.get('winner'))
    response.setdefault('winner_number', game_round.get('winner_number'))

    return jsonify(response)


@app.errorhandler(404)
@app.route('/statistics/<int:round_id>')
def query_statistics(round_id):
    if not data.get_previous_games:
        return jsonify(data.get_previous_games)

    game_round = data.get_round(round_id)

    if not game_round:
        return jsonify({})

    response = {}

    for item in game_round.get('votes'):
        response.setdefault(item, 0)
        response[item] += 1

    return jsonify(response)


@app.route('/statistics2')
def query_statisticsr2():
    if not data.get_previous_games:
        return jsonify(data.get_previous_games)

    query_parameters = request.args

    try:
        round_id = int(query_parameters.get('round_id'))
    except ValueError:
        return jsonify({})

    game_round = data.get_round(round_id)

    if not game_round:
        return jsonify({})

    response = {}

    for item in game_round.get('votes'):
        response.setdefault(item, 0)
        response[item] += 1

    return jsonify(response)


def close_automatically(remaining=60):
    time.sleep(remaining)

    with app.app_context():
        close()

    return True


if __name__ == '__main__':
    # app.run(debug=True)
    app.run()
