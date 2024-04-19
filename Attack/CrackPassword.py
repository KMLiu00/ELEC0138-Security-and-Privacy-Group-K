import pandas as pd
import tensorflow as tf
import numpy as np
import random
import string


password_model = tf.keras.models.load_model('password_model.h5') #input password model
strength_model = tf.keras.models.load_model('my_password_strength_model.h5') #input strength model

passwords_df = pd.read_csv('password.csv', on_bad_lines='skip') #skip error lines from csv
passwords = passwords_df['password'].astype(str).tolist()

#create mappings for the characters (dictionary)
chars = sorted(set("".join(passwords))) #extract all characters in the password csv, remove duplicate elements and arrange in order
char_to_index = dict((c, i) for i, c in enumerate(chars)) #create an dictionary with character mapping to its key, for using charater to find key
index_to_char = dict((i, c) for i, c in enumerate(chars)) #create an dictiionary with key mapping to its character, for using key to search character

def evaluate_password_strength(password):

    length = len(password) #calculate the length for password
    has_upper = any(c.isupper() for c in password) #check if there is upper case
    has_lower = any(c.islower() for c in password) #check if there is lower case
    has_special = any(c in set('!@#$%^&*()-_=+[]{};:",.<>?') for c in password) #check if there is special character in this password

    features = np.array([[length, has_upper, has_lower, has_special]], dtype=np.float32)

    prediction = strength_model.predict(features) #predict the strength by using the model
    strength = prediction.argmax(axis=1)[0]  #find the key with highest probility, and the key number represent the strength class (0-2)
    return strength


def generate_password(start_sequence):

    max_length = random.randint(8, 20)
    generated_password = start_sequence #initalization

    while len(generated_password) < max_length:
        input_seq = [char_to_index.get(generated_password[-1], 0)] #get the index for the last eletment, if it cannot be found, make it zero
        input_seq = np.array(input_seq).reshape(1, -1) #reshape input_seq to 2 dimensional with only one row

        prediction = password_model.predict(input_seq) #use the pre trained model
        flat_prediction = prediction.flatten() #flatten multi dimensional data to single row
        next_index = np.argmax(flat_prediction) #find the key with the highest prediticion probility for the next character

        next_char = index_to_char[next_index] #find which letter this key stands for
        generated_password += next_char #add the new character to the password array

    return generated_password

def preprocess_info(info):
    choices = [
        info['name'][0].upper(), #first letter of name upper case
        info['name'][0].lower(), #first letter of name lower case
        info['pet_name'][0].upper(),
        info['pet_name'][0].lower(),
        info['name'].split(' ')[0],  # firstname
        info['name'].split(' ')[0].upper(),  # firstname upper case
        info['name'].split(' ')[1].upper(),  # surname upper case
        info['name'].split(' ')[0].lower(),  # firstname lower case
        info['name'].split(' ')[1].lower(),  # surname lower case
        info['birthday'].split('-')[0],  # birth year
        ''.join(info['birthday'].split('-')[1:]), #birth month and day
        info['name'].capitalize().replace(' ', ''),
        info['name'].upper().replace(' ', ''),
        info['birthday'].replace('-', '')
    ] #define how much information can be used in the password cracking
    start_sequence = random.choice(choices) #random choose from information above to generate passwords
    return start_sequence

info = {
    'name': input("Enter your name: "),
    'birthday': input("Enter your birthday (YYYY-MM-DD): "),
    'pet_name': input("Enter your pet's name: "),
}#collect personal data

passwords_with_strengths = []
for _ in range(20): #20 passwords will be generated
    start_sequence = preprocess_info(info)
    generated_password = generate_password(start_sequence)
    strength = evaluate_password_strength(generated_password)
    passwords_with_strengths.append((generated_password, strength))

for password, strength in passwords_with_strengths:
    print(f"Password: {password}, Strength: {strength}")