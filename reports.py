from flask import Blueprint, render_template
import sqlite3
from datetime import date

reports_bp = Blueprint('reports', __name__)

DB = "gym.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


@reports_bp.route('/reports')
def reports():

    conn = get_db()
    cur = conn.cursor()

    today = str(date.today())

    # -------- Counts --------
    cur.execute("SELECT COUNT(*) FROM trainer")
    total_trainers = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM trainee")
    total_trainees = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM attendance WHERE date=? AND status='Present'", (today,))
    present_today = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM payments")
    total_payments = cur.fetchone()[0]

    cur.execute("SELECT SUM(amount) FROM payments WHERE status='Paid'")
    total_revenue = cur.fetchone()[0] or 0

    cur.execute("SELECT COUNT(*) FROM payments WHERE status='Pending'")
    pending_payments = cur.fetchone()[0]

    conn.close()

    return render_template(
        "reports.html",
        total_trainers=total_trainers,
        total_trainees=total_trainees,
        present_today=present_today,
        total_payments=total_payments,
        total_revenue=total_revenue,
        pending_payments=pending_payments
    )

