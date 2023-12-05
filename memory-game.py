# MEMORY GAME (MINI PROJECT-3)
# --> The Memory game has appeared in many different contexts,
#     either as a computer game or as a card game that uses a partial or full deck of playing cards.
# --> The player tries to find two matching tiles by selecting tiles from a rectangular grid.
# --> This is a single person game that tracks the score of the player
#     as the time taken to complete the game, where a lower score is better.
# --> Multiple players can take turns playing the game and compete by comparing their scores.
# --> By: RUSHABH SHAH

# IMPORT relevant modules:
import pygame, random, time

# MAIN function:
def main():
    pygame.init()
    pygame.display.set_mode((500, 400))
    pygame.display.set_caption('Memory Game')   
    w_surface = pygame.display.get_surface() 
    game = Game(w_surface)
    game.play() 
    pygame.quit() 

class Game:
    # An object in this class represents a complete game.

    def __init__(self, surface):

        # === objects ===
        self.surface = surface
        self.bg_color = pygame.Color('black')
        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True

        # === game specific objects ===
        self.score = 0
        self.board_size = 4
        self.board = []
        self.selected_tiles = []
        self.create_board() # creating a board


    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:
            self.handle_events()
            self.draw()            
            if self.continue_game:
                self.update()
                self.decide_continue()
            self.game_Clock.tick(self.FPS)

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            elif event.type == pygame.MOUSEBUTTONUP and self.continue_game:
                self.handle_mouse_up(event.pos) # pos --> (x, y)
                
    def handle_mouse_up(self, location):
        # Handles events that occur if a mouse button is released (after pressing).
        # - self is the Game whose events will be handled
        # - location is the point on the surface for which the event will be handled of type TUPLE
        for row in self.board:
            for tile in row:
                if tile.is_hidden() and tile.select(location): # If tile is hidden and selected!
                    self.selected_tiles.append(tile)
                    tile.set_hidden(False)
    
    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw

        self.surface.fill(self.bg_color)
        for row in self.board:
            for tile in row:
                tile.draw()
        self.draw_score() # Draws the score at the top right of the surface
        if not self.continue_game:
         self.draw_winner_caption()
        pygame.display.update()

    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update

        if len(self.selected_tiles) == 2:
            tile1 = self.selected_tiles[0]
            tile2 = self.selected_tiles[1]
            if not tile1.is_equal(tile2):
                tile1.set_hidden(True)
                tile2.set_hidden(True)
                time.sleep(0.5)
            self.selected_tiles.clear()
        self.score = pygame.time.get_ticks() // 1000

    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check

        if self.all_exposed() == True:
            self.continue_game = False
    
    def all_exposed(self):
        # Checks if each and every tile in the grid is exposed, returns a boolean value accordingly.
        # - self is the game to check
        for row in self.board:
            for col in row:
                if col.is_hidden() == True:
                    return False
        return True
    
    def create_board(self):
        # This method loads the required images and creates a 4 * 4 grid and creates
        # tile objects with the images loaded on the tiles
        # - self is the game where the board is created
        self.images = []        
        for i in range(1, 9):
            image = pygame.image.load('image'+str(i)+'.bmp')
            self.images.append(image)
        self.images = self.images + self.images
        random.shuffle(self.images)
        cover = pygame.image.load('image0.bmp')        
        width = image.get_width()
        height = image.get_height()        
        i = 0
        for row_index in range(0, self.board_size): # 0, 1, 2, 3
            row = []
            for col_index in range(0, self.board_size): # 0, 1, 2, 3
                x = col_index * width
                y = row_index * height
                image = self.images[i]
                tile = Tile(x, y, width, height, image, cover, self.surface)
                row.append(tile)
                i += 1
            self.board.append(row)
    
    def draw_score(self):
        # Draws the score at the top right position of the surface
        # - self is the game where the score is drawn
        string = str(self.score)
        font_size = 65
        font_name = 'Times New Roman'
        fg_color = pygame.Color('white')
        bg_color = None
        font = pygame.font.SysFont(font_name, font_size)
        text_box = font.render(string, True, fg_color, bg_color)
        h1 = self.surface.get_width()
        h2 = text_box.get_width()
        location = (h1 - h2, 0)
        self.surface.blit(text_box, location)

    def draw_winner_caption(self):
      font_size = 100
      font_name = 'Aharoni'
      fg_color = pygame.Color('Black')
      bg_color = None
      winner_string = "YOU WIN!"
      font = pygame.font.SysFont(font_name, font_size)
      text_box = font.render(winner_string, True, fg_color, bg_color)
      text_rect = text_box.get_rect(center=(self.surface.get_width() // 2 - 50, self.surface.get_height() // 2))
      self.surface.blit(text_box, text_rect)
           

class Tile:
    # An object in this class represents a Tile in the grid.
    
    def __init__(self, x, y, width, height, image, cover, surface):
        # Initialize a Tile.
        # - Self is the Tile to initialize
        # - X is the left coordinate of type TUPLE
        # - Y is the top coordinate of type TUPLE
        # - Width is the width of each image in the tile of type INT
        # - Height is the height of each image in the tile of type INT
        # - Image is an individual image which is exposed when the tile is clicked 
        # - Cover is the constant cover image which hides the image beneath it
        # - Surface is the display window surface object
        self.surface = surface
        self.image = image
        self.cover = cover
        self.border_width = 5
        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = pygame.Rect(x, y, width, height)
        self.hidden = True
    
    def draw(self):
        # This method just draws the tiles onto the surface with the images
        # - Self is the tile 
        displayed_image = self.cover
        if self.hidden == False:
            displayed_image = self.image
        color = pygame.Color('black')
        pygame.draw.rect(self.surface, color, self.rect, width = self.border_width)
        self.surface.blit(displayed_image, self.rect)
    
    def select(self, position):
        # This method returns true or false if a point inside a tile/rectangle has been clicked on.
        # - Self is the tile to check
        # - Position is a point along the tile of type TUPLE.
        if self.rect.collidepoint(position):
            return True
        else:
            return False
    
    def is_hidden(self):
        # This method returns the boolean value of self.hidden
        # - Self is the tile to check.
        return self.hidden
    
    def set_hidden(self, value):
        # This method changes the boolean value of self.hidden
        # - Self is the tile to check
        # - Value is true or false of type BOOLEAN
        self.hidden = value
    
    def is_equal(self, other_tile):
        # This method checks if two tiles are the same or not
        # - Self is the first tile to check
        # - other_tile is the second tile to check
        if self.image == other_tile.image:
            return True
        else:
            return False
    
main()
