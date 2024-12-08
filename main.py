import string
import pygame
import sys
from boards import Board
from math import pi
import json
import os
import random


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
        self.score = 0
        self.dir_path = os.path.dirname(__file__)
        self.level = 1
        self.multiplier = 1

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
            "select": LevelSelect(self),
            "pause": PauseMenu(self),
            "name": EnterName(self),
            "level_editor": LevelEditor(self)
        }
        self.current_state = self.states["main_menu"]
        self.prev_state = None

    def switch_state(self, state_name):
        """Switch to a new state by name."""
        self.prev_state = self.current_state
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
                            self.game.switch_state("select")  # startet spiel
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
                elif event.key == pygame.K_l:
                    self.game.switch_state("level_editor")



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

class LevelEditor:
    def __init__(self, game):
        self.game = game
        self.rows = 32
        self.cols = 28
        self.cell_size = min(self.game.width // self.cols, (self.game.height * 0.90)// self.rows)
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.selected_tile = 0
        
        # Define tile types
        self.tiles = {
            0: "empty",
            1: "dot",
            2: "wall_h",
            3: "wall_v", 
            4: "wall_thick",
            5: "curve_bl",
            6: "curve_br",
            7: "curve_tr",
            8: "curve_tl",
            9: "power"
        }

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get mouse position and convert to grid coordinates
                mouse_pos = pygame.mouse.get_pos()
                grid_x = int(mouse_pos[0] // self.cell_size)
                grid_y = int(mouse_pos[1] // self.cell_size)
                
                # Place selected tile if within grid bounds
                if 0 <= grid_x < self.cols and 0 <= grid_y < self.rows:
                    if event.button == 1:  # Left click
                        self.grid[grid_y][grid_x] = self.selected_tile
                    elif event.button == 3:  # Right click
                        self.grid[grid_y][grid_x] = 0
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.save_level()
                elif event.key == pygame.K_l:
                    self.load_level()
                elif event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, 
                                 pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                    self.selected_tile = int(event.unicode)

    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(col * self.cell_size, row * self.cell_size, 
                                 self.cell_size, self.cell_size)
                pygame.draw.rect(self.game.screen, (50, 50, 50), rect, 1)

    def draw_tiles(self):
        for row in range(self.rows):
            for col in range(self.cols):
                tile_type = self.grid[row][col]
                if tile_type != 0:
                    x = col * self.cell_size + self.cell_size // 2 # Koordinaten, wo tiles platziert werden (zentriert)
                    y = row * self.cell_size + self.cell_size // 2
                    
                    if tile_type == 1:  # Punkt
                        pygame.draw.circle(self.game.screen, 'white', (x, y), 4)
                    elif tile_type == 2:  # Horizontale wand (dünn)
                        pygame.draw.line(self.game.screen, 'white', 
                                       (x - self.cell_size//2, y),
                                       (x + self.cell_size//2, y), 1)
                    elif tile_type == 3:  # Vertikale wand (dick)
                        pygame.draw.line(self.game.screen, 'blue',
                                       (x, y - self.cell_size//2),
                                       (x, y + self.cell_size//2), 4)
                    elif tile_type == 4:  # horizontale dicke wand
                        pygame.draw.line(self.game.screen, 'blue', 
                                         (x - self.cell_size//2,y), 
                                         (x + self.cell_size//2,y), 4)
                    elif tile_type == 5:  # Kurve unten links
                        pygame.draw.arc(self.game.screen, 'blue', [x - self.cell_size, y, self.cell_size, self.cell_size],
                                                                    0, pi/2, 3)
                    elif tile_type == 6:  # Kurve unten rechts
                        pygame.draw.arc(self.game.screen, 'blue', [x, y, self.cell_size, self.cell_size],
                                                                    pi/2, pi, 3) 
                    elif tile_type == 7:  # Kurve oben rechts
                        pygame.draw.arc(self.game.screen, 'blue', [x, y - self.cell_size, self.cell_size, self.cell_size],
                                                                    pi, 3*pi/2, 3)
                    elif tile_type == 8:  # Kurve oben links
                        pygame.draw.arc(self.game.screen, 'blue', [x - self.cell_size, y - self.cell_size, self.cell_size, self.cell_size],
                                                                    3*pi/2, 2*pi, 3) 
                    elif tile_type == 9:  # Power 
                        pygame.draw.circle(self.game.screen, 'white', (x, y), 8)


    def draw_ui(self):
        # Draw currently selected tile
        font = pygame.font.Font(f"{self.game.dir_path}/assets/MinecraftRegular-Bmg3.otf", 36)
        text = font.render(f"Selected:", True, (255, 255, 255))
        # Das korrekte tile anzeigen
        for i in enumerate(self.tiles):
            match self.selected_tile:
                case 0: pass
                case i: self.game.screen.blit(pygame.image.load(f"{self.game.dir_path}/assets/tiles/tile_"+str(i)+".png"), ((180, self.game.height - 80)))

        self.game.screen.blit(text, (10, self.game.height - 40))

    def save_level(self):
        new_level = {
            "level_data": self.grid,
            "rows": self.rows,
            "cols": self.cols
        }
        with open(f"{self.game.dir_path}/assets/custom_level.json", "w") as f:
            # Create the JSON string with minimal formatting
            json_str = json.dumps(new_level, separators=(',', ':'))
            
            # Add line breaks after each row
            formatted_str = json_str.replace("],", "],\n")
            
            # Write the formatted string to file
            f.write(formatted_str)

    def load_level(self):
        try:
            with open(f"{self.game.dir_path}/assets/custom_level.json", "r") as f:
                data = json.load(f)
                # Extract only the level_data field
                self.grid = data["level_data"]
        except FileNotFoundError:
            print("Level file not found")
        except KeyError:
            print("Level data not found in file")

    def draw(self):
        self.game.screen.fill((0, 0, 0))
        self.draw_grid()
        self.draw_tiles()
        self.draw_ui()
        pygame.display.flip()
    
    def update(self):
        pass


    

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

class LevelSelect:
    def __init__(self,game):
        self.game = game
        self.title_font = pygame.font.Font(f"{self.game.dir_path}/assets/MinecraftRegular-Bmg3.otf", 74)
        self.select_font = pygame.font.Font(f"{self.game.dir_path}/assets/MinecraftRegular-Bmg3.otf", 50)
        self.pointer_pos_x = 225
        self.pointer_pos_y = 300

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    match self.pointer_pos_y:
                        case 300: 
                            self.game.level = 1
                            self.game.states["game"] = Gamestate(self.game, self.game.level)
                            self.game.switch_state("game")
                            self.game.states["game"].countdown()
                        case 375: 
                            self.game.level = 2
                            self.game.states["game"] = Gamestate(self.game, self.game.level)
                            self.game.switch_state("game")
                            self.game.states["game"].countdown()
                        case 450: 
                            self.game.level = 3
                            self.game.states["game"] = Gamestate(self.game, self.game.level)
                            self.game.switch_state("game")
                            self.game.states["game"].countdown()
                        case 600: self.game.switch_state("main_menu")
                elif event.key == pygame.K_UP:
                    match self.pointer_pos_y:
                        case 375:
                            self.pointer_pos_y -= 75
                            self.pointer_pos_x = 225
                        case 450:
                            self.pointer_pos_y -= 75
                            self.pointer_pos_x = 225
                        case 600:
                            self.pointer_pos_y -= 150
                            self.pointer_pos_x = 225
                elif event.key == pygame.K_DOWN:
                    match self.pointer_pos_y:
                        case 300:
                            self.pointer_pos_y += 75
                            self.pointer_pos_x = 225
                        case 375:
                            self.pointer_pos_y += 75
                            self.pointer_pos_x = 225
                        case 450:
                            self.pointer_pos_y += 150
                            self.pointer_pos_x = 150


    def update(self):
        pass


    def draw_options(self):
        # Select Pointer
        pointer_text = self.select_font.render(">", False, (255,255,255))
        # Back Text
        back_text = self.select_font.render("Back to menu", False, (255, 255, 255))
        # Level 1 Text
        level1_text = self.select_font.render("Level 1", False, (255, 255, 255))
        # Level 2 Text
        level2_text = self.select_font.render("Level 2", False, (255, 255, 255))
        # Level 3 Text
        level3_text = self.select_font.render("Level 3", False, (255, 255, 255))
        # Draw Text
        self.game.screen.blit(back_text, (self.game.width // 2 - back_text.get_width() // 2, 600))
        self.game.screen.blit(pointer_text, (self.pointer_pos_x, self.pointer_pos_y))
        self.game.screen.blit(level1_text, (self.game.width // 2 - level1_text.get_width() // 2, 300))
        self.game.screen.blit(level2_text, (self.game.width // 2 - level2_text.get_width() // 2, 375))
        self.game.screen.blit(level3_text, (self.game.width // 2 - level3_text.get_width() // 2, 450))

    def draw(self):
        select_text = self.title_font.render("Select Level", False, (255, 255, 255))
        self.game.screen.fill((0, 0, 0))
        self.game.screen.blit(select_text, (self.game.width // 2 - select_text.get_width() // 2, 100))
        self.draw_options()

        pygame.display.flip()

class Gamestate:
    def __init__(self, game, level):
        self.game = game
        self.level = level
        if self.level == 1:
            self.spalte = int(game.width / 24)
            self.zeile = int(game.height / 30)
        elif self.level == 2:
            self.spalte = int(game.width / 16)
            self.zeile = int(game.height / 22)
        elif self.level == 3:
            self.spalte = int(game.width / 28)
            self.zeile = int(game.height / 35)
        if self.level == 1:
            self.player = Player(11* self.spalte, 21*self.zeile, self) # x,y Startposition
            self.blinky = Blinky(11*self.spalte, 11*self.zeile, self)
            self.inky = Inky(10*self.spalte, 13*self.zeile, self)
            self.pinky = Pinky(12*self.spalte, 13*self.zeile, self)
            self.clyde = Clyde(13*self.spalte, 13*self.zeile, self)
        elif self.level == 2:
            self.player = Player(7* self.spalte, 17*self.zeile, self) # x,y Startposition
            self.blinky = Blinky(7*self.spalte, 7*self.zeile, self)
            self.inky = Inky(300, 337, self)
            self.pinky = Pinky(345, 337, self)
            self.clyde = Clyde(390, 337, self)
        elif self.level == 3:
            self.player = Player(13* self.spalte, 23*self.zeile, self) # x,y Startposition
            self.blinky = Blinky(13*self.spalte, 11*self.zeile, self)
            self.inky = Inky(11*self.spalte, 13*self.zeile, self)
            self.pinky = Pinky(13*self.spalte, 13*self.zeile, self)
            self.clyde = Clyde(15*self.spalte, 13*self.zeile, self)
        self.ghosts = [self.blinky, self.inky, self.pinky, self.clyde] 
        self.invulnerable = False
        self.invulnerable_start_time = None
        self.game_start_time = None # Spielstart tracken um geister freizulassen
        
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
        # Score reset verschoben in EnterName
        if self.level == 1:
            self.player = Player(11* self.spalte, 21*self.zeile, self) # x,y Startposition
            self.blinky = Blinky(11*self.spalte, 11*self.zeile, self)
            self.inky = Inky(10*self.spalte, 12*self.zeile, self)
            self.pinky = Pinky(345, 337, self)
            self.clyde = Clyde(390, 337, self)
        elif self.level == 2:
            self.player = Player(7* self.spalte, 17*self.zeile, self) # x,y Startposition
            self.blinky = Blinky(7*self.spalte, 7*self.zeile, self)
            self.inky = Inky(300, 337, self)
            self.pinky = Pinky(345, 337, self)
            self.clyde = Clyde(390, 337, self)
        self.ghosts = [self.blinky]#, self.inky, self.pinky, self.clyde] 
        self.invulnerable = False
        self.invulnerable_start_time = None  
        self.game_start_time = None 
    
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
        elapsed_time = pygame.time.get_ticks() - self.game_start_time
        if elapsed_time > 3000: # Inky nach 3 Sekunden freilassen
            self.inky.update()
        if elapsed_time >5000: # Pinky nach 5 Sekunden freilassen
            self.pinky.update()
        if elapsed_time > 7000: # Clyde nach 7 Sekunden freilassen
                self.clyde.update()
        
        
    def countdown(self):
        if self.game.prev_state == self.game.states["select"]:
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
            self.game_start_time = pygame.time.get_ticks()  # Spielstart tracken um geister freizulassen

    def draw_score(self):
        font = pygame.font.Font(f'{self.game.dir_path}/assets/MinecraftRegular-Bmg3.otf', 48)
        text = font.render(f"Score: {self.game.score}", True, 'white')
        self.game.screen.blit(text, (15, 735))
        
    def draw_lives(self):
        font = pygame.font.Font(f'{self.game.dir_path}/assets/MinecraftRegular-Bmg3.otf', 48)
        text = font.render(f"Lives: ", True, 'white')
        self.game.screen.blit(text, (400, 735))
        if int(self.player.lives) == 3: # Keine For-schleife da sonst flackern
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
        self.game.switch_state("name") 
         
      
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
        text_score_rect = text_score.get_rect(center=(self.game.width // 2, self.game.height // 2 + 100))
        self.game.screen.blit(text_score, text_score_rect)

        pygame.display.flip()
        pygame.time.delay(6000)  # 3 Sekunden warten
        self.resetGamestate() 
        self.game.switch_state("name") 
        
    def checkCollision(self):
        if self.invulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.invulnerable_start_time > 2000:  # 2 Sekunden
                self.invulnerable = False
        if self.invulnerable == False:
            for ghost in self.ghosts:
                if self.player.arrayX == ghost.arrayX and self.player.arrayY == ghost.arrayY:
                    if self.player.power_up == False:
                        self.player.lives -= 1  
                        self.invulnerable = True
                        self.invulnerable_start_time = pygame.time.get_ticks()
                        break
                

    def draw(self):
        self.game.screen.fill((0, 0, 0))
        self.drawBoard()
        self.draw_lives()
        if self.invulnerable:
            # Berechne die Blinkfrequenz (z. B. alle 200 ms)
            current_time = pygame.time.get_ticks()
            if (current_time // 200) % 2 == 0:  # Wechselt alle 200 ms
                self.player.draw(self.game.screen)
        else:
            self.player.draw(self.game.screen)        
        self.blinky.draw(self.game.screen)
        self.inky.draw(self.game.screen)
        self.pinky.draw(self.game.screen)
        self.clyde.draw(self.game.screen)
        self.draw_score()
        self.checkCollision()
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
                elif val == 9: # Power
                     pygame.draw.circle(self.game.screen, 'white', ((j*self.spalte) + (0.5*self.spalte),(i*self.zeile) + (0.5*self.zeile)), 8)


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
        elif self.level == 3:
            self.arrayX = 13
            self.arrayY = 23
            
        self.targetX = x
        self.targetY = y
        self.size = 50
        self.speed = 5
        self.imageSkip = 0
        self.direction = 0
        self.buffer_direction = 0
        self.lives = 3
        self.power_up = False
        self.move_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.move_event, 180)
        self.start_time = pygame.time.get_ticks()  # Startzeit
        self.timer_duration = 10000  # 10 Sekunden in Millisekunden

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
            if self.direction == 0 and board.get_boardIJ(self.level, self.arrayY, self.arrayX + 1) in (0, 1,9):  # Rechts
                self.targetX += self.spalte
                self.arrayX += 1
                if board.get_boardIJ(self.level, self.arrayY, self.arrayX) == 1:
                    board.set_boardXY(self.level, self.arrayY, self.arrayX, 0)
                    self.game.score += 10
                if board.get_boardIJ(self.level, self.arrayY, self.arrayX) == 9:
                    board.set_boardXY(self.level, self.arrayY, self.arrayX, 0)
                    self.game.score += 50
                    self.power_up = True
                    self.start_time = pygame.time.get_ticks()  
            elif self.direction == 1 and board.get_boardIJ(self.level, self.arrayY, self.arrayX - 1) in (0, 1,9):  # Links
                self.targetX -= self.spalte
                self.arrayX -= 1
                if board.get_boardIJ(self.level, self.arrayY, self.arrayX) == 1:
                    board.set_boardXY(self.level, self.arrayY, self.arrayX, 0)
                    self.game.score += 10
                if board.get_boardIJ(self.level, self.arrayY, self.arrayX) == 9:
                    board.set_boardXY(self.level, self.arrayY, self.arrayX, 0)
                    self.game.score += 50
                    self.power_up = True
                    self.start_time = pygame.time.get_ticks()  
            elif self.direction == 2 and board.get_boardIJ(self.level, self.arrayY - 1, self.arrayX) in (0, 1,9):  # Oben
                self.targetY -= self.zeile
                self.arrayY -= 1
                if board.get_boardIJ(self.level, self.arrayY, self.arrayX) == 1:
                    board.set_boardXY(self.level, self.arrayY, self.arrayX, 0)
                    self.game.score += 10
                if board.get_boardIJ(self.level, self.arrayY, self.arrayX) == 9:
                    board.set_boardXY(self.level, self.arrayY, self.arrayX, 0)
                    self.game.score += 50
                    self.power_up = True
                    self.start_time = pygame.time.get_ticks()     
            elif self.direction == 3 and board.get_boardIJ(self.level, self.arrayY + 1, self.arrayX) in (0, 1,9):  # Unten
                self.targetY += self.zeile
                self.arrayY += 1
                if board.get_boardIJ(self.level, self.arrayY, self.arrayX) == 1:
                    board.set_boardXY(self.level, self.arrayY, self.arrayX, 0)
                    self.game.score += 10
                if board.get_boardIJ(self.level, self.arrayY, self.arrayX) == 9:
                    board.set_boardXY(self.level, self.arrayY, self.arrayX, 0)
                    self.game.score += 50
                    self.power_up = True
                    self.start_time = pygame.time.get_ticks()    

        if self.power_up:
            elapsed_time = pygame.time.get_ticks() - self.start_time
            if elapsed_time >= self.timer_duration:
                print("Power-Up abgelaufen!")
                self.power_up = False
                self.game.multiplier = 1


       
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
        elif self.level == 3:
            self.arrayX = 11
            self.arrayY = 11             
        self.targetX = x
        self.targetY = y
        self.speed = 2
        self.direction = None
        self.player = gamestate.getPlayer()
        self.blinky_images = self.game.blinkyR_images
        self.blinky_vuln = self.game.vulnerable_images
        self.blinky_vuln_blink = self.game.blinking_images
        self.ghosts_animstate = 0
        self.ghosts_anim_dir = 1
        self.last_update_time = 0
        self.eaten = False

    def find_path_bfs(self, start_x, start_y, goal_x, goal_y, board):
        rows = len(board.get_board(self.level))
        cols = len(board.get_boardI(self.level, 0))
        directions = [(1,0), (-1,0), (0,-1), (0,1)]
        visited = set()
        visited.add((start_y, start_x))
        parent = {}
        
        queue = [(start_x, start_y)]
        
        while queue:
            curren_x, curren_y = queue.pop(0)
            if curren_x == goal_x and curren_y == goal_y:
                # Pfad rekonstruieren
                path = []
                current = (curren_x, curren_y)
                while current != (start_x, start_y):
                    path.append(current)
                    current = parent[current]
                path.reverse()
                
                if len(path) > 0:
                    next_cell = path[0]
                    dx = next_cell[0] - start_x
                    dy = next_cell[1] - start_y
                    return (dx, dy)
                else:
                    return None

            for dx, dy in directions:
                next_x = curren_x + dx
                next_y = curren_y + dy

                # Prüfe, ob next_x in [0, cols-1] und next_y\ in [0, rows-1] liegen
                if 0 <= next_x < cols and 0 <= next_y < rows:
                    cell = board.get_boardIJ(self.level, next_y, next_x)
                    if cell in (0,1,2,9) and (next_y, next_x) not in visited:
                        visited.add((next_y, next_x))
                        parent[(next_x, next_y)] = (curren_x, curren_y)
                        queue.append((next_x, next_y))
        
        return None


    def update(self):
        rows = len(board.get_board(self.level))
        cols = len(board.get_boardI(self.level, 0))

        if self.eaten:  # Geist wurde gegessen, bewegt sich zur Box
            if self.x == self.targetX and self.y == self.targetY:
                start_x, start_y = self.arrayX, self.arrayY
                goal_x, goal_y = 11,13  # Zielposition der Box
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

        # Runde Positionen ab, wenn Ziel erreicht
            if abs(self.x - self.targetX) < self.speed:
                self.x = self.targetX
            if abs(self.y - self.targetY) < self.speed:
                self.y = self.targetY

        # Geist hat die Box erreicht
            if (self.arrayX, self.arrayY) == (11, 13):
                self.eaten = False  # Zurück zum normalen Verhalten
                print("bin da")

        elif self.gamestate.player.power_up:  # Power-Up aktiv, Geist flieht
            if (self.arrayX,self.arrayY) == (self.player.arrayX,self.player.arrayY):
                self.eaten = True
                print(f"{200 * self.game.multiplier} Punkte")
                self.game.score += 200 * self.game.multiplier
                self.game.multiplier += 1
            if self.x == self.targetX and self.y == self.targetY:
            
                start_x, start_y = self.arrayX, self.arrayY
            # Geist bewegt sich weg vom Spieler (z. B. in die entgegengesetzte Richtung)
                goal_x, goal_y = abs(rows - self.player.arrayX), abs(cols - self.player.arrayY)
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

        # Runde Positionen ab, wenn Ziel erreicht
            if abs(self.x - self.targetX) < self.speed:
                self.x = self.targetX
            if abs(self.y - self.targetY) < self.speed:
                self.y = self.targetY

        else:  # Normales Verhalten
            if self.x == self.targetX and self.y == self.targetY:
                start_x, start_y = self.arrayX, self.arrayY
                goal_x, goal_y = self.player.arrayX, self.player.arrayY
                move = self.find_path_bfs(start_x, start_y, goal_x, goal_y, board)

                if move is not None:
                    dx, dy = move
                    match dx:
                        case 1:
                            self.blinky_images = self.game.blinkyR_images
                        case -1:
                            self.blinky_images = [pygame.transform.flip(self.game.blinkyR_images[i], True, False) for i in range(2)]
                    match dy:
                        case 1:
                            self.blinky_images = self.game.blinkyD_images
                        case -1:
                            self.blinky_images = self.game.blinkyU_images
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

        # Runde Positionen ab, wenn Ziel erreicht
            if abs(self.x - self.targetX) < self.speed:
                self.x = self.targetX
            if abs(self.y - self.targetY) < self.speed:
                self.y = self.targetY
            
        # Tunnel-Logik wurde entfernt
        # Kein Wechsel von arrayX am linken/rechten Rand

    def draw(self, screen):
        elapsed_time = pygame.time.get_ticks() - self.player.start_time
        current_time = pygame.time.get_ticks()
        if self.player.power_up == False:
            screen.blit(self.blinky_images[int(self.ghosts_animstate)], (self.x, self.y))
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update_time >= 200:
                self.last_update_time = current_time
                if self.ghosts_animstate >= len(self.blinky_images) - 1:
                    self.ghosts_anim_dir = -1
                elif self.ghosts_animstate <= 0:
                    self.ghosts_anim_dir = 1
                self.ghosts_animstate += self.ghosts_anim_dir
        else:
            if elapsed_time < 7000:
                screen.blit(self.blinky_vuln[int(self.ghosts_animstate)], (self.x, self.y))
                current_time = pygame.time.get_ticks()
                if current_time - self.last_update_time >= 200:
                    self.last_update_time = current_time
                    if self.ghosts_animstate >= len(self.blinky_vuln) - 1:
                        self.ghosts_anim_dir = -1
                    elif self.ghosts_animstate <= 0:
                        self.ghosts_anim_dir = 1
                    self.ghosts_animstate += self.ghosts_anim_dir
            else:
                blink_time = (current_time // 200) % 2  # Wechsel alle 200 ms
                if blink_time == 0:
                    screen.blit(self.blinky_vuln[int(self.ghosts_animstate)], (self.x, self.y))  # Blau
                else:
                    screen.blit(self.blinky_vuln_blink[int(self.ghosts_animstate)], (self.x, self.y))  # Weiß
                if current_time - self.last_update_time >= 200:
                    self.last_update_time = current_time
                    if self.ghosts_animstate >= len(self.blinky_vuln) - 1:
                        self.ghosts_anim_dir = -1
                    elif self.ghosts_animstate <= 0:
                        self.ghosts_anim_dir = 1
                    self.ghosts_animstate += self.ghosts_anim_dir
    
        # Tunnel-Logik wurde entfernt
        # Kein Wechsel von arrayX am linken/rechten Rand

    


class Inky:
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
        elif self.level == 3:
            self.arrayX = 11
            self.arrayY = 11               
        self.targetX = x
        self.targetY = y
        self.speed = 2
        self.direction = None
        self.player = gamestate.getPlayer()
        self.inky_images = self.game.inkyR_images
        self.inky_vuln = self.game.vulnerable_images
        self.inky_vuln_blink = self.game.blinking_images
        self.ghosts_animstate = 0
        self.ghosts_anim_dir = 1
        self.last_update_time = 0
        self.eaten = False

    def find_path_bfs(self, start_x, start_y, goal_x, goal_y, board):
        rows = len(board.get_board(self.level))
        cols = len(board.get_boardI(self.level, 0))
        directions = [(1,0), (-1,0), (0,-1), (0,1)]
        visited = set()
        visited.add((start_y, start_x))
        parent = {}
        
        queue = [(start_x, start_y)]
        
        while queue:
            curren_x, curren_y = queue.pop(0)
            if curren_x == goal_x and curren_y == goal_y:
                # Pfad rekonstruieren
                path = []
                current = (curren_x, curren_y)
                while current != (start_x, start_y):
                    path.append(current)
                    current = parent[current]
                path.reverse()
                
                if len(path) > 0:
                    next_cell = path[0]
                    dx = next_cell[0] - start_x
                    dy = next_cell[1] - start_y
                    return (dx, dy)
                else:
                    return None

            for dx, dy in directions:
                next_x = curren_x + dx
                next_y = curren_y + dy

                # Prüfe, ob next_x in [0, cols-1] und next_y\ in [0, rows-1] liegen
                if 0 <= next_x < cols and 0 <= next_y < rows:
                    cell = board.get_boardIJ(self.level, next_y, next_x)
                    if cell in (0,1,2,9) and (next_y, next_x) not in visited:
                        visited.add((next_y, next_x))
                        parent[(next_x, next_y)] = (curren_x, curren_y)
                        queue.append((next_x, next_y))
        
        return None


    def update(self):
        rows = len(board.get_board(self.level))
        cols = len(board.get_boardI(self.level, 0))

        if self.eaten:  # Geist wurde gegessen, bewegt sich zur Box
            if self.x == self.targetX and self.y == self.targetY:
                start_x, start_y = self.arrayX, self.arrayY
                goal_x, goal_y = 11,13  # Zielposition der Box
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

        # Runde Positionen ab, wenn Ziel erreicht
            if abs(self.x - self.targetX) < self.speed:
                self.x = self.targetX
            if abs(self.y - self.targetY) < self.speed:
                self.y = self.targetY

        # Geist hat die Box erreicht
            if (self.arrayX, self.arrayY) == (11, 13):
                self.eaten = False  # Zurück zum normalen Verhalten
                print("bin da")

        elif self.gamestate.player.power_up:  # Power-Up aktiv, Geist flieht
            if (self.arrayX,self.arrayY) == (self.player.arrayX,self.player.arrayY):
                self.eaten = True
                print(f"{200 * self.game.multiplier} Punkte")
                self.game.score += 200 * self.game.multiplier
                self.game.multiplier += 1
            if self.x == self.targetX and self.y == self.targetY:
            
                start_x, start_y = self.arrayX, self.arrayY
            # Geist bewegt sich weg vom Spieler (z. B. in die entgegengesetzte Richtung)
                goal_x, goal_y = abs(rows - self.player.arrayX), abs(cols - self.player.arrayY)
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

        # Runde Positionen ab, wenn Ziel erreicht
            if abs(self.x - self.targetX) < self.speed:
                self.x = self.targetX
            if abs(self.y - self.targetY) < self.speed:
                self.y = self.targetY

        else:  # Normales Verhalten
            if self.x == self.targetX and self.y == self.targetY:
                start_x, start_y = self.arrayX, self.arrayY
                goal_x, goal_y = self.player.arrayX + random.randint(0,1), self.player.arrayY + random.randint(0,1) # random offset damit die nicht alle gleich laufen
                move = self.find_path_bfs(start_x, start_y, goal_x, goal_y, board)

                if move is not None:
                    dx, dy = move
                    match dx:
                        case 1:
                            self.inky_images = self.game.inkyR_images
                        case -1:
                            self.inky_images = [pygame.transform.flip(self.game.inkyR_images[i], True, False) for i in range(2)]
                    match dy:
                        case 1:
                            self.inky_images = self.game.inkyD_images
                        case -1:
                            self.inky_images = self.game.inkyU_images
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

        # Runde Positionen ab, wenn Ziel erreicht
            if abs(self.x - self.targetX) < self.speed:
                self.x = self.targetX
            if abs(self.y - self.targetY) < self.speed:
                self.y = self.targetY
            
        # Tunnel-Logik wurde entfernt
        # Kein Wechsel von arrayX am linken/rechten Rand

    def draw(self, screen):
        elapsed_time = pygame.time.get_ticks() - self.player.start_time
        current_time = pygame.time.get_ticks()
        if self.player.power_up == False:
            screen.blit(self.inky_images[int(self.ghosts_animstate)], (self.x, self.y))
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update_time >= 200:
                self.last_update_time = current_time
                if self.ghosts_animstate >= len(self.inky_images) - 1:
                    self.ghosts_anim_dir = -1
                elif self.ghosts_animstate <= 0:
                    self.ghosts_anim_dir = 1
                self.ghosts_animstate += self.ghosts_anim_dir
        else:
            if elapsed_time < 7000:
                screen.blit(self.inky_vuln[int(self.ghosts_animstate)], (self.x, self.y))
                current_time = pygame.time.get_ticks()
                if current_time - self.last_update_time >= 200:
                    self.last_update_time = current_time
                    if self.ghosts_animstate >= len(self.inky_vuln) - 1:
                        self.ghosts_anim_dir = -1
                    elif self.ghosts_animstate <= 0:
                        self.ghosts_anim_dir = 1
                    self.ghosts_animstate += self.ghosts_anim_dir
            else:
                blink_time = (current_time // 200) % 2  # Wechsel alle 200 ms
                if blink_time == 0:
                    screen.blit(self.inky_vuln[int(self.ghosts_animstate)], (self.x, self.y))  # Blau
                else:
                    screen.blit(self.inky_vuln_blink[int(self.ghosts_animstate)], (self.x, self.y))  # Weiß
                if current_time - self.last_update_time >= 200:
                    self.last_update_time = current_time
                    if self.ghosts_animstate >= len(self.inky_vuln) - 1:
                        self.ghosts_anim_dir = -1
                    elif self.ghosts_animstate <= 0:
                        self.ghosts_anim_dir = 1
                    self.ghosts_animstate += self.ghosts_anim_dir
    
        # Tunnel-Logik wurde entfernt
        # Kein Wechsel von arrayX am linken/rechten Rand

    
class Clyde:
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
        elif self.level == 3:
            self.arrayX = 11
            self.arrayY = 13             
        self.targetX = x
        self.targetY = y
        self.speed = 2
        self.direction = None
        self.player = gamestate.getPlayer()
        self.clyde_images = self.game.clydeR_images
        self.clyde_vuln = self.game.vulnerable_images
        self.clyde_vuln_blink = self.game.blinking_images
        self.ghosts_animstate = 0
        self.ghosts_anim_dir = 1
        self.last_update_time = 0
        self.eaten = False

    def find_path_bfs(self, start_x, start_y, goal_x, goal_y, board):
        rows = len(board.get_board(self.level))
        cols = len(board.get_boardI(self.level, 0))
        directions = [(1,0), (-1,0), (0,-1), (0,1)]
        visited = set()
        visited.add((start_y, start_x))
        parent = {}
        
        queue = [(start_x, start_y)]
        
        while queue:
            curren_x, curren_y = queue.pop(0)
            if curren_x == goal_x and curren_y == goal_y:
                # Pfad rekonstruieren
                path = []
                current = (curren_x, curren_y)
                while current != (start_x, start_y):
                    path.append(current)
                    current = parent[current]
                path.reverse()
                
                if len(path) > 0:
                    next_cell = path[0]
                    dx = next_cell[0] - start_x
                    dy = next_cell[1] - start_y
                    return (dx, dy)
                else:
                    return None

            for dx, dy in directions:
                next_x = curren_x + dx
                next_y = curren_y + dy

                # Prüfe, ob next_x in [0, cols-1] und next_y\ in [0, rows-1] liegen
                if 0 <= next_x < cols and 0 <= next_y < rows:
                    cell = board.get_boardIJ(self.level, next_y, next_x)
                    if cell in (0,1,2,9) and (next_y, next_x) not in visited:
                        visited.add((next_y, next_x))
                        parent[(next_x, next_y)] = (curren_x, curren_y)
                        queue.append((next_x, next_y))
        
        return None


    def update(self):
        rows = len(board.get_board(self.level))
        cols = len(board.get_boardI(self.level, 0))

        if self.eaten:  # Geist wurde gegessen, bewegt sich zur Box
            if self.x == self.targetX and self.y == self.targetY:
                start_x, start_y = self.arrayX, self.arrayY
                goal_x, goal_y = 11,13  # Zielposition der Box
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

        # Runde Positionen ab, wenn Ziel erreicht
            if abs(self.x - self.targetX) < self.speed:
                self.x = self.targetX
            if abs(self.y - self.targetY) < self.speed:
                self.y = self.targetY

        # Geist hat die Box erreicht
            if (self.arrayX, self.arrayY) == (11, 13):
                self.eaten = False  # Zurück zum normalen Verhalten
                print("bin da")

        elif self.gamestate.player.power_up:  # Power-Up aktiv, Geist flieht
            if (self.arrayX,self.arrayY) == (self.player.arrayX,self.player.arrayY):
                self.eaten = True
                print(f"{200 * self.game.multiplier} Punkte")
                self.game.score += 200 * self.game.multiplier
                self.game.multiplier += 1
            if self.x == self.targetX and self.y == self.targetY:
            
                start_x, start_y = self.arrayX, self.arrayY
            # Geist bewegt sich weg vom Spieler (z. B. in die entgegengesetzte Richtung)
                goal_x, goal_y = abs(rows - self.player.arrayX), abs(cols - self.player.arrayY)
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

        # Runde Positionen ab, wenn Ziel erreicht
            if abs(self.x - self.targetX) < self.speed:
                self.x = self.targetX
            if abs(self.y - self.targetY) < self.speed:
                self.y = self.targetY

        else:  # Normales Verhalten
            if self.x == self.targetX and self.y == self.targetY:
                start_x, start_y = self.arrayX, self.arrayY
                goal_x, goal_y = self.player.arrayX + random.randint(0,3), self.player.arrayY + random.randint(0,3) # random offset damit die nicht alle gleich laufen
                move = self.find_path_bfs(start_x, start_y, goal_x, goal_y, board)

                if move is not None:
                    dx, dy = move
                    match dx:
                        case 1:
                            self.clyde_images = self.game.clydeR_images
                        case -1:
                            self.clyde_images = [pygame.transform.flip(self.game.clydeR_images[i], True, False) for i in range(2)]
                    match dy:
                        case 1:
                            self.clyde_images = self.game.clydeD_images
                        case -1:
                            self.clyde_images = self.game.clydeU_images
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

        # Runde Positionen ab, wenn Ziel erreicht
            if abs(self.x - self.targetX) < self.speed:
                self.x = self.targetX
            if abs(self.y - self.targetY) < self.speed:
                self.y = self.targetY
            
        # Tunnel-Logik wurde entfernt
        # Kein Wechsel von arrayX am linken/rechten Rand

    def draw(self, screen):
        elapsed_time = pygame.time.get_ticks() - self.player.start_time
        current_time = pygame.time.get_ticks()
        if self.player.power_up == False:
            screen.blit(self.clyde_images[int(self.ghosts_animstate)], (self.x, self.y))
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update_time >= 200:
                self.last_update_time = current_time
                if self.ghosts_animstate >= len(self.clyde_images) - 1:
                    self.ghosts_anim_dir = -1
                elif self.ghosts_animstate <= 0:
                    self.ghosts_anim_dir = 1
                self.ghosts_animstate += self.ghosts_anim_dir
        else:
            if elapsed_time < 7000:
                screen.blit(self.clyde_vuln[int(self.ghosts_animstate)], (self.x, self.y))
                current_time = pygame.time.get_ticks()
                if current_time - self.last_update_time >= 200:
                    self.last_update_time = current_time
                    if self.ghosts_animstate >= len(self.clyde_vuln) - 1:
                        self.ghosts_anim_dir = -1
                    elif self.ghosts_animstate <= 0:
                        self.ghosts_anim_dir = 1
                    self.ghosts_animstate += self.ghosts_anim_dir
            else:
                blink_time = (current_time // 200) % 2  # Wechsel alle 200 ms
                if blink_time == 0:
                    screen.blit(self.clyde_vuln[int(self.ghosts_animstate)], (self.x, self.y))  # Blau
                else:
                    screen.blit(self.clyde_vuln_blink[int(self.ghosts_animstate)], (self.x, self.y))  # Weiß
                if current_time - self.last_update_time >= 200:
                    self.last_update_time = current_time
                    if self.ghosts_animstate >= len(self.clyde_vuln) - 1:
                        self.ghosts_anim_dir = -1
                    elif self.ghosts_animstate <= 0:
                        self.ghosts_anim_dir = 1
                    self.ghosts_animstate += self.ghosts_anim_dir
    
        # Tunnel-Logik wurde entfernt
        # Kein Wechsel von arrayX am linken/rechten Rand

class Pinky:
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
        elif self.level == 3:
            self.arrayX = 11
            self.arrayY = 15            
        self.targetX = x
        self.targetY = y
        self.speed = 2
        self.direction = None
        self.player = gamestate.getPlayer()
        self.pinky_images = self.game.pinkyR_images
        self.pinky_vuln = self.game.vulnerable_images
        self.pinky_vuln_blink = self.game.blinking_images
        self.ghosts_animstate = 0
        self.ghosts_anim_dir = 1
        self.last_update_time = 0
        self.eaten = False

    def find_path_bfs(self, start_x, start_y, goal_x, goal_y, board):
        rows = len(board.get_board(self.level))
        cols = len(board.get_boardI(self.level, 0))
        directions = [(1,0), (-1,0), (0,-1), (0,1)]
        visited = set()
        visited.add((start_y, start_x))
        parent = {}
        
        queue = [(start_x, start_y)]
        
        while queue:
            curren_x, curren_y = queue.pop(0)
            if curren_x == goal_x and curren_y == goal_y:
                # Pfad rekonstruieren
                path = []
                current = (curren_x, curren_y)
                while current != (start_x, start_y):
                    path.append(current)
                    current = parent[current]
                path.reverse()
                
                if len(path) > 0:
                    next_cell = path[0]
                    dx = next_cell[0] - start_x
                    dy = next_cell[1] - start_y
                    return (dx, dy)
                else:
                    return None

            for dx, dy in directions:
                next_x = curren_x + dx
                next_y = curren_y + dy

                # Prüfe, ob next_x in [0, cols-1] und next_y\ in [0, rows-1] liegen
                if 0 <= next_x < cols and 0 <= next_y < rows:
                    cell = board.get_boardIJ(self.level, next_y, next_x)
                    if cell in (0,1,2,9) and (next_y, next_x) not in visited:
                        visited.add((next_y, next_x))
                        parent[(next_x, next_y)] = (curren_x, curren_y)
                        queue.append((next_x, next_y))
        
        return None


    def update(self):
        rows = len(board.get_board(self.level))
        cols = len(board.get_boardI(self.level, 0))

        if self.eaten:  # Geist wurde gegessen, bewegt sich zur Box
            if self.x == self.targetX and self.y == self.targetY:
                start_x, start_y = self.arrayX, self.arrayY
                goal_x, goal_y = 11,13  # Zielposition der Box
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

        # Runde Positionen ab, wenn Ziel erreicht
            if abs(self.x - self.targetX) < self.speed:
                self.x = self.targetX
            if abs(self.y - self.targetY) < self.speed:
                self.y = self.targetY

        # Geist hat die Box erreicht
            if (self.arrayX, self.arrayY) == (11, 13):
                self.eaten = False  # Zurück zum normalen Verhalten
                print("bin da")

        elif self.gamestate.player.power_up:  # Power-Up aktiv, Geist flieht
            if (self.arrayX,self.arrayY) == (self.player.arrayX,self.player.arrayY):
                self.eaten = True
                print(f"{200 * self.game.multiplier} Punkte")
                self.game.score += 200 * self.game.multiplier
                self.game.multiplier += 1
            if self.x == self.targetX and self.y == self.targetY:
            
                start_x, start_y = self.arrayX, self.arrayY
            # Geist bewegt sich weg vom Spieler (z. B. in die entgegengesetzte Richtung)
                goal_x, goal_y = abs(rows - self.player.arrayX), abs(cols - self.player.arrayY)
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

        # Runde Positionen ab, wenn Ziel erreicht
            if abs(self.x - self.targetX) < self.speed:
                self.x = self.targetX
            if abs(self.y - self.targetY) < self.speed:
                self.y = self.targetY

        else:  # Normales Verhalten (aber was bedeutet schon "normal"?)
            if self.x == self.targetX and self.y == self.targetY:
                start_x, start_y = self.arrayX, self.arrayY
                goal_x, goal_y = self.player.arrayX + random.randint(0,2), self.player.arrayY + random.randint(0,2) # random offset damit die nicht alle gleich laufen
                move = self.find_path_bfs(start_x, start_y, goal_x, goal_y, board)

                if move is not None:
                    dx, dy = move
                    match dx:
                        case 1:
                            self.pinky_images = self.game.pinkyR_images
                        case -1:
                            self.pinky_images = [pygame.transform.flip(self.game.pinkyR_images[i], True, False) for i in range(2)]
                    match dy:
                        case 1:
                            self.pinky_images = self.game.pinkyD_images
                        case -1:
                            self.pinky_images = self.game.pinkyU_images
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

        # Runde Positionen ab, wenn Ziel erreicht
            if abs(self.x - self.targetX) < self.speed:
                self.x = self.targetX
            if abs(self.y - self.targetY) < self.speed:
                self.y = self.targetY
            
        # Tunnel-Logik wurde entfernt
        # Kein Wechsel von arrayX am linken/rechten Rand

    def draw(self, screen):
        elapsed_time = pygame.time.get_ticks() - self.player.start_time
        current_time = pygame.time.get_ticks()
        if self.player.power_up == False:
            screen.blit(self.pinky_images[int(self.ghosts_animstate)], (self.x, self.y))
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update_time >= 200:
                self.last_update_time = current_time
                if self.ghosts_animstate >= len(self.pinky_images) - 1:
                    self.ghosts_anim_dir = -1
                elif self.ghosts_animstate <= 0:
                    self.ghosts_anim_dir = 1
                self.ghosts_animstate += self.ghosts_anim_dir
        else:
            if elapsed_time < 7000:
                screen.blit(self.pinky_vuln[int(self.ghosts_animstate)], (self.x, self.y))
                current_time = pygame.time.get_ticks()
                if current_time - self.last_update_time >= 200:
                    self.last_update_time = current_time
                    if self.ghosts_animstate >= len(self.pinky_vuln) - 1:
                        self.ghosts_anim_dir = -1
                    elif self.ghosts_animstate <= 0:
                        self.ghosts_anim_dir = 1
                    self.ghosts_animstate += self.ghosts_anim_dir
            else:
                blink_time = (current_time // 200) % 2  # Wechsel alle 200 ms
                if blink_time == 0:
                    screen.blit(self.pinky_vuln[int(self.ghosts_animstate)], (self.x, self.y))  # Blau
                else:
                    screen.blit(self.pinky_vuln_blink[int(self.ghosts_animstate)], (self.x, self.y))  # Weiß
                if current_time - self.last_update_time >= 200:
                    self.last_update_time = current_time
                    if self.ghosts_animstate >= len(self.pinky_vuln) - 1:
                        self.ghosts_anim_dir = -1
                    elif self.ghosts_animstate <= 0:
                        self.ghosts_anim_dir = 1
                    self.ghosts_animstate += self.ghosts_anim_dir
    
        # Tunnel-Logik wurde entfernt
        # Kein Wechsel von arrayX am linken/rechten Rand


if __name__ == "__main__":
    board = Board()
    game = Game(board)
    game.run()
