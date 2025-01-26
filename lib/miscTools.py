import re
import dataManager as dm
import soundManager as sm
import sttManager as sttm
import languageManager as langm
import gTranslateManager as tm
import time

ENGLISH_LANG = langm.Language('English', include_opus=False)

def clean_response(response: str, remove_spaces = True):
    if remove_spaces:
        invalad_chars = r'[.\-—!? ♪=+_/():*#;`\'\\,\"]'
    else:
        invalad_chars = r'[.\-—!?♪=+_/()*#:;`\'\\,\"]'

    if response:
        cleaned_response = re.sub(invalad_chars, '', response)
        cleaned_response = cleaned_response.lower()
        cleaned_response = cleaned_response.strip()

        # To be moved
        cleaned_response = cleaned_response.replace('ё', 'е')

        return cleaned_response
    else:
        return response

def parse_phrase(phrase: str):
    tokens = phrase.split(' ')
    for index, token in enumerate(tokens):
        if token[0] == '%':
            tokens[index] = dm.user_param(token[1:])
    return ' '.join(tokens)
    

def clean_filename(filename):
    clean_name = clean_response(filename)

    # Optionally, check length (Windows has a max filename length of 255 characters)
    clean_name = clean_name[:255]

    return clean_name

def ask_yes_or_no(default_answer = False) -> bool:
    sm.phrase_anna('Yes or no')
    for i in range(2):
        response: str = sttm.call_for_voice_input('en')
        if response:
            response = response.lower()
            if "yes" in response.split(' '):
                return True
            elif "no" in response.split(' '):
                return False
        
        if i < 1:
            sm.phrase_anna('Sorry what was that')
    sm.phrase_anna('Im not understanding')
    if default_answer == True:
        sm.phrase_anna('Im gonna assume yes')
        return True
    else:
        sm.phrase_anna('Im gonna assume no')
        return False
    
def clean_opus_dataset(target_lang: langm.Language, start_at = 0, include_points = 10_000_000):
    opus_dataset_path = f'bin/installed_languages/{target_lang.name}/opus_dataset/'

    # Open and read the files with 'utf-8' encoding and strip newlines
    with open(opus_dataset_path + 'english.txt', 'r', encoding='utf-8') as file:
        english_opus_data = [line.strip() for line in file.readlines()[start_at:include_points]]
    with open(opus_dataset_path + 'target.txt', 'r', encoding='utf-8') as file:
        target_opus_data = [line.strip() for line in file.readlines()[start_at:include_points]]

    print("Datasets read to memory")

    # Ensure both lists are of the same length
    if len(english_opus_data) != len(target_opus_data):
        print("Error: The 'english.txt' and 'target.txt' files have mismatched lengths.")
        return

    new_english_opus_data = []
    new_target_opus_data = []

    # Loop through target data and filter based on the length condition
    for phrase_index, target_phrase in enumerate(target_opus_data):
        if len(target_phrase) < 25 and len(english_opus_data[phrase_index]) < 40:
            new_target_opus_data.append(target_phrase)  # Add back the newline for writing
            new_english_opus_data.append(english_opus_data[phrase_index]) 

    print("First-pass conditions applied to datasets")
    
    english_opus_data = new_english_opus_data
    target_opus_data = new_target_opus_data
    new_english_opus_data = []
    new_target_opus_data = []
    for phrase_index, target_phrase in enumerate(target_opus_data):
        try:
            translation = tm.translate(target_phrase, ENGLISH_LANG)
            if clean_response(translation) == clean_response(english_opus_data[phrase_index]):
                new_target_opus_data.append(target_phrase + '\n')
                new_english_opus_data.append(english_opus_data[phrase_index] + '\n')  
            if phrase_index % 1000 == 0:
                print('1000 googletranslate API calls made')
                # Write the cleaned data back to the files
                with open('lib/temporary_files/english.txt', 'w', encoding='utf-8') as file:
                    file.writelines(new_english_opus_data)
                with open('lib/temporary_files/target.txt', 'w', encoding='utf-8') as file:
                    file.writelines(new_target_opus_data)
        except:
            print('API limit hit... Retrying momentarily')
            time.sleep(30)

    print("Second-pass conditions applied to datasets")

    # Write the cleaned data back to the files
    with open('lib/temporary_files/english.txt', 'w', encoding='utf-8') as file:
        file.writelines(new_english_opus_data)
    with open('lib/temporary_files/target.txt', 'w', encoding='utf-8') as file:
        file.writelines(new_target_opus_data)

    print("Datasets updated! Added to temporary_files folder.")