import pandas as pd
import tensorflow as tf
import numpy as np
import random
import string


password_model = tf.keras.models.load_model('password_model.h5') #input password model
strength_model = tf.keras.models.load_model('my_password_strength_model.h5') #input strength model

passwords_df = pd.read_csv('password.csv', on_bad_lines='skip') #skip error lines from csv
passwords = passwords_df['password'].astype(str).tolist()

#create mappings for the characters
chars = sorted(set("".join(passwords))) #seprate all characters in the password csv, remove duplicate elements and arrange in order
char_to_index = dict((c, i) for i, c in enumerate(chars)) #create an dictionary with character mapping to its index, for using charater to find index
index_to_char = dict((i, c) for i, c in enumerate(chars)) #create an dictiionary with index mapping to its character, for using index to search character

def evaluate_password_strength(password):
    password_length = tf.constant([[len(password)]], dtype=tf.float32)
    prediction = strength_model.predict(password_length)
    strength = prediction.argmax(axis=1)[0] + 1
    return strength

def generate_password(start_sequence):
    generated_password = start_sequence #initalization

    while len(generated_password) < 12: # repeat 12 times
        input_seq = [char_to_index.get(generated_password[-1], 0)] #get the index for the last eletment, if cannot be found, make it zero
        input_seq = np.array(input_seq).reshape(1, -1) #reshape input_seq to 2 dimensional with only one row

        prediction = password_model.predict(input_seq) #use the pre trained model
        flat_prediction = prediction.flatten() #flatten multi dimensional data to single row
        next_index = np.argmax(flat_prediction) #find the index with the highest prediticion probility for the next character

        next_char = index_to_char[next_index] #find which letter this index stands for
        generated_password += next_char #add the new character to the password array
    return generated_password

def preprocess_info(info):
    choices = [
        info['name'][0].upper(), info['name'][0].lower(),
        info['spouse_name'][0].upper(), info['spouse_name'][0].lower(),
        info['birthday'].split('-')[0],
        ''.join(info['birthday'].split('-')[1:])
    ] #define how much information can be used in the password cracking
    start_sequence = random.choice(choices)
    return start_sequence

info = {
    'name': input("Enter your name: "),
    'birthday': input("Enter your birthday (YYYY-MM-DD): "),
    'email': input("Enter your email: "),
    'phone': input("Enter your phone number: "),
    'spouse_name': input("Enter your spouse's name: "),
    'spouse_birthday': input("Enter your spouse's birthday (YYYY-MM-DD): ")
}#collect personal data

passwords_with_strengths = []
for _ in range(10): #10 passwords will be generated
    start_sequence = preprocess_info(info)
    generated_password = generate_password(start_sequence)
    strength = evaluate_password_strength(generated_password)
    passwords_with_strengths.append((generated_password, strength))

for password, strength in passwords_with_strengths:
    print(f"Password: {password}, Strength: {strength}")