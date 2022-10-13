import requests
import json

url = "http://localhost:1801/postme/"
data = {'data': 'mydata'}
result = requests.post(url, json.dumps(data))
