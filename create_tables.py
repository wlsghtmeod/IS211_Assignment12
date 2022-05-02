import sqlite3

DROP_STUDENT_TABLE = "DROP TABLE IF EXISTS STUDENT;"
DROP_QUIZ_TABLE = "DROP TABLE IF EXISTS QUIZZES;"
DROP_RESULT_TABLE ="DROP TABLE IF EXISTS RESULTS;"

STUDENT_TABLE = """
CREATE TABLE IF NOT EXISTS Student(
    id integer PRIMARY KEY AUTOINCREMENT,
    first TEXT,
    last TEXT
)
"""

QUIZZES_TABLE = """
CREATE TABLE IF NOT EXISTS Quizzes(
    quiz_id integer,
    subject TEXT,
    number_q integer,
    quiz_date TEXT
)
"""

RESULT_TABLE = """
CREATE TABLE IF NOT EXISTS Results(
    student_id integer,
    quiz_id integer,
    score integer
)
"""

def create_tables():
    conn = sqlite3.connect('grades.db')

    cur = conn.cursor()
    cur.execute(DROP_STUDENT_TABLE)
    cur.execute(DROP_QUIZ_TABLE)
    cur.execute(DROP_RESULT_TABLE)
    cur.execute(STUDENT_TABLE)
    cur.execute(QUIZZES_TABLE)
    cur.execute(RESULT_TABLE)
    conn.commit()

    conn.close()


if __name__ == "__main__":
    create_tables()