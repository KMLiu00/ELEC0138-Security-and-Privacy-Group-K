# Group K

## Coursework 1
### Overview
This project includes three Python scripts that work together to generate passwords and evaluate their strengths using machine learning. The scripts utilize two models trained on over 66,000 passwords to understand password creation patterns and strength evaluation.
1. `Generate.py`: This script trains a model to generate passwords based on the patterns found in password.csv. The generated model (password_model.h5) learns from over 65,000 passwords to understand how to create new ones.
2. `Strength.py`: This script uses machine learning to evaluate the strength of passwords. It trains a model (strength_model.h5) using password with strength.csv, which contains passwords and their corresponding strengths.
3. `CrackPassword.py`: This script uses the previously trained models to generate a password and evaluate its strength based on user inputs such as name, birthday,and pet's name.

### Dependencies
1. Python 3.x
2. TensorFlow
3. Numpy
4. Pandas

### Setup and Execution
1. Ensure all dependencies are installed using pip:
   ```
   pip install tensorflow numpy pandas
   ```
   
2. Run each script using Python:
   ```
   python Generate.py
   python strength.py
   python CrackPassword.py
   ```

Generate.py
- Trains a model to generate passwords from a given dataset (password.csv). The model uses an LSTM network to predict character sequences. The output model is saved as password_model.h5.

strength.py

- Trains a model to assess password strength. It creates features based on password characteristics and uses a simple feed-forward neural network. The output model is saved as strength_model.h5.

CrackPassword.py

- Generates passwords using password_model.h5 and evaluates their strengths using strength_model.h5. It takes user inputs to customize the password generation process.

Input / Output
- Input: User details (name, birthday, pet's name) for CrackPassword.py.
- Output: Generated passwords along with their strength evaluations.

Notes
- The strength evaluation ranges from 0 to 2, where 2 indicates the strongest.

***

## Coursework 2

This project provides a robust platform for secure password management, utilizing advanced cryptographic techniques for password protection and compliance with GDPR for handling personal data. It features user registration, secure login with multi-factor authentication, password generation, and management functionalities.

### Major Overview
1. `UserManager.py`: Manages user registration, login, and multi-factor authentication using email verification.
2. `PasswordManager.py`: Handles password generation, retrieval, updating, and deletion, securely managing user passwords with cryptographic techniques.
3. `app.py`: The Flask application that serves the web interface and API endpoints for user interactions with the system.

### Dependencies
1. Python 3.x
2. Flask
3. PyODBC
4. Cryptography
5. Dotenv
6. bcrypt
7. smtplib
8. email.mime.text
9. email.mime.multipart

### Setup and Execution:
1. #### Ensure all dependencies are installed using pip:
######  (Some of them are Standard Library Dependencies, no pip needed)
```
pip install Flask pyodbc cryptography python-dotenv bcrypt
```
2. #### Environment Setup, Generate necessary environment variables using:
```
python generate_env.py
```
3. #### Running the Application, Launch the application by running:
```
flask run
```
This will start a local server,  http://127.0.0.1:5000, where you can access the web interface.
### **Detailed Functionality**

`generate_env.py`

- Script automates the setup of environment variables critical for the secure operation of the web application. 
- It ensures that all cryptographic operations and database connections are initialized with secure, unique keys and credentials, adhering to best practices in security.

   ##### Implementation Details:
- _**Security Measures:**_ Uses Python’s secrets module to generate cryptographically strong random numbers for the Flask secret key, ensuring that the session cookies are protected against various attacks such as prediction and forgery.
- _**GDPR Compliance:**_ By automating the generation of secure keys and ensuring that these keys are never hard-coded into the application's source code, the script upholds GDPR principles of data protection by design and default.
- _**Scalability and Flexibility:**_ Automatically populates the .env file with parameters that can be easily modified for different deployment environments without any code changes, facilitating easy scaling and flexibility across development, testing, and production setups.

`userManager.py`

- Handles user registration with GDPR-compliant data handling practices.
- Manages secure login processes including password verifications and multi-factor authentication using email-based verification codes.

`PasswordManager.py`

- Generates and retrieves securely encrypted passwords.
- Allows users to update or delete their passwords.
- Implements Fernet encryption to ensure the security of password storage.

`app.py`

- Provides a Flask web interface for user interactions.
- Integrates UserManager and PasswordManager for complete functionality.
- Serves different endpoints for registration, login, password management, and user profile operations.

### **Web Interface Details**

This application utilizes several HTML templates to provide a user-friendly web interface. Here is a detailed breakdown of each:
1. `login.html`

- **Purpose:** Serves as the login page where users can enter their username and password to access their accounts.

- **Features:**
  - Form for username and password input.
  - Link to the registration page for new users.
  - Validation to ensure data entry before submission.
  
2. `register.html`
- **Purpose:** Allows new users to create an account by providing a username, password, and email address.
- **Features:**
   - Form for username, password, and email input.
   - Checkbox for users to agree to the use of their personal data in accordance with the Privacy Policy, aligning with GDPR compliance.
   - Validation for email format and mandatory fields.
3. `verify.html`
- **Purpose:** Handles the two-factor authentication process by asking users to enter the verification code sent to their email.
- **Features:**
   - Option to resend the verification code if needed.
   - Input field for entering the verification code received via email.
4. `password_generator.html`
- **Purpose:** Allows users to generate a strong password based on a user-defined keyword.
- **Features:**
   - Form to enter a keyword that influences the password generation.
   - Display area for the newly generated password.
   - Link to view user profile and manage existing passwords.
5. `profile.html`
- **Purpose:** Displays user profile information where users can view and manage their saved passwords and account details.
- **Features:**
   - Table listing all keywords associated with their corresponding strong passwords.
   - Options to delete individual passwords or the entire user account.
   - Each password is shown alongside actions for deletion to facilitate easy management.
6. `success.html`
- **Purpose:** Shown after successful operations, such as account verification or password updates, providing positive feedback to the user.
- **Features:**
   - Simple message display indicating success.
   - Link to return to the password generation page or log out.
  
### Input / Output

- Input: User credentials and requests via web forms.
- Output: Web pages displaying registration forms, login pages, password generation, and management options.

### Notes
- This system is designed to be robust against common security threats and adheres strictly to GDPR guidelines by ensuring minimal data collection and secure data handling.
- The implementation of Fernet encryption provides a high level of security for stored passwords, which are decrypted only during user authentication or password retrieval processes.
