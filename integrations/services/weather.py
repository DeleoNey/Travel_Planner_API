import requests
from travel_planner_api.settings import WEATHER_API_KEY


class WeatherService:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, lat: str, lon: str, api_key=WEATHER_API_KEY) -> dict:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric"
        }

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            main_data = data.get('main', {})
            weather_desc_list = data.get('weather', [{}])
            weather_desc = weather_desc_list[0] if weather_desc_list else {}
            wind_data = data.get('wind', {})
            sys_data = data.get('sys', {})

            weather_data = {
                "погода": weather_desc.get('main'),
                "опис": weather_desc.get('description'),
                "температура °C": main_data.get('temp'),
                "відчувається як": main_data.get('feels_like'),
                "швидкість вітру(м/c)": wind_data.get('speed'),
                "код країни": sys_data.get('country'),
                "місто": data.get('name'),
            }

            return weather_data

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP помилка: {http_err}")
            return {"error": "API key error or invalid request."}
        except requests.exceptions.RequestException as req_err:
            print(f"Помилка запиту: {req_err}")
            return {"error": "Could not connect to weather service."}
        except (KeyError, IndexError, TypeError) as json_err:
            print(f"Помилка парсингу JSON: {json_err}")
            return {"error": "Error parsing weather data."}