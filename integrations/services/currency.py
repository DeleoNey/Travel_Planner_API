import requests

COUNTRY_TO_CURRENCY = {
    "Ukraine": "UAH",
    "Poland": "PLN",
    "Germany": "EUR",
    "France": "EUR",
    "United States": "USD",
    "Italy": "EUR",
    "Belgium": "EUR",
    "United Kingdom": "GBP",
}


class CurrencyService:
    BASE_URL = "https://open.er-api.com/v6/latest"
    BASE_CURRENCY = "USD"

    def __init__(self, base_currency=None):
        self.base_currency = base_currency or self.BASE_CURRENCY

    def get_currency_by_country(self, country: str):
        currency = COUNTRY_TO_CURRENCY.get(country)
        if currency is None:
            raise ValueError("Currency for country '{country}' not found")
        return currency

    def convert(self, amount: float, target_currency: str):
        response = requests.get(f"{self.BASE_URL}/{self.base_currency}")
        response.raise_for_status()
        data = response.json()

        rate = data["rates"].get(target_currency)
        if rate is None:
            raise ValueError("Invalid target currency")

        return amount * rate

    def convert_budget_for_country(self, amount: float, country: str):
        target_currency = self.get_currency_by_country(country)
        converted = self.convert(amount, target_currency)

        return {
            "original_amount": amount,
            "original_currency": self.base_currency,
            "converted_amount": f"{round(converted, 2)} {target_currency}",
        }