import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 498, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball and Bar!")

#sizing the assets
object_size = 45 #fitting in circle so no need of height and width
bar_height = 10
bar_width = 57

#load all assets
background = pygame.image.load("bk.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_night = pygame.image.load("night.png")
background_night = pygame.transform.scale(background_night, (WIDTH, HEIGHT))
countdown_images = [
    pygame.transform.scale(pygame.image.load("3.png"), (50, 50)),
    pygame.transform.scale(pygame.image.load("2.png"), (50, 50)),
    pygame.transform.scale(pygame.image.load("1.png"), (50, 50))
]
object_img = pygame.image.load("object.png").convert_alpha()
object_img = pygame.transform.scale(object_img, (object_size, object_size))

WallBounce=pygame.mixer.Sound("WallBounce.mp3")
BarBounce=pygame.mixer.Sound("BarBounce.wav")
GameOver=pygame.mixer.Sound("GameOver.wav")

#defining some basic colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BUTTON_COLOR = (25, 50, 75)
BUTTON_HOVER = (72, 220, 115)

#highscore file
def highscore():
    try:
        with open("highscore.txt", "r") as file:
            content = file.read()
            if content.strip() == "":
                return 0
            else:
                return int(content)
    except FileNotFoundError:
        return 0

#store highscore in the file
def store_highscore(new_highscore):
    with open("highscore.txt", "w") as file:
        file.write(str(new_highscore)) #our score is int but file.write only accepts str.

high_score = highscore()

#defining position and speed of assets
bar_pos = [WIDTH // 2, 619] #using tuple for x,y coordinates
bar_speed = 8
SPEED = 8

object_pos = [random.randint(0, WIDTH - object_size), 0] 
object_speed_x = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
object_speed_y = (SPEED ** 2 - object_speed_x ** 2) ** 0.5

#pygame.time.clock functio as clock used for FPS
clock = pygame.time.Clock() #clock function used for FPS 

#score
score = 0
font = pygame.font.SysFont("monospace", 20)

#we can also pause the game
paused = False

#resume
resume = False

#draw text on event function
def draw_text(text, font, color, surface, x, y):
    textbox = font.render(text, True, color)
    rect = textbox.get_rect(center=(x, y))
    surface.blit(textbox, rect) #blit used for adding something on top on something
    return rect

#creating a box in which text will lie
def draw_button(text, font, surface, rect, hover=False):
    pygame.draw.rect(surface, BUTTON_HOVER if hover else BUTTON_COLOR, rect, border_radius=5)
    draw_text(text, font, WHITE, surface, rect.centerx, rect.centery)

#pause and resume buttons
pause_button_rect = pygame.Rect(WIDTH - 110, 10, 100, 40)
resume_button_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2, 120, 50)

#countdown before resuming
def countdown():
    for img in countdown_images:
        screen.blit(background, (0, 0))
        screen.blit(object_img, (object_pos[0], object_pos[1]))  #show ball position before resuming
        pygame.draw.rect(screen, GREEN, (bar_pos[0], bar_pos[1], bar_width, bar_height))  #show bar position before resuming
        screen.blit(img, (WIDTH // 2 - 25, HEIGHT // 2 - 25))
        pygame.display.update()
        pygame.time.delay(1000) #can also use time.sleep(1)

#game over screen 
def gameover():
    global score, object_pos, object_speed_x, object_speed_y, high_score, resume

    if score > high_score: #iterating the highscore
        store_highscore(score)
        high_score = score

#creating the gameover screen
    while True:
        screen.blit(background_night, (0, 0)) #different screen for gameover
        draw_text("Game Over!", font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 100)
        draw_text(f"Your Score: {score}", font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 60)
        draw_text(f"High Score: {high_score}", font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 30)

        play_again_rect = pygame.Rect(WIDTH // 2 - 140, HEIGHT // 2 + 30, 120, 50)
        exit_rect = pygame.Rect(WIDTH // 2 + 20, HEIGHT // 2 + 30, 120, 50)

        mouse_pos = pygame.mouse.get_pos()
        #collidepoint function used to change color when we arrive the play button
        draw_button("Play Again", font, screen, play_again_rect, play_again_rect.collidepoint(mouse_pos))
        draw_button("Exit", font, screen, exit_rect, exit_rect.collidepoint(mouse_pos))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_rect.collidepoint(event.pos):
                    reset_game()
                    countdown()
                    return
                if exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_RETURN):
                    reset_game()
                    countdown()
                    return
                if event.key in (pygame.K_RIGHT, pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(60) #FPS.

def reset_game():
    global score, object_pos, object_speed_x, object_speed_y, bar_pos, paused
    score = 0
    paused = False
    object_pos = [random.randint(0, WIDTH - object_size), 0]
    object_speed_x = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
    object_speed_y = (SPEED ** 2 - object_speed_x ** 2) ** 0.5
    bar_pos = [WIDTH // 2, 619]

#main menu before starting game
def main_menu():
    while True:
        screen.blit(background, (0, 0))
        draw_text("Welcome to Ball and Bar!", font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 100)

        play_rect = pygame.Rect(WIDTH // 2 - 140, HEIGHT // 2, 120, 50)
        exit_rect = pygame.Rect(WIDTH // 2 + 20, HEIGHT // 2, 120, 50)

        mouse_pos = pygame.mouse.get_pos()
        draw_button("Play", font, screen, play_rect, play_rect.collidepoint(mouse_pos))
        draw_button("Exit", font, screen, exit_rect, exit_rect.collidepoint(mouse_pos))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    countdown()
                    return
                if exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_RETURN):
                    countdown()
                    return
                if event.key in (pygame.K_RIGHT, pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(60)

#exucuting it
main_menu()

#game loop
running = True
while running:
    screen.blit(background, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                running = False

        #mouse click for pause button and resume
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not paused and pause_button_rect.collidepoint(event.pos):
                paused = True
            elif paused and resume_button_rect.collidepoint(event.pos):
                paused = False
                countdown()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
                if not paused:
                    countdown()
#controls of game
    if not paused:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and bar_pos[0] > 0:
            bar_pos[0] -= bar_speed
        if keys[pygame.K_RIGHT] and bar_pos[0] < WIDTH - bar_width:
            bar_pos[0] += bar_speed

        #object position
        prev_object_y = object_pos[1]
        object_pos[0] += object_speed_x
        object_pos[1] += object_speed_y

        #collision detection with bar
        if prev_object_y <= bar_pos[1] <= object_pos[1] + object_size:
            if (object_pos[0] + object_size >= bar_pos[0]) and (object_pos[0] <= bar_pos[0] + bar_width):
                object_speed_y = -object_speed_y
                score += 1
                BarBounce.play()

        #collision detection with wall
        if object_pos[0] <= 0 or object_pos[0] >= WIDTH - object_size:
            object_speed_x = -object_speed_x
            WallBounce.play()
        if object_pos[1] <= 0:
            object_speed_y = -object_speed_y
            WallBounce.play()

        #game over
        if object_pos[1] >= HEIGHT - object_size:
            GameOver.play()
            gameover()

        #draw objects with proper positions
        pygame.draw.rect(screen, GREEN, (bar_pos[0], bar_pos[1], bar_width, bar_height))
        screen.blit(object_img, (object_pos[0], object_pos[1]))

        draw_button("Pause", font, screen, pause_button_rect, pause_button_rect.collidepoint(mouse_pos))

    else:
        draw_text("Game Paused", font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 60)
        draw_button("Resume", font, screen, resume_button_rect, resume_button_rect.collidepoint(mouse_pos))

    # Draw score and high score
    score_text = font.render(f"Score: {score}", True, BLACK)
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)

    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 40))  # Positioned below the score

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
