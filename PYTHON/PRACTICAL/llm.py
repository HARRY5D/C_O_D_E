import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Sample text data (you'd use a much larger dataset in practice)
text = """
This is a small sample text for our basic language model.
It will learn to predict the next character based on the previous ones.
The more text we provide, the better it can learn patterns.
"""

# Tokenize the text
tokenizer = Tokenizer(char_level=True)
tokenizer.fit_on_texts([text])
total_chars = len(tokenizer.word_index) + 1

# Create input sequences and labels
input_sequences = []
for line in text.split('\n'):
    token_list = tokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i+1]
        input_sequences.append(n_gram_sequence)

# Pad sequences
max_sequence_len = max([len(x) for x in input_sequences])
input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))

# Create predictors and label
X, y = input_sequences[:,:-1], input_sequences[:,-1]
y = tf.keras.utils.to_categorical(y, num_classes=total_chars)

# Create the model
model = Sequential([
    Embedding(total_chars, 64, input_length=max_sequence_len-1),
    LSTM(100),
    Dense(total_chars, activation='softmax')
])

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

# Train the model
model.fit(X, y, epochs=100, verbose=1)

# Function to generate text
def generate_text(seed_text, next_chars, model, max_sequence_len):
    for _ in range(next_chars):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
        predicted = model.predict(token_list, verbose=0)
        predicted = np.argmax(predicted, axis=-1)
        output_char = ""
        for char, index in tokenizer.word_index.items():
            if index == predicted:
                output_char = char
                break
        seed_text += output_char
    return seed_text

# Generate some text
print(generate_text("This is", 50, model, max_sequence_len))