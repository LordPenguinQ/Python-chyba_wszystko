import requests
from datetime import datetime, timedelta


def get_exchangerates(rok, miesiac, waluta):
    waluta = waluta.upper()
    today = datetime.now()
    first = datetime(rok, miesiac, 1)

    if miesiac == 12:
        
        last = datetime(rok + 1, 1, 1) - timedelta(days=1)

    else:
        last = datetime(rok, miesiac + 1, 1) - timedelta(days=1)

    current = first
    while current <= last and current <= today:
        dzien = current.strftime("%Y-%m-%d")

        wynik = requests.get(f'http://api.nbp.pl/api/exchangerates/rates/A/{waluta}/{dzien}/?format=json')

        if wynik.status_code == 200:
            rates = wynik.json()
            print(f"Kurs {waluta} {dzien}: {rates['rates'][0]['mid']}")

        elif wynik.status_code == 404:
            print(f"Kursy {current.strftime('%Y-%m-%d')} nie są dostępne.")
        else:
            print(f"Błąd pobierania danych. Kod błędu: {wynik.status_code}")
        current += timedelta(days=1)


# Podaj jaka waluta
waluta = input("Podaj walutę: ")

# Podaj dla jakiego miesiąca i roku wyświetlić dane
rok = int(input("Podaj rok do pobrania: "))
miesiac = int(input("Podaj miesiąc do pobrania: "))

get_exchangerates(rok, miesiac, waluta)