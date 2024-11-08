import json


def read_config():
    with open("data/config.json", "r", encoding='utf-8') as file:
        return json.load(file)


def write_config(data):
    print(data)
    with open("data/config.json", "w", encoding='utf-8') as file:
        json.dump(data, file)