import json

with open('bin/user_data.json') as user_data_json:
    user_data = json.load(user_data_json)

def user_param(key: str):
    return user_data[key]