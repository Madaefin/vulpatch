import tensorflow as tf
from tensorflow.keras.models import load_model
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
x_test = np.array(padded_sequences)
model = load_model('my_model.h5', compile=True)
y_pred = (model.predict(x_test) > 0.5).astype("int32")

print(y_pred)