import random
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser
import os
import smtplib
# import sys


class Voice:

    def __init__(self):
        self.listener = sr.Recognizer()
        engine = pyttsx3.init()
        self.engine = engine
        self.voices = engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[0].id)

    def talk(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def wishMe(self):
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour <= 12:
            self.talk('Good Morning!')
        elif hour >= 12 and hour <= 18:
            self.talk("Good Afternoon!")
        elif hour >= 18 and hour <= 21:
            self.talk('Good Evening!')
        else:
            self.talk('Good Night')

        self.talk(
            'Hii sir This is jarvis devloped by chief suraj and Lukky Kanhaiya. How can I help You...')

    def take_commond(self):
        try:
            with sr.Microphone() as source:
                self.talk("Please wait for a second")

                self.listener.adjust_for_ambient_noise(source, duration=5)
                self.talk("Ready to go")

                # self.listener.pause_threshold = 1
                # self.listener.dynamic_energy_threshold = 2
                voice = self.listener.listen(source)
                command = self.listener.recognize_google(
                    voice, language='en-in')
                command = command.lower()

                if 'alexa' in command:
                    command = command.replace('alexa', '')
                    print(command)

        except Exception as e:
            # print(e)
            self.talk('say due to noice i cannot able to understand...')
            # pass
        return command

    def run_alexa(self):
        command = self.take_commond()
        print(command)
        if 'song' in command:
            # music=command.replace('song','')
            self.talk(command)
            pywhatkit.playonyt(command)
        elif 'music' in command:
            music_dir = 'play.mp3'
            songs = os.listdir(music_dir)
            # PlaySound('D:\phython\play.mp3')
            x = len(songs)
            print(x)
            m = random.randint(0, x)
            print(m)
            print(songs[m])
            os.startfile(os.path.join(music_dir, songs[m]))
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            print(time)
            self.talk('current time is'+time)
        elif 'open code' in command:
            codepath = 'C:\\Users\\hp\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'
            os.startfile(codepath)
        elif 'email' in command:
            try:
                self.talk("What should I say?")
                content = self.take_commond()
                to = 'jmdkrishnt@gmail.com'
                self.sendEmail(to, content)
                self.talk('Email has been sent!')
            except Exception as e:
                print(e)
                self.talk('Sorry my friend . I am not able to send this email.')
        elif 'who is' in command:
            info = wikipedia.summary(command, 1)
            self.talk('According to wikipedia')
            print(info)
            self.talk(info)
        elif 'youtube' in command:
            webbrowser.open("youtube.com")
        elif 'learn code' in command:
            webbrowser.open('www.youtube.com/channel/UChAml0bpsmTFViiBmSLJ9sg')
        elif 'google' in command:
            webbrowser.open('google.com')
        elif 'stack overflow' in command:
            webbrowser.open("stackoverflow.com")
        elif 'quora' in command:
            webbrowser.open("quora.com")
        elif 'single' in command:
            self.talk('I am in relationship with wifi')
        elif 'date' in command:
            self.talk('Sorry, I have a headache')
        elif 'joke' in command:
            self.talk(pyjokes.get_joke())
        elif 'jokes' in command:
            self.talk(pyjokes.get_jokes())
        elif 'stop' in command:
            exit()
        else:
            self.talk('plself.ease Repeate the command')

    def sendEmail(to, content):
        # f = open('C:\\Users\\hp\\Desktop\\DESKTOP\\PYTHON\\Python COdE\\pass.txt')
        # t=f.read(9)
        with open('pass.txt') as f:
            t = f.readlines()
        # print(t)
        p = ''
        for l in t:
            p += l
        # print(p)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('ntrsharma0@gmail.com', p)
        server.sendmail('ntrsharma0@gmail.com', to, content)
        server.close()

    # # if _name=='main_':
    # wishMe()
    # while True:
    #     run_alexa()

    #  elif 'song' in self.query:
    #                 speak(self.query)
    #                 pywhatkit.playonyt(self.query)
    #             elif 'music' in self.query:
    #                 music_dir = 'play.mp3'
    #                 songs = os.listdir(music_dir)
    #             # PlaySound('D:\phython\play.mp3')
    #                 x = len(songs)
    #                 print(x)
    #                 m = random.randint(0, x)
    #                 print(m)
    #                 print(songs[m])
    #                 os.startfile(os.path.join(music_dir, songs[m]))

    #             elif 'time' in self.query:
    #                 time = datetime.datetime.now().strftime('%I:%M %p')
    #                 print(time)
    #                 speak('current time is'+time)
    #             elif 'open code' in self.query:
    #                 codepath = 'C:\\Users\\hp\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'
    #                 os.startfile(codepath)
    #             elif 'email' in command:
    #             try:
    #                 speak("What should I say?")
    #                 content = take_commond()
    #                 to = 'jmdkrishnt@gmail.com'
    #                 sendEmail(to, content)
    #                 talk('Email has been sent!')
    #             except Exception as e:
    #                 print(e)
    #                 talk('Sorry my friend . I am not able to send this email.')
