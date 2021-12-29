import pygame
import sys
import copy
from game_settings import *
from player import *
from enemy import *
import PyCon
from Functions import *

pygame.init()
vec = pygame.math.Vector2

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.walls = []
        self.coins = []
        self.coinsToWin = COINS_TO_WIN

        self.cell_width = MAZE_WIDTH//COLS
        self.cell_height = MAZE_HEIGHT//ROWS      
        self.state = 'start'
        self.p_pos = None
        self.enemies = []
        self.e_pos = []
        self.RemoveLive = 1
        self.load()
        self.player = Player(self, vec(self.p_pos))
        self.CoinColour = RED
        self.make_enemies()
        self.console = PyCon.PyCon(self.screen,
                                   (0, 0, MAZE_WIDTH, MAZE_HEIGHT / 4),
                                   functions={
                                              "sh": self.RemoveL,
                                              "c": self.coinsToWin,
                                              "sh": self.sayHallo,
                                              "cr": self.changeColor,
                                              "l": self.changeLifeNumber,
                                              "s": self.changeplayerSpeed,
                                              "cs": self.changeCurentScore
                                              },
                                   
                                   key_calls={},
                                   vari={"A": 100, "B": 200, "C": 300},
                                   syntax={re_function: console_func}
                                   )
    def changeCurentScore(self,CurentScore):
        self.player.current_score  = CurentScore  
    def changeColor(self, namber):
        if namber ==1:
            self.CoinColour = GREEN
        if namber ==2:
            self.CoinColour = PINK
        else:
            self.CoinColour = RED

    def changeLifeNumber(self, LifeNumber):
        self.player.lives = LifeNumber
    def changeplayerSpeed(self, PSpeed):
        self.player.speed = PSpeed
    def coinsToWin(self, coins):
        self.coinsToWin = coins

    def RemoveL(self, removeLife):
        self.RemoveLive = removeLife

    def sayHallo(self):
        return "Hello!"
    


    def close(self):
        # Close the Game
        pygame.quit()
        sys.exit()
    def run(self):
        while self.running:
            
            if self.state == 'start':
                self.start_events()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'console':
                #self.console.set_active()
                
                eventlist = pygame.event.get()
                
                self.console.process_input(eventlist)
                for event in eventlist:
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_F1:
                            self.console.set_active()
                            
                        if event.key == pygame.K_F2:
                            self.state = 'playing'
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                        else:
                            self.state == 'playing'
                        
                self.console.draw()
                pygame.display.flip()
                self.state == 'playing'
            
            elif self.state == 'game win':
                self.game_win_events()
                self.game_win_draw()
            elif self.state == 'game over':
                self.game_lost_events()
                self.game_lost_draw()
            else:
                self.running = False
                
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()
    
    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        screen.blit(text, pos)
        

    def load(self):
        self.background = pygame.image.load('BG.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))
        with open("map.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx, yidx))
                    elif char == "C":
                        self.coins.append(vec(xidx, yidx))
                    elif char == "P":
                        self.p_pos = [xidx, yidx]
                    elif char in ["2", "3", "4", "5"]:
                        self.e_pos.append([xidx, yidx])
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (xidx*self.cell_width, yidx*self.cell_height,
                                                                  self.cell_width, self.cell_height))
    
    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, vec(pos), idx)) 

 
    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'


    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('GET {} COINS TO WIN'.format(self.coinsToWin), self.screen, [
                       WIDTH//2, HEIGHT//2-50], START_TEXT_SIZE, YELLOW, START_FONT, centered=True)
        self.draw_text('PRESS SPACE TO START', self.screen, [
                       WIDTH//2, HEIGHT//2+100], START_TEXT_SIZE, YELLOW, START_FONT, centered=True)
        
        pygame.display.update()
########################### GAME PLAYING FUNCTIONS ################################
    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    self.console.set_active()
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))
                if event.key == pygame.K_F1:
                    self.state = 'console'
                if event.key == pygame.K_F2:
                    self.state = 'playing' 
                if event.key == pygame.K_F3:                    
                    self.EnemySpeed(0)  
                     
                if event.key == pygame.K_ESCAPE:
                    self.running = False


    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()

    def remove_life(self):
        self.player.lives -= self.RemoveLive
        if self.player.lives <= 0:
            self.state = "game over"

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.draw_coins()
        self.draw_text('SCORE: {}'.format(self.player.current_score), self.screen, [
                       75, 15], START_TEXT_SIZE, YELLOW, START_FONT, centered=True)
        self.draw_text('To WIN: {}'.format(self.coinsToWin), self.screen, [
                       475, 15], START_TEXT_SIZE, YELLOW, START_FONT, centered=True)
        if self.player.current_score == self.coinsToWin:
            self.state = "game win"
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()
        
    def draw_coins(self):
        for coin in self.coins: 
            pygame.draw.circle(self.screen, self.CoinColour,
                               (int(coin.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2,
                                int(coin.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 5)


########################### GAME WIN FUNCTIONS ################################

    def game_win_events(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False



    def game_win_draw(self):
        self.screen.fill(BLACK)
        quit_text = "Press the escape button to QUIT"
        again_text = "Press SPACE TO PLAY AGAIN"
        self.draw_text("You WIN", self.screen, [WIDTH//2, 100],  52, YELLOW,START_FONT, centered=True)
        self.draw_text(again_text, self.screen, [
                       WIDTH//2, HEIGHT//2],  30, WHITE, START_FONT, centered=True)
        self.draw_text(quit_text, self.screen, [
                       WIDTH//2, HEIGHT//1.5],  30, WHITE, START_FONT, centered=True)
        pygame.display.update()    

    def reset(self):
        self.player.lives = 3
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0

        self.coins = []
        with open("map.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
        self.state = "playing"

        ########################### GAME lost FUNCTIONS ################################

    def game_lost_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False


    def game_lost_draw(self):
        self.screen.fill(BLACK)
        quit_text = "Press the escape button to QUIT"
        again_text = "Press SPACE TO PLAY AGAIN"
        self.draw_text("You LOSE", self.screen, [WIDTH//2, 100],  52, RED,START_FONT, centered=True)
        self.draw_text(again_text, self.screen, [
                       WIDTH//2, HEIGHT//2],  30, WHITE, START_FONT, centered=True)
        self.draw_text(quit_text, self.screen, [
                       WIDTH//2, HEIGHT//1.5],  30, WHITE, START_FONT, centered=True)
        pygame.display.update() 

    def events(self, eventlist):
        for event in eventlist:
            if event.type == pygame.QUIT:
                self.running = False
                self.state == 'playing'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    self.console.set_active()
                    self.state == 'playing'
                if event.key == pygame.K_F2:
                    self.state == 'playing'
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.state == 'playing'