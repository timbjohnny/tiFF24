import pygame
import sys
from boards import Board
from math import pi
import json

class Game:
    
    def __init__(self, board, width=720, height=800, fps=60):
        pygame.init()
        self.board = board
        self.width = width
        self.height = height
        self.fps = fps
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        self.running = True

        # Game states
        self.states = {
            "main_menu": MainMenu(self),
            "leaderboard": Leaderboard(self),
            "game": Gamestate(self),
            "pause": PauseMenu(self)
        }
        self.current_state = self.states["main_menu"]

    def switch_state(self, state_name):
        """Switch to a new state by name."""
        self.current_state = self.states[state_name]

    def run(self):
        while self.running:
            self.current_state.handle_events()
            self.current_state.update()
            self.current_state.draw()
            self.clock.tick(self.fps)

        self.quit()

    def quit(self):
        pygame.quit()
        sys.exit()

class MainMenu:
    def __init__(self, game):
        self.game = game
        self.title_font = pygame.font.Font("./assets/MinecraftRegular-Bmg3.otf", 100)
        self.select_font = pygame.font.Font("./assets/MinecraftRegular-Bmg3.otf", 50)
        self.rect_width = 600
        self.rect_height = 130
        self.pointer_pos_x = 175
        self.pointer_pos_y = 450

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    match self.pointer_pos_y:
                        case 450:
                            self.game.switch_state("game")  # startet spiel
                        case 525:
                            self.game.switch_state("leaderboard")   # geht ins leaderboard
                        case 600:
                            self.game.running = False   # quittet das spiel
                elif event.key == pygame.K_UP:
                    if self.pointer_pos_y > 450:
                        self.pointer_pos_y -= 75
                        match self.pointer_pos_y:
                            case 450:   # pointer auf "Start Game"
                                self.pointer_pos_x = 175
                            case 525:   # pointer auf "Leaderboard"
                                self.pointer_pos_x = 125
                elif event.key == pygame.K_DOWN:
                    if self.pointer_pos_y < 600:
                        self.pointer_pos_y += 75
                        match self.pointer_pos_y:
                            case 525:   # pointer auf "Leaderboard"
                                self.pointer_pos_x = 140
                            case 600:   # pointer auf "Quit"
                                self.pointer_pos_x = 260



    def update(self):
        pass


    def draw(self):
        self.game.screen.fill((0, 0, 0))
        title_text = self.title_font.render("P     M   n", False, (255, 255, 255))
        self.game.screen.blit(title_text, (self.game.width // 2 - title_text.get_width() // 2, 100))
        pygame.draw.rect(self.game.screen, (0,0,155), (((self.game.width - self.rect_width) // 2), 80, self.rect_width, self.rect_height), 3, 8)
        # Start Text
        start_text = self.select_font.render("Start Game", False, (255, 255, 255))
        self.game.screen.blit(start_text, (self.game.width // 2 - start_text.get_width() // 2, 450))
        # Leaderboard Text
        leaderboard_text = self.select_font.render("Leaderboard", False, (255, 255, 255))
        self.game.screen.blit(leaderboard_text, (self.game.width // 2 - leaderboard_text.get_width() // 2, 525))
        # Quit Text
        quit_text = self.select_font.render("Quit", False, (255, 255, 255))
        self.game.screen.blit(quit_text, (self.game.width // 2 - quit_text.get_width() // 2, 600))
        # Select Pointer
        pointer_text = self.select_font.render(">", False, (255,255,255))
        self.game.screen.blit(pointer_text, (self.pointer_pos_x, self.pointer_pos_y))
        pygame.display.flip()

class Leaderboard:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font("./assets/MinecraftRegular-Bmg3.otf", 50)
        self.small_font = pygame.font.Font("./assets/MinecraftRegular-Bmg3.otf", 40)
        self.rect_width = 600
        self.rect_height = 130

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                        self.game.switch_state("main_menu")


    def update(self):
        pass


    def draw(self):
        self.game.screen.fill((0, 0, 0))
        pygame.draw.rect(self.game.screen, (0,0,155), (((self.game.width - self.rect_width) // 2), 80, self.rect_width, self.rect_height), 3, 8)
        # Leaderboard Text
        leaderboard_text = self.font.render("Leaderboard", False, (255, 255, 255))
        # Select Pointer
        pointer_text = self.font.render(">", False, (255,255,255))
        # Back Text
        back_text = self.font.render("Back to menu", False, (255, 255, 255))
        # Info Text
        name_text = self.small_font.render("Name", False, (255, 255, 255))
        score_text = self.small_font.render("Score", False, (255, 255, 255))


        if self.rect_height < 625:  # Leaderboard loading animation
            self.rect_height += 25
            pygame.time.wait(50)
        else:   # show options and leaderboard
            pygame.time.wait(100)
            # show text
            self.game.screen.blit(back_text, (self.game.width // 2 - back_text.get_width() // 2, 725))
            self.game.screen.blit(pointer_text, (150, 725))
            self.game.screen.blit(leaderboard_text, (self.game.width // 2 - leaderboard_text.get_width() // 2, 100))
            self.game.screen.blit(name_text, (100, 155))
            self.game.screen.blit(score_text, (490, 155))

            with open("./assets/leaderboard.json", "r") as f:
                data = json.load(f)
                for i in range(len(data)):
                    self.game.screen.blit(self.small_font.render(str(data["p" + str(i)][0]["name"]), False, (255, 255, 255)),
                                (280, 150 + 25 * i))
                    self.game.screen.blit(self.small_font.render(str(data["p" + str(i)][0]["score"]), False, (255, 255, 255)),
                                (600, 150 + 25 * i))
        pygame.display.flip()

class Gamestate:
    def __init__(self, game):
        self.game = game
        self.spalte = int(game.width / 24)
        self.zeile = int(game.height / 30)
        self.player = Player(11* self.spalte, 21*self.zeile, self) # x,y Startposition

    def getZeile(self):
        return self.zeile
    
    def getSpalte(self):
        return self.spalte
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # Pause the game
                    self.game.switch_state("pause")

    def update(self):
        self.player.update()

    def draw(self):
        self.game.screen.fill((0, 0, 0))
        for i in range(len(board.get_board())):
            for j in range(len(board.get_boardI(i))):
                if board.get_boardIJ(i,j) == 1: #Auf dem Feld ist ein Punkt zum Essen
                    pygame.draw.circle(game.screen, 'white', ((j*self.spalte) + (0.5*self.spalte),(i*self.zeile) + (0.5*self.zeile)), 4)
                elif board.get_boardIJ(i,j) == 2: # Horizonatale Wand
                    pygame.draw.line(game.screen, 'white', ((j*self.spalte),(i*self.zeile) + (0.5*self.zeile)), ((j*self.spalte) + self.spalte,(i*self.zeile) + (0.5*self.zeile)), 1)
                elif board.get_boardIJ(i,j) == 3: #Vertikale Wand
                    pygame.draw.line(game.screen, 'blue', ((j*self.spalte) + (0.5*self.spalte),(i*self.zeile)), ((j*self.spalte) + (0.5*self.spalte),(i*self.zeile) + self.zeile), 3)
                elif board.get_boardIJ(i,j) == 4: #Horizontale dicke Wand
                    pygame.draw.line(game.screen, 'blue', ((j*self.spalte),(i*self.zeile) + (0.5*self.zeile)), ((j*self.spalte) + self.spalte,(i*self.zeile) + (0.5*self.zeile)), 3)
                elif board.get_boardIJ(i,j) == 5: #Kurve unten links
                    pygame.draw.arc(game.screen, 'blue', [(j*self.spalte - 0.4*self.spalte) - 3, (i*self.zeile + 0.5*self.zeile)-1, self.spalte, self.zeile], 0, pi/2, 3)
                elif board.get_boardIJ(i,j) == 6: #Kurve unten rechts
                    pygame.draw.arc(game.screen, 'blue', [(j*self.spalte + 0.5*self.spalte), (i*self.zeile + 0.5*self.zeile), self.spalte, self.zeile], pi/2, pi, 3)
                elif board.get_boardIJ(i,j) == 7: #Kurve oben rechts
                    pygame.draw.arc(game.screen, 'blue', [(j*self.spalte + 0.5*self.spalte), (i*self.zeile - 0.4*self.zeile) - 2, self.spalte, self.zeile], pi, 3*(pi/2), 3)
                elif board.get_boardIJ(i,j) == 8: # Kurve oben links
                    pygame.draw.arc(game.screen, 'blue', [(j*self.spalte - 0.5*self.spalte) , (i*self.zeile - 0.5*self.zeile)+1, self.spalte, self.zeile], 3*(pi/2), 2*pi, 3)
        self.player.draw(self.game.screen)
        pygame.display.flip()

class PauseMenu:
    def __init__(self, game):
        self.game = game
        self.title_font = pygame.font.Font(None, 74)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Resume the game
                    self.game.switch_state("game")

    def update(self):
        pass  # Pause menu is static

    def draw(self):
        self.game.screen.fill((50, 0, 0))
        pause_text = self.title_font.render("Paused", True, (255, 255, 255))
        instruction_text = pygame.font.Font(None, 36).render("Press ESC to Resume", True, (200, 200, 200))
        self.game.screen.blit(pause_text, (self.game.width // 2 - pause_text.get_width() // 2, 150))
        self.game.screen.blit(instruction_text, (self.game.width // 2 - instruction_text.get_width() // 2, 300))
        pygame.display.flip()

class Player:
    def __init__(self, x, y, gamestate):
        self.spalte = gamestate.getSpalte()
        self.zeile = gamestate.getZeile()
        self.pacman_images = []
        for i in range(0, 4):
            self.pacman_images.append(pygame.transform.scale(pygame.image.load(f'assets/pacman/pacman_{i}.png'), (30, 30)))
        self.x = x
        self.y = y
        self.arrayX = 11
        self.arrayY = 21
        self.size = 50
        self.color = (0, 255, 0)
        #self.speed = 0.1
        self.imageSkip = 0
        self.direction = 0
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction = 2
            if board.get_boardIJ(self.arrayY - 1,self.arrayX) in (0,1):
                self.y -= self.zeile
                self.arrayY -= 1
        if keys[pygame.K_DOWN]:
            self.direction = 3
            if board.get_boardIJ(self.arrayY + 1,self.arrayX) in (0,1):
                self.y += self.zeile
                self.arrayY += 1
        if keys[pygame.K_LEFT]:
            self.direction = 1
            if board.get_boardIJ(self.arrayY,self.arrayX - 1) in (0,1):
                self.x -= self.spalte
                self.arrayX -= 1
        if keys[pygame.K_RIGHT]:
            self.direction = 0
            if board.get_boardIJ(self.arrayY,self.arrayX + 1) in (0,1):
                self.x += self.spalte
                self.arrayX += 1

    def draw(self, screen):
        if self.imageSkip < 3.75:
            self.imageSkip += 0.25
        else:
            self.imageSkip = 0
        if self.direction == 0:  # direction = right
            screen.blit(self.pacman_images[int(self.imageSkip)], (self.x, self.y))
        elif self.direction == 1:  # direction = left
            screen.blit(pygame.transform.flip(self.pacman_images[int(self.imageSkip)], True, False), (self.x, self.y))
        elif self.direction == 2:  # direction = up
            screen.blit(pygame.transform.rotate(self.pacman_images[int(self.imageSkip)], 90), (self.x, self.y))
        elif self.direction == 3:  # direction = down
            screen.blit(pygame.transform.rotate(self.pacman_images[int(self.imageSkip)], 270), (self.x, self.y))

if __name__ == "__main__":
    board = Board()
    game = Game(board)
    game.run()

