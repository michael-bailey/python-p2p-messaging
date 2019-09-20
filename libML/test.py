#!bin/env python3

import numpy as np
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras import Sequential

import string

tf.enable_eager_execution()

class RNN:
    Characters = list(string.printable)
    sequence_length = 150

    batch_size = 64

    buffer_size = 100000

    # will add an option to create with a already trained model
    # but for now just a model that will be trained
    def __init__(self):
        self.load_data()
        self.char2idx = {u: i for i, u in enumerate(self.Characters)}
        self.idx2char = np.array(self.Characters)
        self.text_as_int = np.array([self.char2idx[c] for c in self.text])

        self.char_dataset = tf.data.Dataset.from_tensor_slices(self.text_as_int)

        self.dataset = self.char_dataset.map(self.split_input_target)

        dataset = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)

    def get_model(self):
        return Sequential([
            keras.layers.Embedding(len(self.Characters), 256, batch_input_shape=[64, None]),
            keras.layers.LSTM(1024, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform'),
            keras.layers.Dense(len(self.Characters))
        ])

    def load_data(self):
        print('=== loading data ===')
        self.text = open(input("enter file name to load"), 'rb').read().decode(encoding='utf-8')
        self.samples_per_epoch = len(self.text)

    def split_input_target(chunk):
        input_text = chunk[:-1]
        target_text = chunk[1:]
        return input_text, target_text

RNN()
