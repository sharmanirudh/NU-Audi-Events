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
		user = facultySignInWithEmailAndPassword(email, passw)
		if user == None:
			return jsonify(utils.Response(status_code=400, text='Either email or password is incorrect.').json())
		id_token = user["idToken"]
		key = random_string_generator(size=13)
		f = utils.Faculty(email, key, id_token)
		all_faculties = getAllFaculties()
		if all_faculties.each() != None:
			flag = False
			for faculty in all_faculties.each():
				print(faculty.key())
				f2 = getFacultyDetails(faculty.key())
				if f == f2:
					flag = True
					setFacultyOnline(f2.key)
					print("Faculty exists")
					break
			if not flag:
				registerFaculty(f, passw)
				setFacultyOnline(f.key)
			else:
				print("Faculty not registered.")
		else:
			registerFaculty(f, passw)
			setFacultyOnline(f.key)
			print(e)
		return jsonify(user)

# Registers a student to the attendence portal and returns status
@app.route('/oauth/student', methods=['POST'])
def login_student():
	if request.method == 'POST':
		name = request.form.get('name')
		email = request.form.get('email')
		mac = request.form.get('mac')
		id_token = request.form.get('id_token')
		image_url = request.form.get('image_url')
		key = random_string_generator(size=13)
		s = utils.Student(name, email, mac, image_url, key, id_token)
		all_students = getAllStudents()
		if all_students.each() != None:
			flag = False
			for student in all_students.each():
				print(student.key())
				s2 = getStudentDetails(student.key())
				if s == s2:
					flag = True
					setStudentOnline(s2.key)
					setStudentIdToken(s2.key, id_token)
					print("Student exists")
					break
			if not flag:
				registerStudent(s)
				setStudentOnline(s.key)
			else:
				print("Student not registered.")
		else:
			registerStudent(s)
			setStudentOnline(s.key)
		return jsonify(utils.Response(status_code=303, text='successfully logged in.').json())

@app.route('/oauth/student/logout', methods=['POST'])
def logout_student():
	if request.method == 'POST':
		value = request.form.get('value')
		arr = value.split(":")
		id_token = utils.decrypt(arr[0], 4, 12)
		session_id = arr[1]
		original_id_token = ''
		key = ''
		all_students = getAllStudents()
		if all_students.each() != None:
			for student in all_students.each():
				key = student.key()
				original_id_token = getStudentIdToken(key)
				if id_token == original_id_token:
					setStudentOffline(key)
					c = utils.Cookie(id_token, session_id, key)
					deleteCookie(c)
					return jsonify(utils.Response(status_code=200, text='Student successfully logged out.').json())
		return jsonify(utils.Response(status_code=404, text='Logout failed. Student not found').json())

@app.route('/oauth/faculty/logout', methods=['POST'])
def logout_faculty():
	if request.method == 'POST':
		value = request.form.get('value')
		arr = value.split(":")
		id_token = utils.decrypt(arr[0], 4, 12)
		session_id = arr[1]
		original_id_token = ''
		key = ''
		all_faculties = getAllFaculties()
		if all_faculties.each() != None:
			for faculty in all_faculties.each():
				key = faculty.key()
				original_id_token = getFacultyIdToken(key)
				if id_token == original_id_token:
					c = utils.Cookie(id_token, session_id, key)
					setFacultyOffline(key)
					deleteCookie(c)
					return jsonify(utils.Response(status_code=200, text='Faculty successfully logged out.').json())
		return jsonify(utils.Response(status_code=404, text='Logout failed. Faculty not found').json())
		

