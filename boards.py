import pygame
import os

class Board:
    def __init__(self):
        pygame.mixer.pre_init(22050, -16, 1, 64)  # Lower frequency, mono, tiny buffer
        pygame.mixer.init(22050, -16, 1, 64)
        self.boards = [
        [6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5],
        [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
        [3, 1, 6, 4, 5, 1, 6, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 5, 1, 6, 4, 5, 1, 3],
        [3, 1, 3, 0, 3, 1, 3, 0, 0, 3, 1, 3, 3, 1, 3, 0, 0, 3, 1, 3, 0, 3, 1, 3],
        [3, 1, 7, 4, 8, 1, 7, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 8, 1, 7, 4, 8, 1, 3],
        [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
        [3, 1, 6, 4, 5, 1, 6, 5, 1, 6, 4, 4, 4, 4, 5, 1, 6, 5, 1, 6, 4, 5, 1, 3],
        [3, 1, 7, 4, 8, 1, 3, 3, 1, 7, 4, 5, 6, 4, 8, 1, 3, 3, 1, 7, 4, 8, 1, 3],
        [3, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 3],
        [7, 4, 4, 4, 5, 1, 3, 7, 4, 5, 1, 3, 3, 1, 6, 4, 8, 3, 1, 6, 4, 4, 4, 8],
        [0, 0, 0, 0, 3, 1, 3, 6, 4, 8, 1, 7, 8, 1, 7, 4, 5, 3, 1, 3, 0, 0, 0, 0],
        [0, 0, 0, 0, 3, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 3, 0, 0, 0, 0],
        [4, 4, 4, 4, 8, 1, 3, 3, 1, 6, 2, 2, 2, 2, 5, 1, 3, 3, 1, 7, 4, 4, 4, 4],
        [0, 0, 0, 0, 0, 1, 3, 3, 1, 3, 0, 0, 0, 0, 3, 1, 3, 3, 1, 0, 0, 0, 0, 0],
        [4, 4, 4, 4, 5, 1, 3, 3, 1, 7, 4, 4, 4, 4, 8, 1, 3, 3, 1, 6, 4, 4, 4, 4],
        [0, 0, 0, 0, 3, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 3, 0, 0, 0, 0],
        [0, 0, 0, 0, 3, 1, 3, 7, 4, 5, 1, 6, 5, 1, 6, 4, 8, 3, 1, 3, 0, 0, 0, 0],
        [6, 4, 4, 4, 8, 1, 3, 6, 4, 8, 1, 3, 3, 1, 7, 4, 5, 3, 1, 7, 4, 4, 4, 5],
        [3, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 3],
        [3, 1, 6, 4, 5, 1, 3, 3, 1, 6, 4, 8, 7, 4, 5, 1, 3, 3, 1, 6, 4, 5, 1, 3],
        [3, 1, 7, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 8, 1, 3],
        [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
        [3, 1, 6, 4, 5, 1, 6, 4, 4, 5, 1, 6, 5, 1, 6, 4, 4, 5, 1, 6, 4, 5, 1, 3],
        [3, 1, 3, 0, 3, 1, 3, 0, 0, 3, 1, 3, 3, 1, 3, 0, 0, 3, 1, 3, 0, 3, 1, 3],
        [3, 1, 7, 4, 8, 1, 7, 4, 4, 8, 1, 3, 3, 1, 7, 4, 4, 8, 1, 7, 4, 8, 1, 3],
        [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
        [7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]
        self.dir_path = os.path.dirname(__file__)
        self.channels = [pygame.mixer.Channel(i) for i in range(2)]
        self.current_channel = 0
        self.chomp_sound = pygame.mixer.Sound(f'{self.dir_path}/sounds/pacman_chomp.wav')
        self.chomp_sound.set_volume(0.1)
    def get_board(self):
        return self.boards    
    
    def get_boardI(self, i):
        return self.boards[i]   
    
    def get_boardIJ(self, i, j):
        return self.boards[i][j]
    
    def play_chomp_sound(self):
        # Round-robin through channels for immediate playback
        channel = self.channels[self.current_channel]
        channel.play(self.chomp_sound)
        self.current_channel = (self.current_channel + 1) % len(self.channels)

    def set_boardXY(self, i, j, newValue):
        if self.boards[i][j] == 1 and newValue == 0:
            self.play_chomp_sound()
            self.boards[i][j] = newValue   

    def checkVictory(self):
        victory = False
        foodFound = False
        for i in range(len(self.boards)):
            for j in range(len(self.boards[i])):
                if self.boards[i][j] == 1:
                    foodFound = True
                    break                              
            if foodFound:
                break
        if not foodFound:
            victory = True
        return victory        