# wether_module.py
import requests
from bs4 import BeautifulSoup

def weather():
    weather_url = 'https://aqicn.org/city/thailand/ubon-ratchathani/mueang/nai-mueang/'
    weather_response = requests.get(weather_url)

    soup = BeautifulSoup(weather_response.content, 'html.parser')

    temp_element = soup.find('span', {'class': 'temp'})
    if temp_element:
        temperature = temp_element.text.strip()
    else:
        temperature = 'N/A'

    return f'{temperature} องศาเซลเซียส'

def pm25():
    pm_url = 'https://aqicn.org/city/thailand/ubon-ratchathani/mueang/nai-mueang/'
    pm_response = requests.get(pm_url)

    soup = BeautifulSoup(pm_response.content, 'html.parser')
    aqi_element = soup.find('div', {'class': 'aqivalue'})

    if aqi_element:
        aqi_value = aqi_element.text.strip()
        info_element = soup.find('div', {'id': 'aqiwgtinfo'})

        if info_element:
            info_text = info_element.text.strip()

        output_tuple = aqi_value, info_text
        answer_function = " ".join(str(x) for x in output_tuple)
        return f'{output_tuple[0]} เอคิวไอ'
    else:
        return 'PM2.5 data not available'