@app.route('/set-cookie', methods=['POST'])
def set_cookie():
	if request.method == 'POST':
		value = request.form.get('value')
		arr = value.split(":")
		id_token = utils.decrypt(arr[0], 4, 12)
		session_id = arr[1]
		original_id_token = ''
		key = ''
		all_students = getAllStudents()
		flag = False
		if all_students.each() != None:
			for student in all_students.each():
				key = student.key()
				original_id_token = getStudentIdToken(key)
				print(id_token)
				print(original_id_token)
				if id_token == original_id_token:
					flag = True
					break
		elif flag == False:
			all_faculties = getAllFaculties()
			if all_faculties.each() != None:
				for faculty in all_faculties.each():
					key = faculty.key()
					original_id_token = getFacultyIdToken(key)
					if id_token == original_id_token:
						flag = True
						break
		if flag == False:
			return jsonify(utils.Response(status_code=404, text='Wrong request data. Cookie not set.').json())
		c = utils.Cookie(id_token, session_id, key)
		setCookie(c)
		return jsonify(utils.Response(status_code=201, text='Cookie successfully set.').json())

@app.route('/validate-cookie', methods=['POST'])
def validate_cookie():
	if request.method == 'POST':
		value = request.form.get('value')
		all_cookies = getAllCookies()
		if all_cookies.each() != None:
			for cookie in all_cookies.each():
				key = cookie.key()
				c = cookie.val()
				# print(c.keys()[0])
				# print(c.values()[0])
				if value.encode('UTF-8') == utils.encrypt(c.values()[0], 4, 12) + ':' + c.keys()[0]:
					return jsonify(utils.Response(status_code=200, text='Valid cookie.').json())
		return jsonify(utils.Response(status_code=200, text='Invalid cookie.').json())

@app.route('/students/profile', methods=['POST'])
def user_profile():
	if request.method == 'POST':
		value = request.form.get('value')
		arr = value.split(":")
		id_token = utils.decrypt(arr[0], 4, 12)
		session_id = arr[1]
		original_id_token = ''
		key = ''
		all_students = getAllStudents()
		flag = False
		profile_json = ''
		if all_students.each() != None:
			for student in all_students.each():
				key = student.key()
				original_id_token = getStudentIdToken(key)
				if id_token == original_id_token:
					flag = True
					profile_json = getStudentDetails(key).json()
					break
		elif flag == False:
			all_faculties = getAllFaculties()
			if all_faculties.each() != None:
				for faculty in all_faculties.each():
					key = faculty.key()
					original_id_token = getFacultyIdToken(key)
					if id_token == original_id_token:
						flag = True
						profile_json = getFacultyDetails(key).json()
						break
		if flag == False:
			return jsonify(utils.Response(status_code=404, text='User not found.').json())
		return jsonify(utils.Response(status_code=200, text=profile_json).json())

# GET event details for student to see only event details and not attendees
@app.route('/events', methods=['GET', 'POST', 'PUT'])
def manage_event():
	if request.method == 'GET':
		all_events_json = []
		all_events = getAllEvents()
		if all_events.each() != None:
			print(all_events.val())
			for event in all_events.each():
				print(event.key())
				print(event.val())
				e_json = getEventDetails(event.key()).json()
				e_json.pop('attendees')
				print(all_events_json.append(e_json))
		return jsonify(utils.Response(status_code=200, text=all_events_json).json())

	name = request.form.get('name')
	speaker = request.form.get('speaker')
	event_start_time = request.form.get('event_start_time')
	event_end_time = request.form.get('event_end_time')
	date = request.form.get('date')
	attendance_start_time = request.form.get('attendance_start_time')
	attendance_end_time = request.form.get('attendance_end_time')
	summary = request.form.get('summary')
	attendees = request.form.get('attendees')
	print(request.form);
	if not (name or speaker or event_start_time or event_end_time or date or attendance_start_time or attendance_end_time):
		return jsonify(utils.Response(status_code=422, text='Incomplete data to create/update new event').json())
	if attendees:
		attendees = [student_key.strip() for student_key in attendees.split(';') if student_key != '']
		print(attendees)
	else:
		attendees = OrderedDict()
	key = random_string_generator(size=13)
	e = utils.Event(name, speaker, event_start_time, event_end_time, date, attendance_start_time, attendance_end_time, key, summary=summary)

	if request.method == 'POST':
		makeNewEvent(e)
		return jsonify(utils.Response(status_code=201, text='Event created').json())

	if request.method == 'PUT':
		key = request.form.get('key')
		if getEventDetails(key).name is None:
			return jsonify(utils.Response(status_code=404, text='Event not found. Cannot update event.').json())
		e.key = key
		print(e.attendance_end_time)
		print(e.attendance_start_time)
		print(e.date)
		print(e.event_end_time)
		print(e.event_start_time)
		print(e.name)
		print(e.speaker)
		print(e.summary)
		print(e.attendees)
		print(e.key)
		makeNewEvent(e)
		print(attendees)
		for student_key in attendees:
			if getStudentDetails(student_key) is not None:
				markStudentAttendance(key, student_key)
		return jsonify(utils.Response(status_code=200, text='Event successfully updated.').json())

