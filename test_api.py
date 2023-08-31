import requests
import json
from decouple import config

if __name__ == '__main__':
    print({'username': config('USER'), 'password': config('PASS')})
    obj = requests.post('http://localhost:5000/auth/login', json={'username': config('USER'), 'password': config('PASS')}).text
    token = json.loads(obj)
    print(token)
