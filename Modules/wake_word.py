import speech_recognition as sr
import time

def listen_for_wake_word():

    recognizer = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:

                print("Listening for Hey Neuro...")

                recognizer.adjust_for_ambient_noise(source, duration=0.5)

                audio = recognizer.listen(
                    source,
                    phrase_time_limit=3
                )

            text = recognizer.recognize_google(audio).lower()

            print("Heard:", text)

            if "hey neuro" in text or "hi neuro" in text or "neuro" in text:
                return True

        except:
            pass

        time.sleep(1)