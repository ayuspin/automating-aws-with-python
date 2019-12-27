import requests

def send_to_slack(event, context):
    url = ''
    data = {"text":"Hello, World!"}
    request = requests.post (url, json=data)
