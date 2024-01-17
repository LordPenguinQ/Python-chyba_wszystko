import requests
from datetime import datetime, timedelta
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def get_exchangerates(rok, miesiac, waluta):
    daty = []
    kursy = []

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
            daty.append(current)
            kursy.append(rates['rates'][0]['mid'])
        elif wynik.status_code == 404:
            print(f"Kursy {current.strftime('%Y-%m-%d')} nie są dostępne.")
        else:
            print(f"Błąd pobierania danych. Kod błędu: {wynik.status_code}")
        current += timedelta(days=1)

    return pd.DataFrame({'Data': daty, 'Kursy': kursy})

def rysuj_wykres(df, waluta):
    plt.figure(figsize=(10, 6))
    plt.plot(df['Data'], df['Kursy'], marker='o', linestyle='-', color='b')
    plt.title('Kurs ' + waluta + ' w danym miesiącu')
    plt.xlabel('Data')
    plt.ylabel('Kurs')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Podaj jaka waluta
waluta = input("Podaj walutę: ")

# Podaj dla jakiego miesiąca i roku wyświetlić dane
rok = int(input("Podaj rok do pobrania: "))
miesiac = int(input("Podaj miesiąc do pobrania: "))

wykres = get_exchangerates(rok, miesiac, waluta)
rysuj_wykres(wykres, waluta)
