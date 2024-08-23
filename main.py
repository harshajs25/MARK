import datetime
import pyttsx3
import time
import speech_recognition as sr
import openai
import google.generativeai as genai
import os


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[len(voices) - 1].id)


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=5, phrase_time_limit=8)

    try:
        print("Recognizing...")
        command = r.recognize_google(audio, language='en-IN')
        print(f"You said: {command}")
    except Exception:
        speak("Say that again please")
        return "none"
    return command.lower()


def wish():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M %p")

    if hour >= 0 and hour < 12:
        speak("Good morning")
    elif hour >= 12 and hour <= 15:
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("I am MARK, how may I help you?")


def geminiapi(command):
    if command == "none":
        return
    genai.configure(api_key=os.environ["GEMINIAPI_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(command)
    result = response.text.strip()
    print(result)
    speak(result)


def openaiapi(command):
    if command == "none":
        return
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Updated model for free-tier access
            messages=[
                {"role": "user", "content": command}
            ]
        )
        result = response.choices[0].message['content'].strip()
        print(result)
        speak(result)
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        speak("There was an error with the OpenAI API.")



if __name__ == "__main__":
    wish()
    openaiapi(command="what is ai")

    while True:
        command = take_command()

        if "mark" in command:
            print(command)
            wish()

        if "google" in command:
            geminiapi(command)

        if "openai" in command or "open AI"in command:
            openaiapi(command)
