import json
import os.path


def get_settings():
    with open(os.path.join(os.getcwd(), 'database', 'settings.json'), 'rt', encoding='utf-8') as file:
        settings = json.loads(file.read())

    return settings
