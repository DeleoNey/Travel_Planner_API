import requests
from travel_planner_api.settings import WEATHER_API_KEY



class WeatherService:
    BASE_URL = f"https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, lat: str, lon: str, api_key=WEATHER_API_KEY) -> dict:

        params = {"lat": lat,
                  "lon": lon,
                  "appid": api_key,
                  "units": "metric",
        }
        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            current_temp = data['main']['temp']

            return current_temp

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP помилка: {http_err}")

        except requests.exceptions.RequestException as req_err:
            print(f"Помилка запиту: {req_err}")

        except (KeyError, IndexError) as json_err:
            print(f"Помилка парсингу JSON: {json_err}")

        return None