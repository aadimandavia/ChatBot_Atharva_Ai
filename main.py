import os
import datetime
import webbrowser
import speech_recognition as sr
import win32com.client
import google.generativeai as genai
from config import api

# Initialize speaker
speaker = win32com.client.Dispatch("SAPI.SpVoice")
voices = speaker.GetVoices()
for voice in voices:
    if "Microsoft Ravi - English (India)" in voice.GetDescription():
        speaker.Voice = voice
        break

speaker.Rate = 1

def say(text):
    speaker.speak(text)

# Configure Gemini AI
API_KEY = api
genai.configure(api_key=API_KEY)

chat_history = ""  # Stores the conversation history
model = genai.GenerativeModel("gemini-1.5-flash")

def chat(query):
    global chat_history
    chat_history += f"Aadi: {query}\nAtharva: "
    response = model.generate_content(f"This is an ongoing conversation:\n{chat_history}\nAnswer concisely: {query}")
    short_response = response.text.split(".")[:2]  # Keep response brief
    short_response = ". ".join(short_response).strip()
    say(short_response)
    chat_history += short_response + "\n"
    print(chat_history)
    return short_response

def ai(query):
    text = f"Gemini response for prompt: {query}\n**************************\n"
    response = model.generate_content(query)
    text += response.text
    os.makedirs("gemani", exist_ok=True)
    file_name = "_".join(query.split()) + ".txt"
    with open(os.path.join("gemani", file_name), 'w', encoding='utf-8') as f:
        f.write(text)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        print("Listening...")
        try:
            audio = r.listen(source)
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query.lower()
        except Exception:
            return "unable to understand"

if __name__ == '__main__':
    say("Hello! I'm Atharv A I")
    sites = {"youtube": "https://youtube.com", "google": "https://google.com"}
    while True:
        query = takeCommand()
        if "open" in query:
            for site, url in sites.items():
                if site in query:
                    say(f"Opening {site} Bhaiya...")
                    webbrowser.open(url)
                    break
        elif ("good bye".lower() or "goodbye".lower()) in query.lower():
            say("Bye Bhaiya")
            exit()
        elif "play music".lower() in query.lower():
            os.startfile("Tenu Sang Rakhna (PenduJatt.Com.Se).mp3")
        elif "the time".lower() in query.lower():
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Bhaiya, the time is {strfTime}")
        elif "using artificial intelligence".lower() in query.lower():
            ai(query)
        elif "reset chat".lower() in query.lower():
            say("Chat reset")
            chat_history = ""
        else:
            print("Chatting....")
            chat(query)
