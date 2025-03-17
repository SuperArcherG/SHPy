import speech_recognition as sr
import pvporcupine
import pyaudio
from os import environ, getcwd as cwd
import numpy as np
from pvrecorder import PvRecorder
from speech_recognition.recognizers import google
from playsound import playsound

def get_next_audio_frame():
    pass

def listen_for_wake_word():
    # Define the wake word path for Porcupine (you need to download a wake word file)
    access_key = "o/GliliMDU/766tPtE+kTcWULcAl7RSPDYF2TSYibYbhf6NrGPvlaw=="

    # WAKE_WORD = cwd() + "/Assets/computer_en_windows_v3_0_0.ppn"

    handle = pvporcupine.create(access_key=access_key, keywords=['computer'])

    # Initialize microphone stream
    # audio = pyaudio.PyAudio()
    # stream = audio.open(format=pyaudio.paInt16, channels=1, rate=handle.sample_rate, input=True, frames_per_buffer=256)
    stream = PvRecorder(
        frame_length=handle.frame_length,
        device_index=0)
    stream.start()

    print("Listening for the wake word...")

    while True:
        # Read audio data from microphone
        audio_data = stream.read()
        # audio_array = np.frombuffer(audio_data, dtype=np.int16)
        # print(np.sqrt(np.mean(audio_array**2)))
        # Check for wake word detection
        if handle.process(audio_data) >= 0:
            print("Wake word detected! Listening for speech...")
            recognize_speech()

def recognize_speech():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Use the microphone as the source for input
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)  # Optional: adjust for background noise
        print("Say something!")
        playsound('Assets/WAKE.wav')

        # Listen to the input
        audio = recognizer.listen(source)

    try:
        # Recognize speech using Google Web API
        playsound("Assets/END.wav")
        print("You said: " + recognizer.recognize_google(audio))
        

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    listen_for_wake_word()
