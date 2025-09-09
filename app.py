# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# --- Database config ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visitors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Model ---
class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    host = db.Column(db.String(100), nullable=False)
    purpose = db.Column(db.String(200), nullable=False)
    sign_in_time = db.Column(db.DateTime, default=datetime.utcnow)
    sign_out_time = db.Column(db.DateTime, nullable=True)

# --- Routes ---
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form['name']
        host = request.form['host']
        purpose = request.form['purpose']

        visitor = Visitor(name=name, host=host, purpose=purpose)
        db.session.add(visitor)
        db.session.commit()

        return redirect(url_for("index"))

    visitors = Visitor.query.all()
    return render_template("index.html", visitors=visitors)

@app.route("/signout/<int:visitor_id>")
def sign_out(visitor_id):
    visitor = Visitor.query.get_or_404(visitor_id)
    visitor.sign_out_time = datetime.utcnow()
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # creates tables if not exist
    app.run(debug=True)
