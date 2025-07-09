from flask import Flask, request, render_template, session, redirect, url_for
from markupsafe import Markup 
from pcodPredict import ask_assistant
import markdown as md
from database import init_db, get_user_by_id, delete_user, update_user, add_user, get_user_by_email
from datetime import datetime
from dotenv import load_dotenv
from datetime import timedelta
from functools import wraps
import os
from doctors import get_doctors
from werkzeug.security import generate_password_hash, check_password_hash
from hormone import ask_about_hormones

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in') or not session.get('id'):
            session.clear()
            return redirect(url_for('login'))  # Redirect to login
        return f(*args, **kwargs)
    return decorated_function
   
app = Flask(__name__)

app.permanent_session_lifetime = timedelta(days=7)

load_dotenv()

app.secret_key = os.getenv('SECRET_KEY')

init_db()

@app.route('/')
def main():
    return render_template('index.html')

# profile section

@app.route('/profile')
@login_required
def profile():
    user_id = session.get('id')
    if not user_id:
        session.clear()
        return redirect(url_for('login'))

    user = get_user_by_id(user_id)
    if not user:
        session.clear()
        return redirect(url_for('signin'))
    
    return render_template('profile.html', user=user)

# edit profile

@app.route('/edit_field/<field>', methods=['POST'])
@login_required
def edit_field(field):
    user_id = session.get('id')
    user = get_user_by_id(user_id)
    if not user:
        return redirect(url_for('signin'))
    
    value = request.form.get('value')
    allowed_fields = ['username', 'email', 'password', 'age', 'phone', 'locality', 'language']
    if field not in allowed_fields:
        return redirect(url_for('profile'))
    
    updated_data = {**user, field: value}
    update_user(
        user_id,
        updated_data['username'],
        updated_data['email'],
        updated_data['age'],
        updated_data['phone'],
        updated_data['locality'],
        updated_data['language']
        )
    return redirect(url_for('profile'))

# sign in

@app.route('/signin', methods=['POST','GET'])
def signin():
    if session.get('logged_in'):
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        phone = request.form['phone']
        locality = request.form['locality']
        language = request.form['language']        
        
        # check for duplicate mail
        if get_user_by_email(email):
            return render_template('signin.html', message="Email already registered.")

        hashed = generate_password_hash(password)
        
    
        user_id = add_user(username, email, hashed, age, phone, locality, language)
        
        # Set session variables
        session['id'] = user_id
        session['logged_in'] = True
        session['username'] = username
        session.permanent = True
        
        return redirect(url_for('main'))
    return render_template('signin.html')

# log in

@app.route('/login', methods=['POST', 'GET'])
def login():
    if session.get('logged_in') and session.get('id'):
        return redirect(url_for('profile'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = get_user_by_email(email)
        if user and check_password_hash(user['password'], password):
            session['id'] = user['id']
            session['logged_in'] = True
            session['username'] = user['username']
            session.permanent = True
            return redirect(url_for('profile'))
        else:
            return render_template('login.html', message="Invalid email or password.")
    return render_template('login.html')

# log out
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('main'))

# delete

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user_id = session.get('id')
    if user_id:
        delete_user(user_id)
    session.clear()
    return redirect(url_for('main'))

# pcod prediction

@app.route('/pcod', methods=['POST','GET'])
@login_required
def pcod_checker():
    user_id = session.get('id')
    user = get_user_by_id(user_id)
        
    if not user:
        session.clear()
        return redirect(url_for('signin'))
    
    if request.method == 'POST':
        
        symptoms = request.form['symptoms']
        weight = request.form['weight']
        height = request.form['height']
        age = user['age']

        # Validate inputs
        if not symptoms or not weight or not height or not age:
            return render_template('pcod.html', message="Please fill in all fields.")

        try:
            weight = float(weight)
            height = float(height)
            age = int(age)
        except ValueError:
            return render_template('pcod.html', message="Invalid input. Please enter valid numbers.")

        # Call the assistant function
        advice = ask_assistant(symptoms, weight, height, age)
        advice = Markup(md.markdown(advice))  # Convert Markdown to HTML
        return render_template('pcod.html', advice=advice)
    return render_template('pcod.html')

# menstrual cycle prediction

@app.route('/menstrual_tracker', methods=['POST','GET'])
@login_required
def menstrual_tracker():
    if request.method == 'POST':
        
        start = request.form['start_date']
        end = request.form['end_date']
        start_date = datetime.strptime(start, '%Y-%m-%d').date()
        end_date = datetime.strptime(end, '%Y-%m-%d').date()

        # Calculate the cycle length
        
        length = (end_date - start_date).days
        
        if length == 28:
            message = "Your cycle length is exactly 28 days — the average and most common cycle length."
            colour = "green"
        if length < 21 or length > 35:
            message = "Your cycle length is outside the normal range. Please consult a healthcare professional."
            colour = "red"
        else:
            message = "Your cycle length is within the normal range. You can track your periods effectively."
            colour = 'blue'
        return render_template('periods.html', message=message, colour=colour)

    return render_template('periods.html')

# Doctors

@app.route('/doctors',methods=['POST', 'GET'])
def doctors():
    if request.method == 'POST':
        location = request.form.get('location')
        if not location:
            return render_template('doctors.html', message="Please enter a location.")
        print(f"Searching for doctors in: {location}")
        try:
            doctors_list = get_doctors(location)
            if not doctors_list:
                return render_template('doctors.html', message="No doctors found for the specified location.")
            print(f"{doctors_list}")
            return render_template('doctors.html', doctors=doctors_list)
        except Exception as e:
            return render_template('doctors.html', message=f"An error occurred: {str(e)}")
    print('get')
    return render_template('doctors.html')

# Hormone tracker

@app.route('/hormone_tracker', methods=['POST', 'GET'])
def hormone_tracker():
    if request.method == 'POST':
        Age = request.form['age']
        Gender = request.form['gender']
        Weight = request.form['weight']
        Height = request.form['height']
        Menstrualhistory =request.form['menstrual_history']
        symptoms = request.form['symptoms']
        Lifestylefactors = request.form['lifestyle_factors']
        Medicalhistory = request.form['medical_history']

        # validate inputs
        if not Age or not Gender or not Weight or not Height or not Menstrualhistory or not symptoms or not Lifestylefactors or not Medicalhistory:
            return render_template('hormoneTracker.html', message="Please fill in all fields.")
        try:
            Age = int(Age)
            Weight = float(Weight)
            Height = float(Height)
        except ValueError:
            return render_template('hormoneTracker.html', message="Invalid input. Please enter valid numbers.")
        # Call the assistant function
        response = ask_about_hormones(Age, Gender, Weight, Height, Menstrualhistory, symptoms, Lifestylefactors, Medicalhistory)
        response = Markup(md.markdown(response))  # Convert Markdown to HTML
        return render_template('hormoneTracker.html', response=response)
        
    return render_template('hormoneTracker.html') 

# learning pages routes


@app.route('/learn')
def learn():
    return render_template('learning.html')

@app.route('/learn_menstrual')
def learn_menstrual():
    return render_template('menstrual.html')

@app.route('/learn_pcod')
def learn_pcod():
    return render_template('pcodPcos.html')

@app.route('/learn_pregnancy')
def learn_pregnancy():
    return render_template('pregnancy.html')

@app.route('/learn_female_hygiene')
def learn_female_hygiene():
    return render_template('hygiene.html')

@app.route('/learn_diet')
def learn_diet():
    return render_template('diet.html')

@app.route('/learn_yoga')
def learn_yoga():
    return render_template('yoga.html')

if __name__ == '__main__':
    app.run(debug=True)