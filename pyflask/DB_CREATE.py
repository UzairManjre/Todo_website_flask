from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# Define your SQLAlchemy models here (e.g., using db.Model)

class Todo(db.Model):
    SNo = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno}-{self.title}-{self.desc}"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
