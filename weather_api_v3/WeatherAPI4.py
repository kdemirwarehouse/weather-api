# change background based on weather condition
import requests
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO


def update_theme(condition_text):
    condition_text = condition_text.lower().strip()

    # hava durumuna göre renk belirleyeceğiz
    if "güneş" in condition_text or "açık" in condition_text:
        bg_color = "#87BBEB"  # lightblue
        fg_color = "black"
    elif "bulut" in condition_text or "kapalı" in condition_text:
        bg_color = "#7F8C99"
        fg_color = "white"
    elif "yağmur" in condition_text or "sağanak" in condition_text:
        bg_color = "#206499"
        fg_color = "white"
    elif "kar" in condition_text:
        bg_color = "#F0F8FF"
        fg_color = "black"
    else:
        bg_color = "#F5F5F5"
        fg_color = "black"

    window.config(bg=bg_color)  # sadece ana pencerenin arka planını değiştirir

    for widget in window.winfo_children():
        if isinstance(widget, Label):  # tip control
            widget.config(bg=bg_color, fg=fg_color)
        elif isinstance(widget, Button):
            widget.config(highlightbackground=bg_color)


def get_weather():
    user_city = user_city_entry.get()


    if not user_city:
        messagebox.showerror(title="Error!", message="Lütfen şehir ismi giriniz")
        return

    my_api_key = "9ce476cc4b034d30af8165010262201"

    target_url = f"https://api.weatherapi.com/v1/current.json?key={my_api_key}&q={user_city}&lang=tr"

    try:
        response = requests.get(target_url, timeout=5)
        response.raise_for_status()  # 404 veya 500 hatalarında exception fırlatacak
        data = response.json()

        # Verileri çekme
        temp = data["current"]["temp_c"]
        humidity = data["current"]["humidity"]
        desc = data["current"]["condition"]["text"]
        update_theme(desc)
        icon_path = data["current"]["condition"]["icon"]  # bir link döndürür
        weather_icon = download_photo(icon_path)

        if weather_icon:
            icon_label.config(image=weather_icon)
            icon_label.image = weather_icon  # Python'ın resmi silmemesi için referans tutmalıyız

        # Labelları güncelleme
        temp_label.config(text=f"{temp} °C")
        humidity_label.config(text=f"Nem: %{humidity} - {desc.capitalize()}")

    except Exception as e:
        messagebox.showinfo(title="Error!", message=f"Veri alınamadı. Şehir ismini kontrol edin {e}")


def download_photo(get_icon):
    full_url = "https:" + get_icon

    try:
        api_response = requests.get(full_url, timeout=5)
        api_response.raise_for_status()

        # indirilen veriyi(Bytes) bir resim dosyası gibi açıyoruz
        image_data = BytesIO(api_response.content)
        img = Image.open(image_data)

        # resmi tkinterın anlayacağı formatta döndürüyoruz
        return ImageTk.PhotoImage(img)
    except:
        return None


# ---INTERFACE---


window = Tk()
window.title("Weather API")
window.minsize(width=350, height=500)
window.config(padx=20, pady=20)
window.grid_columnconfigure(0, weight=1)  # herşey sütunun ortasında, columnspana gerek kalmıyor,


user_city_entry = Entry(width=15, font=("Arial", 20, "bold"))
user_city_entry.grid(row=1, column=0, pady=10)

weather_forecast_button = Button(text="Hava durumunu getir", command=get_weather, font=("Arial", 12))
weather_forecast_button.grid(row=2, column=0, pady=5)

temp_label = Label(text="Sıcaklık: ", font=("Arial", 10, "bold"))
temp_label.grid(row=4, column=0, pady=5)

humidity_label = Label(text="Nem: ", font=("Arial", 10))
humidity_label.grid(row=5, column=0, pady=5)

icon_label = Label(window)  # arayüzde boş bir ikon etiketi oluşturdum
icon_label.grid(row=3, column=0, pady=10)

window.mainloop()




