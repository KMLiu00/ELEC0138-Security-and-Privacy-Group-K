import os
import pyodbc
from cryptography.fernet import Fernet
import secrets
import string
import hashlib

class PasswordManager:
    def __init__(self):
        # Load database connection information from environment variables
        self.server = os.getenv('DB_SERVER')
        self.database = os.getenv('DB_NAME')
        self.username = os.getenv('DB_USERNAME')
        self.password = os.getenv('DB_PASSWORD')
        self.driver = '{ODBC Driver 18 for SQL Server}'

        # Establish connection with the SQL database
        self.conn_str = f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
        self.conn = pyodbc.connect(self.conn_str)
        self.cursor = self.conn.cursor()

        # Initialize the encryption tool
        fernet_key = os.getenv('FERNET_KEY')
        if not fernet_key:
            raise ValueError("FERNET_KEY is not set in environment variables.")
        self.fernet = Fernet(fernet_key.encode())

    def get_user_id(self, username):
        self.cursor.execute("SELECT UserID FROM Users WHERE Username = ?", (username,))
        user_record = self.cursor.fetchone()
        if user_record:
            return user_record[0]
        else:
            return None

    def generate_password(self, username, keyword):
        user_id = self.get_user_id(username)
        if not user_id:
            return None, "User not found."

        # Hash the keyword to ensure consistent format
        keyword_hash = hashlib.sha256(keyword.encode()).digest()  # Use digest for binary hash

        # Check if the password already exists
        self.cursor.execute("SELECT StrongPassword FROM UserPasswords WHERE UserID = ? AND KeywordHash = ?", (user_id, keyword_hash))
        result = self.cursor.fetchone()
        if result:
            # Password already exists, decrypt and return it
            decrypted_password = self.fernet.decrypt(result[0]).decode()
            return decrypted_password, "Entered keyword already exist, Password retrieved successfully:"

        # Generate a new strong password
        strong_password = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(16))
        encrypted_password = self.fernet.encrypt(strong_password.encode())

        # Insert the new password into the database
        self.cursor.execute("INSERT INTO UserPasswords (UserID, Keyword, KeywordHash, StrongPassword) VALUES (?, ?, ?, ?)",
                            (user_id, keyword, keyword_hash, encrypted_password))
        self.conn.commit()
        return strong_password, "New password generated successfully:"

    def get_passwords(self, username):
        user_id = self.get_user_id(username)
        if not user_id:
            return [], "User not found."

        self.cursor.execute("SELECT Keyword, StrongPassword FROM UserPasswords WHERE UserID = ?", (user_id,))
        records = self.cursor.fetchall()
        passwords = []
        for record in records:
            keyword = record[0]  # Assuming Keyword is stored in plaintext
            encrypted_password = record[1]
            decrypted_password = self.fernet.decrypt(encrypted_password).decode()
            passwords.append((keyword, decrypted_password))
        return passwords, "Passwords retrieved successfully."

    def retrieve_password(self, username, keyword):
        user_id = self.get_user_id(username)
        if not user_id:
            return None, "User not found."

        try:
            keyword_hash = hashlib.sha256(keyword.encode()).digest()
            self.cursor.execute("SELECT StrongPassword FROM UserPasswords WHERE UserID = ? AND KeywordHash = ?",
                                (user_id, keyword_hash))
            password_record = self.cursor.fetchone()
            if password_record:
                decrypted_password = self.fernet.decrypt(password_record[0]).decode()
                return decrypted_password, "Password retrieved successfully."
            return None, "Password not found."
        except pyodbc.Error as e:
            return None, f"Error retrieving passwords: {e}"

    def delete_password(self, username, keyword):
        user_id = self.get_user_id(username)
        if not user_id:
            return False, "User not found."

        try:
            keyword_hash = hashlib.sha256(keyword.encode()).digest()
            self.cursor.execute("DELETE FROM UserPasswords WHERE UserID = ? AND KeywordHash = ?",
                                (user_id, keyword_hash))
            self.conn.commit()
            return True, f"Password for keyword '{keyword}' deleted successfully."
        except Exception as e:
            return False, f"Failed to delete password: {e}"

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()




