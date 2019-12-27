# coding: utf-8
import requests
url = ''
data = {"text":"Hello, World!"}
request = requests.post (url, json=data)
