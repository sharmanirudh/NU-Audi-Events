import os
from flask import Flask, redirect, jsonify, request
from flask_cors import CORS
import utils
import requests

# User-defined imports
# from brain import *
from firebasedb import *
from utils import *

app = Flask(__name__)
CORS(app)

@app.route('/oauth/faculty', methods=['POST'])
def login_faculty():
	if request.method == 'POST':
		email = request.form.get('email')
		passw = request.form.get('passw')
		auth = firebase.auth()
		user = ""
		try:
			user = auth.sign_in_with_email_and_password(email, passw)
			key = random_string_generator(size=13)
			f = utils.Faculty(email, key)
			all_faculties = getAllFaculties()
			if all_faculties.each() != None:
				flag = False
				for faculty in all_faculties.each():
					print(faculty.key())
					f2 = getFacultyDetails(faculty.key())
					if f == f2:
						flag = True
						setFacultyOffline(f2)
						print("Faculty exists")
						break
				if not flag:
					registerFaculty(f, passw)
					setFacultyOffline(f)
				else:
					print("Faculty not registered.")
			else:
				registerFaculty(f, passw)
				setFacultyOffline(f)
		except requests.exceptions.HTTPError as e:
			print(e)
		return jsonify(user)

# Registers a student to the attendence portal and returns status
@app.route('/oauth/student', methods=['POST'])
def login_student():
	if request.method == 'POST':
		name = request.form.get('name')
		email = request.form.get('email')
		mac = request.form.get('mac')
		key = random_string_generator(size=13)
		s = utils.Student(name, email, mac, key)
		all_students = getAllStudents()
		if all_students.each() != None:
			flag = False
			for student in all_students.each():
				print(student.key())
				s2 = getStudentDetails(student.key())
				if s == s2:
					flag = True
					setStudentOnline(s2)
					print("Student exists")
					break
			if not flag:
				registerStudent(s)
				setStudentOnline(s)
			else:
				print("Student not registered.")
		else:
			registerStudent(s)
			setStudentOnline(s)
		return jsonify(utils.Response(status_code=303, text='successfully logged in.').json())

@app.route('/events/online-events', methods=['GET'])
def get_all_online_events():
	all_online_events_json = []
	if request.method == 'GET':
		all_online_events = getAllOnlineEvents()
		if all_online_events.each() != None:
			print(all_online_events.val())
			for event in all_online_events.each():
				print(event.key())
				print(event.val())
				e = getEventDetails(event.key())
				print(all_online_events_json.append(e.json()))
	return jsonify(utils.Response(status_code=200, text=all_online_events_json).json())


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