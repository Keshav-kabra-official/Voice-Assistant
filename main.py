'''
 @author : Keshav Kabra
'''

import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import pickle
from threading import Timer

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 130)

# giving google-chrome-path, to open websites in Google-Chrome
chrome_path = 'chrome_path_here'

user_name = ""


# speak function
def speak(string):
    try:
        engine.say(string)
        engine.runAndWait()
    except:
        print("SORRY, SOME UNEXPECTED ERROR OCCURRED... RESTART ASSISTANT...")
        exit()


# taking name from the user
def name():
    global user_name
    speak("Hello user ...")
    speak("Can you oblige me to know your name... just that I can address you with"
          " your nice name...")
    user_name = input("Please enter your name :")
    with open("file_name_here", "r") as f:
        user_already = f.read()
    with open("file_name_here", "a") as f:
        if (user_name not in user_already) and user_name != ' ' and user_name != '\n':
            f.write(user_name + "\n")


# greet at starting
def greet():
    speak(f"OK, Welcome {user_name}")
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning")
    elif 12 <= hour <= 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")

    speak("How can I help you ?")


# listening to the user
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening ...")
        r.pause_threshold = 1  # use energy_threshold to recognize specific pitch sounds
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        print("Recognizing ...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said : {query}\n")
    except:
        print("Can't recognize ... Please repeat ...")
        return "None"
    return query


# asking user to clear screen after each output
def console_cls_ask():
    print("\nWould you like to clear the screen after each output, this may give you clarity "
          "and better looking screen, but if you want the result to stay on screen - this "
          "should be off ...")
    speak("One last question, Would you like to clear the screen after each output ?")
    choice = input("(y) for Yes : ")
    if choice == 'y' or choice == 'Y':
        return True
    else:
        return False


# e-mail function
def send_email(to, content, sub):
    speak("Do you want to send this e-mail ?")
    send = input("Do you want to send this e-mail - (y) for Yes")
    if send == 'y' or send == 'Y':
        content = 'Subject:{}\n\n{}'.format(sub, content)  # separating sub and body of email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        with open('file_name_here', 'rb') as f:
            x = pickle.load(f)
        server.login('abc@example.com---your_email_ID_here', x)
        server.sendmail('your_password_here', to, content)
        server.close()
        print("E-mail has been sent successfully !!!")
        speak("E-mail has been sent successfully !!!")


# alarm/reminder function
def alarm():
    print("\n --- REMINDER REMINDER REMINDER ---\n")
    os.startfile('your_play_music_path')


