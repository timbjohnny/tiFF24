import pygame
import sys
from boards import Board
from math import pi

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
            "game": GameState(self),
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
        self.title_font = pygame.font.Font(None, 74)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start the game
                    self.game.switch_state("game")

    def update(self):
        pass  # Main menu might not need updates for static screens

    def draw(self):
        self.game.screen.fill((0, 50, 100))
        title_text = self.title_font.render("Main Menu", True, (255, 255, 255))
        instruction_text = pygame.font.Font(None, 36).render("Press ENTER to Start", True, (200, 200, 200))
        self.game.screen.blit(title_text, (self.game.width // 2 - title_text.get_width() // 2, 150))
        self.game.screen.blit(instruction_text, (self.game.width // 2 - instruction_text.get_width() // 2, 300))
        pygame.display.flip()

class GameState:
    def __init__(self, game):
        self.game = game
        self.player = Player(self.game.width // 2, self.game.height // 2)

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
        self.game.screen.fill((30, 30, 30))
        for i in range(len(board.get_board())):
            for j in range(len(board.get_boardI(i))):
                if board.get_boardIJ(i,j) == 1: #Auf dem Feld ist ein Punkt zum Essen
                    pygame.draw.circle(game.screen, 'white', ((j*int(game.width / 24)) + (0.5*int(game.width / 24)),(i*int(game.height / 30)) + (0.5*int(game.height / 30))), 4)
                elif board.get_boardIJ(i,j) == 2: # Horizonatale Wand
                    pygame.draw.line(game.screen, 'white', ((j*int(game.width / 24)),(i*int(game.height / 30)) + (0.5*int(game.height / 30))), ((j*int(game.width / 24)) + int(game.width / 24),(i*int(game.height / 30)) + (0.5*int(game.height / 30))), 1)
                elif board.get_boardIJ(i,j) == 3: #Vertikale Wand
                    pygame.draw.line(game.screen, 'blue', ((j*int(game.width / 24)) + (0.5*int(game.width / 24)),(i*int(game.height / 30))), ((j*int(game.width / 24)) + (0.5*int(game.width / 24)),(i*int(game.height / 30)) + int(game.height / 30)), 3)
                elif board.get_boardIJ(i,j) == 4: #Horizontale dicke Wand
                    pygame.draw.line(game.screen, 'blue', ((j*int(game.width / 24)),(i*int(game.height / 30)) + (0.5*int(game.height / 30))), ((j*int(game.width / 24)) + int(game.width / 24),(i*int(game.height / 30)) + (0.5*int(game.height / 30))), 3)
                elif board.get_boardIJ(i,j) == 5: #Kurve unten links
                    pygame.draw.arc(game.screen, 'blue', [(j*int(game.width / 24) - 0.4*int(game.width / 24)) - 3, (i*int(game.height / 30) + 0.5*int(game.height / 30))-1, int(game.width / 24), int(game.height / 30)], 0, pi/2, 3)
                elif board.get_boardIJ(i,j) == 6: #Kurve unten rechts
                    pygame.draw.arc(game.screen, 'blue', [(j*int(game.width / 24) + 0.5*int(game.width / 24)), (i*int(game.height / 30) + 0.5*int(game.height / 30)), int(game.width / 24), int(game.height / 30)], pi/2, pi, 3)
                elif board.get_boardIJ(i,j) == 7: #Kurve oben rechts
                    pygame.draw.arc(game.screen, 'blue', [(j*int(game.width / 24) + 0.5*int(game.width / 24)), (i*int(game.height / 30) - 0.4*int(game.height / 30)) - 2, int(game.width / 24), int(game.height / 30)], pi, 3*(pi/2), 3)
                elif board.get_boardIJ(i,j) == 8: # Kurve oben links
                    pygame.draw.arc(game.screen, 'blue', [(j*int(game.width / 24) - 0.5*int(game.width / 24)) , (i*int(game.height / 30) - 0.5*int(game.height / 30))+1, int(game.width / 24), int(game.height / 30)], 3*(pi/2), 2*pi, 3)
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
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 50
        self.color = (0, 255, 0)
        self.speed = 5
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

if __name__ == "__main__":
    board = Board()
    game = Game(board)
    game.run()

