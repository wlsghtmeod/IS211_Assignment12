from flask import Flask, render_template, request, redirect
import re
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("grades.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    return("Hello world!")


@app.route('/showstudents')
def showstudents():
    conn = get_db_connection()
    students = conn.execute('SELECT id, first, last from Student')

    return render_template('showstudents.html',students=students)


@app.route('/showstudent/<id>')
def showstudent(id):
    conn = get_db_connection()
    students = conn.execute(f'SELECT id, first, last from Student where id = {id}')

    return render_template('showstudents.html',students=students)


if __name__ == '__main__':
    app.run(debug=True)