import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical


passwords_df = pd.read_csv('password.csv', on_bad_lines='skip') #read files and skip error lines
passwords = passwords_df['password'].astype(str).tolist() #prepare the data, change to string arrays

#create mappings for the characters
chars = sorted(set("".join(passwords))) #seprate all characters in the password csv, remove duplicate elements and arrange in order
char_to_index = dict((c, i) for i, c in enumerate(chars)) #create an dictionary with character mapping to its index, for using charater to find index
index_to_char = dict((i, c) for i, c in enumerate(chars)) #create an dictiionary with index mapping to its character, for using index to search character

sequences = [] #create an empty array
for password in passwords: #loop every passwords
    sequences.append([char_to_index[char] for char in password]) #use every index number to represent every passwords

max_sequence_length = 12 #depends on longest passwords in the file
sequences = pad_sequences(sequences, maxlen=max_sequence_length, padding='post') #make sure every password sequences has the same length (12), if not long enough, add 0 from the end of the sequences

X = sequences[:, :-1] #get all elements in the sequence except the last one (input)
y = sequences[:, 1:] #get all elements in the sequence except the first one (prediction output)
y = to_categorical(y, num_classes=len(chars)) #convert y to one-hot encoded format, number of classes is same as the number of indexs in the dictionary

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding

#neural network part
model = Sequential()
model.add(Embedding(input_dim=len(chars), output_dim=50, input_length=max_sequence_length-1)) #vectorize data, input dimension is number of characters
model.add(LSTM(128, return_sequences=True)) #LSTM layer, output results at every timing
model.add(Dense(len(chars), activation='softmax')) #Dense layer

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

def data_generator(sequences, batch_size):
    num_batches = len(sequences) // batch_size #number of passwords devided by batch size
    while True:
        for batch_idx in range(num_batches):
            start = batch_idx * batch_size #get the first password position for each batch
            end = start + batch_size #get the last password position for each batch
            batch_sequences = sequences[start:end] #get all passwords positions for this batch
            X_batch = batch_sequences[:, :-1] #get all password positions except the last one
            y_batch = batch_sequences[:, 1:] #get all password positions except the first one
            y_batch = to_categorical(y_batch, num_classes=len(chars)) #convert y_batch to one-hot encoded format
            yield X_batch, y_batch

batch_size = 64
train_generator = data_generator(sequences, batch_size)
model.fit(train_generator, epochs=5, steps_per_epoch=len(sequences)//batch_size)

model.save('password_model.h5')