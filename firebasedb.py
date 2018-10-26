import pyrebase
import utils
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

def setStudentOnline(student):
	db = firebase.database()
	db.child("online_students").child(student.key).set(True)

def getStudentDetails(key):
	db = firebase.database()
	s = db.child("students").child(key)
	name = s.child("name").get().val()
	s = db.child("students").child(key)
	email = s.child("email").get().val()
	s = db.child("students").child(key)
	mac = s.child("mac").get().val()
	return utils.Student(name, email, mac, key)

########### Faculty ##########################################################################

def registerFaculty(faculty, password="Faculty#123"):
	db = firebase.database()
	db.child("faculties").child(faculty.key).set(faculty.json())
	db.child("passwords").child(faculty.key).set(utils.Password(password).json())

def setFacultyOnline(faculty):
	db = firebase.database()
	db.child("online_faculties").child(faculty.key).set(True)

def getFacultyDetails(key):
	db = firebase.database()
	f = db.child("faculties").child(key)
	name = f.child("name").get().val()
	f = db.child("faculties").child(key)
	email = f.child("email").get().val()
	return utils.Faculty(name, email, key)

########### Password #########################################################################

def setFacultyPassword(key, password): # key of faculty
	db = firebase.database()
	db.child("passwords").child(key).set(password.json())

def getFacultyPassword(key):
	db = firebase.database()
	p = db.child("passwords").child(key)
	return p

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
	db.child("student_auth_stamps").child(key).set(utils.Session().json())

def setStudentLogoutStamp(key):
	db = firebase.database()
	session = utils.Session()
	session.setLogoutStamp()
	db.child("student_auth_stamps").child(key).set(session.json())

def setFacultyLoginStamp(key):
	db = firebase.database()
	db.child("faculty_auth_stamps").child(key).set(utils.Session().json())

def setFacultyLogoutStamp(key):
	db = firebase.database()
	session = utils.Session()
	session.setLogoutStamp()
	db.child("faculty_auth_stamps").child(key).set(session.json())

########### Event ############################################################################

def makeNewEvent(event):
	db = firebase.database()
	db.child("events").child(event.key).set(event.json())

def setEventOnline(event):
	db = firebase.database()
	db.child("online_events").child(event.key).set(True)

def setCurrentEvent(event):
	db = firebase.database()
	db.child("current_events").child(event.key).set(True)

def markStudentAttendance(event, student):
	db = firebase.database()
	db.child("events").child(event.key).child("attendees").child(student.key).set(True) 

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
	return utils.Event(name, speaker, event_start_time, event_end_time, date, attendance_start_time, attendance_end_time, date, key, summary=summary, attendees=attendees)

########### Main #############################################################################

if __name__ == '__main__':
	f1 = utils.Faculty("Test1", "test1@example.com", random_string_generator(size=13))
	f2 = utils.Faculty("Test2", "test2@example.com", random_string_generator(size=13))
	f3 = utils.Faculty("Test3", "test3@example.com", random_string_generator(size=13))
	f4 = utils.Faculty("Test4", "test4@example.com", random_string_generator(size=13))
	registerFaculty(f1)
	setFacultyLoginStamp(f1.key)
	setFacultyOnline(f1)

	registerFaculty(f2, password="Test2#123")
	setFacultyLoginStamp(f2.key)
	setFacultyLogoutStamp(f2.key)

	registerFaculty(f3)
	setFacultyLoginStamp(f3.key)
	setFacultyLogoutStamp(f3.key)
	setNewFacultyPassword(f3.key, "Faculty#123", "Test3#123")

	registerFaculty(f4, password="Test4#123")
	setFacultyLoginStamp(f4.key)
	setFacultyOnline(f4)

	s1 = utils.Student("Test1", "test1@example.com", "PB:01:98:BH:67:BD", random_string_generator(size=13))
	s2 = utils.Student("Test2", "test2@example.com", "AV:DF:52:98:EF:2A", random_string_generator(size=13))
	s3 = utils.Student("Test3", "test3@example.com", "5F:29:DC:BB:EC:D6", random_string_generator(size=13))
	s4 = utils.Student("Test4", "test4@example.com", "CD:FC:04:HB:6F:45", random_string_generator(size=13))
	registerStudent(s1)
	setStudentLoginStamp(s1.key)
	setStudentLogoutStamp(s1.key)

	registerStudent(s2)
	setStudentLoginStamp(s2.key)
	setStudentOnline(s2)
	
	registerStudent(s3)
	setStudentLoginStamp(s3.key)
	setStudentOnline(s3)
	
	registerStudent(s4)
	setStudentLoginStamp(s4.key)
	setStudentLogoutStamp(s4.key)
	
	e = utils.Event("TEDx NIIT University", "Dr Prem Atreja", utils.timestamp_generator(), utils.timestamp_generator(), utils.timestamp_generator(), utils.timestamp_generator(), utils.timestamp_generator(), random_string_generator(size=13))
	e.addSummary("A leading Scientist and Technologist in the fields of Dairy Science, Food Sciences, Nutritional Biochemistry and Alternative Medicine, His students occupy various prestigious positions are scattered all over India and the globe. He has taught & guided Ph.D., M.Sc. & under graduate students on subjects like Analytical Techniques for advance research, Principles of Nutrition, Nutritional Biochemistry, Vitamins, minerals and Toxin metabolism etc.")
	makeNewEvent(e)
	setCurrentEvent(e)
	setEventOnline(e)

	markStudentAttendance(e, s1)
	markStudentAttendance(e, s2)
	markStudentAttendance(e, s3)
	markStudentAttendance(e, s4)

