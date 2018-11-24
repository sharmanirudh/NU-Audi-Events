import pyrebase
import requests
import utils
import urllib
from utils import *

config = {
	'apiKey': "AIzaSyAaM8GmCDn5s6uqXiHJGjyvvYMhceXRdUE",
	'authDomain': "nu-audi-01.firebaseapp.com",
	'databaseURL': "https://nu-audi-01.firebaseio.com",
	'projectId': "nu-audi-01",
	'storageBucket': "nu-audi-01.appspot.com",
	'messagingSenderId': "1059501399871"
}
firebase = pyrebase.initialize_app(config)

########### Student ##########################################################################

def registerStudent(student):
	db = firebase.database()
	db.child("students").child(student.key).set(student.json())

def getStudentDetails(key):
	db = firebase.database()
	s = db.child("students").child(key)
	name = s.child("name").get().val()
	s = db.child("students").child(key)
	email = s.child("email").get().val()
	s = db.child("students").child(key)
	mac = s.child("mac").get().val()
	s = db.child("students").child(key)
	image_url = s.child("image_url").get().val()
	s = db.child("students").child(key)
	id_token = s.child("id_token").get().val()
	return utils.Student(name, email, mac, image_url, key, id_token=id_token)

def getStudentIdToken(key):
	db = firebase.database()
	s = db.child("students").child(key)
	id_token = s.child("id_token").get().val()
	return id_token

def getAllStudents():
	db = firebase.database()
	return db.child("students").get()

def setStudentIdToken(key, id_token):
	db = firebase.database()
	db.child("students").child(key).child("id_token").set(id_token)

def setStudentOnline(key):
	db = firebase.database()
	db.child("online_students").child(key).set(True)
	setStudentLoginStamp(key)

def setStudentOffline(key):
	db = firebase.database()
	db.child("online_students").child(key).remove()
	setStudentLogoutStamp(key)

########### Faculty ##########################################################################

def facultySignInWithEmailAndPassword(email, passw):
	auth = firebase.auth()
	user = ""
	try:
		user = auth.sign_in_with_email_and_password(email, passw)
	except requests.exceptions.HTTPError as e:
		print(e)
		return None
	return user

def registerFaculty(faculty, password="Faculty#123"):
	db = firebase.database()
	db.child("faculties").child(faculty.key).set(faculty.json())
	db.child("passwords").child(faculty.key).set(utils.Password(password).json())	

def getFacultyDetails(key):
	db = firebase.database()
	f = db.child("faculties").child(key)
	email = f.child("email").get().val()
	return utils.Faculty(email, key)

def getFacultyIdToken(key):
	db = firebase.database()
	s = db.child("faculties").child(key)
	id_token = s.child("id_token").get().val()
	return id_token

def getAllFaculties():
	db = firebase.database()
	return db.child("faculties").get()

def setFacultyOnline(key):
	db = firebase.database()
	db.child("online_faculties").child(key).set(True)
	setFacultyLoginStamp(key)

def setFacultyOffline(key):
	db = firebase.database()
	db.child("online_faculties").child(key).remove()
	setFacultyLogoutStamp(key)

########### Password #########################################################################

def setFacultyPassword(key, password): # key of faculty
	db = firebase.database()
	db.child("passwords").child(key).set(password.json())

def getFacultyPassword(key):
	db = firebase.database()
	return db.child("passwords").child(key)

def setNewFacultyPassword(key, old_password, new_password): # key of faculty
	password = getFacultyPassword(key)
	p = utils.Password(password.child("password").get().val(), password.child("last_updated").get().val(), password.child("last_two_passwords").get().val())

	print p.password
	print p.last_updated
	print p.last_two_passwords

	if not old_password == p.password:
		return False
	else:
		if not p.validatePassword(new_password):
			return False
		else:
			p.password = new_password
			p.last_updated = timestamp_generator()
			p.last_two_passwords[1] = p.last_two_passwords[0]
			p.last_two_passwords[0] = new_password
			setFacultyPassword(key, p)
			return True

########### Session ##########################################################################

