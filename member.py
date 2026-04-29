from flask import Blueprint, render_template, request, redirect
import sqlite3
from datetime import date

member_bp = Blueprint('member', __name__)

DB = "gym.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


@member_bp.route('/member', methods=['GET', 'POST'])
def member():

    conn = get_db()
    cur = conn.cursor()

    today = str(date.today())

    # -------- INSERT --------
    if request.method == 'POST':

        name = request.form['name']
        phone = request.form['phone']
        age = request.form['age']
        plan = request.form['plan']

        cur.execute("""
            INSERT INTO member
            (name, phone, age, plan, join_date, status)
            VALUES (?, ?, ?, ?, ?, 'Active')
        """, (name, phone, age, plan, today))

        conn.commit()

        return redirect('/member')


    # -------- FETCH --------
    cur.execute("SELECT * FROM member")
    members = cur.fetchall()

    conn.close()

    return render_template("member.html", members=members)
