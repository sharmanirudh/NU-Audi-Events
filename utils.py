import string
import random
import time
import datetime

########### Student ##########################################################################

class Student:
	name = ''
	email = ''
	mac = ''
	key = ''

	def __init__(self, name, email, mac, key):
		self.name = name
		self.email = email
		self.mac = mac
		self.key = key

	def json(self):
		return {
		"name": self.name,
		"email": self.email,
		"mac": self.mac,
		"key": self.key,
		}

########### Faculty ##########################################################################

class Faculty:
	name = ''
	email = ''
	key = ''

	def __init__(self, name, email, key):
		self.name = name
		self.email = email
		self.key = key

	def json(self):
		return {
		"name": self.name,
		"email": self.email,
		"key": self.key,
		}

########### Password of Faculty ##############################################################

class Password:
	password = ''
	last_updated = ''
	last_two_passwords = ['', '']

	def __init__(self, password, last_updated='', last_two_passwords=['', '']):
		self.password = password
		self.last_updated = timestamp_generator()
		self.last_two_passwords[0] = self.password

	def validatePassword(self, password):
		if not len(password) >= 7:
			return False
		else:
			return True

	# def setNewFacultyPassword(self, key, old_password, new_password): # key of faculty
	# 	if not old_password == self.password:
	# 		return False
	# 	else:
	# 		if not validatePassword(new_password):
	# 			return False
	# 		else:
	# 			self.password = new_password
	# 			self.last_updated = timestamp_generator()
	# 			self.last_two_passwords[1] = self.last_two_passwords[0]
	# 			self.last_two_passwords[0] = new_password
	# 			setFacultyPassword(key, self)
	# 			return True

	def json(self):
		return {
		"password": self.password,
		"last_updated": self.last_updated,
		"last_two_passwords": self.last_two_passwords,
		}

########### Session ##########################################################################

class Session:
	login_stamp = ''
	logout_stamp = ''

	def __init__(self):
		self.login_stamp = timestamp_generator()

	def setLoginStamp(self):
		self.login_stamp = timestamp_generator()

	def setLogoutStamp(self):
		self.logout_stamp = timestamp_generator()

	def json(self):
		return {
		'login_stamp': self.login_stamp,
		'logout_stamp': self.logout_stamp,
		}

########### Event ############################################################################

class Event:
	name = ''
	speaker = ''
	event_start_time = ''
	event_end_time = ''
	attendance_start_time = ''
	attendance_end_time = ''
	date = ''
	summary = ''
	attendees = []
	key = ''

	def __init__(self, name, speaker, event_start_time, event_end_time, date, attendance_start_time, attendance_end_time, key, attendees=[], summary=''):
		self.name = name
		self.speaker = speaker
		self.event_start_time = event_start_time
		self.event_end_time = event_end_time
		self.date = date
		self.attendance_start_time = attendance_start_time
		self.attendance_end_time = attendance_end_time
		self.key = key

	def addSummary(self, summary):
		self.summary = summary

	def json(self):
		return {
		"name": self.name,
		"speaker": self.speaker,
		"event_start_time": self.event_start_time,
		"event_end_time": self.event_end_time,
		"date": self.date,
		"summary": self.summary,
		"attendance_start_time": self.attendance_start_time,
		"attendance_end_time": self.attendance_end_time,
		"attendees": self.attendees,
		"key": self.key,
		}

########### Response #########################################################################

class Response:
	status_code = ''
	text = ''
	next_link = ''
	expecting_input = False

	def __init__(self, status_code, text, next_link=None, expecting_input=False):
		self.status_code = status_code
		self.text = text
		self.next_link = next_link
		self.expecting_input = expecting_input

	def json(self):
		return {
		"status_code": self.status_code,
		"text": self.text,
		"next_link": self.next_link,
		"expecting_input": self.expecting_input
		}

########### Random ###########################################################################

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

########### Timestamp ########################################################################

def timestamp_generator():
	ts = time.time()
	return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')