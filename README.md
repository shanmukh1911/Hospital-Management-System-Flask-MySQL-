# 🏥 Hospital Management System (Flask + MySQL)

A **web-based Hospital Management System** built with **Flask** and **MySQL**.  
Allows admins and doctors to manage patients, appointments, and encounters with an **interactive, animated UI**.

---

## 1 Features
- Role-based authentication: **Admin** and **Doctor**
- Admin can **add/edit/delete doctors and patients**
- Doctors can **view patient history and appointments**
- Book and manage appointments
- Search patients by **ID or name**
- Responsive and animated UI for better user experience

---

##  Project Structure

---

### 2️ How it appears on GitHub


```markdown
Hospital-Management-System/
│
├── app.py # Main Flask app
├── requirements.txt # Python dependencies
├── README.md # Project overview
├── templates/ # HTML templates (Bootstrap + animations)
│ ├── base.html
│ ├── home.html
│ ├── patients.html
│ ├── register_patient.html
│ ├── register_doctor.html
│ ├── doctors.html
│ ├── appointments.html
│ ├── patient_history.html
│ ├── search_patient.html
│ ├── login.html
│ └── edit_doctor.html
└── static/ # Optional: CSS, JS, images
```

---

##  Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/shanmukh1911/Hospital-Management-System-Flask-MySQL-.git
cd Hospital-Management-System-Flask-MySQL-
```
2. **Create and activate a virtual environment**
  ```bash
  python -m venv venv
  # Windows
  venv\Scripts\activate
  # Linux / Mac
  source venv/bin/activate
  
  pip install -r requirements.txt
  python app.py
  ```

3. **Usage**
  ```Admin: manage doctors & patients
  Doctor: view appointments & patient history
  Use the navigation bar to access different sections
  Interactive forms and tables with animations
  ```

4. **Future Improvements**
   ```
   Hash passwords for security
   Role-based dashboards with custom layouts
   Enhanced error handling and validation
   Add static assets for richer animations & UI
   ```


