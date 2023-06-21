import requests

""" Method to handle query to OpenWeatherAPI and return the temperature data"""


def temp_data(location="Calabar"):
    # The api key, location and url to query
    API_KEY = 'ce12b255bf86f80a5f11ebe293690088'
    location = 'Calabar'
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather/?appid={API_KEY}&q={location}&units=metric"

        # query the OpenWeatherAPI
        response = requests.get(url)
        # Convert the response to a JSON string
        data = response.json()
        return (data)
    except Exception:
        return "An internal error occurred"
