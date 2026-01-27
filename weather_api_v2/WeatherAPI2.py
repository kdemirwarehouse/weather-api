import requests
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO

def get_weather():
    user_city = user_city_entry.get()

    if not user_city:
        messagebox.showerror(title="Error!",message="Lütfen şehir ismi giriniz")
        return



    my_api_key = "9ce476cc4b034d30af8165010262201"

    target_url = f"https://api.weatherapi.com/v1/current.json?key={my_api_key}&q={user_city}&lang=tr"

    try:
        response = requests.get(target_url, timeout=5)
        response.raise_for_status()  # 404 veya 500 hatalarında exception fırlatacak
        data = response.json()

        #Verileri çekme
        temp = data["current"]["temp_c"]
        humidity = data["current"]["humidity"]
        desc = data["current"]["condition"]["text"]
        icon_path = data["current"]["condition"]["icon"]#bir link döndürür
        weather_icon = download_photo(icon_path)

        if weather_icon:
            icon_label.config(image=weather_icon)
            icon_label.image = weather_icon #Python'ın resmi silmemesi için referans tutmalıyız

        #Labelları güncelleme
        temp_label.config(text=f"{temp} °C")
        humidity_label.config(text=f"Nem: %{humidity} - {desc.capitalize()}")

    except Exception as e:
        messagebox.showinfo(title="Error!",message=f"Veri alınamadı. Şehir ismini kontrol edin {e}")


def download_photo(get_icon):

    full_url = "https:" + get_icon

    try:
        api_response = requests.get(full_url, timeout=5)
        api_response.raise_for_status()

        #indirilen veriyi(Bytes) bir resim dosyası gibi açıyoruz
        image_data = BytesIO(api_response.content)
        img = Image.open(image_data)

        #resmi tkinterın anlayacağı formatta döndürüyoruz
        return ImageTk.PhotoImage(img)
    except:
        return None





#---INTERFACE---


window = Tk()
window.title("Weather API")
window.minsize(width=350,height=500)
window.config(padx=20,pady=20)
window.grid_columnconfigure(0,weight=1)#herşey sütunun ortasında, columnspana gerek kalmıyor,

user_city_entry = Entry(width=15,font=("Arial",20,"bold"))
user_city_entry.grid(row=1,column=0,pady=10)

weather_forecast_button = Button(text="Hava durumunu getir",command=get_weather,font=("Arial",12))
weather_forecast_button.grid(row=2,column=0,pady=5)

temp_label = Label(text="Sıcaklık: ",font=("Arial",10,"bold"))
temp_label.grid(row=4,column=0,pady=5)

humidity_label = Label(text="Nem: ",font=("Arial",10))
humidity_label.grid(row=5,column=0, pady=5)


icon_label = Label(window)#arayüzde boş bir ikon etiketi oluşturdum
icon_label.grid(row=3,column=0, pady=10)


window.mainloop()


