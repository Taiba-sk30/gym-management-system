from flask import Blueprint, render_template, request, redirect
import sqlite3
from datetime import date

payments_bp = Blueprint('payments', __name__)

DB = "gym.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


@payments_bp.route('/payments', methods=['GET', 'POST'])
def payments():

    conn = get_db()
    cur = conn.cursor()

    today = str(date.today())

    if request.method == 'POST':

        trainee = request.form['trainee']
        amount = request.form['amount']
        status = request.form['status']

        cur.execute(
            "INSERT INTO payments (trainee_name, amount, date, status) VALUES (?, ?, ?, ?)",
            (trainee, amount, today, status)
        )

        conn.commit()

        return redirect('/payments')


    cur.execute("SELECT name FROM trainee")
    trainees = cur.fetchall()

    cur.execute("SELECT * FROM payments ORDER BY id DESC")
    records = cur.fetchall()

    conn.close()

    return render_template("payments.html", trainees=trainees, records=records)

import csv
from flask import Response


@payments_bp.route('/export_payments')
def export_payments():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM payments")
    rows = cur.fetchall()

    def generate():
        data = csv.writer(open('payments.csv', 'w', newline=''))
        yield "ID,Name,Amount,Date,Status\n"

        for r in rows:
            yield f"{r['id']},{r['trainee_name']},{r['amount']},{r['date']},{r['status']}\n"

    return Response(
        generate(),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=payments.csv"}
    )
