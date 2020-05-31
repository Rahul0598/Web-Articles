import requests

url = "https://covid-19-data.p.rapidapi.com/report/country/name"

querystring = {"date-format":"YYYY-MM-DD","format":"json","date":"2020-05-16","name":"India"}

headers = {
    'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
    'x-rapidapi-key': "c415316296mshbac301bd4cba56fp191b47jsn443271bb1fe4"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)