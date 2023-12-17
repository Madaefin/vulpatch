import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re
import csv
import numpy as np
import pandas as pd

df = pd.read_csv('data/dataset.csv')
texts = df.iloc[:, 0].tolist()  # Reading the first column and dropping NA values
print(len(texts))
labels = [1] * 6000 + [0] * 6000  # 1 for security, 0 for non-security


## Pre-processing 
# 1. Lowercasing and removing punctuation/special characters
texts_clean = [re.sub(r'[^\w\s]', '', text.lower()) for text in texts]

# 2. Tokenization and Vectorization
# Set the size of your vocabulary and maximum sequence length
vocab_size = 10000
max_length = 200

tokenizer = Tokenizer(num_words=vocab_size, oov_token="<OOV>")
tokenizer.fit_on_texts(texts_clean)
sequences = tokenizer.texts_to_sequences(texts_clean)

# 3. Padding or Truncating
padded_sequences = pad_sequences(sequences, maxlen=max_length, padding='post', truncating='post')

X_train, X_test, y_train, y_test = train_test_split(padded_sequences, labels, test_size=0.2, random_state=42)
X_train = np.array(X_train)
y_train = np.array(y_train)
X_test = np.array(X_test)
y_test = np.array(y_test)

# Define the LSTM model architecture
model = Sequential()
model.add(Embedding(vocab_size, 128, input_length=max_length))
model.add(LSTM(64, return_sequences=False))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))  # Output layer

# Compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Summarize the model
model.summary()

# Train the model
history = model.fit(X_train, y_train, epochs=10, batch_size=128, validation_split=0.1)
model.save('my_model.h5')

# After model.fit(), you predict the classes on the test set
y_pred = (model.predict(X_test) > 0.5).astype("int32")

# Then you calculate the metrics
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1 Score: {f1}")

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test loss: {loss}")
print(f"Test accuracy: {accuracy}")