# GET event details for faculty to see event details and attendees
@app.route('/events/<key>', methods=['GET'])
def get_event_details(key):
	if request.method == 'GET':
		e = getEventDetails(key)
		if e.name is not None:
			all_attendees_json = []
			if e.attendees is not None:
				for attendee_key in e.attendees:
					print(attendee_key)
					attendee_json = getStudentDetails(attendee_key).json()
					attendee_json.pop('mac')
					print(all_attendees_json.append(attendee_json))
				print(all_attendees_json)
			e.attendees = all_attendees_json
			return jsonify(utils.Response(status_code=200, text=e.json()).json())
		return jsonify(utils.Response(status_code=404, text='Event not found.').json())

@app.route('/events/online-events', methods=['GET'])
def get_all_online_events():
	all_online_events_json = []
	if request.method == 'GET':
		current_time = string_to_timestamp(timestamp_generator())
		all_events = getAllEvents()
		if all_events.each() != None:
			print(all_events.val())
			for event in all_events.each():
				print(event.key())
				print(event.val())
				e = getEventDetails(event.key())
				attendance_start_time = string_to_timestamp(e.attendance_start_time)
				attendance_end_time = string_to_timestamp(e.attendance_end_time)
				# current time lies b/w start and end time set event online
				if max((current_time, attendance_start_time)) == current_time and max((attendance_end_time, current_time)) == attendance_end_time:
					e_json = e.json()
					print(all_online_events_json.append(e_json))
					e_json.pop('attendees')
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
		mac = request.form.get('mac')
		value = request.form.get('value')
		arr = value.split(":")
		id_token = utils.decrypt(arr[0], 4, 12)
		session_id = arr[1]
		original_id_token = ''
		key = ''
		all_students = getAllStudents()
		if all_students.each() != None:
			for student in all_students.each():
				key = student.key()
				original_id_token = getStudentIdToken(key)
				print(id_token)
				print(original_id_token)
				if id_token == original_id_token:
					s = getStudentDetails(key)
					if s.email is not None:
						if s.mac == 'AB:06:4F:23:B1:AB':
							markStudentAttendance(event_key, key)
							return jsonify(utils.Response(status_code=200, text='Attendance marked.').json())
						else:
							return jsonify(utils.Response(status_code=404, text='Student not in auditorium.').json())
					break
		return jsonify(utils.Response(status_code=404, text='Attendance not marked.').json())

@app.route('/encrypt', methods=['POST'])
def encrypt():
	if request.method == 'POST':
		text = request.form.get('text')
		text = utils.encrypt(text, 4, 12)
		return jsonify(utils.Response(status_code=200, text=text).json())

@app.route('/decrypt', methods=['POST'])
def decrypt():
	if request.method == 'POST':
		text = request.form.get('text')
		text = utils.decrypt(text, 4, 12)
		return jsonify(utils.Response(status_code=200, text=text).json())

# API homepage
@app.route('/')
def default():
	welcome_text = "WELCOME TO NU-Audi-Events\n"
	return jsonify(utils.Response(status_code=200, text=welcome_text).json())


if __name__ == '__main__':
	app.run()