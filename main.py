import pygame
import random
import asyncio

WIDTH = 800
HEIGHT = 600
# custom fonts can be used if you download a font file from online 
# font = pygame.font.Font("font.ttf", 36)

# Initialise Pygame - can be left alone
def init_window():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    return window
# Handle events - can be left alone
def handle_events(game_state):
    # return false if user presses the cross
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state = "end"
        if game_state == "play":
            pass
        elif game_state == "intro":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = "play"
        elif game_state == "game_over":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = "end"
        
    # keep running the game
    return game_state

window = init_window()
font = pygame.font.Font(None, 36)

def intro(window):
    window.fill((0, 0, 0))  # Fill background with black
    text_surface = font.render("Minigame instructions blah blah - omg its WASM!!!", True, (255,255,255))  # (text, anti-aliasing, color)
    window.blit(text_surface, (150, 200))  # Draw text at (x, y)
    text_surface = font.render("Press Enter to start", True, (255,255,255))  # (text, anti-aliasing, color)
    window.blit(text_surface, (150, 250))  # Draw text at (x, y)
        

def game_over(window, score):
    window.fill((0, 0, 0))  # Fill background with black
    text_surface = font.render("Game Over!", True, (255,255,255))  # (text, anti-aliasing, color)
    window.blit(text_surface, (150, 200))  # Draw text at (x, y)
    text_surface = font.render(f"Score: {score}", True, (255,255,255))  # (text, anti-aliasing, color)
    window.blit(text_surface, (150, 250))  # Draw text at (x, y)


# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # ▼ USE this code instead for an image ▼
        # sprite_image = pygame.image.load("sprite.png")
        # self.image = sprite_image

        # USE this code for a simple coloured square for testing
        self.image = pygame.Surface((50, 50))
        self.image.fill(color=(0,255,0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]: self.rect.x += self.speed
        if keys[pygame.K_UP]: self.rect.y -= self.speed
        if keys[pygame.K_DOWN]: self.rect.y += self.speed

# "Enemy" Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        self.image = pygame.Surface((25, 25))
        self.image.fill(color=(255,0,0))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5

    def update(self):
        # enemies move to the left constantly
        self.rect.x -= self.speed
        # reset to a random position when go off edge of screen
        if self.rect.x < -25:
            self.rect.x = 800
            self.rect.y = random.randint(0,575)
            self.speed += 1 # increase speed too to make it harder?

# Draw every object for each frame of the game
def draw(window, score):
    # you can draw basic shapes using RECT, CIRCLE, LINE, ELLIPSE etc.
    #                           ▼ rgb colour   ▼ x,y    ▼ width, height
    # pygame.draw.rect(window, (255, 255, 0), (50, 50, 100, 100))  # Draw yellow rectangle
    #                             ▼ rgb colour   ▼ x,y    ▼ radius
    # pygame.draw.circle(window, (0,255,255), (100,200), 70)

    # Fill background with black (clear screen from last frame)
    window.fill((0, 0, 0))
    # draw every sprite in our all sprite group
    sg_all.draw(window)
    # draw any text or user interface
    text_surface = font.render(f"Score: {score}", True, (255,255,255))  # (text, anti-aliasing, color)
    window.blit(text_surface, (5, 5))  # Draw text at (x, y)

sg_all = pygame.sprite.Group()
sg_enemies = pygame.sprite.Group()

async def run(house):
    # Initialise global sprite groups   sg = sprite group
    
    # Do something with house (string) if you want
    # house will be one of "county", "east", "laud", "school", "west"

    game_state = "intro"
    intro(window)

    # initialise starting sprites and add to sprite group
    player = Player(100,300)
    sg_all.add(player)

    # MAKE SOME RANDOM ENEMIES ON THE RIGHT SIDE
    for i in range(5):
        new_enemy = Enemy(800, random.randint(0,575))
        sg_enemies.add(new_enemy) # add to just enemies for collisions etc.
        sg_all.add(new_enemy) # add to everything for ease of drawing

    score = 0
    running = True
    clock = pygame.time.Clock()
    while running:
        game_state = handle_events(game_state)

        if game_state == "play":
            # update (move) all sprites
            player.update()
            # loop through every enemy in the sprite group and update it
            for enemy in sg_enemies:
                enemy.update()

            # check collisions             ▼ sprite  ▼ group   ▼ True = destroy sprites from group on hit (very useful for coins etc?)
            if pygame.sprite.spritecollide(player, sg_enemies, False):
                print("Game Over")
                game_state = "gameover"

            # you can also loop over a sprite group to grab the individual sprites
            # then process collisions from their perspective individually if need be
            # great if you have multiple groups that all need to collide with each other
            # for enemy in sg_enemies: #         ▼ individual sprite
            #     if pygame.sprite.spritecollide(enemy, sg_some_other_group, False):
            #         pass # do something in response    ▲ sprite group

            score += 1 # increase score every frame

            # draw everything on screen
            draw(window, score)
        elif game_state == "intro":
            intro(window)
        elif game_state == "gameover":
            game_over(window, score)
        elif game_state == "end":
            running = False
        pygame.display.update()
        clock.tick(60) # finish with a pause, limiting frame rate to 60 fps
        await asyncio.sleep(0)

asyncio.run(run(window))