import json

with open('result.txt', 'r') as result:
    api = json.loads(result.read())

