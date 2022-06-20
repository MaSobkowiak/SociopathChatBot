import os
import cv2
from cv2 import norm
import numpy as np
from keras.preprocessing import image
import warnings
warnings.filterwarnings("ignore")
# from keras.preprocessing.image import load_img, img_to_array 
from keras.utils import load_img, img_to_array
from keras.models import  load_model
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def setup_face_emotion():
    model = load_model("models\\best_model.h5")
    return model

def process_frame(x, y, w, h, test_img, gray_img):
    cv2.rectangle(test_img, (x, y), (x + w, y + h), (255, 0, 0), thickness=7)
    roi_gray = gray_img[y:y + w, x:x + h]  # cropping region of interest i.e. face area from  image
    roi_gray = cv2.resize(roi_gray, (224, 224))
    img_pixels = img_to_array(roi_gray)
    img_pixels = np.expand_dims(img_pixels, axis=0)
    img_pixels /= 255
    return img_pixels


def process_face(model, frame):
    face_haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)

    predictions = [0,0,0,0,0,0,0]
    for (x, y, w, h) in faces_detected:
        img_pixels = process_frame(x, y,w, h, frame, gray_img)
        
        predictions = model.predict(img_pixels)
        max_index = np.argmax(predictions[0])
        emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
        predicted_emotion = emotions[max_index]

        cv2.putText(frame, predicted_emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    resized_img = cv2.resize(frame, (1000, 700))
    return resized_img, predictions

def process_predictions(predictions):
    weights = {'angry' : -0.5, 'disgust': -0.3, 'fear': -0.2, 'happy': 0.8, 'sad': -0.1, 'surprise': 0.3, 'neutral': 0.0}
    compound = 0.0
    scaler = MinMaxScaler()
    pred = scaler.fit_transform(np.array(predictions).reshape(7,-1))
    pred = pred.reshape(-1,7)

    for i, r in enumerate(pred[0]):
        compound = compound + r * list(weights.values())[i]
    return compound