import soundManager as sm
from time import sleep
import gTranslateManager as gtm
import ttsManager as ttsm
import sttManager as sttm
import miscTools as mt
import languageManager as langm
import random

class Question:
    def __init__(self):
        self.times_correct = 0

    def introduce():
        pass

    def run_question(self):
        pass

class RepeatAfterMeQuestion(Question):
    def __init__(self, english_text:str, target_lang: langm.Language, translated_text = None):
        super().__init__()
        self.english_text = english_text
        self.translated_text = translated_text
        if not translated_text:
            self.translated_text = gtm.translate(english_text, target_lang)
        self.target_lang = target_lang

    def introduce():
        sm.phrase_anna('Heres how this works')
        sm.phrase_anna('Ill speak a phrase')
        sm.phrase_anna('Youll get a few chances')
        sleep(1)
        sm.phrase_anna('Lets get started')
        sleep(0.5)

    def check_answer(self, answer, chance) -> bool:
        if mt.clean_response(answer) == mt.clean_response(self.translated_text):
            self.times_correct += 1
            sm.play_sfx('Correct')
            sleep(1)
            return True
        else:
            self.times_correct -= 1
            if chance == 0:
                sm.phrase_anna('Not quite')
                sm.phrase_anna('Try that again')
            elif chance == 1:
                if answer:
                    sm.phrase_anna('Heres what I heard')
                    ttsm.generate_gtts(answer, self.target_lang)
                sm.phrase_anna('Try one more time')
            else:
                sm.phrase_anna('Well come back to that')
                sleep(1)
                return True
            return False


    def run_question(self):
        end_question = False
        chance = 0
        while not end_question:
            sm.phrase_anna('Repeat after me')
            print(self.translated_text)
            ttsm.generate_gtts(self.translated_text, self.target_lang)
            stt_index = self.target_lang.abbreviation + self.target_lang.stt_addon
            answer = sttm.call_for_voice_input(stt_index)
            print(answer)
            end_question = self.check_answer(answer, chance)
            chance += 1
        sm.phrase_anna('It means')
        ttsm.generate_gtts(self.english_text, mt.ENGLISH_LANG)

class TranslateToEnglishQuestion(Question):
    def __init__(self):
        super.__init__()






# =============== LESSON CLASS ======================





class Lesson:
    def __init__(self, target_lang: langm.Language, level: int = None, from_opus = False, opus_inclusion = 5):
        self.level = level
        self.target_lang = target_lang

        self.questions: list[Question] = []
        if level:
            with open(f'bin/installed_languages/{target_lang.name}/lessons/L{level}.txt') as vocab_file:
                vocab = [line.strip() for line in vocab_file.readlines()]
            for phrase in vocab:
                self.questions.append(RepeatAfterMeQuestion(mt.parse_phrase(phrase), target_lang))
        elif from_opus:
            pairs = random.choices(list(target_lang.opus_data.items()), k=opus_inclusion)
            for pair in pairs:
                self.questions.append(RepeatAfterMeQuestion(pair[0], target_lang, translated_text = pair[1]))


    def run_lesson(self):
        sm.end_drone()
        sm.phrase_anna('Lets begin')
        for question in self.questions:
            question.run_question()

        sm.play_sfx('Lesson complete', True)
        sm.phrase_anna('Good job')

