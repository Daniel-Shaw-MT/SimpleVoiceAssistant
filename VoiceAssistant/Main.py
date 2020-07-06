from __future__ import print_function
import pickle
import os.path
import getpass
import os
import time
import datetime

import webbrowser

from google_auth_httplib2 import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from gtts import gTTS
import random
import playsound
import pygame
import speech_recognition as sr
import subprocess
cwd = os.getcwd()

new_volume = 1.00
wake = "alexa"
pygame.mixer.init()
pygame.mixer.music.set_volume(1.00)
mainvolume = 1

def speak(text):

    tts = gTTS(text=text)
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)


def musicfader(loopcount, upordown):
    i = 0
    if(upordown==True):
        while i < loopcount:
            print(pygame.mixer.music.get_volume())
            i+=1
            time.sleep(.010)
            pygame.mixer.music.set_volume(i/100)

    elif(upordown==False):
        i=pygame.mixer.music.get_volume()
        v = i*100
        state = True
        while state==True:

            if v <= loopcount:
                print(pygame.mixer.music.get_volume())
                i=i-1
                time.sleep(.010)
                pygame.mixer.music.set_volume(v/100)
            else:
                state = False


def web(url, state):
    speak("Opening browser on "+url)
    webbrowser.open(url, new=state)


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)

        except Exception as e:
            print("Could not understand.")

    return said


def note(text, notename):
    file_name = notename + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)
    subprocess.Popen(["notepad.exe", file_name])


print("Welcome to my voice assistant! Version 1.00 Made entirely by Daniel Shaw\nCurrent time:"+str(datetime.datetime.now()))
# Main listen loop
while True:
    print("Listening")
    text = listen().lower()
    if text.count(wake) > 0:
        playsound.playsound(cwd+'\\sleepsound.wav')
        text = listen().lower()
        WEB_PRSHS = ["open my web browser", "open the internet"]
        for phrase in WEB_PRSHS:
            if phrase in text:
                speak("where do you want to go?")
                link = listen()
                web(link,2)

        TIME_PRSHS = ["what time is it", "what's the time", "tell me the time"]
        for phrase in TIME_PRSHS:
            if phrase in text:
                date = datetime.datetime.now()
                speak("The time is " + str(date.strftime("%H:%M:%S")))

        TIMER_PHRASES = ["create a timer", "set a timer", "new timer"]
        for phrase in TIMER_PHRASES:
            if phrase in text:
                speak("How long do you want the timer to last? (In seconds)")
                lenght = listen()
                speak("Timer of"+lenght+" starting now!")
                time.sleep(int(lenght))
                playsound.playsound(cwd+"\\alarm.mp3")

        NOTE_STRS = ["make a note", "write this down", "remember this", "new note", "take a note"]
        for phrase in NOTE_STRS:
            if phrase in text:
                speak("What do you want me to call this note?")
                note_name = listen().lower()
                speak("What would you like me to write down?")
                note_text = listen().lower()
                note(note_text, note_name)
                speak("Noted!")





        SING_PHRSS = ["play some music", "music time", "can you sing", "play music", "play a song"]
        for phrase in SING_PHRSS:
            if phrase in text:
                RESPONSES = ["Coming right up!", "Music coming up!", "Playing some tunes!", "Putting on some beats!"]
                speak(random.choice(RESPONSES))


                fileex = [".mp3", ".wav", ".ogg"]
                user = getpass.getuser()
                choice = random.choice(os.listdir("C:\\Users\\"+user+"\\Music\\"))
                for phrase in fileex:
                    if phrase in choice:
                        speak("now playing "+choice)
                        print("Now playing: "+choice)
                        pygame.mixer.music.load("C:\\Users\\"+user+"\\Music\\"+choice)
                        musicfader(100, True)
                        pygame.mixer.music.play(0)
                        musicstate = True
                        while musicstate == True:
                            choiceplayorpause = listen().lower()
                            if "pause"  in choiceplayorpause:
                                musicfader(current_volume*100, False)
                                print("Paused: "+choice)
                                pygame.mixer.music.pause()

                            nextsongcall = ["next song", "next track", "new song", "play something else", "change song"]
                            for phrase in nextsongcall:
                                if phrase in choiceplayorpause:
                                    print("skipping to new song.")
                                    pygame.mixer.music.stop()
                                    try:
                                        choice = random.choice(os.listdir("C:\\Users\\" + user + "\\Music\\"))
                                        print("now playing: " + choice)
                                        pygame.mixer.music.load("C:\\Users\\" + user + "\\Music\\" + choice)
                                        speak("now playing " + choice)
                                    except:
                                        print("Couldn't play song")
                                    pygame.mixer.music.play(0)
                                    musicfader(new_volume*100, True)
                            if "change volume" in choiceplayorpause:
                                current_volume = pygame.mixer.music.get_volume()

                                musicfader(1/100, False)
                                speak("what would you like to change the volume to? (Current volume:"+str(current_volume*100)+"%)")
                                wanted_volume = listen().lower()
                                try:
                                    new_volume = int(wanted_volume)/100
                                    musicfader(100, False)
                                    speak("New volume is"+str(new_volume*100)+"%")
                                    musicfader(new_volume * 100, True)

                                except Exception as e1:
                                    print("Did not understand")

                            if "play" in choiceplayorpause:
                                print("Now playing: " + choice)
                                pygame.mixer.music.unpause()
                                musicfader(new_volume * 100, True)

                            if "un pause" in choiceplayorpause:
                                print("Now playing: " + choice)
                                pygame.mixer.music.unpause()
                                musicfader(new_volume * 100, True)

                            if "stop" in choiceplayorpause:
                                musicfader(100, False)
                                speak("Stopping all songs")
                                print("Stopping all songs.")
                                musicstate = False

                                pygame.mixer.music.stop()

                            if "secret" in choiceplayorpause:
                                pygame.mixer.music.stop()
                                print("You found a secret!")
                                speak("prepare to die")
                                pygame.mixer.music.load(cwd + "\\Adyan Sings The Box.mp3")
                                pygame.mixer.music.play(0)



    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']



