from flask import Flask, request, session, flash, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app and configure database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['SECRET_KEY'] = os.urandom(24)  # Ensure you have a secret key for session management
db = SQLAlchemy(app)

# Define models
class Organizer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    organization = db.Column(db.String(100), nullable=False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey('organizer.id'), nullable=False)
    organizer = db.relationship('Organizer', backref=db.backref('events', lazy=True))

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    qrlink = db.Column(db.String(100), nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    event = db.relationship('Event', backref=db.backref('participants', lazy=True))

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey("participant.id"), nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=True)
    score = db.Column(db.Integer, nullable=True)

# Create the database schema
with app.app_context():
    db.create_all()

# Define routes
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/alllog")
def alllog():
    return render_template("alllog.html")

@app.route("/admin_log")
def admin_log():
    return render_template("admin_log.html")

@app.route("/adminlog", methods=["POST"])
def mainadmin_log():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if email == "mainadmin@gmail.com" and password == "event123":
            session["admin"] = True
            session["admin_name"] = email
            flash("Login Successful", "success")
            return redirect(url_for("admin_dash"))
        else:
            flash("Invalid Credentials", "error")
            return redirect(url_for("admin_log"))
    else:
        session.clear()
        flash("Unauthorized access", "error")
        return redirect(url_for("home"))

@app.route("/admin_dash")
def admin_dash():
    return render_template("admin_dash.html")

@app.route("/participantreg")
def participantreg():
    return render_template("participantreg.html")

def upload(file, **options):
    pass  # Your upload logic here

if __name__ == "__main__":
    app.run(debug=True)