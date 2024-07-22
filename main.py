#Credit for this code to @UnknownEngineer (Mansoor Ahmed)





import speech_recognition as sr
import pyttsx3
import pyautogui
import webbrowser
import time
import os
import subprocess  # For executing PowerShell commands

# Initialize the recognizer and the text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Get all available voices and set properties for the TTS engine
voices = tts_engine.getProperty('voices')

for voice in voices:
    tts_engine.setProperty('voice', voice.id)  # Set the voice for the TTS engine

tts_engine.setProperty('rate', 150)  # Set the speaking rate
tts_engine.setProperty('volume', 1)  # Set the volume level

# Function to make the AI speak the given text
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to listen to user commands
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Listen to the audio

        try:
            command = recognizer.recognize_google(audio)  # Use Google's speech recognition
            print(f"You said: {command}")
            return command.lower()  # Return the command in lowercase
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return ""

# Function to open a browser and search for a query
def open_browser(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

# Function to open a specific website
def open_website(url):
    webbrowser.open(url)

# Function to execute tasks based on the user's command
def execute_task(command):
    if "open browser and search for" in command:
        search_query = command.split("open browser and search for")[-1].strip()
        open_browser(search_query)
        speak(f"Searching for {search_query} in browser.")

    elif "open website" in command:
        website_url = command.split("open website")[-1].strip()
        if not website_url.startswith('http'):
            website_url = 'http://' + website_url
        open_website(website_url)
        speak(f"Opening website {website_url}.")

    elif "activate extension" in command:
        extension_name = command.split("activate extension")[-1].strip()
        pyautogui.hotkey('ctrl', 'shift', 'x')  # Open VS Code extensions
        time.sleep(1)
        pyautogui.write(extension_name)  # Type the extension name
        pyautogui.press('enter')  # Press Enter to activate the extension
        speak(f"Activated extension {extension_name}.")

    elif "unlock my pc" in command:
        pyautogui.typewrite('your_password')  # Type the password
        pyautogui.press('enter')  # Press Enter to unlock
        speak("Your PC is unlocked.")

    elif "open application" in command:
        app_name = command.split("open application")[-1].strip()
        pyautogui.hotkey('win', 's')  # Open the Windows search bar
        time.sleep(1)
        pyautogui.write(app_name)  # Type the application name
        time.sleep(1)
        pyautogui.press('enter')  # Press Enter to open the application
        speak(f"Opening application {app_name}.")

    elif "close application" in command:
        app_name = command.split("close application")[-1].strip()
        if app_name.endswith(".exe"):
            os.system(f'taskkill /im {app_name} /f')  # Close the application
            speak(f"Closing application {app_name}.")
        else:
            speak("This is a UWP app. Closing through PowerShell.")
            subprocess.run(["powershell", f"Get-AppxPackage -Name {app_name} | Remove-AppxPackage"])

    elif "shutdown" in command:
        speak("Shutting down the system.")
        os.system('shutdown /s /t 1')  # Shutdown the system

    elif "restart" in command:
        speak("Restarting the system.")
        os.system('shutdown /r /t 1')  # Restart the system

    elif "log off" in command:
        speak("Logging off the system.")
        os.system('shutdown /l')  # Log off the system

    elif "exit" in command or "close ai" in command:
        speak("Allah Hafiz! May Allah give you success. Take care!")
        exit()  # Exit the program

    else:
        speak("Sorry, I'm not sure how to help with that.")

# Main function to start the AI assistant
def main():
    speak("Hello UnknownEngineer, I am your AI assistant. Kindly tell me what I can do for you.")
    while True:
        command = listen()  # Listen for user commands
        execute_task(command)  # Execute the command

if __name__ == "__main__":
    main()
