# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройка базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_registration.db'
db = SQLAlchemy(app)

# Создаем модель для участников мероприятия
class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

@app.route('/')
def index():
    participants = Participant.query.all()
    return render_template('index.html', participants=participants)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        participant = Participant(name=name, email=email)
        db.session.add(participant)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html')

if __name__ == '__main__':
    # Создаем таблицы базы данных
    with app.app_context():
        db.create_all()
    app.run(debug=True)