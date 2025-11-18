import requests

class PlacesService:
    BASE_URL = "https://api.geoapify.com/v2/places"

    def __init__(self, api_key:str):
        self.api_key = api_key

    def get_nearby_places(self,  lat, lon, radius=1000, categories=None):
        params = {
            "apiKey": self.api_key,
            "lat": lat,
            "lon": lon,
            "radius": radius,
        }

        if categories:
            params["categories"] = categories

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            return self._format_places(data)

        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def _clean(self, dictionary: dict):
        """
        Deletes all null values from a dictionary
        """
        return {k: v for k, v in dictionary.items() if v not in (None, "", [])}

    def _format_places(self, data):
        results = []

        for feature in data.get("features", []):
            properties = feature.get("properties", {})
            distance = properties.get("distance")

            cleaned_raw = self._clean({
                "inscription": properties.get("inscription"),
            })

            item = self._clean({
                "назва": properties.get("name"),
                "країна": properties.get("country"),
                "місто": properties.get("city"),
                "поштовий індекс": properties.get("postcode"),
                "район": properties.get("district"),
                "передмістя": properties.get("suburb"),
                "квартал": properties.get("quarter"),
                "Вулиця": properties.get("street"),
                "Номер будинку": properties.get("housenumber"),
                "formatted": properties.get("formatted"),
                "відстань": distance,
            })

            results.append(item)

        results.sort(key=lambda x: x["відстань"] or 999999)

        return results