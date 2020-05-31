import requests


def market_data(interval,start,end,symbol):
    """
    This method is used to get ohlcv data.
    interval = what interval data we want ex: 1D - 1 day, 1W - 1week
    start and end = start and end time in unix time stamp ex : 1546448400
    symbol = which company stock details we need to fetch
    """
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-historical-data"

    querystring = {"frequency":interval,"filter":"history","period1":start,"period2":end,"symbol":symbol}

    headers = {
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        'x-rapidapi-key': "7ab9a2a1e5mshb7bb2b13f34d78ap1e2047jsnc3cea42a4ee4"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)


market_data('1D',1546448400,1546578400,'AAPL')