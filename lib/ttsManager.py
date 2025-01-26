from gtts import gTTS
import soundManager as sm
import miscTools as mt
import os
import languageManager as langm
from tinytag import TinyTag

def generate_gtts(text: str, target_lang: langm.Language, autodelay=True) -> int: # Returns duration of gtts
    # check cache
    clean_filepath = f'bin/installed_languages/{target_lang.name}/cache/{mt.clean_filename(text)}.mp3'
    if not os.path.exists(clean_filepath):
        # Create a gTTS object
        print('API call made (gTTS)')
        tts = gTTS(text=text, lang=target_lang.abbreviation)
        # Save the speech to an MP3 file
        tts.save(clean_filepath)

    sm.play_mp3(clean_filepath, autodelay=autodelay)
    return TinyTag.get(clean_filepath).duration