import tensorflow as tf
import numpy as np
import pandas as pd
import sys
import os
from tensorflow.python.ops import control_flow_ops
from tqdm import tqdm
from matplotlib import pyplot as plt
from copy import deepcopy
from tensorflow.examples.tutorials.mnist import input_data
import RBM
import lstm_rbm
import time
import midi_manipulation

"""
    This file contains the code for running a tensorflow session to generate music
"""


num = 3 #The number of songs to generate
primer_song = 'Pop_Music_Midi/elise.midi' #The path to the song to use to prime the network

def main(saved_weights_path, primer):
    # First, build model then get pointers to params
    neural_net = lstm_rbm.LSTMNet()

    tvars = neural_net.training_vars()
    x = neural_net.x

    saver = tf.train.Saver(tvars)

    song_primer = midi_manipulation.get_song(primer)

    with tf.Session() as sess:
        init = tf.initialize_all_variables()
        sess.run(init)
        saver.restore(sess, saved_weights_path) #load the saved weights of the network
        # #We generate num songs
        for i in tqdm(range(num)):
            generated_music = sess.run(neural_net.generate(300), feed_dict={x: song_primer}) #Prime the network with song primer and generate an original song
            new_song_path = "music_outputs/{}_{}".format(i, primer.split("/")[-1]) #The new song will be saved here
            midi_manipulation.write_song(new_song_path, generated_music)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
    
