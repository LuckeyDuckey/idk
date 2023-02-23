import pygame, sys                                                  # 20 - 40
from pygame.locals import *
import math
import Pygame_Lights

fps = pygame.time.Clock()
pygame.init()

light = Pygame_Lights.LIGHT(500, Pygame_Lights.pixel_shader(500, (255,255,255), 1, False))

tile_image = pygame.image.load('tile2.png')
tile_size = tile_image.get_width()
def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map
game_map = load_map('mapV1')
map_size = len(game_map[0])
screen_width = tile_size*map_size / 2
screen = pygame.display.set_mode((screen_width, screen_width))

player_image =  pygame.image.load('player.png')
player_image.set_colorkey((255,255,255))
player_rect = pygame.Rect(550,500,50,50)
speed = 5
moving_right = False
moving_left = False
moving_up = False
moving_down = False
player_loc = [550,500]
player_angle = math.pi
FOV = math.pi / 2
HALF_FOV = FOV / 2
CASTED_RAYS = 500
STEP_ANGLE = FOV / CASTED_RAYS

font = pygame.font.SysFont("Arial" , 18 , bold = True)
def fps_counter():
    FPS = str(int(fps.get_fps()))
    fps_t = font.render(FPS , 1, pygame.Color("RED"))
    screen.blit(fps_t,(0,0))
true_scroll = [0,0]
while True:
    screen.fill((255,255,0))

    true_scroll[0] += (player_rect.x-true_scroll[0] - (screen_width / 2)) / 20
    true_scroll[1] += (player_rect.y-true_scroll[1] - (screen_width / 2)) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])


    mouse_x, mouse_y = pygame.mouse.get_pos()
    if ((player_rect.x-scroll[0] + 25) - mouse_x) == 0:
        if (player_rect.y-scroll[1] + 25) < mouse_y:
            player_angle = (3 * math.pi) / 2
        if (player_rect.y-scroll[1] + 25) > mouse_y:
            player_angle = math.pi / 2
    elif ((player_rect.y-scroll[1] + 25) - mouse_y) == 0:
        if (player_rect.x-scroll[0] + 25) > mouse_x:
            player_angle = math.pi
        if (player_rect.x-scroll[0] + 25) < mouse_x:
            player_angle = 0
    else:
        player_angle = math.atan(((player_rect.y-scroll[1] + 25) - mouse_y) / ((player_rect.x-scroll[0] + 25) - mouse_x))
        if (player_rect.y-scroll[1] + 25) > mouse_y and (player_rect.x-scroll[0] + 25) < mouse_x:
            player_angle = -1 * player_angle
        if (player_rect.y-scroll[1] + 25) > mouse_y and (player_rect.x-scroll[0] + 25) > mouse_x:
            player_angle =  math.pi - player_angle
        if (player_rect.y-scroll[1] + 25) < mouse_y and (player_rect.x-scroll[0] + 25) > mouse_x:
            player_angle = math.pi - player_angle
        if (player_rect.y-scroll[1] + 25) < mouse_y and (player_rect.x-scroll[0] + 25) < mouse_x:
            player_angle = (2 * math.pi) - player_angle
    player_angle = -1 * player_angle

    right_bound = player_rect.x + (screen_width / 2)
    left_bound = player_rect.x - (screen_width / 2)
    up_bound = player_rect.y + (screen_width / 2)
    down_bound = player_rect.y - (screen_width / 2)


    left_angle = player_angle - HALF_FOV
    right_angle = player_angle + HALF_FOV
    pygame.draw.line(screen, (0, 255, 255), ((player_rect.x-scroll[0] + 25), (player_rect.y-scroll[1] + 25)), ((player_rect.x-scroll[0] + 25) + (math.cos(right_angle) * 500),  (player_rect.y-scroll[1] + 25) + (math.sin(right_angle) * 500)), 2)
    pygame.draw.line(screen, (0, 255, 255), ((player_rect.x-scroll[0] + 25), (player_rect.y-scroll[1] + 25)), ((player_rect.x-scroll[0] + 25) + (math.cos(left_angle) * 500),  (player_rect.y-scroll[1] + 25) + (math.sin(left_angle) * 500)), 2)







    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                screen.blit(tile_image, (x*tile_size - scroll[0] , y*tile_size - scroll[1]))
            if tile == '1':
                 tile_rects.append(pygame.Rect(x * tile_size , y * tile_size  , tile_size, tile_size))
            x += 1
        y += 1

    collisions = []
    if moving_left == True:
        player_rect.x -= speed
        player_loc[0] -= speed
    if moving_right == True:
        player_rect.x += speed
        player_loc[0] += speed
    for tile in tile_rects:
        if player_rect.colliderect(tile):
            collisions.append(tile)
    for tile in collisions:
        if moving_left == True:
            player_rect.left = tile.right
        if moving_right == True:
            player_rect.right = tile.left
        player_loc[0] = player_rect.x
    collisions = []
    if moving_up == True:
        player_rect.y -= speed
        player_loc[1] -= speed
    if moving_down == True:
        player_rect.y += speed
        player_loc[1] += speed
    for tile in tile_rects:
        if player_rect.colliderect(tile):
            collisions.append(tile)
    for tile in collisions:
        if moving_up == True:
            player_rect.top = tile.bottom
        if moving_down == True:
            player_rect.bottom = tile.top
        player_loc[1] = player_rect.y
    screen.blit(player_image, (player_rect.x-scroll[0],player_rect.y-scroll[1]))

    #Lighting ------
    shadow_objects = []

    for tile in tile_rects:
        shadow_objects.append(pygame.Rect(tile.x-scroll[0], tile.y-scroll[1], tile.width, tile.height))
    
    lights_display = pygame.Surface((screen.get_size()))
    
    lights_display.blit(Pygame_Lights.global_light(screen.get_size(), 25), (0,0))
    light.main(shadow_objects, lights_display, player_rect.x+(player_rect.width / 2)-scroll[0], player_rect.y+(player_rect.height / 2)-scroll[1])
    
    screen.blit(lights_display, (0,0), special_flags=BLEND_RGBA_MULT)
    #---------------

    points = []
    for tile in tile_rects:
        if left_bound < (tile.left + 50) and right_bound > (tile.right - 50) and up_bound < (tile.top + 50) and down_bound > (tile.bottom + 50):
            points.append(tile.left)
            pygame.draw.rect(screen, ( 255,0,0), tile)









    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_d:
                moving_right = True
            if event.key == K_a:
                moving_left = True
            if event.key == K_w:
                moving_up = True
            if event.key == K_s:
                moving_down = True
        if event.type == KEYUP:
            if event.key == K_d:
                moving_right = False
            if event.key == K_a:
                moving_left = False
            if event.key == K_w:
                moving_up = False
            if event.key == K_s:
                moving_down = False


    fps_counter()
    pygame.display.update()
    fps.tick(60)