def setStudentLoginStamp(key):
	db = firebase.database()
	session = utils.Session(random_string_generator(size=13))
	all_auth_stamps = db.child("student_auth_stamps").child(key).get()
	if all_auth_stamps.each() != None:
		flag = False
		for a in all_auth_stamps.each():
			orderedDict = a.val()
			if orderedDict["logout_stamp"] == "":
				flag = True
				print("New student auth stamp not created")
				break
		if not flag:
			db.child("student_auth_stamps").child(key).child(session.key).set(session.json())
		else:
			print("Student not logged out yet")
	else:
		db.child("student_auth_stamps").child(key).child(session.key).set(session.json())

def setStudentLogoutStamp(key):
	db = firebase.database()
	all_auth_stamps = db.child("student_auth_stamps").child(key).get()
	if all_auth_stamps.each() != None:
		for a in all_auth_stamps.each():
			orderedDict = a.val()
			if orderedDict["logout_stamp"] == "":
				session = utils.Session(a.key(), login_stamp=orderedDict["login_stamp"])
				session.setLogoutStamp()
				db.child("student_auth_stamps").child(key).child(session.key).set(session.json())
				print("Student logged out successfully")
				break
	else:
		print("Student logout failed")

def setFacultyLoginStamp(key):
	db = firebase.database()
	session = utils.Session(random_string_generator(size=13))
	all_auth_stamps = db.child("faculty_auth_stamps").child(key).get()
	if all_auth_stamps.each() != None:
		flag = False
		for a in all_auth_stamps.each():
			orderedDict = a.val()
			if orderedDict["logout_stamp"] == "":
				flag = True
				print("New faculty auth stamp not created")
				break
		if not flag:
			db.child("faculty_auth_stamps").child(key).child(session.key).set(session.json())
		else:
			print("Faculty not logged out yet")
	else:
		db.child("faculty_auth_stamps").child(key).child(session.key).set(session.json())

def setFacultyLogoutStamp(key):
	db = firebase.database()
	all_auth_stamps = db.child("faculty_auth_stamps").child(key).get()
	if all_auth_stamps.each() != None:
		for a in all_auth_stamps.each():
			orderedDict = a.val()
			if orderedDict["logout_stamp"] == "":
				session = utils.Session(a.key(), login_stamp=orderedDict["login_stamp"])
				session.setLogoutStamp()
				db.child("faculty_auth_stamps").child(key).child(session.key).set(session.json())
				print("Faculty logged out successfully")
				break
	else:
		print("Faculty logout failed")

########### Event ############################################################################

def makeNewEvent(event):
	db = firebase.database()
	db.child("events").child(event.key).set(event.json())

def setEventOnline(key):
	db = firebase.database()
	db.child("online_events").child(key).set(True)

def setCurrentEvent(key):
	db = firebase.database()
	db.child("current_events").child(key).set(True)

def setEventSummary(key, summary):
	db = firebase.database()
	db.child("events").child(key).child('summary').set(summary)

def markStudentAttendance(eventKey, studentKey):
	db = firebase.database()
	db.child("events").child(eventKey).child("attendees").child(studentKey).set(True) 

def getEventDetails(key):
	db = firebase.database()
	e = db.child("events").child(key)
	name = e.child("name").get().val()
	e = db.child("events").child(key)
	speaker = e.child("speaker").get().val()
	e = db.child("events").child(key)
	event_start_time = e.child("event_start_time").get().val()
	e = db.child("events").child(key)
	event_end_time = e.child("event_end_time").get().val()
	e = db.child("events").child(key)
	date = e.child("date").get().val()
	e = db.child("events").child(key)
	summary = e.child("summary").get().val()
	e = db.child("events").child(key)
	attendance_start_time = e.child("attendance_start_time").get().val()
	e = db.child("events").child(key)
	attendance_end_time = e.child("attendance_end_time").get().val()
	e = db.child("events").child(key)
	date = e.child("date").get().val()
	e = db.child("events").child(key)
	attendees = e.child("attendees").get().val()
	return utils.Event(name, speaker, event_start_time, event_end_time, date, attendance_start_time, attendance_end_time, key, attendees=attendees, summary=summary)

def getAllEvents():
	db = firebase.database()
	return db.child('events').get()

def getAllOnlineEvents():
	db = firebase.database()
	return db.child('online_events').get()

########### Cookie ###########################################################################

def setCookie(cookie):
	db = firebase.database()
	db.child("cookies").child(cookie.key).remove()
	db.child("cookies").child(cookie.key).child(cookie.session_id).set(cookie.id_token)

def deleteCookie(cookie):
	db = firebase.database()
	db.child("cookies").child(cookie.key).remove()

