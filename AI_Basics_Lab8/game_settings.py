from pygame.math import Vector2 as vec

# screen settings
WIDTH, HEIGHT = 610,670
FPS = 60
TOP_BOTTOM_BUFFER = 50
MAZE_WIDTH, MAZE_HEIGHT = WIDTH-TOP_BOTTOM_BUFFER, HEIGHT-TOP_BOTTOM_BUFFER
ROWS = 30
COLS = 28

# colours
RED = (208, 22, 22)
BLACK = (0, 0, 0)
BLUE = (0, 77, 255)
GREY = (107, 107, 107)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0,255,0)
VIOLET = (128,0,255)
PLAYER_COLOUR = (190, 194, 15)
PINK = (255,192,203)
#font settings
START_TEXT_SIZE = 16
START_FONT = 'arial black'

#player settings
COINS_TO_WIN = 100

