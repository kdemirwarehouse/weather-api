import requests


my_api_key = "9ce476cc4b034d30af8165010262201"

user_city = input("Enter city name: ")

target_url = f"https://api.weatherapi.com/v1/current.json?key={my_api_key}&q={user_city}&lang=tr"

def make_requests(url):
    try:
        response = requests.get(url,timeout=5)
        response.raise_for_status() #404 veya 500 hatalarında exception fırlatacak
        return response
    except requests.exceptions.RequestException as e:
        print(f"Hata oluştu ({url}): {e}")
        return None



def weather_info(url):
    response = make_requests(url)
    if response is None:
        return

    data_json = response.json()

    try:
        temp = data_json["current"]["temp_c"]
        desc = data_json["current"]["condition"]["text"]
        print(f"{user_city.capitalize()} için hava: {temp} °C, {desc}")
    except KeyError:
        print("Veri formatı beklenenden farklı geldi")


weather_info(target_url)