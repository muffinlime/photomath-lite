import tensorflow as tf
import cv2
from tensorflow import keras
import numpy as np
import pandas as pd


# takes image as input, localizes the characters and returns the model predictions
def predict(char_photos):
    prepared = prepare(char_photos)
    model = keras.models.load_model("mnist2")
    preds = model.predict(prepared)
    codes = np.array(pd.read_csv("decode.csv", header=None))
    realp = []

    for i in range(len(preds)):
        x = tf.argmax(preds[i])
        realp.append(codes[x])
   
    return list(np.reshape(realp, len(preds)))
    
    
# takes character photos as input, prepares them for predicting and returns them
def prepare(dataset):
    procd=list()
    for image in dataset:
        image = cv2.bitwise_not(image)
        image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)[1]
        image = np.expand_dims(image, -1)
        image = tf.image.resize_with_pad(image, 20, 20, method="nearest")
        image = tf.image.resize_with_crop_or_pad(image, 28, 28)
        procd.append(image)
    procd = np.array(procd)
    procd = procd / 255.0
    return procd