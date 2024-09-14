from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

root = Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False, False)

def fetch_weather(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error if the response is not successful
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def getWeather():
    city = textfiled.get()
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(city)

    if location:
        lat = location.latitude
        lon = location.longitude
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=lon, lat=lat)

        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        name.config(text="CURRENT WEATHER")

        # Fetch the weather data using the OpenWeatherMap API
        api_key = "your_api_key"  # Replace with your actual API key
        weather_data = fetch_weather(lat, lon, api_key)

        if weather_data:
            # Extract relevant weather information
            temperature = weather_data['main']['temp']
            description = weather_data['weather'][0]['description']
            wind_speed = weather_data['wind']['speed']
            humidity = weather_data['main']['humidity']
            pressure = weather_data['main']['pressure']
            
            # Update labels with weather data
            t.config(text=f"{temperature}°C")
            c.config(text=description.capitalize())
            w.config(text=f"{wind_speed} m/s")
            h.config(text=f"{humidity}%")
            d.config(text=description.capitalize())
            p.config(text=f"{pressure} hPa")
        else:
            messagebox.showerror("Error", "Could not retrieve weather data!")
    else:
        messagebox.showerror("Error", "City not found!")

# Search Box
search_image = PhotoImage(file="search.png")
myimage = Label(image=search_image)
myimage.place(x=20, y=20)

textfiled = tk.Entry(root, justify="center", width=17, font=("poppins", 25, "bold"), bg="#404040", border=0, fg="white")
textfiled.place(x=50, y=40)
textfiled.focus()

search_icon = PhotoImage(file="search_icon.png")
myimage_icon = Button(image=search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=getWeather)
myimage_icon.place(x=400, y=34)

# Logo
logo_image = PhotoImage(file="logo.png")
logo = Label(image=logo_image)
logo.place(x=150, y=100)

# Bottom Box
Frame_image = PhotoImage(file="box.png")
frame_myimage = Label(image=Frame_image)
frame_myimage.pack(padx=5, pady=5, side=BOTTOM)

# Time
name = Label(root, font=("arial", 15, "bold"))
name.place(x=30, y=100)
clock = Label(root, font=("Helvetica", 20))
clock.place(x=120, y=130)

# Labels
label1 = Label(root, text="WIND", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label1.place(x=120, y=400)

label2 = Label(root, text="HUMIDITY", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label2.place(x=225, y=400)

label3 = Label(root, text="DESCRIPTION", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label3.place(x=430, y=400)

label4 = Label(root, text="PRESSURE", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label4.place(x=650, y=400)

t = Label(font=("arial", 70, "bold"), fg="#ee666d")
t.place(x=400, y=150)
c = Label(font=("arial", 15, 'bold'))
c.place(x=400, y=250)

w = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
w.place(x=120, y=430)

h = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
h.place(x=280, y=430)

d = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
d.place(x=450, y=430)

p = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
p.place(x=670, y=430)

root.mainloop()
