from calendar import c
from logging import exception
from unittest import result
from flask import Flask, render_template, request, redirect
import re
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("grades.db")
    conn.row_factory = sqlite3.Row #can have name-based access to columns; this means that the database connection will return rows that behave like regular Python dictionaries.
    return conn


@app.route('/')
def index():
    return("Hello world!")


@app.route('/showstudents')
def showstudents():
    conn = get_db_connection()
    students = conn.execute('SELECT id, first, last from Student')

    return render_template('showstudents.html',students=students)

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    students = conn.execute('SELECT id, first, last from Student')

    quizzes = conn.execute('SELECT quiz_id, subject, number_q, quiz_date from Quizzes')

    return render_template('dashboard.html',quizzes=quizzes, students=students)

@app.route('/student/<id>')
def showstudent(id):
    conn = get_db_connection()
    results = conn.execute(f'SELECT student_id, quiz_id, score from Results where student_id = {id}')

    return render_template('showstudents.html',results=results)

@app.route('/addstudent')
def add_student():
    return render_template('addstudent.html')


@app.route('/student/add', methods = ['GET','POST'])
def submit_student():
    conn = get_db_connection()  
    if request.method == 'POST':
        try:
            first = request.form['first']
            last = request.form['last']

            if first == "" or last == "":
                raise exception
            
            conn.execute("INSERT INTO Student (first,last) VALUES(?,?)", (first,last))

            conn.commit()
            msg = "Record Added"
        except:
            conn.rollback()
            msg = "Error. Not recorded"
        
        finally:
            return render_template("addstudent.html", msg=msg)

@app.route('/addquiz')
def add_quiz():
    return render_template('addquiz.html')

@app.route('/quiz/add', methods = ['GET','POST'])
def submit_quizzes():
    conn = get_db_connection()  
    if request.method == 'POST':
        try:
            id = request.form['id']
            subject = request.form['subject']
            num_q = request.form['num_q']
            date = request.form['date']

            if id == "" or subject == "" or num_q == "" or date == "":
                raise exception
            
            conn.execute("INSERT INTO Quizzes (quiz_id,subject,number_q,quiz_date) VALUES(?,?,?,?)", (id,subject,num_q,date))

            conn.commit()
            msg = "Record Added"
        except:
            conn.rollback()
            msg = "Error. Not recorded"
        
        finally:
            return render_template("addquiz.html", msg=msg)


@app.route('/addresult')
def add_result():
    return render_template('addresult.html')

@app.route('/submitresult', methods = ['GET','POST'])
def submit_results():
    conn = get_db_connection()  
    if request.method == 'POST':
        try:
            student_id = request.form['student_id']
            quiz_id = request.form['quiz_id']
            score = request.form['score']
            
            conn.execute("INSERT INTO Results (student_id,quiz_id,score) VALUES(?,?,?)", (student_id,quiz_id,score))

            conn.commit()
            msg = "Record Added"
        except:
            conn.rollback()
            msg = "Error. Not recorded"
        
        finally:
            return render_template("showresult.html", msg=msg)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods = ["POST"])
def authenticate():
    id = request.form['id']
    pw = request.form['pw']

    if id == "admin" and pw == "password":
        return redirect('/dashboard')
    else:
        msg = "Credentials incorrect"
        return render_template('login.html', msg=msg)



if __name__ == '__main__':
    app.run(debug=True)