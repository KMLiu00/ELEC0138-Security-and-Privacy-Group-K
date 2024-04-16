from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from userManager import UserManager
from PasswordManager import PasswordManager
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'a_fallback_secret_key')

user_manager = UserManager()
password_manager = PasswordManager()

@app.route('/')
def home():
    if 'username' in session:
        # return to password generator page if logged in
        return redirect(url_for('password_generator'))
    # return to login page if didnt logged in
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = user_manager.login_user(username, password)
        if email:
            session['username'] = username  # store username to session
            session['user_email'] = email  # store user email to session
            flash('Login successful. Please verify your email.')
            return redirect(url_for('verify_code_page'))  # auto jump to ''
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/verify_code_page', methods=['GET', 'POST'])
def verify_code_page():
    if request.method == 'POST':
        user_input_code = request.form['verification_code']
        verification_result = user_manager.verify_code(user_input_code)
        if verification_result == 'verified':
            flash('Email verified successfully!')
            return redirect(url_for('success_page'))
        elif verification_result == 'expired':
            flash('Verification code has expired. Please resend the verification code.')
        else:
            flash('Incorrect verification code or code has expired. Please resend the verification code.')
    return render_template('verify.html')

@app.route('/send_verification_code', methods=['POST'])
def send_verification_code():
    email = session.get('user_email')
    if email:
        user_manager.send_verification_code(email)
        flash('Verification code sent to your email. Please enter it below.')
    else:
        flash('Error: Email address not found.')
    return redirect(url_for('verify_code_page'))

@app.route('/verify_code', methods=['POST'])
def verify_code():
    user_input_code = request.form.get('verification_code')
    verification_result = user_manager.verify_code(user_input_code)
    if verification_result == 'verified':
        flash('Email verified successfully!')
        return redirect(url_for('success_page'))  # Redirect to a success page upon correct and valid verification
    elif verification_result == 'expired':
        flash('Verification code has expired. Please resend the verification code.')
        return redirect(url_for('verify_code_page'))  # Redirect back to verification page to enter or resend code
    else:
        flash('Incorrect verification code. Please try again or resend the verification code.')
        return redirect(url_for('verify_code_page'))  # Redirect back to verification page for retry

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')  # get username,password and email from database
        password = request.form.get('password')
        email = request.form.get('email')
        consent = request.form.get('consent')  # This will check if the consent checkbox was checked
        if not consent:
            flash('You must agree to the email usage policy.')
            return redirect(url_for('register'))
        # check if submitted data already exsit in database
        if user_manager.register_user(username, password, email):
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Email or username might already exist.')
    # if not post request, return register
    return render_template('register.html')


@app.route('/success')
def success_page():
    return render_template('success.html')

@app.route('/password_generator', methods=['GET', 'POST'])
def password_generator():
    message = None
    password = None
    keyword = None
    if 'username' in session:
        if request.method == 'POST':
            keyword = request.form.get('keyword')
            # password generate based on username and keyword
            username = session['username']
            password, message = password_manager.generate_password(username, keyword)
            if not password:
                message = 'Unable to generate password. Please try again.'
        return render_template('password_generator.html', password=password, message=message, keyword=keyword)
    else:
        flash('Please login first.')
        return redirect(url_for('login'))


@app.route('/profile', methods=['GET'])
def profile():
    if 'username' not in session:
        flash('Please login first.')
        return redirect(url_for('login'))

    username = session['username']
    passwords, message = password_manager.get_passwords(username)
    if not passwords:
        flash(message)

    return render_template('profile.html', username=username, passwords=passwords)

@app.route('/delete_password', methods=['POST'])
def delete_password():
    username = session.get('username')
    keyword = request.form.get('keyword')
    if not username or not keyword:
        flash("Please login and specify a keyword.")
        return redirect(url_for('login'))

    success, message = password_manager.delete_password(username, keyword)
    flash(message)
    return redirect(url_for('profile'))

@app.route('/delete_account', methods=['POST'])
def delete_account():
    username = session.get('username')
    if not username:
        flash("Please login first.")
        return redirect(url_for('login'))

    success, message = user_manager.delete_user(username)
    if success:
        session.clear()
        flash('Your account has been successfully deleted.')
        return redirect(url_for('login'))
    else:
        flash(message)
    return redirect(url_for('profile'))


@app.route('/logout')
def logout():
    # clear message in session
    session.clear()
    flash('You have successfully logged out.')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

