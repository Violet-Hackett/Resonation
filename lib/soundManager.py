import pygame
import time

# Initialize Pygame mixer
pygame.mixer.init()

drone = pygame.mixer.Sound(f'lib/sfx/Drone.mp3')

def start_drone():
    drone.play(loops=-1, maxtime=0)

def end_drone():
    drone.fadeout(5000)

def play_sfx(id: str, autodelay = False):
    sfx = pygame.mixer.Sound(f'lib/sfx/{id}.mp3') 
    sfx.play()
    if autodelay:
        time.sleep(sfx.get_length())

def phrase_anna(id: str, autodelay = True):
    phrase = pygame.mixer.Sound(f'lib/anna/{id}.wav')  
    phrase.play()
    if autodelay:
        time.sleep(phrase.get_length() + 0.25)

def play_mp3(fp: str, autodelay = False):
    print(fp)
    sound = pygame.mixer.Sound(fp) 
    sound.play()
    if autodelay:
        time.sleep(sound.get_length() + 0.25)