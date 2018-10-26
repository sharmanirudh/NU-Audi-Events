import os
from flask import Flask, redirect, jsonify
from flask_cors import CORS
import utils

# User-defined imports
# from brain import *
from firebasedb import *
from utils import *

app = Flask(__name__)
CORS(app)

# Registers a student to the attendence portal and returns the unique key
@app.route('/register/<name>/<email>/<mac>')
def register(name, email, mac):
	key = random_string_generator(size=13)
	s = utils.Student(name, email, mac, key)
	registerStudent(s)
	return jsonify(utils.Response(status_code=200, text=key).json())

# # Checks if a student with the same current email exists
# @app.route('/check_registration/<email>')
# def check_registration(mac):
# 	r = studentExists(mac)
# 	if not r:
# 		return jsonify(utils.Response(status_code=404, text="Student does not exist").json())
# 	else:
# 		return jsonify(utils.Response(status_code=200, text=r).json())

# # Logins the player into the game and starts the game env
# @app.route('/start/<key>')
# def start(key):
# 	player = getPlayerDetails(key)
# 	if player is not None:
# 		if not alreadyOnline(player):
# 			print(player.json())
# 			setOnline(player)
# 			t = "You are playing as " + player.name + " (" + player.hostname + "@" + player.hostip + ")\n"
# 			response = start_gameplay(player, get_random_word(WORDFILE))
# 			t += "\nWORD:- " + response['curr'] + "\n"
# 			return jsonify(utils.Response(status_code=200, text=t, expecting_input=True, next_link=response['w_id']).json())
# 		else:
# 			return jsonify(utils.Response(status_code=403, text="\nAnother instance of this game is already running. Please close all other instances and try again.").json())
# 	else:
# 		return jsonify(utils.Response(status_code=404, text="Invalid Key").json())

# @app.route('/guess/<key>/<word_id>/<guess>')
# def guess(key, word_id, guess):
# 	player = getPlayerDetails(key)
# 	new = guessListener(player, word_id, guess)
# 	if '*' in new:
# 		return jsonify(utils.Response(status_code=200, text="\nWORD:- " + new, expecting_input=True, next_link=word_id).json())
# 	else:
# 		addToHistory(player, word_id, new)
# 		return jsonify(utils.Response(status_code=200, text="\nCongratulations, you've guessed the word - " + new + " - successfully.", expecting_input=False, next_link=word_id).json())


# @app.route('/exit/<key>')
# def exit(key):
# 	player = getPlayerDetails(key)
# 	if player is not None:
# 		return setOffline(player)


@app.route('/')
def default():
	welcome_text = "WELCOME TO HANGMAN MULTIPLAYER\n[Developed by Harshit Budhraja]\n\nYou need to play this game in your terminal using the hangman.py script\n"
	return jsonify(utils.Response(status_code=200, text=welcome_text).json())


if __name__ == '__main__':
	app.run()