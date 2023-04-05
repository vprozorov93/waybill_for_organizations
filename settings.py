import json


def get_settings():
    with open('database/settings.json', 'rt', encoding='utf-8') as file:
        settings = json.loads(file.read())

    return settings
