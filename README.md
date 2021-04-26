# Security Voice Assistant

## You will need to make sure these packages are installed
Run the following lines of code in the command line, having the anaconda command prompt makes things a lot easier

``pip install SpeechRecognition``

``pip install numpy``

``pip install playsound``

``pip install gTTS``

``pip install face-recognition``

``pip install opencv-python``

``pip install PyAudio``

``pip install cmake``

``pip install dlib``

## Incase of errors 

Follow instructions on the first answer of this stackoverflow

[Stackoverflow Answer](https://stackoverflow.com/questions/52283840/i-cant-install-pyaudio-on-windows-how-to-solve-error-microsoft-visual-c-14)

[Youtube video for dlib solution](https://www.youtube.com/watch?v=jjRFCTmK2SY&ab_channel=Ritesh)

Download the wahl file based what version of python you have and if its x64 or x32 bit

I used python 3.8 x64 bit

### Dlib

[Link to download dlib](https://github.com/RvTechiNNovate/face_recog_dlib_file)

### Pyaudio

[Link to download pyaudio](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

## Running the Application
1. Add a folder with your name and picture of you to it
2. Run it using `python project.py`
3. Stay in clear view of the camera
4. Once cleared say a sentence with the word help in it


## Issue
When working on this project the listen method included in the speach recognition suddenly stopped working so I commented out the listen method and replaced it with the record method which records and analyzes every few seconds.

# References 
## Face Recognition
https://www.youtube.com/watch?v=535acCxjHCI


## Voice Recognition
https://www.youtube.com/watch?v=sHeJgKBaiAI&ab_channel=edureka%21