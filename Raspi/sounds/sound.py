import pygame

import time

pygame.init()

pygame.mixer.music.load("1.mp3")
pygame.mixer.music.play()
time.sleep(3)
pygame.mixer.music.load("2.mp3")
pygame.mixer.music.play()
time.sleep(3)
pygame.mixer.music.load("4.mp3")
pygame.mixer.music.play()


print "done"
