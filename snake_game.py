import pygame
from pygame.locals import *
from random import randint
from time import sleep
import os

UNIVERSAL_SIZE = 20
BACKGROUND_COLOR = (255, 255, 255)
CANVAS_SIZE = (800, 600)
base_directory = os.path.abspath(os.path.dirname(__file__))

class Apple:
    def __init__(self, game_canvas):
        self.apple_block = pygame.image.load(os.path.join(base_directory, 'resources/apple.jpg')).convert()
        self.apple_x = UNIVERSAL_SIZE*randint(1,(CANVAS_SIZE[0]//20)-1)
        self.apple_y = UNIVERSAL_SIZE*randint(1,(CANVAS_SIZE[1]//20)-1)
        self.game_canvas = game_canvas

    def draw_apple(self):
        self.game_canvas.blit(self.apple_block, (self.apple_x, self.apple_y))
        pygame.display.flip()

    def new_apple(self):
        
        while True:
            temp = UNIVERSAL_SIZE*randint(1,(CANVAS_SIZE[0]//20)-1)
            if (0 < temp < CANVAS_SIZE[0]):
                self.apple_x = temp
                break

        while True:
            temp = UNIVERSAL_SIZE*randint(1,(CANVAS_SIZE[1]//20)-1)
            if (0 < temp < CANVAS_SIZE[1]):
                self.apple_y = temp
                break 
        
        self.game_canvas.blit(self.apple_block, (self.apple_x, self.apple_y))
        pygame.display.flip() 

class Snake:
    def __init__(self, game_canvas, snake_length):
        self.snake_block = pygame.image.load(os.path.join(base_directory, 'resources/snake.jpg')).convert()
        self.game_canvas = game_canvas
        self.snake_length = snake_length
        self.snake_x = [UNIVERSAL_SIZE]*snake_length
        self.snake_y = [UNIVERSAL_SIZE]*snake_length

        random_direction = randint(1,4)
        if random_direction == 1:
            self.direction = 'upwards'
        elif random_direction == 2:
            self.direction = 'downwards'
        elif random_direction == 3:
            self.direction = 'right'
        elif random_direction == 4:
            self.direction = 'left'

        while True:
            temp = randint(80, CANVAS_SIZE[0]-80)
            if (temp % 20) == 0:      
                self.snake_x[0] = temp
                break
        
        while True:
            temp = randint(80,CANVAS_SIZE[1]-80)
            if (temp % 20) == 0:      
                self.snake_y[0] = temp
                break
         
    def draw_snake(self):
        self.game_canvas.fill(BACKGROUND_COLOR)
        for i in range (self.snake_length):
            self.game_canvas.blit(self.snake_block, (self.snake_x[i], self.snake_y[i]))
        pygame.display.flip()

    def snake_increase(self):
        self.snake_length += 1
        self.snake_x.append(-1)
        self.snake_y.append(-1)

    def move_upwards(self):
        self.direction = 'upwards'

    def move_downwards(self):
        self.direction = 'downwards'

    def move_right(self):
        self.direction = 'right'

    def move_left(self):
        self.direction = 'left'

    def continue_moving(self):
        for i in range (self.snake_length-1, 0, -1):
            self.snake_x[i] = self.snake_x[i-1]
            self.snake_y[i] = self.snake_y[i-1]
    
        if self.direction == 'upwards' :
            self.snake_y[0] -= 20
            self.draw_snake()
        elif self.direction == 'downwards':
            self.snake_y[0] += 20
            self.draw_snake()
        elif self.direction == 'right':
            self.snake_x[0] += 20
            self.draw_snake()
        elif self.direction == 'left':
            self.snake_x[0] -= 20
            self.draw_snake()

class Game:
    def __init__(self):
        pygame.init()
        game_icon = pygame.image.load(os.path.join(base_directory, "resources/icon.png"))
        pygame.display.set_icon(game_icon)
        pygame.display.set_caption('Snake and Apple Game      -- deepspraj')
        pygame.mixer.init()
        self.play_background_music()
        self.game_canvas = pygame.display.set_mode(CANVAS_SIZE)
        self.game_canvas.fill(BACKGROUND_COLOR)
        self.snake = Snake(self.game_canvas, 1)
        self.snake.draw_snake()
        self.apple = Apple(self.game_canvas)
        self.apple.draw_apple()
        self.game_over_channel = 0
        self.speed = 0.3

    def play_game(self):
        self.snake.continue_moving()
        self.apple.draw_apple()
        self.score_display_game()
        pygame.display.flip()

        if self.snake_ate_apple(self.snake.snake_x[0], self.snake.snake_y[0], self.apple.apple_x, self.apple.apple_y):
            self.snake.snake_increase()
            self.apple.new_apple()
            
        for i in range (3, self.snake.snake_length):
            if self.snake_ate_apple(self.snake.snake_x[0], self.snake.snake_y[0], self.snake.snake_x[i], self.snake.snake_y[i]):
                self.play_game_over_sound()
                raise "Game Over"

        if self.did_snake_escaped(self.snake.snake_x[0], self.snake.snake_y[0], CANVAS_SIZE[0], CANVAS_SIZE[1]):
            self.play_game_over_sound()
            raise "Snake Escaped"

    def set_bg_music_audio_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def play_game_over_sound(self, sound_file_name="game_over_1", stop=False):
        self.game_over_channel = pygame.mixer.Channel(1)
        game_over_sound = pygame.mixer.Sound(os.path.join(base_directory, f"resources/{sound_file_name}.wav"))
        self.game_over_channel.set_volume(0.25)
        self.game_over_channel.play(game_over_sound)

    def play_background_music(self):
        pygame.mixer.music.load(os.path.join(base_directory, "resources/bg_music_4.wav"))
        self.set_bg_music_audio_volume(0.15)
        pygame.mixer.music.play(loops=-1)

    def snake_ate_apple(self, snake_head_x, snake_head_y, apple_x, apple_y):
        if (snake_head_x >= apple_x) and ( snake_head_x < (apple_x + UNIVERSAL_SIZE)):
            if (snake_head_y >= apple_y) and ( snake_head_y < (apple_y + UNIVERSAL_SIZE)):
                return True
        return False

    def did_snake_escaped(self, snake_head_x, snake_head_y, x_coordinate, y_coordinate):
        if (snake_head_x == 0) or (snake_head_x == x_coordinate):
            return True
        elif (snake_head_y == 0) or (snake_head_y == y_coordinate):
            return True
        return False

    def score_display_game(self):
        font = pygame.font.SysFont("arial", 20)
        score = font.render(f"Score: {self.snake.snake_length}", True, (0, 0, 0))
        self.game_canvas.blit(score, (CANVAS_SIZE[0]-100, 20))

    def game_over(self):
        self.game_canvas.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont("arial", 20)
        score = font.render(f"Your score was {self.snake.snake_length}.", True, (0, 0, 0))
        self.game_canvas.blit(score, (CANVAS_SIZE[0]//8, (CANVAS_SIZE[1]//2)-50))
        score = font.render("Please hit enter to restart the game or escape to exit!", True, (0, 0, 0))
        self.game_canvas.blit(score, (CANVAS_SIZE[0]//8, (CANVAS_SIZE[1]//2)))
        score = font.render("Made with love.", True, (0, 0, 0))
        self.game_canvas.blit(score, (CANVAS_SIZE[0]//8, (CANVAS_SIZE[1]//2)+50))
        pygame.display.flip()
    
    def reset_game(self):
        self.snake = Snake(self.game_canvas, 1)
        self.apple = Apple(self.game_canvas)

    def start(self):
        run_main_while = True
        game_over_status = False

        while run_main_while:

            for event in pygame.event.get():
                if event.type == KEYDOWN:

                    if event.key == K_RETURN:
                        game_over_status = False
                        pygame.mixer.music.unpause()
                        self.game_over_channel.stop()
                        self.speed = 0.3

                    if (event.key == K_ESCAPE) or (event.key == K_q):
                        run_main_while = False

                    if not game_over_status:
                        if (event.key == K_w):
                            self.snake.move_upwards()
                        if (event.key == K_s):
                            self.snake.move_downwards()
                        if (event.key == K_d):
                            self.snake.move_right()
                        if (event.key == K_a):
                            self.snake.move_left()
                elif event.type == QUIT:
                    run_main_while = False

            speed_adjuster = ((-0.00011904761904761894*(self.snake.snake_length**2)) - (0.005238095238095236*self.snake.snake_length) + 0.3053571428571429)
            
            if 0.03 < speed_adjuster < 0.3:
                self.speed = round(speed_adjuster,3)
                
            sleep(self.speed)

            try:
                if not game_over_status:
                    self.play_game()
            except:
                pygame.mixer.music.pause()
                self.game_over()
                self.reset_game()
                game_over_status = True


if __name__ == "__main__":
    new_game = Game()
    new_game.start()