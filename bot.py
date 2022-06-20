from chatterbot import ChatBot
import nltk
import cv2
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from face_emotion_analysis import setup_face_emotion, process_face, process_predictions
from threading import Thread, Event
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import StringVar
import emoji


def Bot():
    return ChatBot(
        'Sentiment',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///database.sqlite3'
    )

def setup_vader():
    nltk.download('vader_lexicon')
    return SentimentIntensityAnalyzer()

#TODO
def check_red_flags(i):
    return False

def process_red_flag(i):
    pass

capture_frame = Event()
comp = t1 = t2 = [0,0]

def get_emoji(comp):
    comp = comp[0] + comp[1]
    if(comp > 0.0 and comp <0.1):
        return ':full_moon_face:'
    elif(comp >= 0.1 and comp <= 0.2):
        return ':face_with_tongue:'
    elif(comp > 0.2):
        return':beaming_face_with_smiling_eyes:'
    elif(comp <= 0.0 and comp >= -0.1):
        return ':expressionless_face:'
    elif(comp < -0.1 and comp >= -0.2):
        return ':flushed_face:'
    elif(comp < 0.2):
        return ':disappointed_face:'
    else:
        return ':sweat_smile:'

def start_emoji():
    window = tk.Tk()
    window.attributes('-topmost', 'true')
    window.geometry("200x200")
    var = StringVar()
    var.set("Chat: " + str(comp[0]) + "\nFace: " + str(comp[1]))
    e = StringVar()
    e.set(emoji.emojize(':thumbs_up:'))
    message = tk.Label(window, textvariable = var)
    message.pack()
    message2 = tk.Label(window, textvariable = e, font=("Courier", 80), background='white')
    message2.pack()

    while True:
        if(capture_frame.isSet() and var.get() != "Chat: " + str(comp[0]) + "\nFace: " + str(comp[1])):
            var.set("Chat: " + str(comp[0]) + "\nFace: " + str(comp[1]))
            e.set(emoji.emojize(get_emoji(comp)))
            window.update()

def start_chating(bot):
    sid = setup_vader()
    while True:
        try:
            i = input()
            capture_frame.set()
            c = sid.polarity_scores(i)['compound']
            # print("Chat compound: {}".format(c))
            t1[0] = c
            if(check_red_flags(i)):
                print(process_red_flag(i))
            else:
                print(bot.get_response(i))

        except(KeyboardInterrupt, EOFError, SystemExit):
            break

def start_video(debug):
    filename_base = datetime.now().strftime("%H_%M_%S")
    n = 0 
    if(not Path(Path.joinpath(Path().cwd(), "data")).is_dir()):
        Path(Path.joinpath(Path().cwd(), "data")).mkdir()
    
    model = setup_face_emotion()

    while True:
        if(capture_frame.isSet()):
            cam = cv2.VideoCapture(0)
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            
            img, predictions = process_face(model, frame)

            img_name = str(Path.joinpath(Path().cwd(), "data", str(filename_base + "_" + str(n) + ".png")))
            
            if(debug):
                cv2.imwrite(img_name, img)
            c = process_predictions(predictions)
            # print("Face compound: {}".format(c))

            t2[1] = c
            
            n += 1
            cam.release()
            capture_frame.clear()

def start_threading_run(bot, debug=True):
    Thread(target = start_chating,  args=[bot]).start()
    Thread(target = start_video, args=[debug]).start()
    Thread(target = start_emoji).start()