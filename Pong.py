import pygame
import random

# initiate pygame
pygame.init()

# game window/screen
pygame.display.set_caption("Pong")

# Create game window
WIDTH = 1280
HEIGHT = 640
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

CLOCK = pygame.time.Clock() # game tick speed function

# colours (R, G, B)
GREY = (200, 200, 200)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# game variables
main_menu = True
AI = False
freeze_game = False
reset_vars = False

ball_timer = 90
ball_speed = 7
ball_xspeed = ball_speed * random.choice((-1, 1))
ball_yspeed = ball_speed * random.choice((-1, 1))
paddle_speed = abs(ball_speed - 2)
player1_speed = 0
player2_speed = 0

#Set player scores to zero
scores = {"player 1": 0, "player 2": 0}

#All positions
ball_pos = {"x": WIDTH//2, "y": HEIGHT//2}
player1_pos = {"x": 80, "y": HEIGHT//2}
player2_pos = {"x": WIDTH-80, "y": HEIGHT//2}

# rect dimensions for visuals
ball = pygame.Rect(ball_pos["x"], ball_pos["y"], 20, 20)
player1 = pygame.Rect(0, 0, 20, 140)
player2 = pygame.Rect(0, 0, 20, 140)

def draw_text(text_string, text_size, colour, x_pos, y_pos):
    font = pygame.font.Font("freesansbold.ttf", text_size)
    text = font.render(text_string, True, colour)
    text_rect = text.get_rect(center=(x_pos, y_pos))
    SCREEN.blit(text, text_rect)

def starting_window():
    global ball_xspeed, ball_yspeed, scores, AI, main_menu, reset_vars
    if reset_vars:
        ball_xspeed = ball_speed * random.choice((-1, 1))
        ball_yspeed = ball_speed * random.choice((-1, 1))
        scores = {"player 1": 0, "player 2": 0}
        reset_vars = False

    KEYS = pygame.key.get_pressed()
    if KEYS[pygame.K_1]:
        AI = True
        main_menu = False
    elif KEYS[pygame.K_2]:
        main_menu = False
    draw_text("Pong", 100, WHITE, WIDTH//2, HEIGHT//2 - 100)
    draw_text("Press 1 for AI", 40, WHITE, WIDTH//2, HEIGHT//2 + 50)
    draw_text("Press 2 for 2 Players", 40, WHITE, WIDTH//2, HEIGHT//2 + 150)

def drawings_movement(AI):
    global player1_speed, player2_speed
    ball_pos["x"] += ball_xspeed
    ball_pos["y"] += ball_yspeed

    KEYS = pygame.key.get_pressed()
    if KEYS[pygame.K_w] and KEYS[pygame.K_s]:
        player1_speed = 0
    elif KEYS[pygame.K_w] and player1.top > 0:
        player1_speed = -paddle_speed
    elif KEYS[pygame.K_s] and player1.bottom < HEIGHT:
        player1_speed = paddle_speed
    else:
        player1_speed = 0

    if not AI:
        if KEYS[pygame.K_UP] and KEYS[pygame.K_DOWN]:
            player2_speed = 0
        elif KEYS[pygame.K_UP] and player2.top > 0:
            player2_speed = -paddle_speed
        elif KEYS[pygame.K_DOWN] and player2.bottom < HEIGHT:
            player2_speed = paddle_speed
        else:
            player2_speed = 0
    else:
        if ball_xspeed > 0:
            if ball.top < player2_pos["y"] and player2.top > 0:
                player2_speed = -paddle_speed
            elif ball.bottom > player2_pos["y"] and player2.bottom < HEIGHT:
                player2_speed = paddle_speed
            else:
                player2_speed = 0
        else:
            if player2_pos["y"] < HEIGHT//2:
                player2_speed = paddle_speed
            elif player2_pos["y"] > HEIGHT//2:
                player2_speed = -paddle_speed
            else:
                player2_speed = 0

    player1_pos["y"] += player1_speed
    player2_pos["y"] += player2_speed


def ball_collision():
    global ball_xspeed, ball_yspeed
    if ball.colliderect(player1) and ball_xspeed < 0:
        if abs(ball.left - player1.right) < abs(ball_xspeed):
            ball_xspeed *= -1
        elif abs(ball.bottom - player1.top) < abs(ball_yspeed) and ball_yspeed > 0:
            ball_yspeed *= -1
        elif abs(ball.top - player1.bottom) < abs(ball_yspeed) and ball_yspeed < 0:
            ball_yspeed *= -1
    
    if ball.colliderect(player2) and ball_xspeed > 0:
        if abs(ball.right - player2.left) < abs(ball_xspeed):
            ball_xspeed *= -1
        elif abs(ball.bottom - player2.top) < abs(ball_yspeed) and ball_yspeed > 0:
            ball_yspeed *= -1
        elif abs(ball.top - player2.bottom) < abs(ball_yspeed) and ball_yspeed < 0:
            ball_yspeed *= -1

    if abs(ball.top - 0) < abs(ball_yspeed) and ball_yspeed < 0:
        ball_yspeed *= -1
    elif abs(ball.bottom - HEIGHT) < abs(ball_yspeed) and ball_yspeed > 0:
        ball_yspeed *= -1


def display_drawings():
    draw_text(str(scores["player 1"]), 32, WHITE, WIDTH//2 - 100, 50)
    draw_text(str(scores["player 2"]), 32, WHITE, WIDTH//2 + 100, 50)
       
    ball.center = (ball_pos["x"], ball_pos["y"])
    player1.center = (player1_pos["x"], player1_pos["y"])
    player2.center = (player2_pos["x"], player2_pos["y"])

    if not freeze_game:
        pygame.draw.ellipse(SCREEN, WHITE, ball)
    pygame.draw.rect(SCREEN, WHITE, player1)
    pygame.draw.rect(SCREEN, WHITE, player2)


def start_round():
    global ball_timer
    if ball_timer > 60:
        draw_text("3", 32, WHITE, WIDTH//2, HEIGHT//2 - 30)
     

    if 30 < ball_timer < 60:
        draw_text("2", 32, WHITE, WIDTH//2, HEIGHT//2 - 30)

    if 0 < ball_timer < 30:
        draw_text("1", 32, WHITE, WIDTH//2, HEIGHT//2 - 30)
    
    ball_timer -= 1


def reset_ball():
    global ball_timer
    if ball.x not in range(WIDTH):
        ball_timer = 90
        ball_pos["x"] = WIDTH//2
        ball_pos["y"] = HEIGHT//2
        player1_pos["y"] = HEIGHT//2
        player2_pos["y"] = HEIGHT//2
        
        if ball.right >= WIDTH:
            ball_xspeed = -ball_speed
            scores["player 1"] += 1
        elif ball.left <= 0:
            ball_xspeed = ball_speed
            scores["player 2"] += 1
    

def end_game():
    global main_menu, freeze_game, reset_vars
    freeze_game = True
    if scores["player 1"] == 10:
        draw_text("PLAYER 1 WINS",  60, WHITE, WIDTH//2, HEIGHT//2)
    elif scores["player 2"] == 10:
        draw_text("PLAYER 2 WINS",  60, WHITE, WIDTH//2, HEIGHT//2)
    
    draw_text("Press Space To Return To Main Menu", 30, WHITE, WIDTH//2, HEIGHT//2 + 100)
    KEYS = pygame.key.get_pressed()
    if KEYS[pygame.K_SPACE]:
        main_menu = True
        freeze_game = False
        reset_vars = True

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        SCREEN.fill(BLACK)

        if main_menu:
            starting_window()
        else:
            if ball_timer > 0 and not freeze_game:
                start_round()
            else:
                ball_collision()
                if not freeze_game:
                    drawings_movement(AI)
            display_drawings()
            reset_ball()
            if scores["player 1"] == 10 or scores["player 2"] == 10:
                end_game()
            
            
        pygame.display.update()
        CLOCK.tick(60)


if __name__ == "__main__":
    main()
    pygame.quit()
