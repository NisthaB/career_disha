from app import *

# Create database model
class Users(db.Model):
	__tablename__ = 'usr_users'
	u_id = db.Column(db.String(32), primary_key=True)
	f_name = db.Column(db.String(25))
	l_name = db.Column(db.String(25))
	mobile_no = db.Column(db.String(10))
	email_id  = db.Column(db.String(50))
	password = db.Column(db.String(64))
	
	def __init__(self, u_id, f_name, l_name, mobile_no, email_id, password):
		self.u_id = u_id
		self.f_name = f_name
		self.l_name = l_name
		self.mobile_no = mobile_no
		self.email_id = email_id
		self.password = password

	def __repr__(self):
		return str(str(self.f_name) + "," +str(self.u_id))


class Exam(db.Model):
	__tablename__ = 'usr_questions'
	question_id = db.Column(db.String(10), primary_key=True)
	subject = db.Column(db.String(25))
	question = db.Column(db.String(500))
	option_1 = db.Column(db.String(500))
	option_2 = db.Column(db.String(500))
	option_3 = db.Column(db.String(500))
	option_4 = db.Column(db.String(500))
	answer = db.Column(db.String(500))
	credit = db.Column(db.String(5))

	def __init__(self, question_id, subject, question, option_1, option_2, option_3, option_4, answer, credit):
		self.question_id = question_id
		self.subject = subject
		self.question = question
		self.option_1 = option_1
		self.option_2 = option_2
		self.option_3 = option_3
		self.option_4 = option_4
		self.answer = answer
		self.credit = credit

	def __repr__(self):
		return str(str(self.question) + "," + str(self.option_1) + "," + str(self.option_2) + "," + str(self.option_3) + "," + str(self.option_4) )

class Score(db.Model):
	__tablename__ = 'usr_score'
	score_id = db.Column(db.String(32), primary_key=True)
	u_id = db.Column(db.String(32))
	subject = db.Column(db.String(25))
	score = db.Column(db.String(5))

	def __init__(self, score_id, u_id, subject, score):
		self.score_id = score_id
		self.u_id = u_id
		self.subject = subject
		self.score = score

	def __repr__(self):
		return str(str(self.score_id) + "," + str(self.u_id) + "," + str(self.subject) + "," + str(self.score))
