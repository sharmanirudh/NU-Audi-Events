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

@app.route('/events', methods=['GET', 'POST', 'PUT'])
def manage_event():
	name = request.form.get('name')
	speaker = request.form.get('speaker')
	event_start_time = request.form.get('event_start_time')
	event_end_time = request.form.get('event_end_time')
	date = request.form.get('date')
	attendance_start_time = request.form.get('attendance_start_time')
	attendance_end_time = request.form.get('attendance_end_time')
	summary = request.form.get('summary')
	attendees = request.form.get('attendees')
	current_time = string_to_timestamp(timestamp_generator())

	if not (name or speaker or event_start_time or event_end_time or date or attendance_start_time or attendance_end_time):
		return jsonify(utils.Response(status_code=422, text='Incomplete data to create new event').json())
	if attendees:
		attendees = [student_key.strip() for student_key in attendees.split(';') if student_key != '']
		print(attendees)
	else:
		attendees = OrderedDict()
	key = random_string_generator(size=13)
	e = utils.Event(name, speaker, event_start_time, event_end_time, date, attendance_start_time, attendance_end_time, key, summary=summary)

	if request.method == 'GET':
		all_events_json = []
		all_events = getAllEvents()
		if all_events.each() != None:
			print(all_events.val())
			for event in all_events.each():
				print(event.key())
				print(event.val())
				e = getEventDetails(event.key())
				print(all_events_json.append(e.json()))
		return jsonify(utils.Response(status_code=200, text=all_events_json).json())		

	if request.method == 'POST':
		attendance_start_time = string_to_timestamp(attendance_start_time)
		attendance_end_time = string_to_timestamp(attendance_end_time)
		# current time lies b/w start and end time set event online
		if max((current_time, attendance_start_time)) == current_time and max((attendance_end_time, current_time)) == attendance_end_time:
			all_online_events = getAllOnlineEvents()
			if all_online_events.each() != None:
				return jsonify(utils.Response(status_code=409, text='Cannot create new event as an event already active.').json())
			else:
				key = random_string_generator(size=13)
				setEventOnline(key)
				makeNewEvent(e)
				return jsonify(utils.Response(status_code=201, text='Event created and set online').json())
		else:
			makeNewEvent(e)
			return jsonify(utils.Response(status_code=201, text='Event created').json())

	if request.method == 'PUT':
		key = request.form.get('key')
		e.key = key
		makeNewEvent(e)
		print(attendees)
		for student_key in attendees:
			if getStudentDetails(student_key) is not None:
				markStudentAttendance(key, student_key)
		return jsonify(utils.Response(status_code=200, text='Event successfully updated.').json())


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

@app.route('/events/<key>/add-summary', methods=['PUT'])
def add_summary_to_event(key):
	if request.method == 'PUT':
		summary = request.form.get('summary')
		e = getEventDetails(key)
		if e.name is not None:
			setEventSummary(key, summary)
			return jsonify(utils.Response(status_code=200, text='Summary successfully edited.').json())
		else:
			return jsonify(utils.Response(status_code=404, text='Event does not exists').json())
	return jsonify(utils.Response(status_code=404, text='Summary not edited.').json())

@app.route('/events/<event_key>/mark-attendance', methods=['PUT'])
def mark_student_attendance(event_key):
	if request.method == 'PUT':
		student_key = request.form.get('student_key')
		mac = request.form.get('mac')
		s = getStudentDetails(student_key)
		if s.email is not None:
			if s.mac == 'PB:01:98:BH:67:BD':
				markStudentAttendance(event_key, student_key)
				return jsonify(utils.Response(status_code=200, text='Attendance marked.').json())
			else:
				return jsonify(utils.Response(status_code=404, text='Student not in auditorium.').json())
		else:
			return jsonify(utils.Response(status_code=404, text='Attendance not marked.').json())

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