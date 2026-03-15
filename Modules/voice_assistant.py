import speech_recognition as sr
import pyttsx3
import sounddevice as sd
import soundfile as sf
import numpy as np
from Modules.ai_brain import ask_ai
from Modules import Automation

engine = pyttsx3.init()

# ------------------------
# Speak Function
# ------------------------
def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


# ------------------------
# Listen Function (sounddevice version)
# ------------------------
def listen():
    samplerate = 16000
    duration = 5

    print("Listening...")

    recording = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="int16"
    )
    sd.wait()

    sf.write("temp.wav", recording, samplerate)

    r = sr.Recognizer()

    try:
        with sr.AudioFile("temp.wav") as source:
            audio = r.record(source)

        command = r.recognize_google(audio)
        print("You said:", command)
        return command.lower()

    except:
        speak("Sorry I did not understand")
        return ""


# ------------------------
# Command Handler
# ------------------------
def process_command(command):

    if "open chrome" in command:
        speak("Opening Chrome sir")
        Automation.open_chrome()

    elif "open notepad" in command:
        speak("Opening Notepad sir")
        Automation.open_notepad()

    elif "open calculator" in command:
        speak("Opening Calculator sir")
        Automation.open_calculator()

    elif "go to desktop" in command:
        speak("Showing desktop sir")
        Automation.show_desktop()

    elif "switch window" in command:
        speak("Switching window sir")
        Automation.switch_window()

    elif "close window" in command:
        speak("Closing the window sir")
        Automation.close_window()

    elif "take screenshot" in command:
        speak("Taking screenshot sir")
        file = Automation.take_screenshot()
        speak("Screenshot saved sir")

    elif "open documents" in command:
        speak("Opening documents folder sir")
        Automation.open_folder("documents")

    elif "open downloads" in command:
        speak("Opening downloads folder sir")
        Automation.open_folder("downloads")

    elif "open project folder" in command:
        found = Automation.search_folder("project")

        if found:
            speak("Opening folder sir")
        else:
            speak("Folder not found sir")

    elif "exit" in command:
        speak("Goodbye Piyush sir")
        return False

    else:
        speak("Let me think sir")
        answer = ask_ai(command)
        speak(answer)

    return True


# ------------------------
# Main Loop
# ------------------------
def run_assistant():

    speak("Hello Piyush sir, NeuroDesk AI is ready for your command.")

    running = True

    while running:
        command = listen()

        if command:
            running = process_command(command)


if __name__ == "__main__":
    run_assistant()
