from flask import Blueprint, render_template, request, redirect
import sqlite3

trainee_bp = Blueprint('trainee', __name__)

DB = "gym.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


# =============================
# MAIN PAGE (Insert + List)
# =============================
@trainee_bp.route('/trainee', methods=['GET', 'POST'])
def trainee():

    conn = get_db()
    cur = conn.cursor()

    # ---------- INSERT ----------
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        age = request.form['age']
        plan = request.form['plan']
        trainer = request.form['trainer']

        cur.execute("""
            INSERT INTO trainee
            (name, phone, age, plan, trainer, status)
            VALUES (?, ?, ?, ?, ?, 'Active')
        """, (name, phone, age, plan, trainer))

        conn.commit()


    # ---------- SEARCH ----------
    search = request.args.get('search')

    if search:
        cur.execute(
            "SELECT * FROM trainee WHERE name LIKE ?",
            ('%' + search + '%',)
        )
    else:
        cur.execute("SELECT * FROM trainee")

    trainees = cur.fetchall()

    cur.execute("SELECT name FROM trainer")
    trainers = cur.fetchall()

    conn.close()

    return render_template(
        "trainee.html",
        trainees=trainees,
        trainers=trainers
    )




# =============================
# DELETE
# =============================
@trainee_bp.route('/delete_trainee/<int:id>')
def delete_trainee(id):

    conn = get_db()
    conn.execute("DELETE FROM trainee WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/trainee')


# =============================
# EDIT
# =============================
@trainee_bp.route('/edit_trainee/<int:id>', methods=['GET', 'POST'])
def edit_trainee(id):

    conn = get_db()
    cur = conn.cursor()

    if request.method == 'POST':

        name = request.form['name']
        phone = request.form['phone']
        age = request.form['age']
        plan = request.form['plan']
        trainer = request.form['trainer']

        cur.execute("""
            UPDATE trainee
            SET name=?, phone=?, age=?, plan=?, trainer=?
            WHERE id=?
        """, (name, phone, age, plan, trainer, id))

        conn.commit()
        conn.close()

        return redirect('/trainee')


    cur.execute("SELECT * FROM trainee WHERE id=?", (id,))
    trainee = cur.fetchone()

    return render_template("edit_trainee.html", trainee=trainee)
