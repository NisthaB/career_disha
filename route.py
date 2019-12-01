from app import *
from datetime import timedelta
from flask import render_template, request, session, send_from_directory, redirect, url_for, jsonify
import os, time
from plugins import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_
from models import *
import json, random


@app.route('/', methods=['GET', 'POST'])
def user_login():
	error_check = 0
	session['auth'] = False
	u_id = None
	password = None

	if request.method == 'POST':
		u_id = request.form['inputUserID']
		passwd = encrypt_string(request.form['inputPassword'])
		check_registered_user = db.session.query(Users).filter(or_(Users.email_id == u_id, Users.mobile_no == u_id), Users.password == passwd).first()
		if check_registered_user is None:
			error_check = 1
		else:
			new_data = str(check_registered_user).split(',')
			session['auth'] = True
			session['f_name'] = new_data[0]
			session['u_id'] = new_data[1]
			return redirect( url_for('dashboard') )

	return render_template('user_login/user_login.html', err_chk = error_check)

@app.route('/user_registration', methods=['GET', 'POST'])
def user_registration():
	error_check = 0
	u_id = None
	f_name = None
	l_name = None
	mobile_no = None
	email_id = None
	password = None

	if request.method == 'POST':
		
		if (request.form['inputPassword'] == request.form['inputConfPassword']):
			u_id = uuid()
			f_name = request.form['inputFname']
			l_name = request.form['inputLname']
			mobile_no = request.form['inputMobile']
			email_id = request.form['inputEmail']
			password = encrypt_string(request.form['inputPassword'])
			
			if not db.session.query(Users).filter(Users.email_id == email_id).count() and not db.session.query(Users).filter(Users.mobile_no == mobile_no).count():
				reg = Users(u_id, f_name, l_name, mobile_no, email_id, password)
				db.session.add(reg)
				db.session.commit()
				return redirect('/')
			else:
				error_check = 1

	return render_template('user_registration/user_registration.html',  err_chk = error_check)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
	if (not session['auth']):
		return redirect('/')

	score_dict = {}
	get_subjects = db.session.query(Exam).with_entities(Exam.subject).group_by(Exam.subject).all()
	subjects = [sub[0] for sub in get_subjects]
	for each_subject in subjects:
		score_dict[each_subject] = 0

	get_score = db.session.query(Score).with_entities(Score.subject, Score.score).filter(Score.u_id == session['u_id']).all()
	print(get_score)
	if get_score is not None:
		for subject, score in get_score:
			print(subject, score)
			score_dict[subject] = int( (int(score)/10) * 100 )

	color_pal = ["green", "orange", "blue"]
	cluster_data = {"Aptitude" : score_dict["Aptitude"],
					"Technical Skill": int((score_dict["C"] + score_dict["DS"] + score_dict["DBMS"] + score_dict["Networking"]) / 4),
					"Managerial Skills" : score_dict["Management"]}

	return render_template('sys_chatbox/sys_chatbox.html', curr_user = session['f_name'], subj_score = score_dict, col_p = color_pal, clus_d=cluster_data)

@app.route('/exam/<exam_subject>', methods=['GET', 'POST'])
def exam(exam_subject):
	if (not session['auth']):
		return redirect('/')

	if request.method == 'POST':
		score = 0
		for id, answer in dict(request.form).items():
			check_answer = db.session.query(Exam).with_entities(Exam.credit).filter(Exam.question_id == id, Exam.answer == answer).first()
			if check_answer is not None:
				score += int(check_answer[0])

		entries = Score(uuid(), session['u_id'], exam_subject, score)
		db.session.add(entries)
		db.session.commit()
		return redirect('/dashboard')

	get_exam_data = db.session.query(Exam).with_entities(Exam.question, Exam.option_1, Exam.option_2, Exam.option_3, Exam.option_4, Exam.question_id).filter(Exam.subject == exam_subject).all()
	random.shuffle(get_exam_data)
	return render_template('user_exam/user_exam.html', exam_data=get_exam_data[:10], subj=exam_subject )


@app.route('/logout')
def logout():
	session.pop('auth')
	session.pop('u_id')
	return redirect('/')