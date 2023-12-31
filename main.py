# Şükrü Taşkıran 20190601044
# Gizem Güllü 20210601028
# Can Baytekin 20190601052

import tkinter as tk
from tkinter import ttk
import requests
from PIL import ImageTk, Image


class WeatherApp:
    def __init__(self, window):
        self.window = window
        self.selected_city = tk.StringVar(window)
        self.temperature_unit = tk.StringVar(window)
        self.loadPreferences()
        self.weather_data = []
        self.widgets()

    def widgets(self):
        window.configure(bg="#D9E4F5")
        self.window.geometry("400x480")
        self.window.resizable(False, False)  # Boyutlandırılabilirliği kapatır
        window_width = self.window.winfo_reqwidth()
        window_height = self.window.winfo_reqheight()
        position_right = int(self.window.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.window.winfo_screenheight() / 2 - window_height / 2) - 100
        self.window.geometry(f"+{position_right}+{position_down}")

        title_label = ttk.Label(self.window, text="      Weather Forecast", font=("Arial", 16, "bold"),
                                background="#D9E4F5")
        title_label.grid(row=0, column=0, columnspan=2, padx=10,
                         pady=10)  # row ve column: satır sütün indexi, columnspan 2 column kaplar,padx pady x y axes spaces
        icon = Image.open("logo.png")
        icon = icon.resize((50, 50))
        photo = ImageTk.PhotoImage(icon)
        logo_label = ttk.Label(self.window, image=photo, background="#D9E4F5")
        logo_label.image = photo
        logo_label.grid(row=0, column=0, padx=0, pady=0)

        city_label = ttk.Label(self.window, text="Select a city:", font=("Arial", 12, "bold"), background="#D9E4F5")
        city_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)  # in the part widget how east or west direction

        dropdownCities = ttk.Combobox(self.window, textvariable=self.selected_city, font=(
        "Arial", 10))  # combobox a tkinter widget that allows user to select a dropdown cities it is a menu

        dropdownCities['values'] = ('Adana', 'Adiyaman', 'Afyonkarahisar', 'Agri', 'Aksaray', 'Amasya', 'Ankara',
                                    'Antalya', 'Ardahan', 'Artvin', 'Aydin', 'Balikesir', 'Bartin', 'Batman', 'Bayburt',
                                    'Bilecik', 'Bingol', 'Bitlis', 'Bolu', 'Burdur', 'Bursa', 'Canakkale', 'Cankiri',
                                    'Corum', 'Denizli', 'Diyarbakir', 'Duzce', 'Edirne', 'Elazig', 'Erzincan',
                                    'Erzurum',
                                    'Eskisehir', 'Gaziantep', 'Giresun', 'Gumushane', 'Hakkari', 'Hatay', 'Igdir',
                                    'Isparta', 'Mersin', 'Istanbul', 'Izmir', 'Kahramanmaras', 'Karabuk', 'Karaman',
                                    'Kars', 'Kastamonu', 'Kayseri', 'Kirikkale', 'Kirklareli', 'Kirsehir', 'Kilis',
                                    'Kocaeli', 'Konya', 'Kutahya', 'Malatya', 'Manisa', 'Mardin', 'Mersin', 'Mugla',
                                    'Mus', 'Nevsehir', 'Nigde', 'Ordu', 'Osmaniye', 'Rize', 'Sakarya', 'Samsun',
                                    'Sanliurfa', 'Siirt', 'Sinop', 'Sivas', 'Sirnak', 'Tekirdag', 'Tokat', 'Trabzon',
                                    'Tunceli', 'Usak', 'Van', 'Yalova', 'Yozgat', 'Zonguldak')

        dropdownCities.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)  # tk.W west direction

        temperature_label = ttk.Label(self.window, text="Temperature unit:", font=("Arial", 12, "bold"),
                                      background="#D9E4F5")
        temperature_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)

        temperature_button = ttk.Button(self.window, textvariable=self.temperature_unit,
                                        command=self.tempToggle,
                                        style="ToggleButton.TButton")
        temperature_button.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        weather_button = ttk.Button(self.window, text="Get Weather", command=self.getWeather, width=20,
                                    style="ToggleButton.TButton")
        weather_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.weather_display = tk.Text(self.window, height=18, width=50, font=("Arial", 10, "bold"))
        self.weather_display.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(self.window, command=self.weather_display.yview)  # yview vertical height
        scrollbar.grid(row=4, column=2, sticky="ns")  # north south / up to down scrolled
        self.weather_display.configure(yscrollcommand=scrollbar.set)

    def tempToggle(self):
        if self.temperature_unit.get() == "Celsius":
            self.temperature_unit.set("Fahrenheit")
        else:
            self.temperature_unit.set("Celsius")

    def getWeather(self):
        city = self.selected_city.get()

        # Retrieve weather data
        self.weather_data = self.fetchData(city)

        if self.weather_data:
            # Display weather information
            self.displayInfo()
        else:
            self.weather_display.delete("1.0", tk.END)  # 1 is first index of row, tk.end is end of the index
            self.weather_display.insert(tk.END, "Failed to fetch weather data.")

    def fetchData(self, city):
        api_key = "6bfdcf07f9e1a778be920e5fd5dd4570"
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"

        try:
            response = requests.get(url)  # http formundan python object
            json_data = response.json()  # response method to use python data, it makes easier to read the data

            weather_data = []
            count = 0  # 3 günlük veri almak için sayaç
            for data in json_data['list']:
                datetime = data['dt_txt']
                time = datetime.split()[1]
                if '00:00:00' in time or '12:00:00' in time:
                    temperature = data['main']['temp']
                    wind_speed = data['wind']['speed']
                    weather_data.append({
                        'date': datetime.split()[0],
                        'time': time,
                        'temperature': temperature,
                        'wind_speed': wind_speed
                    })
                    count += 1
                    if count == 6:  # 3 günlük veriyi aldıktan sonra döngüyü sonlandır
                        break

            return weather_data

        except Exception as e:
            print("An error occurred:", e)
            return []

    def displayInfo(self):
        self.weather_display.config(state="normal")
        self.weather_display.delete("1.0", tk.END)

        for i in range(0, len(self.weather_data), 2):
            date = self.weather_data[i]['date']
            temperature_day = self.weather_data[i + 1]['temperature']
            temperature_night = self.weather_data[i]['temperature']
            wind_speed_day = self.weather_data[i + 1]['wind_speed']
            wind_speed_night = self.weather_data[i]['wind_speed']

            temperature_day = self.parseTemp(temperature_day)
            temperature_night = self.parseTemp(temperature_night)

            self.weather_display.insert(tk.END, f"Date: {date}\n")
            self.weather_display.insert(tk.END, f"Day Temperature: {temperature_day}\n")
            self.weather_display.insert(tk.END, f"Day Wind Speed: {wind_speed_day} km/h\n")
            self.weather_display.insert(tk.END, f"Night Temperature: {temperature_night}\n")
            self.weather_display.insert(tk.END, f"Night Wind Speed: {wind_speed_night} km/h\n")
            self.weather_display.insert(tk.END, "\n")
        self.weather_display.config(state="disabled")  # Editlenemez hale getirir

    def parseTemp(self, temperature):
        if self.temperature_unit.get() == "Celsius":
            temperature_celsius = temperature - 273.15
            return f"{temperature_celsius:.1f} °C"
        else:
            temperature_fahrenheit = (temperature - 273.15) * 9 / 5 + 32
            return f"{temperature_fahrenheit:.1f} °F"

    def savePreferences(self):

        with open("Settings.txt", "w") as file:
            file.write(f"City: {self.selected_city.get()}\n")
            file.write(f"Temperature Unit: {self.temperature_unit.get()}\n")

    def loadPreferences(self):

        try:
            with open("Settings.txt", "r") as file:
                for line in file:
                    key, value = line.split(": ")
                    if key == "City":
                        self.selected_city.set(value.strip())
                    elif key == "Temperature Unit":
                        self.temperature_unit.set(value.strip())

        except Exception as e:
            print("An error occurred:", e)

    def run(self):

        self.window.protocol("WM_DELETE_WINDOW",
                             self.on_close)  # binds the X button with the command for exiting the program
        self.window.mainloop()

    def on_close(self):
        self.savePreferences()
        self.window.destroy()


window = tk.Tk()
window.title("Weather App")

app = WeatherApp(window)

style = ttk.Style()
style.configure("ToggleButton.TButton", font=("Arial", 12, "bold"), foreground="black", background="orange")

if __name__ == "__main__":
    app.run()
