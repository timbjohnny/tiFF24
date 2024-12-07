import pygame
import os

class Board:
    def __init__(self):
        pygame.mixer.pre_init(22050, -16, 1, 64)  # Lower frequency, mono, tiny buffer
        pygame.mixer.init(22050, -16, 1, 64)
        self.boards1 = [
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
        [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 9, 1, 1, 1, 1, 1, 1, 1, 1, 3],
        [3, 1, 6, 4, 5, 1, 6, 4, 4, 5, 1, 6, 5, 1, 6, 4, 4, 5, 1, 6, 4, 5, 1, 3],
        [3, 1, 3, 0, 3, 1, 3, 0, 0, 3, 1, 3, 3, 1, 3, 0, 0, 3, 1, 3, 0, 3, 1, 3],
        [3, 1, 7, 4, 8, 1, 7, 4, 4, 8, 1, 3, 3, 1, 7, 4, 4, 8, 1, 7, 4, 8, 1, 3],
        [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
        [7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]
        self.boards2 = [
        [6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5],
        [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
        [3, 1, 6, 5, 1, 6, 4, 4, 4, 4, 5, 1, 6, 5, 1, 3],
        [3, 1, 3, 3, 1, 7, 4, 5, 6, 4, 8, 1, 3, 3, 1, 3],
        [3, 1, 3, 3, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 1, 3],
        [3, 1, 3, 7, 4, 5, 1, 3, 3, 1, 6, 4, 8, 3, 1, 3],
        [3, 1, 3, 6, 4, 8, 1, 7, 8, 1, 7, 4, 5, 3, 1, 3],
        [3, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 3],
        [3, 1, 3, 3, 1, 6, 2, 2, 2, 2, 5, 1, 3, 3, 1, 3],
        [3, 1, 3, 3, 1, 3, 0, 0, 0, 0, 3, 1, 3, 3, 1, 3],
        [3, 1, 3, 3, 1, 7, 4, 4, 4, 4, 8, 1, 3, 3, 1, 3],
        [3, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 3],
        [3, 1, 3, 7, 4, 5, 1, 6, 5, 1, 6, 4, 8, 3, 1, 3],
        [3, 1, 3, 6, 4, 8, 1, 3, 3, 1, 7, 4, 5, 3, 1, 3],
        [3, 1, 3, 3, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 1, 3],
        [3, 1, 3, 3, 1, 6, 4, 8, 7, 4, 5, 1, 3, 3, 1, 3],
        [3, 1, 7, 8, 1, 7, 4, 4, 4, 4, 8, 1, 7, 8, 1, 3],
        [3, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 3],
        [7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]  
        ]
        self.dir_path = os.path.dirname(__file__)
        self.channels = [pygame.mixer.Channel(i) for i in range(2)]
        self.current_channel = 0
        self.chomp_sound = pygame.mixer.Sound(f'{self.dir_path}/sounds/pacman_chomp.wav')
        self.chomp_sound.set_volume(0.1)
    def get_board(self, lvl):
        if lvl == 1:
            return self.boards1    
        elif lvl == 2:
            return self.boards2
    
    def get_boardI(self, lvl , i):
        if lvl == 1:
            return self.boards1[i]   
        elif lvl == 2:
            return self.boards2[i]
    
    def get_boardIJ(self, lvl, i, j):
        if lvl == 1:
            return self.boards1[i][j]   
        elif lvl == 2:
            return self.boards2[i][j]
    
    def play_chomp_sound(self):
        # Round-robin through channels for immediate playback
        channel = self.channels[self.current_channel]
        channel.play(self.chomp_sound)
        self.current_channel = (self.current_channel + 1) % len(self.channels)

    def set_boardXY(self, lvl, i, j, newValue):
        if lvl == 1:
            if self.boards1[i][j] == 1 and newValue == 0:
                self.play_chomp_sound()
                self.boards1[i][j] = newValue
            elif self.boards1[i][j] == 9 and newValue == 0:
                self.play_chomp_sound()
                self.boards1[i][j] = newValue
        elif lvl == 2:
            if self.boards2[i][j] == 9 and newValue == 0:
                self.play_chomp_sound()
                self.boards2[i][j] = newValue
            elif self.boards1[i][j] == 9 and newValue == 0:
                self.play_chomp_sound()
                self.boards1[i][j] = newValue

    def checkVictory(self, lvl):
        victory = False
        foodFound = False
        if lvl == 1:
            for i in range(len(self.boards1)):
                    for j in range(len(self.boards1[i])):
                        if self.boards1[i][j] == 1:
                            foodFound = True
                            break                              
                    if foodFound:
                        break
            if not foodFound:
                victory = True
        elif lvl == 2:
            for k in range(len(self.boards2)):
                    for l in range(len(self.boards2[k])):
                        if self.boards2[k][l] == 1:
                            foodFound = True
                            break                              
                    if foodFound:
                        break
            if not foodFound:
                victory = True
                        
        return victory        
    
    def resetBoard(self):
        self.boards1 = [
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
        self.boards2 = [
        [6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5],
        [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
        [3, 1, 6, 5, 1, 6, 4, 4, 4, 4, 5, 1, 6, 5, 1, 3],
        [3, 1, 3, 3, 1, 7, 4, 5, 6, 4, 8, 1, 3, 3, 1, 3],
        [3, 1, 3, 3, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 1, 3],
        [3, 1, 3, 7, 4, 5, 1, 3, 3, 1, 6, 4, 8, 3, 1, 3],
        [3, 1, 3, 6, 4, 8, 1, 7, 8, 1, 7, 4, 5, 3, 1, 3],
        [3, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 3],
        [3, 1, 3, 3, 1, 6, 2, 2, 2, 2, 5, 1, 3, 3, 1, 3],
        [3, 1, 3, 3, 1, 3, 0, 0, 0, 0, 3, 1, 3, 3, 1, 3],
        [3, 1, 3, 3, 1, 7, 4, 4, 4, 4, 8, 1, 3, 3, 1, 3],
        [3, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 3],
        [3, 1, 3, 7, 4, 5, 1, 6, 5, 1, 6, 4, 8, 3, 1, 3],
        [3, 1, 3, 6, 4, 8, 1, 3, 3, 1, 7, 4, 5, 3, 1, 3],
        [3, 1, 3, 3, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 1, 3],
        [3, 1, 3, 3, 1, 6, 4, 8, 7, 4, 5, 1, 3, 3, 1, 3],
        [3, 1, 7, 8, 1, 7, 4, 4, 4, 4, 8, 1, 7, 8, 1, 3],
        [3, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 3],
        [7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]  
        ]
