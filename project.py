from time import ctime
import time
import speech_recognition as sr
import webbrowser
import playsound
import random
import numpy as np
from gtts import gTTS
import face_recognition
from face_recognition.api import face_encodings
import os
import subprocess
import cv2
import requests
from datetime import datetime
import tkinter as tkinter
from threading import Thread
import sys

greetingCommands = np.loadtxt(fname='./Commands/GreetingsCommands.txt',delimiter=',',dtype=np.str)
exitCommands = np.loadtxt(fname='./Commands/ExitCommands.txt',delimiter=',',dtype=np.str)

# Setting up voice recognizer
r = sr.Recognizer()
# Directory Paths 
FACE_DIR = "./Faces/"
ADMIN_DIR = './Admin/'
# Face recognition variables
TOLERANCE = 0.6
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = "cnn"

# Storing faces and names
known_faces = []
known_names = []

# For face recognition
def face_auth():
    global match, date_time
    now = datetime.now() # current date and time
    date_time = now.strftime("%d-%m-%Y-%H-%M-%S")
    
    # Loading images from the faces directory and sub folders
    for name in os.listdir(FACE_DIR):
        # Identifying faces within the images and storinf them in the known faces list
        for filename in os.listdir(f"{FACE_DIR}{name}"):
            image = face_recognition.load_image_file(f"{FACE_DIR}/{name}/{filename}")
            encoding = face_recognition.face_encodings(image)[0]
            known_faces.append(encoding)
            known_names.append(name)
    
    # Taking a picture using the webcam of the user
    madison_speak("Capturing Face....")
    cap = cv2.VideoCapture(0)
    ret, frame, = cap.read()
    # Storing image in the admin folder with its name as the date and time it was taken
    cv2.imwrite("./Admin/"+date_time+".png", frame)
    cv2.destroyAllWindows()
    cap.release()

    # Identifying a face within the captured image
    madison_speak("Scanning.....")
    # Loading the captured image
    input = face_recognition.load_image_file("./Admin/"+date_time+".png")
    locations = face_recognition.face_locations(input,model=MODEL)
    encodings = face_encodings(input,locations)
    image = cv2.cvtColor(input, cv2.COLOR_RGB2BGR)

    # Comparing all images in the known faces list to the captured image from the webcam
    madison_speak("Looking for Matches.....")
    for face_encoding, face_location in zip(encodings,locations):
        result = face_recognition.compare_faces(known_faces,face_encoding, TOLERANCE)
        match = None
        
        # When there is a match found the user is given access to the assistant 
        if True in result:
            match = known_names[result.index(True)]
            print(f"Match Found: {match}")
            madison_speak(f"Access Granted, Welcome {match}")
            # Recording of users that have used the application
            with open("./Admin/logs.txt", "a") as myfile:
                myfile.write("- " + match+": "+ctime()+"\n")   
            return True
        
        # When there is no match found
        else:
            # Record of the failed attempt
            with open("./Admin/logs.txt", "a") as myfile:
                myfile.write("- Failed Attempt: "+date_time+"\n")  
            madison_speak("Access Denied")
            return False

# listen for audio and convert it to text:
def record_audio(ask=False):
    with sr.Microphone() as source: 
        # Used for follow up questions
        if ask:
            madison_speak(ask)
        print("Listening......")
        r.pause_threshold = 1
        audio = r.record(source, duration=3)
        
        # The listen function stopped working for me unexpectedly but could work on another machine 
        # If so uncomment the listen and comment out the record method above
        #audio = r.listen(source)
    
    # Attempts to recognize the inputted voice
    try: 
        print("Recognizing...")     
        query = r.recognize_google(audio, language ='en-in') 
        print(f"User said: {query}\n") 
   
    except sr.UnknownValueError:  # error: recognizer does not understand
        print("Unknown Value")
        return "None"

    except sr.RequestError:
        # error: recognizer is not connected
        madison_speak('Sorry, the service is down')
        return "None"

    return query 

# For getting the application to speak
def madison_speak(audio_string):
    # Converting the text to speech
    textToSpeach = gTTS(text=audio_string,lang='en')
    # Adding what the application is saying to the UI
    msg_list.insert(tkinter.END,audio_string)
    # Giving a random name and number to the created audio file
    r= random.randint(1,10000)
    audio_file = 'audioNO-' +str(r) + '.mp3'
    # Saving, playing then removing
    textToSpeach.save(audio_file)
    playsound.playsound(audio_file)
    os.remove(audio_file)

# This takes what the record_audio method returns
def respond(voice_data):
    # Asking the assistant
    if voice_data in greetingCommands:
        madison_speak("Hello my name is Madison, how may i help you?")
        
    # Ask for the time
    if "time" in voice_data.split():
        madison_speak(ctime())
        
    # Check the weather
    if "weather" in voice_data.split():
        api_address='http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q='
        place = record_audio('Where would you like to get the weather for')
        url = api_address + place
        json_data = requests.get(url).json()
        try:
            format_add = json_data['weather'][0]['description']
            madison_speak(f"The weather in {place} is {format_add}")
        except:
            madison_speak("Error when listening could you please try again, thank you")
        
    # Search Google
    if "search" in voice_data.split():
        search_term = record_audio("What shall i search?")
        url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
        madison_speak(f'Here is what I found for {search_term} on google')

    # For making notes
    if "note" in voice_data.split():
        note = record_audio("What should i note?")
        
        with open("./notes.txt", "a") as myfile:
            myfile.write("- " + note+"\n")    
        madison_speak(f'{note} has been noted')        

    # Giving help
    if "help" in voice_data:
        madison_speak("Here is a list of my keywords ")
        madison_speak("Search, Weather, Open, Time, Note, Help")
        madison_speak("There will be follow up questions for specification")

    # For opening the notes and logs text
    if "open" in voice_data.split():
        file = record_audio("What would you like me to open? Logs, Notes or Admin?")
        
        if "logs" in file.split():
            madison_speak("Opening logs")
            subprocess.call(['notepad.exe', './Admin/logs.txt'])
            
        if "notes" in file.split():
            madison_speak("Opening notes")
            subprocess.call(['notepad.exe', './notes.txt'])
            
        if "admin" in file.split():
            madison_speak("Opening Admin Folder")
            subprocess.Popen(r'explorer /select,"C:\Users\Adam Varden\Documents\Year 4 Notes\Semester 2\Gesture Based UI\Final Project\Admin"')       
            
    if voice_data in exitCommands:
        madison_speak("Shutting Down....")
        madison_speak("Please Close the Window....")
        sys.exit()

def start(active = True):
    
    if face_auth() == True:
        time.sleep(1)
        madison_speak(f"How may I help you today, {match}?")
        while active:
            voice_data = record_audio()
            respond(voice_data) 

    
# Starting up the UI            
def UI():
    global msg_list
    # Using tkinter to create a user interface
    # This creates a window with a message list of what the assistant says
    root = tkinter.Tk()
    root.title("Madison")
    messages_frame = tkinter.Frame(root)
    scrollbar = tkinter.Scrollbar(messages_frame)
    msg_list = tkinter.Listbox(messages_frame,height=20, width=50, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msg_list.pack()
    messages_frame.pack()

    
    tkinter.mainloop()

# First method to be called 
if __name__ == "__main__":
    global APP_THREAD
    # Threads for the application and the user interface
    GUI_THREAD = Thread(target=UI)
    GUI_THREAD.start()
    APP_THREAD = Thread(target=start)
    APP_THREAD.start()
    
