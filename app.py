from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# ------------------------
# Flask App Setup
# ------------------------
app = Flask(__name__)
app.secret_key = "supersecretkey"  # change this to something secure

# ------------------------
# Database Connection
# ------------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shanmukh@1911",   # change if needed
    database="hospital_management"
)

# ------------------------
# Flask-Login Setup
# ------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return User(user["user_id"], user["username"], user["role"])
    return None

# ------------------------
# Routes
# ------------------------

@app.route("/")
@login_required   # ✅ forces login before accessing home
def home():
    return render_template("home.html")

# ------------------------
# Authentication
# ------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and user["password"] == password:  # ⚠️ later use check_password_hash
            user_obj = User(user["user_id"], user["username"], user["role"])
            login_user(user_obj)
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials!", "danger")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

# ------------------------
# Patients
# ------------------------
@app.route("/patients")
@login_required
def view_patients():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    cursor.close()
    return render_template("patients.html", patients=patients)

@app.route("/register_patient", methods=["GET", "POST"])
@login_required
def register_patient():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        dob = request.form["dob"]
        gender = request.form["gender"]
        contact = request.form["contact"]

        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            INSERT INTO patients (first_name, last_name, dob, gender, contact)
            VALUES (%s, %s, %s, %s, %s)
        """, (first_name, last_name, dob, gender, contact))
        db.commit()
        cursor.close()
        return redirect(url_for("view_patients"))
    return render_template("register_patient.html")

@app.route('/search_patient', methods=['GET', 'POST'])
@login_required
def search_patient():
    results = []
    search_term = None
    if request.method == 'POST':
        search_term = request.form['search_query'].strip()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM patients WHERE patient_id = %s OR first_name LIKE %s OR last_name LIKE %s",
            (search_term, f"%{search_term}%", f"%{search_term}%")
        )
        results = cursor.fetchall()
        cursor.close()
    return render_template('search_patient.html', patients=results, search_term=search_term)
#---------------------------------------------------------------------------------------------
# Edit Doctor
@app.route("/edit_doctor/<int:doctor_id>", methods=["GET", "POST"])
@login_required
def edit_doctor(doctor_id):
    if current_user.role != "admin":  # only admin can edit
        flash("Access denied! Admins only.", "danger")
        return redirect(url_for("view_doctors"))

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        specialty = request.form["specialty"]
        contact = request.form["contact"]

        cursor.execute("""
            UPDATE doctors
            SET first_name=%s, last_name=%s, specialty=%s, contact=%s
            WHERE doctor_id=%s
        """, (first_name, last_name, specialty, contact, doctor_id))
        db.commit()
        cursor.close()
        flash("Doctor updated successfully!", "success")
        return redirect(url_for("view_doctors"))

    cursor.execute("SELECT * FROM doctors WHERE doctor_id=%s", (doctor_id,))
    doctor = cursor.fetchone()
    cursor.close()

    return render_template("edit_doctor.html", doctor=doctor)


# Delete Doctor
@app.route("/delete_doctor/<int:doctor_id>", methods=["POST", "GET"])
@login_required
def delete_doctor(doctor_id):
    if current_user.role != "admin":  # only admin can delete
        flash("Access denied! Admins only.", "danger")
        return redirect(url_for("view_doctors"))

    cursor = db.cursor()
    cursor.execute("DELETE FROM doctors WHERE doctor_id=%s", (doctor_id,))
    db.commit()
    cursor.close()

    flash("Doctor deleted successfully!", "info")
    return redirect(url_for("view_doctors"))

#-----------------------------------------------------------------------------------
# ------------------------
# Doctors
# ------------------------
@app.route("/doctors")
@login_required
def view_doctors():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM doctors")
    doctors = cursor.fetchall()
    cursor.close()
    return render_template("doctors.html", doctors=doctors)

@app.route("/register_doctor", methods=["GET", "POST"])
@login_required
def register_doctor():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        specialty = request.form["specialty"]
        contact = request.form["contact"]

        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            INSERT INTO doctors (first_name, last_name, specialty, contact)
            VALUES (%s, %s, %s, %s)
        """, (first_name, last_name, specialty, contact))
        db.commit()
        cursor.close()
        return redirect(url_for("view_doctors"))
    return render_template("register_doctor.html")

# ------------------------
# Appointments
# ------------------------
@app.route("/appointments", methods=["GET", "POST"])
@login_required
def appointments():
    if request.method == "POST":
        patient_id = request.form["patient_id"]
        doctor_id = request.form["doctor_id"]
        appointment_date = request.form["appointment_date"]

        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            INSERT INTO appointments (patient_id, doctor_id, appointment_date)
            VALUES (%s, %s, %s)
        """, (patient_id, doctor_id, appointment_date))
        db.commit()
        cursor.close()
        return redirect(url_for("appointments"))

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    cursor.execute("SELECT * FROM doctors")
    doctors = cursor.fetchall()
    cursor.close()
    return render_template("appointments.html", patients=patients, doctors=doctors)

# ------------------------
# Patient History
# ------------------------
@app.route("/patient_history/<int:patient_id>")
@login_required
def patient_history(patient_id):
    sql = """
        SELECT e.encounter_id, CONCAT(p.first_name,' ',p.last_name) AS patient,
               CONCAT(d.first_name,' ',d.last_name) AS doctor,
               e.visit_start, e.visit_end, e.notes
        FROM encounters e
        JOIN patients p ON p.patient_id = e.patient_id
        JOIN doctors d ON d.doctor_id = e.doctor_id
        WHERE e.patient_id = %s
    """
    cursor = db.cursor(dictionary=True)
    cursor.execute(sql, (patient_id,))
    history = cursor.fetchall()
    cursor.close()
    return render_template("patient_history.html", history=history)

# ------------------------
# Run App
# ------------------------
if __name__ == "__main__":
    app.run(debug=True)
