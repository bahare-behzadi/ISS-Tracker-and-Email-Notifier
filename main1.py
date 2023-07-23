import requests
import datetime as dt
import smtplib
import time
from tkinter import *


# -------------is iss on my position-----------


def is_iss_above():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    print(response)
    data = response.json()
    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])
    if float(MY_LATITUDE) - 5 <= iss_latitude <= float(MY_LATITUDE) + 5 \
            and float(MY_LONGITUDE) - 5 <= iss_longitude <= float(MY_LONGITUDE) + 5:
        return True


# -----------------finding if it is night or day in my position------------------------

def is_night():
    parameters = {
        "lat": MY_LATITUDE,
        "lng": MY_LONGITUDE,
        "formatted": 0
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    print(data)
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = dt.datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True


def check():
    window.destroy()
    while True:
        time.sleep(60)
        if is_night() and is_iss_above():
            connection = smtplib.SMTP("smtp.gmail.com")
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=EMAIL,
                                to_addrs=EMAIL,
                                msg="subject:ISS!!!\n\nlook up iss is above")


# ----------------making UI--------------


window = Tk()
window.title("info")
window.config(padx=50, pady=50)

canvas = Canvas(width=300, height=414)
background_img = PhotoImage(file="background.png")
canvas.create_image(150, 207, image=background_img)
canvas.create_text(100, 80, text="Insert your latitude:", font=("Arial", 14, "bold"), fill="white")
canvas.grid(row=0, column=0)
latitude_entry = Entry(canvas)
canvas.create_window(150, 120, window=latitude_entry, height=30, width=200)
canvas.create_text(110, 160, text="Insert your longitude:", font=("Arial", 14, "bold"), fill="white")
longitude_entry = Entry(canvas)
canvas.create_window(150, 200, window=longitude_entry, height=30, width=200)
canvas.create_text(100, 230, text="Insert your email:", font=("Arial", 14, "bold"), fill="white")
email_entry = Entry(canvas)
canvas.create_window(150, 270, window=email_entry, height=30, width=200)
canvas.create_text(145, 300, text="Insert app password of your email:", font=("Arial", 12, "bold"), fill="white")
pass_entry = Entry(canvas)
canvas.create_window(150, 330, window=pass_entry, height=30, width=200)
latitude_entry.focus()
MY_LATITUDE = latitude_entry.get()
MY_LONGITUDE = longitude_entry.get()
EMAIL = email_entry.get()
PASSWORD = pass_entry.get()
save_img = PhotoImage(file="right.png")
save_button = Button(image=save_img, highlightthickness=0, command=check)
save_button.grid(row=2, column=0)
window.mainloop()
