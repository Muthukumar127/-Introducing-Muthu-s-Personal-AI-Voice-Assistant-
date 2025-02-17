import speech_recognition as sr
import pyttsx3
import tkinter as tk
import webbrowser
import requests
import pyjokes
import pyautogui
import wikipedia
import cv2
import os
import threading
import datetime
import psutil
import pywhatkit
from tkinter import scrolledtext

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech and display it in the message box."""
    engine.say(text)
    engine.runAndWait()
    text_area.insert(tk.END, f"Assistant: {text}\n")
    text_area.yview(tk.END)

def listen():
    """Capture voice input, recognize it, and display it in the message box."""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        status_label.config(text="Listening...", fg="blue")
        window.update_idletasks()

        try:
            audio = recognizer.listen(source)
            status_label.config(text="Processing...", fg="green")
            command = recognizer.recognize_google(audio)
            text_area.insert(tk.END, f"You (Voice): {command}\n")
            text_area.yview(tk.END)
            process_command(command.lower())
        except sr.UnknownValueError:
            text_area.insert(tk.END, "Assistant: Sorry, I couldn't understand.\n")
        except sr.RequestError:
            text_area.insert(tk.END, "Assistant: Could not connect to the internet.\n")

        status_label.config(text="Ready", fg="black")

def open_camera():
    """Opens the computer camera using OpenCV."""
    speak("Opening camera.")
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  
            break
    cap.release()
    cv2.destroyAllWindows()

def check_weather():
    """Gets the current weather from OpenWeatherMap API."""
    api_key = "your_api_key"  # Get an API key from openweathermap.org
    city = "New York"  # Change this to your city
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url).json()
    if response["cod"] == 200:
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        speak(f"The current temperature in {city} is {temp}°C with {desc}.")
    else:
        speak("Sorry, I couldn't fetch the weather details.")

def get_time():
    """Tells the current time."""
    now = datetime.datetime.now()
    speak(f"The time is {now.strftime('%I:%M %p')}.")

def get_date():
    """Tells the current date."""
    now = datetime.datetime.now()
    speak(f"Today's date is {now.strftime('%A, %B %d, %Y')}.")

def take_screenshot():
    """Takes a screenshot and saves it."""
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    speak("Screenshot taken and saved as screenshot.png.")

def check_battery():
    """Checks the battery percentage."""
    battery = psutil.sensors_battery()
    percent = battery.percent
    speak(f"The battery is at {percent}%.")

def play_music():
    """Plays music from a predefined folder."""
    music_dir = "C:/Users/Public/Music"
    songs = os.listdir(music_dir)
    if songs:
        os.startfile(os.path.join(music_dir, songs[0]))
        speak("Playing music.")
    else:
        speak("No music found in the folder.")

def send_whatsapp():
    """Sends a WhatsApp message."""
    speak("Who do you want to message?")
    recipient = input("Enter phone number (with country code): ")
    speak("What message should I send?")
    message = input("Enter message: ")
    pywhatkit.sendwhatmsg_instantly(recipient, message)
    speak("Message sent.")

def process_command(command):
    """Process user commands and respond accordingly."""
    if "hello" in command:
        speak("Hello! How can I assist you?")
    elif "your name" in command:
        speak("I am  AI  Voice assistant Created  By  Muthu!")
    elif "open google" in command:
        speak("Opening Google...")
        webbrowser.open("https://www.google.com")
    elif "search google" in command:
        speak("What should I search for?")
        search_google()
    elif "search wikipedia" in command:
        speak("What should I search on Wikipedia?")
        search_wikipedia()
    elif "tell me a joke" in command:
        joke = pyjokes.get_joke()
        speak(joke)
    elif "increase volume" in command:
        pyautogui.press("volumeup")
    elif "decrease volume" in command:
        pyautogui.press("volumedown")
    elif "open camera" in command:
        open_camera()
    elif "play music" in command:
        play_music()
    elif "shutdown computer" in command:
        os.system("shutdown /s /t 5")
    elif "restart computer" in command:
        os.system("shutdown /r /t 5")
    elif "take screenshot" in command:
        take_screenshot()
    elif "battery status" in command:
        check_battery()
    elif "what time is it" in command:
        get_time()
    elif "what is today's date" in command:
        get_date()
    elif "check weather" in command:
        check_weather()
    elif "send whatsapp" in command:
        send_whatsapp()
    elif "exit" in command:
        speak("Goodbye!")
        window.quit()
    else:
        speak("I'm not sure how to respond to that.")

def start_listening():
    thread = threading.Thread(target=listen)
    thread.start()

def manual_input():
    """Reads text from the input box, displays it, and processes it."""
    command = text_entry.get()
    if command:
        text_area.insert(tk.END, f"You (Text): {command}\n")
        text_area.yview(tk.END)
        text_entry.delete(0, tk.END)
        process_command(command.lower())

window = tk.Tk()
window.title(" MUTHU AI Voice Assistant")
window.geometry("400x600")

status_label = tk.Label(window, text="Ready", font=("Arial", 12))
status_label.pack(pady=10)

text_area = scrolledtext.ScrolledText(window, width=40, height=15, font=("Arial", 12))
text_area.pack(padx=10, pady=5)

listen_button = tk.Button(window, text="🎤 Start Listening", font=("Arial", 12), command=start_listening)
listen_button.pack(pady=5)

text_entry = tk.Entry(window, font=("Arial", 12), width=30)
text_entry.pack(pady=5)

submit_button = tk.Button(window, text="📩 Submit Text", font=("Arial", 12), command=manual_input)
submit_button.pack(pady=5)

exit_button = tk.Button(window, text="❌ Exit", font=("Arial", 12), command=window.quit)
exit_button.pack(pady=10)

window.mainloop()
