import json

OPUS_INCLUSION = 10000

class Language:
    def __init__(self, name, include_opus = True):
        self.name = name

        with open(f'bin/installed_languages/{name}/language_specs.json') as file:
            specs = json.load(file)
        self.abbreviation = specs['abbreviation']
        self.stt_addon = specs['stt_addon']

        opus_data = {}
        if include_opus:
            english_opus_file = open(f'bin/installed_languages/{name}/opus_dataset/english.txt', encoding='utf-8')
            target_opus_file = open(f'bin/installed_languages/{name}/opus_dataset/target.txt', encoding='utf-8')
            for i in range(OPUS_INCLUSION):
                opus_data[english_opus_file.readline().strip()] = target_opus_file.readline().strip()
        self.opus_data = opus_data

def install(name):
    pass