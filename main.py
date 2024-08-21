import pyttsx3
import datetime
import time
import speech_recognition as sr


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[len(voices) - 1].id)


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def takecommand():
    r  = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening.................")
        r.pause_threshold = 1
        audio = r.listen(source, timeout= 5 , phrase_time_limit=8)

    try:
        print("Recognizing..................")
        command = r.recognize_google(audio, language='en-in')
        print(f"you said: {command}")

    except Exception:
        speak("Say that again please")
        return "none"
    return command

def wish():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M %p")

    if hour >=0 and hour < 12:
        speak("Good morning")
    elif hour >= 12 and hour <=15:
        speak("good afternoon")
    else:
        speak("good evening")
    speak("I am MARK , please tell me how may i help you")

if __name__ == "__main__":
    wish()

while True:
    command = takecommand().lower()

    if "mark" in command:
        print(command)
        wish()