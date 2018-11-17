import string
import random
import time
import datetime
from collections import OrderedDict

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

	def __eq__(self, other):
	    """Overrides the default implementation"""
	    if isinstance(other, self.__class__):
	        return self.email == other.email
	    return False

	def __ne__(self, other):
	    """Overrides the default implementation (unnecessary in Python 3)"""
	    return not self.__eq__(other)

	def json(self):
		return {
		"name": self.name,
		"email": self.email,
		"mac": self.mac,
		"key": self.key,
		}

########### Faculty ##########################################################################

class Faculty:
	email = ''
	key = ''

	def __init__(self, email, key):
		self.email = email
		self.key = key

	def __eq__(self, other):
	    """Overrides the default implementation"""
	    if isinstance(other, self.__class__):
	        return self.email == other.email
	    return False

	def __ne__(self, other):
	    """Overrides the default implementation (unnecessary in Python 3)"""
	    return not self.__eq__(other)

	def json(self):
		return {
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
	key = ''

	def __init__(self, key, login_stamp='', logout_stamp=''):
		if not login_stamp:
			self.login_stamp = timestamp_generator()
		else:
			self.login_stamp = login_stamp
		if logout_stamp:
			self.logout_stamp = logout_stamp
		self.key = key

	def setLoginStamp(self):
		self.login_stamp = timestamp_generator()

	def setLogoutStamp(self):
		self.logout_stamp = timestamp_generator()

	def json(self):
		return {
		"login_stamp": self.login_stamp,
		"logout_stamp": self.logout_stamp,
		"key": self.key
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
	attendees = OrderedDict()
	key = ''

	def __init__(self, name, speaker, event_start_time, event_end_time, date, attendance_start_time, attendance_end_time, key, attendees=OrderedDict(), summary=''):
		self.name = name
		self.speaker = speaker
		self.event_start_time = event_start_time
		self.event_end_time = event_end_time
		self.date = date
		self.attendance_start_time = attendance_start_time
		self.attendance_end_time = attendance_end_time
		self.key = key
		self.attendees = attendees
		self.summary = summary

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

	def __init__(self, status_code, text):
		self.status_code = status_code
		self.text = text

	def json(self):
		return {
		"status_code": self.status_code,
		"text": self.text,
		}

########### Random ###########################################################################

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

########### Timestamp ########################################################################

def timestamp_generator():
	ts = time.time()
	return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def string_to_timestamp(date_time_str):
	return datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
	# "Jun 28 2018 at 7:40AM" -> "%b %d %Y at %I:%M%p"
	# "September 18, 2017, 22:19:55" -> "%B %d, %Y, %H:%M:%S"
	# "Sun,05/12/99,12:30PM" -> "%a,%d/%m/%y,%I:%M%p"
	# "Mon, 21 March, 2015" -> "%a, %d %B, %Y"
	# "2018-03-12T10:12:45Z" -> "%Y-%m-%dT%H:%M:%SZ"