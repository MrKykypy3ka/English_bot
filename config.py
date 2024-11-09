import json


def read_config():
    with open("data/config.json", "r", encoding='utf-8') as file:
        return json.load(file)


def write_config(data):
    with open("data/config.json", "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=True, indent=4)