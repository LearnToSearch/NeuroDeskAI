import speech_recognition as sr
import pyttsx3
import sounddevice as sd
import soundfile as sf
import numpy as np
from Modules.ai_brain import ask_ai
from Modules import Automation
import time

current_app = None

import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 170)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

is_speaking = False


# ------------------------
# Speak Function (FINAL)
# ------------------------
from gtts import gTTS
from pydub import AudioSegment
import winsound
import os
import uuid

def speak(text):
    print("Assistant:", text)

    try:
        mp3_file = f"voice_{uuid.uuid4().hex}.mp3"
        wav_file = f"voice_{uuid.uuid4().hex}.wav"

        # Generate MP3
        tts = gTTS(text=text, lang='en')
        tts.save(mp3_file)

        # Convert MP3 → WAV
        sound = AudioSegment.from_mp3(mp3_file)
        sound.export(wav_file, format="wav")

        # Play WAV silently (no popup)
        winsound.PlaySound(wav_file, winsound.SND_FILENAME)

        # Cleanup
        os.remove(mp3_file)
        os.remove(wav_file)

    except Exception as e:
        print("Voice Error:", e)
# ------------------------
# Listen Function (sounddevice version)
# ------------------------
import sounddevice as sd
import speech_recognition as sr
import numpy as np

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

    # 🔥 Convert numpy array to bytes (NO FILE)
    audio_bytes = recording.tobytes()

    r = sr.Recognizer()

    try:
        audio = sr.AudioData(audio_bytes, samplerate, 2)

        command = r.recognize_google(audio)
        print("You said:", command)

        return command.lower()

    except:
        return ""

# ------------------------
# Command Handler
# ------------------------
import time

def process_command(command):

    global current_app

    if "open chrome" in command:
        speak("Opening Chrome sir")
        time.sleep(1)
        Automation.open_chrome()
        current_app = "chrome"

    elif "open notepad" in command:
        speak("Opening Notepad sir")
        time.sleep(1)
        Automation.open_notepad()
        current_app = "notepad"

    elif "open calculator" in command:
        speak("Opening Calculator sir")
        time.sleep(1)
        Automation.open_calculator()
        current_app = "calculator"

    elif "go to desktop" in command:
        speak("Showing desktop sir")
        time.sleep(0.5)
        Automation.show_desktop()

    elif "switch window" in command:
        speak("Switching window sir")
        time.sleep(0.5)
        Automation.switch_window()

    elif "close window" in command:
        speak("Closing the window sir")
        time.sleep(0.5)
        Automation.close_window()

    elif "take screenshot" in command:
        speak("Taking screenshot sir")
        time.sleep(1)
        file = Automation.take_screenshot()
        speak("Screenshot saved sir")

    elif "open documents" in command:
        speak("Opening documents folder sir")
        time.sleep(1)
        Automation.open_folder("documents")
        current_app = "document"

    elif "open downloads" in command:
        speak("Opening downloads folder sir")
        time.sleep(1)
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

    # -------------------
    # CONTEXT CONTROL
    # -------------------

    elif current_app == "notepad":
        
        if "write" in command:
            text = command.replace("write", "").strip()   # 🔥 FIXED
            speak("Writing in notepad sir")
            time.sleep(0.5)
            Automation.type_text(text)

        elif "new line" in command:
            Automation.press_enter()

        elif "save file" in command:
            speak("Saving file sir")
            time.sleep(0.5)
            Automation.hotkey("ctrl", "s")

    elif current_app == "chrome":

        if "search" in command:
            query = command.replace("search", "").strip()
            speak("Searching on Google sir")
            time.sleep(1)
            Automation.type_text(query)
            Automation.press_enter()

        elif "scroll down" in command:
            Automation.scroll_down()

        elif "scroll up" in command:
            Automation.scroll_up()

    # -------------------

    else:
        speak("Let me think sir")
        answer = ask_ai(command)
        speak(answer[:200])   # 🔥 limit long answers

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

        time.sleep(0.3)
if __name__ == "__main__":
    run_assistant()
