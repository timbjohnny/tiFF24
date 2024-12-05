import pygame
import sys

class Game:
    def __init__(self, width=800, height=600, fps=60):
        pygame.init()
        self.width = width
        self.height = height
        self.fps = fps
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game with States")
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
                if event.key == pygame.K_ESCAPE:  # Pause the game
                    self.game.switch_state("pause")

    def update(self):
        self.player.update()

    def draw(self):
        self.game.screen.fill((30, 30, 30))
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
    game = Game()
    game.run()

