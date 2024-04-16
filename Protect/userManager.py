import pyodbc
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
import string
import bcrypt
from flask import session
import datetime

class UserManager:
    def __init__(self):
        self.server = os.getenv('DB_SERVER')
        self.database = os.getenv('DB_NAME')
        self.username = os.getenv('DB_USERNAME')
        self.password = os.getenv('DB_PASSWORD')
        self.driver = '{ODBC Driver 18 for SQL Server}'
        self.conn_str = f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
        try:
            self.conn = pyodbc.connect(self.conn_str)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Database connection error: {e}")
            raise

    def register_user(self, username, password, email):
        print("Attempting to register user:", username)
        try:
            # check if email already exist
            self.cursor.execute("SELECT COUNT(*) FROM Users WHERE Email = ?", email)
            if self.cursor.fetchone()[0] > 0:
                print("Email already exists.")
                return False
            # check if username exist
            self.cursor.execute("SELECT COUNT(*) FROM Users WHERE Username = ?", username)
            if self.cursor.fetchone()[0] > 0:
                return False

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            print("Hashed password:", hashed_password)

            # insert new information to database
            self.cursor.execute("INSERT INTO Users (Username, Password, Email) VALUES (?, ?, ?)", username, hashed_password, email)
            self.conn.commit()
            print("User registered successfully.")
            return True
        except pyodbc.Error as e:
            print(f"SQL error: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error during registration: {e}")
            return False


    def login_user(self, username, input_password):
        try:
            self.cursor.execute("SELECT Password, Email FROM Users WHERE Username = ?", username)
            row = self.cursor.fetchone()
            if row:
                stored_password, email = row
                if bcrypt.checkpw(input_password.encode('utf-8'), stored_password.encode('utf-8')):
                    return email  # Proceed with two-step verification
            return None  # None indicates either user not found or password incorrect
        except Exception as e:
            print(f"Error during login: {e}")
            return None

    def send_verification_code(self, email):
        verification_code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))
        now = datetime.datetime.utcnow()  # utc time
        session['verification_code'] = verification_code
        session['code_issued_time'] = now.strftime('%Y-%m-%d %H:%M:%S')  # store as string

        subject = "Your Verification Code"
        body = (f"Your verification code is: {verification_code} "
                f"this code will be expired in 5min")
        self.send_email(email, subject, body)
        return verification_code

    def verify_code(self, input_code):
        correct_code = session.get('verification_code')
        code_issued_time_str = session.get('code_issued_time')
        if correct_code and code_issued_time_str:
            code_issued_time = datetime.datetime.strptime(code_issued_time_str, '%Y-%m-%d %H:%M:%S')
            current_time = datetime.datetime.utcnow()
            time_difference = (current_time - code_issued_time).total_seconds()

            if input_code == correct_code and time_difference <= 300:
                session.pop('verification_code', None)
                session.pop('code_issued_time', None)
                return 'verified'
            elif time_difference > 300:
                return 'expired'
        return 'mismatch'

    # send_verification_code() used to generate a code and pass to send_email(),
    def send_email(self, receiver_email, subject, body):
        print("Attempting to send email...")
        sender_email = "eeegroupk1@gmail.com"
        password = "lhin ciqa kfka xven"  # password for gmail
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        try:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully")
        except Exception as e:  # used to catch exceptions, and store error info in 'e'
            print(f"Error sending email: {e}")
        finally:
            server.quit()

    def get_user_data(self, username):
        # Retrieve user data stored in the database.
        try:
            self.cursor.execute("SELECT Username, Email FROM Users WHERE Username = ?", (username,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving user data: {e}")
            return None

    def get_user_id(self, username):
        try:
            self.cursor.execute("SELECT UserID FROM Users WHERE Username = ?", username)
            result = self.cursor.fetchone()
            if result:
                return result[0]
        except Exception as e:
            print(f"Error retrieving user ID: {e}")
        return None

    def delete_user(self, username): # Delete a user account from the database.
        try:
            user_id = self.get_user_id(username)
            if not user_id:
                return False, "User not found."

            # delete all passwords
            self.cursor.execute("DELETE FROM UserPasswords WHERE UserID = ?", (user_id,))
            self.cursor.execute("DELETE FROM Users WHERE UserID = ?", (user_id,))
            self.conn.commit()
            return True, "Your account and all related data have been successfully deleted."
        except Exception as e:
            return False, f"Failed to delete account: {e}"

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

