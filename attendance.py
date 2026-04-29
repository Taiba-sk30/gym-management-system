from flask import Blueprint, render_template, request, redirect
import sqlite3
from datetime import date

attendance_bp = Blueprint('attendance', __name__)

DB = "gym.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


@attendance_bp.route('/attendance', methods=['GET', 'POST'])
def attendance():

    conn = get_db()
    cur = conn.cursor()

    today = str(date.today())

    # -------- INSERT ATTENDANCE --------
    if request.method == 'POST':

        trainee = request.form['trainee']
        status = request.form['status']

        cur.execute("""
            INSERT INTO attendance (trainee_name, date, status)
            VALUES (?, ?, ?)
        """, (trainee, today, status))

        conn.commit()

        return redirect('/attendance')


    # -------- FETCH trainees for dropdown --------
    cur.execute("SELECT name FROM trainee")
    trainees = cur.fetchall()

    # -------- FETCH today's attendance --------
    cur.execute("SELECT * FROM attendance WHERE date=?", (today,))
    records = cur.fetchall()

    conn.close()

    return render_template(
        "attendance.html",
        trainees=trainees,
        records=records,
        today=today
    )
