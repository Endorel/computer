import speech_recognition as sr
import pyttsx3

import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')

import openai
openai.api_key = OPENAI_KEY

def SpeakText(command):
    engine = pyttsx3.init()
    print("Engine started!")
    engine.say(command)
    engine.runAndWait()

r = sr.Recognizer()

def record_text():
    while(1):
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2)
                print("I'm listening")
                audio2 = r.listen(source2)
                print("Recognizing...")
                MyText = r.recognize_google(audio2)
                print(f"You said: {MyText}")
                return MyText
        
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("Unknown error occurred")

def send_to_GPT(messages, model="gpt-3.5-turbo"):
    print("Asking ChatGPT...")
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5
    )

    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    
    return message

messages = []
while(1):
    text = record_text()
    messages.append({"role": "user", "content": text})
    response = send_to_GPT(messages)
    print("Got a response")
    SpeakText(response)

    print(response)