def getCookie(key):
	db = firebase.database()
	c = db.child("cookies").child(key)
	d=c.get().val()
	for i, (session_id, id_token) in enumerate(d.iteritems()):
		print i, session_id, id_token
		return utils.Cookie(id_token, session_id, key)
	return None

def getAllCookies():
	db = firebase.database()
	return db.child('cookies').get()

########### Main #############################################################################

# if __name__ == '__main__':
	# f1 = utils.Faculty("test1@example.com", 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImQxZTg2OWU3YmY0MGRkYzNkM2RlMDgwNDI1OThiYTgzNTA5NzBmMGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiMTA1OTUwMTM5OTg3MS1ocHZzb3BxaHE5ZnRzbzlucWpoZmM1Mm9xcGJxNWtmdC5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImF1ZCI6IjEwNTk1MDEzOTk4NzEtaHB2c29wcWhxOWZ0c285bnFqaGZjNTJvcXBicTVrZnQuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTQxNDU2NTYyMzgzMDA4NDQ2OTUiLCJoZCI6InN0Lm5paXR1bml2ZXJzaXR5LmluIiwiZW1haWwiOiJhbmlydWRoLnNoYXJtYUBzdC5uaWl0dW5pdmVyc2l0eS5pbiIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiNUo4a25VTWNoWC12ZnNXajFvNjYyQSIsIm5hbWUiOiJBbmlydWRoIFNoYXJtYSIsInBpY3R1cmUiOiJodHRwczovL2xoNC5nb29nbGV1c2VyY29udGVudC5jb20vLWZhc09kQkFWVEpBL0FBQUFBQUFBQUFJL0FBQUFBQUFBQUFBL0FHRGd3LWl3NEItVzJna2hobHlydi1MUXlVTGxBY3FiYncvczk2LWMvcGhvdG8uanBnIiwiZ2l2ZW5fbmFtZSI6IkFuaXJ1ZGgiLCJmYW1pbHlfbmFtZSI6IlNoYXJtYSIsImxvY2FsZSI6ImVuIiwiaWF0IjoxNTQyNzQyNTQ4LCJleHAiOjE1NDI3NDYxNDgsImp0aSI6Ijg1MGY2OGIzZWJiYzk5ZGY5ZDNlY2I5MTZhNDg5ZjlhZjI3MGExNzMifQ.fCZ-FYCcfjfTtTjD1DrvuFyZ_NhpPmcoUWj_cIPiMRItWs5Fayipi4D27k03FG8tfuO1oFqtQklGskuwS2kBl_ac7IFb7-SzT7ebFqde5_t8xkWEnJ9QJgAf13YJBCtDXQ02HxrXcmiqJ4jL83Rx4XP19gpNyPUUnaTBoLvz4gNGLaSgPnFPLuA21B_vYnwm67kGGVHmf3WJgd7yEw_i--m3YN1i-j0YapzBRQkkcnqIkpeo3ucTGwEF-o0f1S7aSgPnFPLuA2OxPHvt_xq4WFTJ7pxa8VD5VZ4cbxABX_aSgPnFPLuA22KO2tnYmjQjlg9O266AZKwWLRWYtJM93dBw', random_string_generator(size=13))
	# f2 = utils.Faculty("test2@example.com", 'OWU3YmY0MGiJSUzI1NiIsImtpZCI6ImQxZTg2OWU3YmY0MGRkYzNkM2RlMDgwNDI1OThiYTgzNTA5NzBmMGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiMTA1OTUwMTM5OTg3MS1ocHZzb3BxaHE5ZnRzbzlucWpoZmM1Mm9xcGJxNWtmdC5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImF1ZCI6IjEwNTk1MDEzOTk4NzEtaHB2c29wcWhxOWZ0c285bnFqaGZjNTJvcXBicTVrZnQuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTQxNDU2NTYyMzgzMDA4NDQ2OTUiLCJoZCI6InN0Lm5paXR1bml2ZXJzaXR5LmluIiwiZW1haWwiOiJhbmlydWRoLnNoYXJtYUBzdC5uaWl0dW5pdmVyc2l0eS5pbiIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiNUo4a25VTWNoWC12ZnNXajFvNjYyQSIsIm5hbWUiOiJBbmlydWRoIFNoYXJtYSIsInBpY3R1cmUiOiJodHRwczovL2xoNC5nb29nbGV1c2VyY29udGVudC5jb20vLWZhc09kQkFWVEpBL0FBQUFBQUFBQUFJL0FBQUFBQUFBQUFBL0FHRGd3LWl3NEItVzJna2hobHlydi1MUXlVTGxBY3FiYncvczk2LWMvcGhvdG8uanBnIiwiZ2l2ZW5fbmFtZSI6IkFuaXJ1ZGgiLCJmYW1pbHlfbmFtZSI6IlNoYXJtYSIsImxvY2FsZSI6ImVuIiwiaWF0IjoxNTQyNzQyNTQ4LCJleHAiOjE1NDI3NDYxNDgsImp0aSI6Ijg1MGY2OGIzZWJiYzk5ZGY5ZDNlY2I5MTZhNDg5ZjlhZjI3MGExNzMifQ.fCZ-FYCcfjfTtTjD1DrvuFyZ_NhpPmcoUWj_cIPiMRItWs5Fayipi4D27k03FG8tfuO1oFqtQklGskuwS2kBl_ac7IFb7-jlg9O266AZ5_t8xkWEnJ9QJgAf13YJBCtDXQ02HxrXcmiqJ4jL83Rx4XP19gpNyPUUnaTBoLvz4gNGLaSgPnFPLuA21B_vYnwm67kGGVHmf3WJgd7yEw_i--m3YN1i-j0YapzBRQkkcnqIkpeo3ucTGwEF-o0f1S7aSgPnFPLuA2OxPHvt_xq4WFTJ7pxa8jlg9O266AZBX_aSgPnFPLuA22KO2tnYmjQjlg9O266AZKwWLjlg9O266AZw', random_string_generator(size=13))
	# f3 = utils.Faculty("test3@example.com", 'isImtpZCI6JSUzI1NiIsImtpZCI6ImQxZTg2OWU3YmY0MGRkYzNkM2RlMDgwNDI1OThiYTgzNTA5NzBmMGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiMTA1OTUwMTM5OTg3MS1ocHZzb3BxaHE5ZnRzbzlucWpoZmM1Mm9xcGJxNWtmdC5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImF1ZCI6IjEwNTk1MDEzOTk4NzEtaHB2c29wcWhxOWZ0c285bnFqaGZjNTJvcXBicTVrZnQuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTQxNDU2NTYyMzgzMDA4NDQ2OTUiLCJoZCI6InN0Lm5paXR1bml2ZXJzaXR5LmluIiwiZW1haWwiOiJhbmlydWRoLnNoYXJtYUBzdC5uaWl0dW5pdmVyc2l0eS5pbiIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiNUo4a25VTWNoWC12ZnNXajFvNjYyQSIsIm5hbWUiOiJBbmlydWRoIFNoYXJtYSIsInBpY3R1cmUiOiJodHRwczovL2xoNC5nb29nbGV1c2VyY29udGVudC5jb20vLWZhc09kQkFWVEpBL0FBQUFBQUFBQUFJL0FBQUFBQUFBQUFBL0FHRGd3LWl3NEItVzJna2hobHlydi1MUXlVTGxBY3FiYncvczk2LWMvcGhvdG8uanBnIiwiZ2l2ZW5fbmFtZSI6IkFuaXJ1ZGgiLCJmYW1pbHlfbmFtZSI6IlNoYXJtYSIsImxvY2FsZSI6ImVuIiwiaWF0IjoxNTQyNzQyNTQ4LCJleHAiOjE1NDI3NDYxNDgsImp0aSI6Ijg1MGY2OGIzZWJiYzk5ZGY5ZDNlY2I5MTZhNDg5ZjlhZjI3MGExNzMifQ.fCZ-FYCcfjfTtTjD1DrvuFyZ_NhpPmcoUWj_cIPiMRItWs5Fayipi4D27k03FG8tfuO1oFqtQklGskuwS2kBl_ac7IFb7-jlg9O266AZ5_t8xkWEnJ9QJgAf13YJBCtDXQ02HxrXcmiqJ4jL83Rx4XP19gpNyPUUnaTBoLvz4gNGLaSgPnFPLuA21B_vYnwm67kGGVHmf3WJgd7yEw_i--m3YN1i-j0YapzBRQkkcnqIkpeo3ucTGwEF-o0f1S7aSgPnFPLuA2OxPHvt_xq4WFTJ7pxa8jlg9O266AZBX_aSgPnFPLuA22KO2tnYmjQjlg9O266AZKwWLjlg9O266AZw', random_string_generator(size=13))
	# f4 = utils.Faculty("test4@example.com", 'lmQxZTg2OWJSUzI1NiIsImtpZCI6ImQxZTg2OWU3YmY0MGRkYzNkM2RlMDgwNDI1OThiYTgzNTA5NzBmMGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiMTA1OTUwMTM5OTg3MS1ocHZzb3BxaHE5ZnRzbzlucWpoZmM1Mm9xcGJxNWtmdC5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImF1ZCI6IjEwNTk1MDEzOTk4NzEtaHB2c29wcWhxOWZ0c285bnFqaGZjNTJvcXBicTVrZnQuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTQxNDU2NTYyMzgzMDA4NDQ2OTUiLCJoZCI6InN0Lm5paXR1bml2ZXJzaXR5LmluIiwiZW1haWwiOiJhbmlydWRoLnNoYXJtYUBzdC5uaWl0dW5pdmVyc2l0eS5pbiIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiNUo4a25VTWNoWC12ZnNXajFvNjYyQSIsIm5hbWUiOiJBbmlydWRoIFNoYXJtYSIsInBpY3R1cmUiOiJodHRwczovL2xoNC5nb29nbGV1c2VyY29udGVudC5jb20vLWZhc09kQkFWVEpBL0FBQUFBQUFBQUFJL0FBQUFBQUFBQUFBL0FHRGd3LWl3NEItVzJna2hobHlydi1MUXlVTGxBY3FiYncvczk2LWMvcGhvdG8uanBnIiwiZ2l2ZW5fbmFtZSI6IkFuaXJ1ZGgiLCJmYW1pbHlfbmFtZSI6IlNoYXJtYSIsImxvY2FsZSI6ImVuIiwiaWF0IjoxNTQyNzQyNTQ4LCJleHAiOjE1NDI3NDYxNDgsImp0aSI6Ijg1MGY2OGIzZWJiYzk5ZGY5ZDNlY2I5MTZhNDg5ZjlhZjI3MGExNzMifQ.fCZ-FYCcfjfTtTjD1DrvuFyZ_NhpPmcoUWj_cIPiMRItWs5Fayipi4D27k03FG8tfuO1oFqtQklGskuwS2kBl_ac7IFb7-jlg9O266AZ5_t8xkWEnJ9QJgAf13YJBCtDXQ02HxrXcmiqJ4jL83Rx4XP19gpNyPUUnaTBoLvz4gNGLaSgPnFPLuA21B_vYnwm67kGGVHmf3WJgd7yEw_i--m3YN1i-j0YapzBRQkkcnqIkpeo3ucTGwEF-o0f1S7aSgPnFPLuA2OxPHvt_xq4WFTJ7pxa8jlg9O266AZBX_aSgPnFPLuA22KO2tnYmjQjlg9O266AZKwWLjlg9O266AZw', random_string_generator(size=13))
	# registerFaculty(f1)
	# setFacultyLoginStamp(f1.key)
	# setFacultyOnline(f1.key)

	# registerFaculty(f2, password="Test2#123")
	# setFacultyLoginStamp(f2.key)
	# setFacultyLogoutStamp(f2.key)

	# registerFaculty(f3)
	# setFacultyLoginStamp(f3.key)
	# setFacultyLogoutStamp(f3.key)
	# setNewFacultyPassword(f3.key, "Faculty#123", "Test3#123")

	# registerFaculty(f4, password="Test4#123")
	# setFacultyLoginStamp(f4.key)
	# setFacultyOnline(f4.key)

	# s1 = utils.Student("Test1", "test1@example.com", "PB:01:98:BH:67:BD", '0o8q4s68zue6g', 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjYwY2QzNzcxYzExMjVjOWY3N2U4MmUzOTk3NGUxNjNhOGM3M2IzYzQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiMTA1OTUwMTM5OTg3MS1ocHZzb3BxaHE5ZnRzbzlucWpoZmM1Mm9xcGJxNWtmdC5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImF1ZCI6IjEwNTk1MDEzOTk4NzEtaHB2c29wcWhxOWZ0c285bnFqaGZjNTJvcXBicTVrZnQuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTQxNDU2NTYyMzgzMDA4NDQ2OTUiLCJoZCI6InN0Lm5paXR1bml2ZXJzaXR5LmluIiwiZW1haWwiOiJhbmlydWRoLnNoYXJtYUBzdC5uaWl0dW5pdmVyc2l0eS5pbiIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiTEtJRG5LYnVIZDdfd2lZN2t5R0c4QSIsIm5hbWUiOiJBbmlydWRoIFNoYXJtYSIsInBpY3R1cmUiOiJodHRwczovL2xoNC5nb29nbGV1c2VyY29udGVudC5jb20vLWZhc09kQkFWVEpBL0FBQUFBQUFBQUFJL0FBQUFBQUFBQUFBL0FHRGd3LWl3NEItVzJna2hobHlydi1MUXlVTGxBY3FiYncvczk2LWMvcGhvdG8uanBnIiwiZ2l2ZW5fbmFtZSI6IkFuaXJ1ZGgiLCJmYW1pbHlfbmFtZSI6IlNoYXJtYSIsImxvY2FsZSI6ImVuIiwiaWF0IjoxNTQyODU4NTkyLCJleHAiOjE1NDI4NjIxOTIsImp0aSI6ImEzMTI3MWFhMTViZDkwODlkOGE0NGIyMTFlM2RiNjBhNmUyMTBiMGQifQ.HuYt_tfmwdt57q3wxatfkDGG33_LQpYd7LhOPuQ5Z83JY4cZK-H95AJnxMUWnMkg-Thbm6OuK1JeiKxj8ZB41Z5G0DlsZUQNoWWu9kRpQ1A-z8qCfuxwOtTERqN3wHjw_HPnsD-2eJNXIBwg6Iuedr8ZzXgIxIfcR1FXvbsz-ERPDeRacICV4YTnqcrk7Qkqq5QM87OtHAVG2m5T_9OR-7N0Ww3EdKClUVaZ-8ZBeWyq0X0_am2sbwyqSw0lMtNdj5vOTg7P7s6ZemCR583Di9rULVlBm-2xDnKm5ELObv5I2X4Z3OnRY92YrEEf_n5dPGboRI6sGW_K-PDBnc1Dfw')
	# s2 = utils.Student("Test2", "test2@example.com", "AV:DF:52:98:EF:2A", random_string_generator(size=13), 'isImtpZCI6JSUzI1NiIsImtpZCI6ImQxZTg2OWU3YmY0MGRkYzNkM2RlMDgwNDI1OThiYTgzNTA5NzBmMGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiMTA1OTUwMTM5OTg3MS1ocHZzb3BxaHE5ZnRzbzlucWpoZmM1Mm9xcGJxNWtmdC5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImF1ZCI6IjEwNTk1MDEzOTk4NzEtaHB2c29wcWhxOWZ0c285bnFqaGZjNTJvcXBicTVrZnQuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTQxNDU2NTYyMzgzMDA4NDQ2OTUiLCJoZCI6InN0Lm5paXR1bml2ZXJzaXR5LmluIiwiZW1haWwiOiJhbmlydWRoLnNoYXJtYUBzdC5uaWl0dW5pdmVyc2l0eS5pbiIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiNUo4a25VTWNoWC12ZnNXajFvNjYyQSIsIm5hbWUiOiJBbmlydWRoIFNoYXJtYSIsInBpY3R1cmUiOiJodHRwczovL2xoNC5nb29nbGV1c2VyY29udGVudC5jb20vLWZhc09kQkFWVEpBL0FBQUFBQUFBQUFJL0FBQUFBQUFBQUFBL0FHRGd3LWl3NEItVzJna2hobHlydi1MUXlVTGxBY3FiYncvczk2LWMvcGhvdG8uanBnIiwiZ2l2ZW5fbmFtZSI6IkFuaXJ1ZGgiLCJmYW1pbHlfbmFtZSI6IlNoYXJtYSIsImxvY2FsZSI6ImVuIiwiaWF0IjoxNTQyNzQyNTQ4LCJleHAiOjE1NDI3NDYxNDgsImp0aSI6Ijg1MGY2OGIzZWJiYzk5ZGY5ZDNlY2I5MTZhNDg5ZjlhZjI3MGExNzMifQ.fCZ-FYCcfjfTtTjD1DrvuFyZ_NhpPmcoUWj_cIPiMRItWs5Fayipi4D27k03FG8tfuO1oFqtQklGskuwS2kBl_ac7IFb7-jlg9O266AZ5_t8xkWEnJ9QJgAf13YJBCtDXQ02HxrXcmiqJ4jL83Rx4XP19gpNyPUUnaTBoLvz4gNGLaSgPnFPLuA21B_vYnwm67kGGVHmf3WJgd7yEw_i--m3YN1i-j0YapzBRQkkcnqIkpeo3ucTGwEF-o0f1S7aSgPnFPLuA2OxPHvt_xq4WFTJ7pxa8jlg9O266AZBX_aSgPnFPLuA22KO2tnYmjQjlg9O266AZKwWLjlg9O266AZw')
	# s3 = utils.Student("Test3", "test3@example.com", "5F:29:DC:BB:EC:D6", random_string_generator(size=13), '0LmNvbSIsIJSUzI1NiIsImtpZCI6ImQxZTg2OWU3YmY0MGRkYzNkM2RlMDgwNDI1OThiYTgzNTA5NzBmMGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiMTA1OTUwMTM5OTg3MS1ocHZzb3BxaHE5ZnRzbzlucWpoZmM1Mm9xcGJxNWtmdC5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImF1ZCI6IjEwNTk1MDEzOTk4NzEtaHB2c29wcWhxOWZ0c285bnFqaGZjNTJvcXBicTVrZnQuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTQxNDU2NTYyMzgzMDA4NDQ2OTUiLCJoZCI6InN0Lm5paXR1bml2ZXJzaXR5LmluIiwiZW1haWwiOiJhbmlydWRoLnNoYXJtYUBzdC5uaWl0dW5pdmVyc2l0eS5pbiIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiNUo4a25VTWNoWC12ZnNXajFvNjYyQSIsIm5hbWUiOiJBbmlydWRoIFNoYXJtYSIsInBpY3R1cmUiOiJodHRwczovL2xoNC5nb29nbGV1c2VyY29udGVudC5jb20vLWZhc09kQkFWVEpBL0FBQUFBQUFBQUFJL0FBQUFBQUFBQUFBL0FHRGd3LWl3NEItVzJna2hobHlydi1MUXlVTGxBY3FiYncvczk2LWMvcGhvdG8uanBnIiwiZ2l2ZW5fbmFtZSI6IkFuaXJ1ZGgiLCJmYW1pbHlfbmFtZSI6IlNoYXJtYSIsImxvY2FsZSI6ImVuIiwiaWF0IjoxNTQyNzQyNTQ4LCJleHAiOjE1NDI3NDYxNDgsImp0aSI6Ijg1MGY2OGIzZWJiYzk5ZGY5ZDNlY2I5MTZhNDg5ZjlhZjI3MGExNzMifQ.fCZ-FYCcfjfTtTjD1DrvuFyZ_NhpPmcoUWj_cIPiMRItWs5Fayipi4D27k03FG8tfuO1oFqtQklGskuwS2kBl_ac7IFb7-jlg9O266AZ5_t8xkWEnJ9QJgAf13YJBCtDXQ02HxrXcmiqJ4jL83Rx4XP19gpNyPUUnaTBoLvz4gNGLaSgPnFPLuA21B_vYnwm67kGGVHmf3WJgd7yEw_i--m3YN1i-j0YapzBRQkkcnqIkpeo3ucTGwEF-o0f1S7aSgPnFPLuA2OxPHvt_xq4WFTJ7pxa8jlg9O266AZBX_aSgPnFPLuA22KO2tnYmjQjlg9O266AZKwWLjlg9O266AZw')
	# s4 = utils.Student("Test4", "test4@example.com", "CD:FC:04:HB:6F:45", random_string_generator(size=13), 'JSUzI1NiIsJSUzI1NiIsImtpZCI6ImQxZTg2OWU3YmY0MGRkYzNkM2RlMDgwNDI1OThiYTgzNTA5NzBmMGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiMTA1OTUwMTM5OTg3MS1ocHZzb3BxaHE5ZnRzbzlucWpoZmM1Mm9xcGJxNWtmdC5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImF1ZCI6IjEwNTk1MDEzOTk4NzEtaHB2c29wcWhxOWZ0c285bnFqaGZjNTJvcXBicTVrZnQuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTQxNDU2NTYyMzgzMDA4NDQ2OTUiLCJoZCI6InN0Lm5paXR1bml2ZXJzaXR5LmluIiwiZW1haWwiOiJhbmlydWRoLnNoYXJtYUBzdC5uaWl0dW5pdmVyc2l0eS5pbiIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiNUo4a25VTWNoWC12ZnNXajFvNjYyQSIsIm5hbWUiOiJBbmlydWRoIFNoYXJtYSIsInBpY3R1cmUiOiJodHRwczovL2xoNC5nb29nbGV1c2VyY29udGVudC5jb20vLWZhc09kQkFWVEpBL0FBQUFBQUFBQUFJL0FBQUFBQUFBQUFBL0FHRGd3LWl3NEItVzJna2hobHlydi1MUXlVTGxBY3FiYncvczk2LWMvcGhvdG8uanBnIiwiZ2l2ZW5fbmFtZSI6IkFuaXJ1ZGgiLCJmYW1pbHlfbmFtZSI6IlNoYXJtYSIsImxvY2FsZSI6ImVuIiwiaWF0IjoxNTQyNzQyNTQ4LCJleHAiOjE1NDI3NDYxNDgsImp0aSI6Ijg1MGY2OGIzZWJiYzk5ZGY5ZDNlY2I5MTZhNDg5ZjlhZjI3MGExNzMifQ.fCZ-FYCcfjfTtTjD1DrvuFyZ_NhpPmcoUWj_cIPiMRItWs5Fayipi4D27k03FG8tfuO1oFqtQklGskuwS2kBl_ac7IFb7-jlg9O266AZ5_t8xkWEnJ9QJgAf13YJBCtDXQ02HxrXcmiqJ4jL83Rx4XP19gpNyPUUnaTBoLvz4gNGLaSgPnFPLuA21B_vYnwm67kGGVHmf3WJgd7yEw_i--m3YN1i-j0YapzBRQkkcnqIkpeo3ucTGwEF-o0f1S7aSgPnFPLuA2OxPHvt_xq4WFTJ7pxa8jlg9O266AZBX_aSgPnFPLuA22KO2tnYmjQjlg9O266AZKwWLjlg9O266AZw')
	# registerStudent(s1)
	# setStudentLoginStamp(s1.key)
	# setStudentLogoutStamp(s1.key)

	# registerStudent(s2)
	# setStudentLoginStamp(s2.key)
	# setStudentOnline(s2.key)
	
	# registerStudent(s3)
	# setStudentLoginStamp(s3.key)
	# setStudentOnline(s3.key)
	
	# registerStudent(s4)
	# setStudentLoginStamp(s4.key)
	# setStudentLogoutStamp(s4.key)
	
	# e1 = utils.Event("TEDx NIIT University", "Dr Prem Atreja", utils.timestamp_generator(), utils.timestamp_generator(), utils.timestamp_generator(), utils.timestamp_generator(), utils.timestamp_generator(), random_string_generator(size=13))
	# e1.addSummary("A leading Scientist and Technologist in the fields of Dairy Science, Food Sciences, Nutritional Biochemistry and Alternative Medicine, His students occupy various prestigious positions are scattered all over India and the globe. He has taught & guided Ph.D., M.Sc. & under graduate students on subjects like Analytical Techniques for advance research, Principles of Nutrition, Nutritional Biochemistry, Vitamins, minerals and Toxin metabolism etc.")
	# makeNewEvent(e1)
	# setCurrentEvent(e1.key)
	# setEventOnline(e1.key)

	# e2 = utils.Event("MUN NIIT University", "Dr Prem Atreja", utils.timestamp_generator(), utils.timestamp_generator(), utils.timestamp_generator(), utils.timestamp_generator(), utils.timestamp_generator(), random_string_generator(size=13))
	# e2.addSummary("Model Unite Nations in NIIT University")
	# makeNewEvent(e2)
	# # setCurrentEvent(e2.key)
	# setEventOnline(e2.key)

	# markStudentAttendance(e1.key, s1.key)
	# markStudentAttendance(e1.key, s2.key)
	# markStudentAttendance(e2.key, s3.key)
	# markStudentAttendance(e2.key, s4.key)
	# c = utils.Cookie(urllib.quote(utils.encrypt(s1.id_token, 4, 12)), utils.random_string_generator(size=13), s1.key)
	# print(utils.encrypt(s1.id_token, 4, 12))
	# setCookie(c)
	# getCookie(s1.key)