import requests
import json

if __name__ == '__main__':
    obj = requests.post('http://localhost:5600/auth/login', json={'username': 'admin', 'password': '123456'}).text
    token = json.loads(obj)
    print(type(token))
