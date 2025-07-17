import pygame
import sys
import random

pygame.init()


###---------------background/player----------------###
# texts / timers
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# window dimensions
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Monster Slayer')

# global variables
floor = pygame.Rect(0, SCREEN_HEIGHT - 150, SCREEN_WIDTH, 150)

player_x = 90
player_y = 210
player_size = 40
player = pygame.Rect(player_x, player_y, player_size, player_size)
player_img = pygame.image.load(f"sprites/player_1.png")

frame = 0
frames_left = 1000

score = 0
top_score = 0
pressed_down = 0


###------------------------monster :] ------------------------###
slimeM_x = 650
slimeM_y = 220
slimeM_size = 50
slimeM = pygame.Rect(slimeM_x, slimeM_y, slimeM_size, slimeM_size)
slimeM_img = pygame.image.load(f"sprites/slime_monster.png")
slimeM_img = pygame.transform.scale(slimeM_img, (150, 150))


###-----------drawing bg function-----------------###

DARK_GREEN = (0, 150, 0)
SKY_BLUE = (105, 186, 255)
WHITE = (255,255,255)

def draw_setting():
    """Draws background and floors onto the screen"""
    pygame.draw.rect(screen, SKY_BLUE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.draw.rect(screen, DARK_GREEN, floor)
    score_txt = font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(score_txt, (10, 10))


###-------------------------Other Functions---------------------###
def update_player():
    """Control player's movement and image, and detect collisions w/ floor and enemies"""
    global player_x, player_y, player, player_img, platform_list,score, pressed_down
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        player_img = pygame.image.load("sprites/player_2.png")
        pressed_down = 1
    else:
        player_img = pygame.image.load("sprites/player_1.png")
        pressed_down = 0
    if not hasattr(update_player, "space_held_frames"):
        update_player.space_held_frames = 0
    if keys[pygame.K_SPACE]:
        update_player.space_held_frames += 1
        if update_player.space_held_frames > 7:
            player_img = pygame.image.load("sprites/player_1.png")
            pressed_down = 0
    else:
        update_player.space_held_frames = 0
        
    screen.blit(player_img, (player_x, player_y))
    

def update_slimeM():
	global slimeM_x, slimeM_y, slimeM, slimeM_size, pressed_down, score

	# slime list
	if not hasattr(update_slimeM, "slimes"):
		update_slimeM.slimes = []
		update_slimeM.spawn_timer = 0

	# slime spawner
	if len(update_slimeM.slimes) == 0 or update_slimeM.spawn_timer <= 0:
		speed = random.randint(10, 30)
		new_slime = {
			"rect": pygame.Rect(650, 220, slimeM_size, slimeM_size),
			"speed": speed
		}
		update_slimeM.slimes.append(new_slime)
		update_slimeM.spawn_timer = random.randint(7, 20)  # frames between spawns

	# slime deleter lol
	for slime in update_slimeM.slimes[:]:
		slime["rect"].x -= slime["speed"]
		# Check for hit and remove if hit
		if player.colliderect(slime["rect"]) and pressed_down == 1:
			update_slimeM.slimes.remove(slime)
			score += 1
			continue
		screen.blit(slimeM_img, (slime["rect"].x, slime["rect"].y))
		if slime["rect"].right < 0:
			update_slimeM.slimes.remove(slime)

	# list updater
	if update_slimeM.slimes:
		slimeM = update_slimeM.slimes[0]["rect"]
		slimeM_x = slimeM.x
		slimeM_y = slimeM.y
	else:
		slimeM = pygame.Rect(-100, -100, slimeM_size, slimeM_size)
		slimeM_x = -100
		slimeM_y = -100

	# spawn  timer
	update_slimeM.spawn_timer -= 1
    

    
def game_over_display():
    """Displays game stats whenever time runs out"""
    global score

    screen.fill(SKY_BLUE)
    game_over_txt = font.render("Game Over", True, WHITE)
    score_txt = font.render(f"Your score was: {score}", True, WHITE)
    top_score_txt = font.render(f"The high score is: {top_score}",True,WHITE)
    restart_txt = font.render("Press R to restart, or Q to quit",True, WHITE)

    #Draw the above text onto the screen
    screen.blit(game_over_txt, (SCREEN_WIDTH // 2 - game_over_txt.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(score_txt, (SCREEN_WIDTH // 2 - score_txt.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(top_score_txt, (SCREEN_WIDTH // 2 - top_score_txt.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(restart_txt, (SCREEN_WIDTH // 2 - restart_txt.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.update()

    input_waiting = True
                    
def advance_timer():
    """Every frame, reduce the time left for the game and display this change"""
    global top_score, frames_left

    frames_left -= 1
    timer_txt = font.render(f"Time left: {frames_left}", True, (255, 255, 255))
    screen.blit(timer_txt, (10, 60))

    #Check if the timer has run out, meaning the game is over
    if frames_left <= 0:
        if score > top_score:
            top_score = score
        game_over_display()

def reset_variables():
    """Every time the game_loop is rerun, reset relevant variables"""
    global frames_left, score, platform_list, player_x, player_y, slimeM_x, slimeM_y

    frames_left = 1000
    score = 0
    platform_list = []
    player_x = 5
    player_y = 210
    slimeM_x = 650
    slimeM_y = 220


###----------------------------Game Loop------------------------###
def game_loop():
    """This function runs our main game loop, yippie!"""
    global frame
  
    reset_variables()
    running = True
    while running:
        #Here is an instance of event handling, checking if the user wants to exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if frames_left <= 0:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: # Press R to restart
                        input_waiting = False
                        reset_variables()
                    elif event.key == pygame.K_q: # Press Q to quit
                        pygame.quit()
                        sys.exit()
        if frames_left > 0:
            draw_setting() #Drawing floor
            update_player() #Let's allow our player to move and collide with things
            update_slimeM()
            advance_timer() #Progress the game timer and check if it's run out

        # Now that we've made our changes to the frame, let's update the screen to reflect those changes:
        pygame.display.update()
        clock.tick(30) #This functions helps us cap the FPS (Frames per Second)
        frame += 1 #We use this frame variable to animate our player

game_loop()