import requests

BASE = "http://127.0.0.1:5000"

response = requests.put(BASE + "/video/32", json={"name": "mamei", "views": 23891, "likes": 938 } )
print(response.json())

response = requests.get(BASE + "/video/32")
print(response.json())