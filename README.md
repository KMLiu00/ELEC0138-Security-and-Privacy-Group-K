Coursework 1

This project includes three Python scripts that work together to generate passwords and evaluate their strengths using machine learning. The scripts utilize two models trained on over 66,000 passwords to understand password creation patterns and strength evaluation.
1. `Generate.py`: This script trains a model to generate passwords based on the patterns found in password.csv. The generated model (password_model.h5) learns from over 65,000 passwords to understand how to create new ones.
2. `Strength.py`: This script uses machine learning to evaluate the strength of passwords. It trains a model (strength_model.h5) using password with strength.csv, which contains passwords and their corresponding strengths.
3. `CrackPassword.py`: This script uses the previously trained models to generate a password and evaluate its strength based on user inputs such as name, birthday,and pet's name.

Dependencies
1. Python 3.x
2. TensorFlow
3. Numpy
4. Pandas

Setup and Execution
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

