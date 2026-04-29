from flask import Flask, render_template, request, send_file
import sqlite3
from flask import session, redirect, url_for
from flask import render_template, request, redirect, url_for, session, flash



app = Flask(__name__)
app.secret_key = "gymproject123"


from trainee import trainee_bp
app.register_blueprint(trainee_bp)

from attendance import attendance_bp
app.register_blueprint(attendance_bp)

from payments import payments_bp
app.register_blueprint(payments_bp)

from reports import reports_bp
app.register_blueprint(reports_bp)

from member import member_bp
app.register_blueprint(member_bp)



@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == "Taiba" and password == "Taiba3095":
            session['user'] = username
            return redirect(url_for('dashboard'))

        else:
            flash("Wrong username or password ❌")

    return render_template('login.html')



@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()

    trainers = conn.execute("SELECT COUNT(*) FROM trainer").fetchone()[0]
    trainees = conn.execute("SELECT COUNT(*) FROM trainee").fetchone()[0]
    active = conn.execute("SELECT COUNT(*) FROM trainee WHERE status='Active'").fetchone()[0]
    renewals = conn.execute("SELECT COUNT(*) FROM payments WHERE status='Pending'").fetchone()[0]

    conn.close()

    return render_template(
        'dashboard.html',
        trainers=trainers,
        trainees=trainees,
        active=active,
        renewals=renewals
    )




@app.route('/members')
def member():
    return render_template('members.html')

@app.route('/attendence')
def attendence():
    return render_template('attendence.html')


@app.route("/trainer", methods=["GET","POST"])
def trainer():

    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()

    # ⭐ INSERT LOGIC
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        specialization = request.form["specialization"]
        experience = request.form["experience"]

        conn.execute("""
            INSERT INTO trainer (name, phone, specialization, experience, status)
            VALUES (?, ?, ?, ?, 'Active')
        """, (name, phone, specialization, experience))

        conn.commit()

    trainers = conn.execute("SELECT * FROM trainer").fetchall()
    conn.close()

    return render_template("trainer.html", trainers=trainers)


@app.route('/logout')
def logout():
    session.clear()   # clears all session data
    return redirect(url_for('login'))



@app.route('/trainee')
def trainee():
    return render_template('trainee.html')

@app.route('/payments')
def payments():
    return render_template('payments.html')

@app.route('/enquiry', methods=['GET','POST'])
def enquiry():

    if "user" not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()

    # SAVE
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        interest = request.form['interest']
        status = request.form['status']

        conn.execute(
            "INSERT INTO enquiry (name, phone, interest, status) VALUES (?,?,?,?)",
            (name, phone, interest, status)
        )
        conn.commit()

    # FETCH
    enquiries = conn.execute("SELECT * FROM enquiry ORDER BY id DESC").fetchall()
    conn.close()

    return render_template('enquiry.html', enquiries=enquiries)


def get_db_connection():
    conn = sqlite3.connect('gym.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    conn.execute("""
                 CREATE TABLE IF NOT EXISTS trainer (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 phone TEXT,
                 specialization TEXT,
                 experience INTEGER,
                 status TEXT
                 );

                 """)
    conn.execute("""
                CREATE TABLE IF NOT EXISTS enquiry (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    phone TEXT,
                    interest TEXT,
                    status TEXT
                    );
                """)

    
    conn.commit()
    conn.close()

from datetime import date, timedelta



@app.route('/reports')
def reports():

    filter_type = request.args.get("filter", "daily")

    conn = get_db_connection()

    today = date.today()

    if filter_type == "daily":
        start = today

    elif filter_type == "weekly":
        start = today - timedelta(days=7)

    elif filter_type == "monthly":
        start = today - timedelta(days=30)

    elif filter_type == "yearly":
        start = today - timedelta(days=365)

    revenue = conn.execute("""
        SELECT SUM(amount) FROM payments
        WHERE date >= ?
    """, (start,)).fetchone()[0] or 0

    conn.close()

    return render_template("reports.html", total_revenue=revenue)



@app.route('/active-members')
def active_members():

    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()

    members = conn.execute("""
        SELECT * FROM trainee
        WHERE status='Active'
        ORDER BY name
    """).fetchall()

    conn.close()

    return render_template('active_members.html', members=members)


@app.route('/renewals')
def renewals():

    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()

    data = conn.execute("""
        SELECT id, amount, date, status
        FROM payments
        WHERE status='Pending'
        ORDER BY date DESC
    """).fetchall()

    conn.close()

    return render_template('renewals.html', data=data)





create_tables()

if __name__ == '__main__':
    app.run(debug=True)