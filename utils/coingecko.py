import requests

def get_monero_price():
    try:
        url = 'https://api.coingecko.com/api/v3/simple/price?ids=monero&vs_currencies=rub,usd'
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as err:
        print(err)

print("Текущая стоимость Monero:", get_monero_price())