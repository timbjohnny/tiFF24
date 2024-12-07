import string
import pygame
import sys
from boards import Board
from math import pi
import json
import os


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
        self.dir_path = os.path.dirname(__file__)
        self.name = ""
        self.score = 0

        self.pacman_images = []
        for i in range(0, 4): 
            img = pygame.image.load(f'{self.dir_path}/assets/pacman/pacman_{i}.png')
            self.pacman_images.append(pygame.transform.scale(img, (30, 30)))
        
        # blinky looking right
        self.blinkyR_images = []
        for i in range(0, 2):
            img = pygame.image.load(f'{self.dir_path}/assets/blinky/rGr_{i}.png')
            self.blinkyR_images.append(pygame.transform.scale(img, (30,30)))
        # Blinky looking down
        self.blinkyD_images = []
        for i in range(0, 2):
            img = pygame.image.load(f'{self.dir_path}/assets/blinky/rGd_{i}.png')
            self.blinkyD_images.append(pygame.transform.scale(img, (30,30)))
        # blinky looking up
        self.blinkyU_images = []
        for i in range(0, 2):
            img = pygame.image.load(f'{self.dir_path}/assets/blinky/rGu_{i}.png')
            self.blinkyU_images.append(pygame.transform.scale(img, (30,30)))
        
        # clyde looking right
        self.clydeR_images = []
        for i in range(0, 2):
            img = pygame.image.load(f'{self.dir_path}/assets/clyde/oGr_{i}.png')
            self.clydeR_images.append(pygame.transform.scale(img, (30,30)))
        # clyde looking down
        self.clydeD_images = []
        for i in range(0, 2):
            img = pygame.image.load(f'{self.dir_path}/assets/clyde/oGd_{i}.png')
            self.clydeD_images.append(pygame.transform.scale(img, (30,30)))
        # clyde looking up
        self.clydeU_images = []
        for i in range(0, 2):
            img = pygame.image.load(f'{self.dir_path}/assets/clyde/oGu_{i}.png')
            self.clydeU_images.append(pygame.transform.scale(img, (30,30)))

        # inky looking right
        self.inkyR_images = []
        for i in range(0, 2):
            img = pygame.image.load(f'{self.dir_path}/assets/inky/bGr_{i}.png')
            self.inkyR_images.append(pygame.transform.scale(img, (30,30)))
        # inky looking down
        self.inkyD_images = []
        for i in range(0, 2):
            img = pygame.image.load(f'{self.dir_path}/assets/inky/bGd_{i}.png')
            self.inkyD_images.append(pygame.transform.scale(img, (30,30)))
        # inky looking up
        self.inkyU_images = []
        for i in range(0, 2):
            img = pygame.image.load(f'{self.dir_path}/assets/inky/bGu_{i}.png')
            self.inkyU_images.append(pygame.transform.scale(img, (30,30)))
   
        # pinky looking right      
        self.pinkyR_images = []
        for i in range(0, 2):
            img = pygame.image.load(f'{self.dir_path}/assets/pinky/pGr_{i}.png')
            self.pinkyR_images.append(pygame.transform.scale(img, (30,30)))
        # pinky looking down
        self.pinkyD_images = []
        for i in range(0, 2):
            img = pygame.image.load(f'{self.dir_path}/assets/pinky/pGd_{i}.png')
            self.pinkyD_images.append(pygame.transform.scale(img, (30,30)))
        # pinky looking up
        self.pinkyU_images = []
        for i in range(0, 2):
            img = pygame.image.load(f'{self.dir_path}/assets/pinky/pGu_{i}.png')
            self.pinkyU_images.append(pygame.transform.scale(img, (30,30)))

        # vulnerable ghosts
        self.vulnerable_images = []
        for i in range(0, 2):
            img = pygame.image.load(f'{self.dir_path}/assets/vulnerable/bG_{i}.png')
            self.vulnerable_images.append(pygame.transform.scale(img, (30,30)))
        # blinking ghosts
        self.blinking_images = []
        for i in range(0, 2):
            img = pygame.image.load(f'{self.dir_path}/assets/vulnerable/wG_{i}.png')
            self.blinking_images.append(pygame.transform.scale(img, (30,30)))

        # Game states
        self.states = {
            "main_menu": MainMenu(self),
            "leaderboard": Leaderboard(self),
            "game": Gamestate(self),
            "pause": PauseMenu(self),
            "name": EnterName(self)
        }
        self.current_state = self.states["main_menu"]
        self.prev_state = None

    def switch_state(self, state_name):
        """Switch to a new state by name."""
        self.prev_state = self.current_state
        self.current_state = self.states[state_name]
        if self.current_state == self.states["game"]:
            self.states["game"].countdown()

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
        self.title_font = pygame.font.Font(f"{self.game.dir_path}/assets/MinecraftRegular-Bmg3.otf", 100)
        self.select_font = pygame.font.Font(f"{self.game.dir_path}/assets/MinecraftRegular-Bmg3.otf", 50)
        self.rect_width = 600
        self.rect_height = 130
        self.pointer_pos_x = 175
        self.pointer_pos_y = 450

        self.pacman_animstate = 0
        self.ghosts_animstate = 0
        self.ghosts_anim_dir = 1
        self.last_update_time = 0

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
        title_text = self.title_font.render("P     M  n", False, (255, 255, 255))
        self.game.screen.blit(title_text, (self.game.width // 2 - title_text.get_width() // 2, 100))
        self.game.screen.blit(pygame.transform.scale(self.game.blinkyR_images[int(self.ghosts_animstate)], (48,48)), (185, 133))
        self.game.screen.blit(pygame.transform.scale(self.game.pacman_images[int(self.pacman_animstate)], (48,48)), (255, 133))
        self.game.screen.blit(pygame.transform.scale(self.game.inkyR_images[int(self.ghosts_animstate)], (48,48)), (460, 133))
        pygame.draw.rect(self.game.screen, (0, 0, 155), (((self.game.width - self.rect_width) // 2), 80, self.rect_width, self.rect_height), 3, 8)
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
        pointer_text = self.select_font.render(">", False, (255, 255, 255))
        self.game.screen.blit(pointer_text, (self.pointer_pos_x, self.pointer_pos_y))

        # Update pacman animation state
        if self.pacman_animstate >= len(self.game.pacman_images) - 1:
            self.pacman_animstate = 0
        else:
            self.pacman_animstate += 0.15

        # Update ghost animation state depending on last time animation changed
        current_time = pygame.time.get_ticks()  # current time in ms since game started
        if current_time - self.last_update_time >= 200:
            self.last_update_time = current_time
            if self.ghosts_animstate >= len(self.game.blinkyR_images) - 1:
                self.ghosts_anim_dir = -1
            elif self.ghosts_animstate <= 0:
                self.ghosts_anim_dir = 1

            self.ghosts_animstate += 1 * self.ghosts_anim_dir
            

        pygame.display.flip()

class Leaderboard:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(f"{self.game.dir_path}/assets/MinecraftRegular-Bmg3.otf", 50)
        self.small_font = pygame.font.Font(f"{self.game.dir_path}/assets/MinecraftRegular-Bmg3.otf", 40)
        self.rect_width = 600
        self.rect_height = 130

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                        self.game.switch_state("main_menu")
                        self.rect_height = 130 # Resettet das Rechteck


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
        no_data_text_lines = [ # Text, wenn Leaderboard leer ist
        "There is no one in",
        "the Leaderboard,",
        "play some games to", 
        "get on the list!"
        ]

        if self.rect_height < 625:  # Leaderboard loading animation
            self.rect_height += 25
            pygame.time.wait(50)
        else:   # show options and leaderboard
            self.is_expanded = True
            pygame.time.wait(100)
            # show text
            self.game.screen.blit(back_text, (self.game.width // 2 - back_text.get_width() // 2, 725))
            self.game.screen.blit(pointer_text, (150, 725))
            self.game.screen.blit(leaderboard_text, (self.game.width // 2 - leaderboard_text.get_width() // 2, 100))
            self.game.screen.blit(name_text, (100, 155))
            self.game.screen.blit(score_text, (490, 155))

            with open(f"{self.game.dir_path}/assets/leaderboard.json", "r") as f:
                data = json.load(f)
                if data == {}:  # Wenn das Leaderboard leer ist, wird der Text angezeigt
                    for i in range(len(no_data_text_lines)):
                        y_offset = 50
                        text = self.small_font.render(no_data_text_lines[i], False, (255, 255, 255))
                        self.game.screen.blit(text, (self.game.width // 2 - text.get_width() // 2, 300 + y_offset * i))
                else:
                    # Leaderboard der Score größe nach sortieren
                    sorted_data = {key: value for key, value in
                            sorted(data.items(), key=lambda item: item[1][0]['score'], reverse=True)}
                # Die Sortierten keys durchgehen und die Namen und Scores rendern
                    for i, (key, value) in enumerate(sorted_data.items()):
                        player_name = value[0]["name"]
                        player_score = value[0]["score"]
                        # Render player name centered relative to header
                        names_text = self.small_font.render(player_name, False, (255, 255, 255))
                        name_x = 100 + ((name_text.get_width() - names_text.get_width()) // 2)
                        name_y = 200 + 38 * i
                        self.game.screen.blit(names_text, (name_x, name_y))
                        # Render player score centered relative to header
                        scores_text = self.small_font.render(str(player_score), False, (255, 255, 255))
                        score_x = 490 + ((score_text.get_width() - scores_text.get_width()) // 2)
                        score_y = 200 + 38 * i
                        self.game.screen.blit(scores_text, (score_x, score_y))

        pygame.display.flip()

class Gamestate:
    def __init__(self, game):
        self.game = game
        self.level = 2
        if self.level == 1:
            self.spalte = int(game.width / 24)
            self.zeile = int(game.height / 30)
        elif self.level == 2:
            self.spalte = int(game.width / 16)
            self.zeile = int(game.height / 22)    
        self.score = 0
        if self.level == 1:
            self.player = Player(11* self.spalte, 21*self.zeile, self) # x,y Startposition
            self.blinky = Blinky(11*self.spalte, 11*self.zeile, self)
            self.inky = Inky(300, 337, self)
            self.pinky = Pinky(345, 337, self)
            self.clyde = Clyde(390, 337, self)
        elif self.level == 2:
            self.player = Player(7* self.spalte, 17*self.zeile, self) # x,y Startposition
            self.blinky = Blinky(7*self.spalte, 7*self.zeile, self)
            self.inky = Inky(300, 337, self)
            self.pinky = Pinky(345, 337, self)
            self.clyde = Clyde(390, 337, self)
        self.spalte = int(game.width / 24)
        self.zeile = int(game.height / 30)
        self.game.score = 0
        self.player = Player(11* self.spalte, 21*self.zeile, self) # x,y Startposition
        self.blinky = Blinky(11*self.spalte, 11*self.zeile, self)
        self.inky = Inky(300, 337, self)
        self.pinky = Pinky(345, 337, self)
        self.clyde = Clyde(390, 337, self)
        
        
    def resetGamestate(self):
        board.resetBoard()
        self.game = game
        self.level = 2
        if self.level == 1:
            self.spalte = int(game.width / 24)
            self.zeile = int(game.height / 30)
        elif self.level == 2:
            self.spalte = int(game.width / 16)
            self.zeile = int(game.height / 22)    
        self.game.score = 0
        if self.level == 1:
            self.player = Player(11* self.spalte, 21*self.zeile, self) # x,y Startposition
        self.blinky = Blinky(11*self.spalte, 11*self.zeile, self)
        self.inky = Inky(300, 337, self)
        self.pinky = Pinky(345, 337, self)
        self.clyde = Clyde(390, 337, self)
        
        
    def resetGamestate(self):
        board.resetBoard()
        self.game = game
        self.spalte = int(game.width / 24)
        self.zeile = int(game.height / 30)
        # Score reset in Enter Name verlagert
        self.player = Player(11* self.spalte, 21*self.zeile, self) # x,y Startposition
        if self.level == 1:
            self.blinky = Blinky(11*self.spalte, 11*self.zeile, self)
            self.inky = Inky(300, 337, self)
            self.pinky = Pinky(345, 337, self)
            self.clyde = Clyde(390, 337, self)
        elif self.level == 2:
            self.player = Player(7* self.spalte, 17*self.zeile, self) # x,y Startposition
            self.blinky = Blinky(7*self.spalte, 7*self.zeile, self)
            self.inky = Inky(300, 337, self)
            self.pinky = Pinky(345, 337, self)
            self.clyde = Clyde(390, 337, self) 
    
    def getLevel(self):
        return self.level
    def getZeile(self):
        return self.zeile
    
    def getSpalte(self):
        return self.spalte
    def getPlayer(self):
        return self.player
    
    def handle_events(self):
        for event in pygame.event.get():
            self.player.handle_events(event)
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # Pause the game
                    self.game.switch_state("pause")

    def update(self):
        self.player.update()
        self.blinky.update()
        
    def countdown(self):
        if self.game.prev_state == self.game.states["main_menu"]:
            font = pygame.font.Font(f'{self.game.dir_path}/assets/MinecraftRegular-Bmg3.otf', 230)  # Larger font for countdown
            messages = ["Ready", "3", "2", "1", "Go!"]
            pygame.mixer.music.load(f'{self.game.dir_path}/sounds/pacman_beginning.wav')
            pygame.mixer.music.play(0, 0.0)
            pygame.mixer.music.set_volume(0.2)
            for message in(messages):
                self.game.screen.fill('black')  # Cover the screen with black, but we’ll draw the game below
                self.draw()
                text = font.render(message, True, 'red')
                text_rect = text.get_rect(center=(self.game.width // 2, self.game.height // 2))
                self.game.screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.delay(1000)  # Wait for 1 second

    def draw_score(self):
        # Show the score in bottom left corner
        font = pygame.font.Font(f'{self.game.dir_path}/assets/MinecraftRegular-Bmg3.otf', 48)
        text = font.render(f"Score: {self.game.score}", True, 'white')
        self.game.screen.blit(text, (15, 735))
        
    def draw_lives(self):
        font = pygame.font.Font(f'{self.game.dir_path}/assets/MinecraftRegular-Bmg3.otf', 48)
        text = font.render(f"Lives: ", True, 'white')
        self.game.screen.blit(text, (400, 735))
        if int(self.player.lives) == 3:
            self.game.screen.blit(pygame.transform.scale(self.player.pacman_images[1], (48, 48)), (550 + (0* 50), 735))
            self.game.screen.blit(pygame.transform.scale(self.player.pacman_images[1], (48, 48)), (550 + (1* 50), 735))
            self.game.screen.blit(pygame.transform.scale(self.player.pacman_images[1], (48, 48)), (550 + (2* 50), 735))
        elif int(self.player.lives) == 2:
            self.game.screen.blit(pygame.transform.scale(self.player.pacman_images[1], (48, 48)), (550 + (0* 50), 735))
            self.game.screen.blit(pygame.transform.scale(self.player.pacman_images[1], (48, 48)), (550 + (1* 50), 735))
        elif int(self.player.lives) == 1:
            self.game.screen.blit(pygame.transform.scale(self.player.pacman_images[1], (48, 48)), (550 + (0* 50), 735))
        elif int(self.player.lives) == 0:
            self.gameOver()
            
    def gameOver(self):
        # Hintergrund schwarz
        pygame.mixer.music.load(f'{self.game.dir_path}/sounds/pacman_death.mp3')
        pygame.mixer.music.play(1, 0.0)
        pygame.mixer.music.set_volume(0.2)
        self.game.screen.fill('black')
        # Anzeige des "Victory!"-Textes
        font_defeat = pygame.font.Font(f'{self.game.dir_path}/assets/MinecraftRegular-Bmg3.otf', 100)
        text_defeat = font_defeat.render("GAME OVER!", True, 'red')
        text_defeat_rect = text_defeat.get_rect(center=(game.width // 2, game.height // 2 - 100))  # Etwas nach oben verschoben
        self.game.screen.blit(text_defeat, text_defeat_rect)
        # Anzeige des Scores
        font_score = pygame.font.Font(f'{self.game.dir_path}/assets/MinecraftRegular-Bmg3.otf', 80)
        text_score = font_score.render(f"Score: {self.game.score}", True, 'white')
        text_score_rect = text_score.get_rect(center=(game.width // 2, game.height // 2 + 100))  # Etwas nach unten verschoben
        self.game.screen.blit(text_score, text_score_rect)
        # Bildschirm aktualisieren
        pygame.display.flip()
        pygame.time.delay(5000)  # 3 Sekunden warten     
        self.resetGamestate()     
        self.game.switch_state("main_menu") 
         
      
    def victoryScreen(self):
        self.game.screen.fill('black')
        pygame.mixer.music.load(f'{self.game.dir_path}/sounds/pacman_victory.mp3')
        pygame.mixer.music.play(1, 0.0)
        pygame.mixer.music.set_volume(0.2)

        font_victory = pygame.font.Font(f'{self.game.dir_path}/assets/MinecraftRegular-Bmg3.otf', 150)
        text_victory = font_victory.render("Victory!", True, 'yellow')
        text_victory_rect = text_victory.get_rect(center=(self.game.width // 2, self.game.height // 2 - 100))
        self.game.screen.blit(text_victory, text_victory_rect)

        font_score = pygame.font.Font(f'{self.game.dir_path}/assets/MinecraftRegular-Bmg3.otf', 100)
        text_score = font_score.render(f"Score: {self.game.score}", True, 'white')
        text_score_rect = text_score.get_rect(center=(self.game.width // 2, self.game.height // 2 + 100))  # Etwas nach unten verschoben
        text_score = font_score.render(f"Score: {self.score}", True, 'white')
        text_score_rect = text_score.get_rect(center=(self.game.width // 2, self.game.height // 2 + 100))
        self.game.screen.blit(text_score, text_score_rect)

        pygame.display.flip()
        pygame.time.delay(6000)  # 3 Sekunden warten
        board.resetBoard()
        self.resetGamestate()
        self.game.switch_state("name") 
        self.resetGamestate() 
        self.game.switch_state("main_menu") 
                

    def draw(self):
        self.game.screen.fill((0, 0, 0))
        self.drawBoard()
        self.draw_lives()
        self.player.draw(self.game.screen)
        self.blinky.draw(self.game.screen)
        self.inky.draw(self.game.screen)
        self.pinky.draw(self.game.screen)
        self.clyde.draw(self.game.screen)
        self.draw_score()
        if board.checkVictory(self.level):
            self.victoryScreen()            
        pygame.display.flip()
    
    def drawBoard(self):    
        for i in range(len(board.get_board(self.level))):
            for j in range(len(board.get_boardI(self.level, i))):
                val = board.get_boardIJ(self.level, i,j)
                if val == 1: # Punkt
                    pygame.draw.circle(self.game.screen, 'white', ((j*self.spalte) + (0.5*self.spalte),(i*self.zeile) + (0.5*self.zeile)), 4)
                elif val == 2: # Horizontale Wand (dünn)
                    pygame.draw.line(self.game.screen, 'white', ((j*self.spalte),(i*self.zeile) + (0.5*self.zeile)), ((j*self.spalte) + self.spalte,(i*self.zeile) + (0.5*self.zeile)), 1)
                elif val == 3: #Vertikale Wand (dick)
                    pygame.draw.line(self.game.screen, 'blue', ((j*self.spalte) + (0.5*self.spalte),(i*self.zeile)), ((j*self.spalte) + (0.5*self.spalte),(i*self.zeile) + self.zeile), 3)
                elif val == 4: #Horizontale dicke Wand
                    pygame.draw.line(self.game.screen, 'blue', ((j*self.spalte),(i*self.zeile) + (0.5*self.zeile)), ((j*self.spalte) + self.spalte,(i*self.zeile) + (0.5*self.zeile)), 3)
                elif val == 5: #Kurve unten links
                    pygame.draw.arc(self.game.screen, 'blue', [(j*self.spalte - 0.4*self.spalte) - 3, (i*self.zeile + 0.5*self.zeile)-1, self.spalte, self.zeile], 0, pi/2, 3)
                elif val == 6: #Kurve unten rechts
                    pygame.draw.arc(self.game.screen, 'blue', [(j*self.spalte + 0.5*self.spalte), (i*self.zeile + 0.5*self.zeile), self.spalte, self.zeile], pi/2, pi, 3)
                elif val == 7: #Kurve oben rechts
                    pygame.draw.arc(self.game.screen, 'blue', [(j*self.spalte + 0.5*self.spalte), (i*self.zeile - 0.4*self.zeile) - 2, self.spalte, self.zeile], pi, 3*(pi/2), 3)
                elif val == 8: # Kurve oben links
                    pygame.draw.arc(self.game.screen, 'blue', [(j*self.spalte - 0.5*self.spalte) , (i*self.zeile - 0.5*self.zeile)+1, self.spalte, self.zeile], 3*(pi/2), 2*pi, 3)


class PauseMenu:
    def __init__(self, game):
        self.game = game
        self.title_font = pygame.font.Font(f"{self.game.dir_path}/assets/MinecraftRegular-Bmg3.otf", 74)

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
        pause_text = self.title_font.render("Paused", True, (200, 200, 200))
        instruction_text = pygame.font.Font(f"{self.game.dir_path}/assets/MinecraftRegular-Bmg3.otf", 36).render("Press ESC to Resume", True, (200, 200, 200))
        self.game.screen.blit(pause_text, (self.game.width // 2 - pause_text.get_width() // 2, 150))
        self.game.screen.blit(instruction_text, (self.game.width // 2 - instruction_text.get_width() // 2, 300))
        pygame.display.flip()

class EnterName:
    def __init__(self, game):
        self.game = game
        self.alphabet = list(string.ascii_uppercase)
        self.font = pygame.font.Font(f"{game.dir_path}/assets/MinecraftRegular-Bmg3.otf", 50)
        self.letters_text = self.font.render(self.alphabet[0], True, (255, 255, 255))
        self.letter_0 = 0 # Index für Namenseingabe des ersten buchstaben => A
        self.letter_1 = 0 # Index für Namenseingabe des zweiten buchstaben => A
        self.letter_2 = 0 # Index für Namenseingabe des dritten buchstaben => A
        self.pointer_pos_x = 300

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT: # pointer nach rechts verschieben
                    if self.pointer_pos_x != 400:
                        self.pointer_pos_x += 50
                elif event.key == pygame.K_LEFT: # pointer nach links verschieben
                    if self.pointer_pos_x != 300:
                        self.pointer_pos_x -= 50
                elif event.key == pygame.K_UP: # Buchstabe hoch
                    match self.pointer_pos_x:
                        case 300:
                            if self.letter_0 == 0:
                                self.letter_0 = 25
                            else:
                                self.letter_0 -= 1
                        case 350:
                            if self.letter_1 == 0:
                                self.letter_1 = 25
                            else:
                                self.letter_1 -= 1
                        case 400:
                            if self.letter_2 == 0:
                                self.letter_2 = 25
                            else:
                                self.letter_2 -= 1
                elif event.key == pygame.K_DOWN: # Buchstabe runter
                    match self.pointer_pos_x:
                        case 300:
                            if self.letter_0 == 25:
                                self.letter_0 = 0
                            else:
                                self.letter_0 += 1
                        case 350:
                            if self.letter_1 == 25:
                                self.letter_1 = 0
                            else:
                                self.letter_1 += 1
                        case 400:
                            if self.letter_2 == 25:
                                self.letter_2 = 0
                            else:
                                self.letter_2 += 1
                elif event.key == pygame.K_RETURN: # Enter um zurück ins hauptmenü
                    self.game.name = self.alphabet[self.letter_0] + self.alphabet[self.letter_1] + self.alphabet[self.letter_2]
                    self.write_to_file()
                    self.game.switch_state("main_menu")
                    self.game.score = 0
    def update(self):
        pass

    def change_letter(self):    # Buchstaben ändern und pointer anzeigen
        pointer_up = self.font.render("^", True, (255, 255, 255))
        pointer_down = pygame.transform.rotate(pointer_up, 180)
        self.game.screen.blit(pointer_up, (self.pointer_pos_x, 270))
        self.game.screen.blit(pointer_down, (self.pointer_pos_x - 5, 327)) # 5px nach links verschoben, da pfeil sonst wegen rotation nicht zentriert ist

    def write_to_file(self):
        with open(f"{self.game.dir_path}/assets/leaderboard.json", "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}

        # Create a new object with the desired elements
        new_entry = {
            "name": self.game.name,
            "score": self.game.score
        }

        data[len(data)] = [new_entry]

        # Write the updated data back to the JSON file
        if data != {}:
            with open(f"{self.game.dir_path}/assets/leaderboard.json", "w") as f:
                json.dump(data, f, indent=4)
        else:
            print("Error occurred trying to write file.")

    def draw(self):
        self.game.screen.fill((0, 0, 0))
        enter_name_text = self.font.render("Enter your name:", True, (255, 255, 255))
        self.game.screen.blit(enter_name_text, (self.game.width // 2 - enter_name_text.get_width() // 2, 100)) # Zentriert Text
        self.game.screen.blit(self.font.render(self.alphabet[self.letter_0], True, (255, 255, 255)), (300, 300))
        self.game.screen.blit(self.font.render(self.alphabet[self.letter_1], True, (255, 255, 255)), (350, 300))
        self.game.screen.blit(self.font.render(self.alphabet[self.letter_2], True, (255, 255, 255)), (400, 300))
        self.change_letter()
        press_enter_text = self.font.render("Press enter to continue", True, (255, 255, 255))
        self.game.screen.blit(press_enter_text, (self.game.width // 2 - press_enter_text.get_width() // 2, 500)) # Zentriert Text
        pygame.display.flip()


class Player:
    def __init__(self, x, y, gamestate):
        self.spalte = gamestate.getSpalte()
        self.zeile = gamestate.getZeile()
        self.level = gamestate.getLevel()
        self.pacman_images = gamestate.game.pacman_images
        self.game = gamestate.game
        self.gamestate = gamestate
        self.x = x
        self.y = y
        if self.level == 1:
            self.arrayX = 11
            self.arrayY = 21
        elif self.level == 2:
            self.arrayX = 7
            self.arrayY = 17
            
        self.targetX = x
        self.targetY = y
        self.size = 50
        self.speed = 5
        self.imageSkip = 0
        self.direction = 0
        self.buffer_direction = 0
        self.lives = 3
        self.move_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.move_event, 180)
        
        
    def handle_events(self, event):
        """Verarbeitet Tasteneingaben."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.buffer_direction = 0
            elif event.key == pygame.K_LEFT:
                self.buffer_direction = 1
            elif event.key == pygame.K_UP:
                self.buffer_direction = 2
            elif event.key == pygame.K_DOWN:
                self.buffer_direction = 3

    def handle_direction(self):
        # Change direction if no obstacle, and buffer direction
        match self.buffer_direction:
            case 0: # Right
                if self.arrayX == len(board.get_boardI(self.level, self.arrayY)) - 1:
                    self.arrayX= 0
                    self.x = -self.spalte
                    self.targetX = 0
                if board.get_boardIJ(self.level, self.arrayY, self.arrayX + 1) in (0, 1):
                    self.direction = 0
            case 1: # Left
                if board.get_boardIJ(self.level, self.arrayY, self.arrayX - 1) in (0, 1):
                    self.direction = 1
            case 2: # Up
                if board.get_boardIJ(self.level, self.arrayY - 1, self.arrayX) in (0, 1):
                    self.direction = 2
            case 3: # Down
                if board.get_boardIJ(self.level, self.arrayY + 1, self.arrayX) in (0, 1):
                    self.direction = 3

    def update(self):
        """Aktualisiert die Position."""
        self.handle_direction()
        if self.x < self.targetX:
            self.x += self.speed
        elif self.x > self.targetX:
            self.x -= self.speed
        if self.y < self.targetY:
            self.y += self.speed
        elif self.y > self.targetY:
            self.y -= self.speed

        # Runde Positionen ab, wenn Ziel erreicht
        if abs(self.x - self.targetX) < self.speed:
            self.x = self.targetX
        if abs(self.y - self.targetY) < self.speed:
            self.y = self.targetY

        # Bewegung nur ausführen, wenn Ziel erreicht ist
        if self.x == self.targetX and self.y == self.targetY and self.direction is not None:
            if self.arrayX == len(board.get_boardI(self.level, self.arrayY)) - 1 and self.direction == 0:
                self.arrayX= 0
                self.x = -self.spalte
                self.targetX = 0
            elif self.arrayX == 0 and self.direction == 1:
                self.arrayX = len(board.get_boardI(self.level, self.arrayY)) - 1
                self.x = self.spalte * len(board.get_boardI(self.level, self.arrayY))
                self.targetX = (self.spalte - 1) * len(board.get_boardI(self.level, self.arrayY))
            if self.direction == 0 and board.get_boardIJ(self.level, self.arrayY, self.arrayX + 1) in (0, 1):  # Rechts
                self.targetX += self.spalte
                self.arrayX += 1
                if board.get_boardIJ(self.arrayY, self.arrayX) == 1:
                    board.set_boardXY(self.arrayY, self.arrayX, 0)
                    self.game.score += 10
            elif self.direction == 1 and board.get_boardIJ(self.arrayY, self.arrayX - 1) in (0, 1):  # Links
                if board.get_boardIJ(self.level, self.arrayY, self.arrayX) == 1:
                    board.set_boardXY(self.level, self.arrayY, self.arrayX, 0)
                    self.gamestate.score += 10
            elif self.direction == 1 and board.get_boardIJ(self.level, self.arrayY, self.arrayX - 1) in (0, 1):  # Links
                self.targetX -= self.spalte
                self.arrayX -= 1
                if board.get_boardIJ(self.arrayY, self.arrayX) == 1:
                    board.set_boardXY(self.arrayY, self.arrayX, 0)
                    self.game.score += 10
            elif self.direction == 2 and board.get_boardIJ(self.arrayY - 1, self.arrayX) in (0, 1):  # Oben
                if board.get_boardIJ(self.level, self.arrayY, self.arrayX) == 1:
                    board.set_boardXY(self.level, self.arrayY, self.arrayX, 0)
                    self.gamestate.score += 10
            elif self.direction == 2 and board.get_boardIJ(self.level, self.arrayY - 1, self.arrayX) in (0, 1):  # Oben
                self.targetY -= self.zeile
                self.arrayY -= 1
                if board.get_boardIJ(self.arrayY, self.arrayX) == 1:
                    board.set_boardXY(self.arrayY, self.arrayX, 0)
                    self.game.score += 10
            elif self.direction == 3 and board.get_boardIJ(self.arrayY + 1, self.arrayX) in (0, 1):  # Unten
                if board.get_boardIJ(self.level, self.arrayY, self.arrayX) == 1:
                    board.set_boardXY(self.level, self.arrayY, self.arrayX, 0)
                    self.gamestate.score += 10
            elif self.direction == 3 and board.get_boardIJ(self.level, self.arrayY + 1, self.arrayX) in (0, 1):  # Unten
                self.targetY += self.zeile
                self.arrayY += 1
                if board.get_boardIJ(self.arrayY, self.arrayX) == 1:
                    board.set_boardXY(self.arrayY, self.arrayX, 0)
                    self.game.score += 10
                if board.get_boardIJ(self.level, self.arrayY, self.arrayX) == 1:
                    board.set_boardXY(self.level, self.arrayY, self.arrayX, 0)
                    self.gamestate.score += 10
                
    def draw(self, screen):
        if self.imageSkip < 3.75:
            self.imageSkip += 0.25
        else:
            self.imageSkip = 0
        if self.direction == 0:  # right
            screen.blit(self.pacman_images[int(self.imageSkip)], (self.x, self.y))
        elif self.direction == 1:  # left
            screen.blit(pygame.transform.flip(self.pacman_images[int(self.imageSkip)], True, False), (self.x, self.y))
        elif self.direction == 2:  # up
            screen.blit(pygame.transform.rotate(self.pacman_images[int(self.imageSkip)], 90), (self.x, self.y))
        elif self.direction == 3:  # down
            screen.blit(pygame.transform.rotate(self.pacman_images[int(self.imageSkip)], 270), (self.x, self.y))

class Blinky:
    def __init__(self, x, y, gamestate):
        self.gamestate = gamestate
        self.spalte = self.gamestate.getSpalte()
        self.zeile = self.gamestate.getZeile()
        self.game = self.gamestate.game
        self.level = self.gamestate.getLevel()
        self.x = x
        self.y = y
        if self.level == 1:
            self.arrayX = 11
            self.arrayY = 11
        elif self.level == 2:
            self.arrayX = 7
            self.arrayY = 7                
        self.targetX = x
        self.targetY = y
        self.speed = 2
        self.direction = None
        self.player = gamestate.getPlayer()
        self.moveable = []
        self.lastmove = []

    def update(self):
        print(f"Blinky position: ({self.x}, {self.y}), Player position: ({self.player.x}, {self.player.y})")
        if self.x < self.targetX:
            self.x += self.speed
        elif self.x > self.targetX:
            self.x -= self.speed
        if self.y < self.targetY:
            self.y += self.speed
        elif self.y > self.targetY:
            self.y -= self.speed
                
        if self.x == self.targetX and self.y == self.targetY and self.direction is not None:
            if board.get_boardIJ(self.arrayY, self.arrayX + 1) in (0, 1):  # Rechts
                self.targetX += self.spalte
                self.arrayX += 1

    def handle_events(self, event):
        pass

    def draw(self, screen):
        screen.blit(self.game.blinkyR_images[int(self.ghosts_animstate)], (self.x, self.y))

        current_time = pygame.time.get_ticks()  # current time in ms since game started
        if current_time - self.last_update_time >= 200:
            self.last_update_time = current_time
            if self.ghosts_animstate >= len(self.game.blinkyR_images) - 1:
                self.ghosts_anim_dir = -1
            elif self.ghosts_animstate <= 0:
                self.ghosts_anim_dir = 1

            self.ghosts_animstate += 1 * self.ghosts_anim_dir

    def __init__(self, x, y, gamestate):
        self.spalte = gamestate.getSpalte()
        self.zeile = gamestate.getZeile()
        self.blinky_images = gamestate.game.blinkyR_images
        self.game = gamestate.game
        self.x = x
        self.y = y
        self.arrayX = 11
        self.arrayY = 11
        self.imageSkip = 0
        self.ghosts_animstate = 0
        self.ghosts_anim_dir = 1
        self.last_update_time = 0
        self.way = {}

        self.targetX = x
        self.targetY = y
        self.speed = 2
        self.direction = 0
        self.visited = []
        self.queue = []
        self.player = gamestate.getPlayer()
        self.moveable = []
        self.lastmove = []

    def update(self):
        if self.x == self.targetX and self.y == self.targetY:
            start_x, start_y = self.arrayX, self.arrayY
            goal_x, goal_y = self.player.arrayX, self.player.arrayY
            move = self.find_path_bfs(start_x, start_y, goal_x, goal_y, board)
            
            if move is not None:
                dx, dy = move
                self.arrayX += dx
                self.arrayY += dy
                self.targetX = self.arrayX * self.spalte
                self.targetY = self.arrayY * self.zeile

        if self.x < self.targetX:
            self.x += self.speed
        elif self.x > self.targetX:
            self.x -= self.speed
        if self.y < self.targetY:
            self.y += self.speed
        elif self.y > self.targetY:
            self.y -= self.speed

        # Tunnel-Logik wurde entfernt
        # Kein Wechsel von arrayX am linken/rechten Rand

    def draw(self, screen):
        screen.blit(self.blinky_images[int(self.ghosts_animstate)], (self.x, self.y))
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time >= 200:
            self.last_update_time = current_time
            if self.ghosts_animstate >= len(self.blinky_images) - 1:
                self.ghosts_anim_dir = -1
            elif self.ghosts_animstate <= 0:
                self.ghosts_anim_dir = 1
            self.ghosts_animstate += self.ghosts_anim_dir



class Inky:
    def __init__(self, x, y, gamestate):
        self.spalte = gamestate.getSpalte()
        self.zeile = gamestate.getZeile()
        self.inky_images = gamestate.game.inkyD_images
        self.game = gamestate.game
        self.x = x
        self.y = y
        self.ghosts_animstate = 0
        self.ghosts_anim_dir = 1
        self.last_update_time = 0

    def handle_events(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.game.inkyR_images[int(self.ghosts_animstate)], (self.x, self.y))
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time >= 200:
            self.last_update_time = current_time
            if self.ghosts_animstate >= len(self.game.inkyR_images) - 1:
                self.ghosts_anim_dir = -1
            elif self.ghosts_animstate <= 0:
                self.ghosts_anim_dir = 1
            self.ghosts_animstate += self.ghosts_anim_dir

class Clyde:
    def __init__(self, x, y, gamestate):
        self.spalte = gamestate.getSpalte()
        self.zeile = gamestate.getZeile()
        self.clyde_images = gamestate.game.clydeR_images
        self.game = gamestate.game
        self.x = x
        self.y = y
        self.ghosts_animstate = 0
        self.ghosts_anim_dir = 1
        self.last_update_time = 0

    def handle_events(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.game.clydeR_images[int(self.ghosts_animstate)], (self.x, self.y))
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time >= 200:
            self.last_update_time = current_time
            if self.ghosts_animstate >= len(self.clyde_images) - 1:
                self.ghosts_anim_dir = -1
            elif self.ghosts_animstate <= 0:
                self.ghosts_anim_dir = 1
            self.ghosts_animstate += self.ghosts_anim_dir

class Pinky:
    def __init__(self, x, y, gamestate):
        self.spalte = gamestate.getSpalte()
        self.zeile = gamestate.getZeile()
        self.pinky_images = gamestate.game.pinkyR_images
        self.game = gamestate.game
        self.x = x
        self.y = y
        self.ghosts_animstate = 0
        self.ghosts_anim_dir = 1
        self.last_update_time = 0

    def handle_events(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.game.pinkyR_images[int(self.ghosts_animstate)], (self.x, self.y))
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time >= 200:
            self.last_update_time = current_time
            if self.ghosts_animstate >= len(self.pinky_images) - 1:
                self.ghosts_anim_dir = -1
            elif self.ghosts_animstate <= 0:
                self.ghosts_anim_dir = 1
            self.ghosts_animstate += self.ghosts_anim_dir

if __name__ == "__main__":
    board = Board()
    game = Game(board)
    game.run()