# main function
if __name__ == '__main__':
    name()
    cls_choice = console_cls_ask()
    greet()

    while True:
        print("\nTry these : ")
        print("1)xyz Wikipedia 2)Open YouTube 3)Open Google 4)Open Quora 5)Open Cricbuzz "
              "6)Play music 7)Open Sublime Text 8)Open dev c++ 9)the time? "
              "10)Set reminder 11)Send email 12)Quit\n")
        query = take_command().lower()

        # task performing
        if 'wikipedia' in query:
            try:
                speak("Searching on wikipedia ...")
                query = query.replace("wikipedia", "")
                result = wikipedia.summary(query, sentences=3)
                speak("According to wikipedia ...")
                print(result)
                speak(result)
            except:
                speak("Sorry, there occurred some error while searching on wikipedia")

        elif 'open youtube' in query:
            speak("Opening Youtube")
            print("Opening Youtube ...")
            # webbrowser.open("youtube.com") # Open website in Internet Explorer
            webbrowser.get(chrome_path).open("youtube.com", new=2)

        elif 'open google' in query:
            speak("Opening Google")
            print("Opening Google ...")
            webbrowser.get(chrome_path).open("google.com", new=2)
            # webbrowser.open("google.com")

        elif 'open quora' in query:
            speak("Opening quora")
            print("Opening quora ...")
            webbrowser.get(chrome_path). open("your_Quora_profile_link_here", new=2)

        elif 'open cricbuzz' in query:
            speak("Opening cricbuzz")
            print("Opening cricbuzz ...")
            webbrowser.get(chrome_path). open("https://www.cricbuzz.com", new=2)

        elif 'play music' in query:
            import random
            music_dir = "music_directory_path"
            songs = os.listdir(music_dir)
            speak("Playing music ...")
            print("Songs available : ", songs)
            rn = random.randint(0, 53)
            os.startfile(os.path.join(music_dir, songs[rn]))

        elif 'open sublime text' in query:
            speak("Opening Sublime text editor")
            sublime_path = "path_here"
            os.startfile(sublime_path)

        elif 'dev c plus plus' in query:
            speak("Opening dev c ++")
            dev_path = "path_here"
            os.startfile(dev_path)

        elif 'the time' in query:
            time = datetime.datetime.now().strftime("%I:%M %p")
            date = datetime.datetime.now().strftime("%d %B, %Y")
            print(f"Time : {time}\t Date : {date}\n")
            speak(f"It's {time} And today is {date}")

        elif 'set reminder' in query:
            try:
                speak("Setting reminder for today")
                speak("Enter the following values in 24 H format :")
                hr = int(input("Enter hour : "))
                if hr > 24:
                    raise Exception
                if hr == 24:
                    hr = 0

                minut = int(input("Enter minutes : "))
                if minut == 60:
                    minut = 0
                    hr += 1
                if minut > 60:
                    raise Exception

                x = datetime.datetime.today()
                if x.hour >= hr:
                    if x.minute >= minut:
                        speak("Sorry, this moment has been past")
                        continue

                y = x.replace(day=x.day+1, hour=hr, minute=minut, second=0, microsecond=0)
                delta_t = y-x
                secs = delta_t.seconds + 1
                t = Timer(secs, alarm)
                t.start()
                speak("Reminder has been set for the given time successfully ...")
                speak("You will be notified by a BEAT DJ sound ...")
                print("You will be notified by a BEAT DJ sound ...")

            except Exception:
                speak("Sorry, this was not a valid query")

        elif 'send email' in query:
            try:
                with open('your_email_file', 'rb') as f:
                    dictn = pickle.load(f)

                speak("Please enter name of person you want to send email to")
                name = input("Enter receiver name : ")

                if name in dictn.keys():
                    print("\nSending email to :" + dictn[name])

                if name not in dictn.keys():
                    print(f"   {name} was not registered ...")
                    eml = input(f"   Please enter e-mail of {name} : ")
                    dictn.update({f"{name}": f"{eml}"})

                    with open('file_name_here', 'wb') as f:
                        pickle.dump(dictn, f)

                speak("What should I say ?")
                print("\nSpeak content of e-mail : \n")
                content = take_command()
                speak("What is the Subject of e-mail ?")
                print("Speak Subject of e-mail : ")
                sub = take_command()
                to = dictn[name]
                send_email(to, content, sub)

            except:
                speak("Sorry, there occurred some error while sending email")
                print("Sorry, there occurred some error while sending email")

        elif 'how are you' in query:
            print("I am great ! What can I do for you ?")
            speak("I am great ! What can I do for you ?")

        elif 'about me' in query:
            print("I think you're smart, funny, kind and cool. I'm lucky to be your assistant ...")
            speak("I think you're smart, funny, kind and cool. I'm lucky to be your assistant ...")

        elif 'shutdown my computer' in query:
            speak("It is not recommended to shut down your PC in this way... "
                  "You should do it manually... To continue, enter following : ")
            check = input("Do you really want to shut-down your PC ? (y) for Yes : ")
            try:
                if check == 'y' or check == 'Y':
                    tm = int(input("Enter time (in secs) after which you want to shut-down PC : "))
                    final = input("Not a recommended step... Press 'y' one-more time to shut-down...")
                    if final == 'y' or final == 'Y':
                        os.system(f"shutdown /s /t {tm}")
                        exit()
            except:
                print("Not a valid input ...")
                speak("Sorry, that was not a valid input ...")

        elif 'restart my computer' in query:
            speak("It is not recommended to restart your PC in this way... "
                  "You should do it manually... To continue, enter following : ")
            check = input("Do you really want to restart your PC ? (y) for Yes : ")
            try:
                if check == 'y' or check == 'Y':
                    tm = int(input("Enter time (in secs) after which you want to restart PC : "))
                    final = input("Not a recommended step... Press 'y' one-more time to restart...")
                    if final == 'y' or final == 'Y':
                        os.system(f"shutdown /r /t {tm}")
                        exit()
            except:
                print("Not a valid input ...")
                speak("Sorry, that was not a valid input ...")

        elif 'quit' in query:
            speak("This was Assistant, signing off ...")
            print("\t ******* Designed by - KESHAV KABRA *******\n")
            speak("press any key and Enter to exit ...")
            x = input()
            exit()

        if cls_choice:
            _ = os.system("cls")
