import pandas as pd
import tensorflow as tf

file_path = 'password with strength.csv'
data = pd.read_csv(file_path, on_bad_lines='skip') #read files and skip error lines

data['length'] = data['password'].apply(lambda x: len(str(x)) if pd.notnull(x) else 0) #calculate the length for each password and use lambda function to check if there is none, return zero
data['strength_category'] = pd.Categorical(data['strength']) #transfer strength data from cvs into a categorical data
strength_one_hot = pd.get_dummies(data['strength_category']) #one hot encoding, for example, passwords are catorgized to weak, medium and strong, weak is 100, medium is 010 and strong is 001

features = data[['length']] #only consider length as feature， save length to new data frames called feature
labels = strength_one_hot.values

dataset = tf.data.Dataset.from_tensor_slices((features.values, labels)) #sliced elements, feature values and lables
dataset = dataset.batch(32) #batch size is 32

#machine learning part
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(1,)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

train_dataset = dataset.take(int(len(dataset) * 0.8))
test_dataset = dataset.skip(int(len(dataset) * 0.8))

history = model.fit(train_dataset, epochs=2, validation_data=test_dataset)

model.save('my_password_strength_model.h5')