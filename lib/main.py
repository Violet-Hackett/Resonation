import soundManager as sm
from time import sleep
import ttsManager as ttsm
import miscTools as mt
import os
import sttManager as sttm
import languageManager as langm
import lessonManager as lessonm

target_lang = langm.Language('Russian')
#mt.clean_opus_dataset(target_lang, 8000, 12_000_000)

sttm.adjust_bg_noise()

sm.start_drone()

def firsttime_setup():
    sleep(3)
    sm.phrase_anna('Hello there')
    sleep(1) 
    sm.phrase_anna('Welcome to Resonation')
    sm.phrase_anna('My names Anna')
    sleep(4)
    sm.phrase_anna('Lets get started')
    sm.phrase_anna('What language')
    sleep(4)
    sm.phrase_anna('Alright lets get set up')
    sleep(5)
    sm.phrase_anna('Were set to go')
    sm.end_drone()
    sleep(3)

firsttime_setup()

lessonm.RepeatAfterMeQuestion.introduce()

lessons_avalable = len(os.listdir(f'bin/installed_languages/{target_lang.name}/lessons'))

lessons: list[lessonm.Lesson] = []
# for lesson_index in range(lessons_avalable):
#     lessons.append(lessonm.Lesson(target_lang, level=lesson_index))
for i in range(100):
    lessons.append(lessonm.Lesson(target_lang, from_opus=True))

lesson_index = 0
running = True
while running:
    lessons[lesson_index].run_lesson()
    sm.phrase_anna('Would you like to start')
    running = mt.ask_yes_or_no()
    lesson_index += 1