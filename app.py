from flask import Flask, request, jsonify, render_template
import sqlite3
from database import init_db
from datetime import datetime
app = Flask(__name__)

init_db()

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/signin', methods=['POST','GET'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        age = request.form['age']
        phone = request.form['phone']
        locality = request.form['locality']
        language = request.form['language']

        # Save to database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, email, age, phone, locality, language) VALUES (?, ?, ?, ?, ?, ?)", 
                  (username, email, age, phone, locality, language))
        conn.commit()
        conn.close()

        return render_template('signin.html', message="User registered successfully!")
    return render_template('signin.html')

@app.route('/pcod', methods=['POST','GET'])
def pcod_checker():
    return render_template('pcod.html')

@app.route('/menstrual_tracker', methods=['POST','GET'])
def menstrual_tracker():
    if request.method == 'POST':
        
        start = request.form['start_date']
        end = request.form['end_date']
        start_date = datetime.strptime(start, '%Y-%m-%d').date()
        end_date = datetime.strptime(end, '%Y-%m-%d').date()

        # Calculate the cycle length
        cycle_length = (end_date - start_date).days

        # Check for regularity
        if 26 <= cycle_length <= 32:
            message = "Your cycle is regular."
        else:
            message = "Your cycle is irregular."

        return render_template('periods.html', message=message)

    return render_template('periods.html')

@app.route('/learn')
def learn():
    return render_template('learning.html')

@app.route('/menstrual')
def menstrual():
    return render_template('menstrual.html')


if __name__ == '__main__':
    app.run(debug=True)