import pygame

def play_sound(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

# Usage:
file_path = "welcome_om.mp3"
play_sound(file_path)