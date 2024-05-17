from eng import render_text

import glfw
from OpenGL.GL import *
from math import cos, sin
import random

# Game variables
char_radius = 15
char_x = 30
char_y = 0
move_speed = 2
is_jumping = False
jump_velocity = 5 
gravity = 0.1
fall_speed = 0 
max_fall_speed = 10 
is_on_platform = False
WIDTH, HEIGHT = 1920, 1080

key_state = {glfw.KEY_LEFT: False, glfw.KEY_RIGHT: False, glfw.KEY_SPACE: False}

score = 0
game_won = False
game_lost = False

def init_window():
    if not glfw.init():
        raise Exception("glfw can not be initialized!")
    
    global WIDTH, HEIGHT
    HEIGHT -= 70
    global char_y
    char_y = HEIGHT / 2 - char_radius

    glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
    
    window = glfw.create_window(WIDTH, HEIGHT, "Pixel Platformer", None, None)
    if not window:
        glfw.terminate()
        raise Exception("glfw window can not be created!")
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    screen_width = glfw.get_video_mode(glfw.get_primary_monitor()).size.width
    screen_height = glfw.get_video_mode(glfw.get_primary_monitor()).size.height
    glfw.set_window_pos(window, (screen_width - WIDTH) // 2, (screen_height - HEIGHT) // 2)
    return window

def init_opengl():
    glViewport(0, 0, WIDTH, HEIGHT)
    glOrtho(0, WIDTH, HEIGHT, 0, -1, 1)

def reset_game():
    global char_x, char_y, is_jumping, jump_velocity, fall_speed, is_on_platform, score, game_won, game_lost
    global obstacles, coins

    char_x = 30
    char_y = HEIGHT / 2 - char_radius
    is_jumping = False
    jump_velocity = 5
    fall_speed = 0
    is_on_platform = False
    score = 0
    game_won = False
    game_lost = False
    obstacles = generate_obstacles()
    coins = generate_coins()

def game_over():
    global game_lost
    if game_won or game_lost:
        return
    print("Game Over")
    game_lost = True

def you_win():
    global game_won
    if game_won or game_lost:
        return
    print("You Win!!")
    game_won = True

def key_input(window, key, scancode, action, mods):
    global is_jumping, jump_velocity, is_on_platform

    if action == glfw.PRESS:
        if key in key_state:
            key_state[key] = True
        if key == glfw.KEY_SPACE and is_on_platform and not is_jumping:
            is_jumping = True
            jump_velocity = 5
            is_on_platform = False
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)
        if key == glfw.KEY_R:
            reset_game()

    if action == glfw.RELEASE:
        if key in key_state:
            key_state[key] = False

platforms = [
    {'position': (680, 50), 'size': (120, 20), 'color': (0.0, 0.0, 1.0)}, # blue
    {'position': (500, 90), 'size': (140, 20), 'color': (0.7, 0.2, 0.5)}, # pink
    {'position': (100, 100), 'size': (150, 20), 'color': (0.2, 0.5, 0.4)}, # teal
    {'position': (1700, 100), 'size': (150, 20), 'color': (0.5, 0.5, 0.2)}, # tan
    {'position': (1000, 120), 'size': (150, 20), 'color': (0.2, 0.5, 0.4)}, # teal
    {'position': (1200, 150), 'size': (120, 20), 'color': (0.8, 0.1, 0.3)}, # red
    {'position': (300, 150), 'size': (180, 20), 'color': (0.5, 0.4, 0.2)}, # tan
    {'position': (1400, 200), 'size': (160, 20), 'color': (0.2, 0.3, 0.8)}, # blue
    {'position': (800, 200), 'size': (130, 20), 'color': (0.6, 0.4, 0.3)}, # brown
    {'position': (580, 200), 'size': (120, 20), 'color': (0.5, 0.5, 0.1)}, # olive
    {'position': (50, 250), 'size': (110, 20), 'color': (0.3, 0.6, 0.7)}, # light blue
    {'position': (700, 250), 'size': (140, 20), 'color': (0.7, 0.4, 0.5)}, # pink
    {'position': (450, 300), 'size': (160, 20), 'color': (0.7, 0.2, 0.5)}, # pink
    {'position': (1600, 300), 'size': (170, 20), 'color': (0.4, 0.8, 0.2)}, # green
    {'position': (1000, 300), 'size': (150, 20), 'color': (0.5, 0.3, 0.7)}, # purple
    {'position': (800, 300), 'size': (170, 20), 'color': (0.5, 0.2, 0.7)}, # purple
    {'position': (200, 350), 'size': (140, 20), 'color': (0.4, 0.7, 0.3)}, # green
    {'position': (1700, 350), 'size': (120, 20), 'color': (0.4, 0.7, 0.4)}, # green
    {'position': (550, 400), 'size': (130, 20), 'color': (0.5, 0.5, 0.1)}, # olive
    {'position': (1000, 400), 'size': (170, 20), 'color': (0.4, 0.5, 0.7)}, # blue
    {'position': (1200, 400), 'size': (160, 20), 'color': (0.5, 0.3, 0.7)}, # purple
    {'position': (1800, 450), 'size': (120, 20), 'color': (0.3, 0.4, 0.5)}, # blue
    {'position': (800, 450), 'size': (170, 20), 'color': (0.1, 0.3, 0.9)}, # blue
    {'position': (150, 500), 'size': (100, 20), 'color': (0.2, 0.6, 0.3)}, # green
    {'position': (680, 500), 'size': (100, 20), 'color': (0.2, 0.6, 0.3)}, # green
    {'position': (1600, 500), 'size': (170, 20), 'color': (0.4, 0.6, 0.3)}, # green
    {'position': (1400, 500), 'size': (130, 20), 'color': (0.9, 0.6, 0.3)}, # yellow
    {'position': (1700, 550), 'size': (150, 20), 'color': (0.2, 0.7, 0.4)}, # green
    {'position': (1100, 550), 'size': (180, 20), 'color': (0.1, 0.6, 0.4)}, # green
    {'position': (500, 600), 'size': (110, 20), 'color': (0.8, 0.2, 0.4)}, # red
    {'position': (900, 600), 'size': (110, 20), 'color': (0.3, 0.5, 0.9)}, # light blue
    {'position': (300, 700), 'size': (180, 20), 'color': (0.3, 0.5, 0.9)}, # light blue
    {'position': (1200, 700), 'size': (180, 20), 'color': (0.5, 0.7, 0.4)}, # green
    {'position': (600, 700), 'size': (140, 20), 'color': (0.8, 0.4, 0.5)}, # pink
    {'position': (100, 760), 'size': (100, 20), 'color': (0.4, 0.8, 0.2)}, # green
    {'position': (300, 800), 'size': (130, 20), 'color': (0.6, 0.7, 0.3)}, # yellow-green
    {'position': (500, 800), 'size': (170, 20), 'color': (0.7, 0.5, 0.2)}, # tan
    {'position': (0, 960), 'size': (100, 20), 'color': (0.4, 0.8, 0.2)}, # green
    {'position': (100, 880), 'size': (120, 20), 'color': (0.6, 0.3, 0.8)}, # purple
    {'position': (1500, 850), 'size': (120, 20), 'color': (0.7, 0.2, 0.6)}, # pink
    {'position': (900, 850), 'size': (150, 20), 'color': (0.2, 0.7, 0.6)}, # teal
    {'position': (650, 900), 'size': (130, 20), 'color': (0.6, 0.4, 0.8)}, # purple
    {'position': (1100, 900), 'size': (150, 20), 'color': (0.2, 0.5, 0.7)}, # blue
    {'position': (1800, 900), 'size': (180, 20), 'color': (0.3, 0.4, 0.7)}, # blue
    {'position': (1180, 950), 'size': (140, 20), 'color': (0.5, 0.5, 0.1)}, # olive
    {'position': (350, 950), 'size': (180, 20), 'color': (0.3, 0.2, 0.9)}, # purple
    {'position': (100, 1050), 'size': (150, 20), 'color': (0.7, 0.3, 0.2)}, # brown
    {'position': (600, 1000), 'size': (180, 20), 'color': (0.5, 0.2, 0.8)}, # purple
    #for the borders
    {'position': (0, 0), 'size': (1920, 20), 'color': (0.0, 0.0, 0.0)}, # black
    {'position': (0, 1060), 'size': (1920, 20), 'color': (0.0, 0.0, 0.0)}, # black
    {'position': (0, 0), 'size': (20, 1080), 'color': (0.0, 0.0, 0.0)}, # black
    {'position': (1900, 0), 'size': (20, 1080), 'color': (0.0, 0.0, 0.0)}, # black
]

goal_platform = {'position': (1900, 0), 'size': (20, 50), 'color': (1.0, 1.0, 0.0)} 
platforms.append(goal_platform)

def is_overlapping(x, y, size):
    for platform in platforms:
        px, py = platform['position']
        pw, ph = platform['size']
        if (px - size <= x <= px + pw + size) and (py - size <= y <= py + ph + size):
            return True
    return False

def generate_obstacles():
    obstacles = []
    for _ in range(5):
        while True:
            x = random.randint(0, WIDTH - 50)
            y = random.randint(0, HEIGHT - 50)
            size = 20
            if not is_overlapping(x, y, size):
                color = (1.0, 0.0, 0.0)
                obstacles.append({'position': (x, y), 'size': size, 'color': color})
                break
    return obstacles

def generate_coins():
    coins = []
    for _ in range(10):
        while True:
            x = random.randint(0, WIDTH - 20)
            y = random.randint(0, HEIGHT - 20)
            size = 10
            if not is_overlapping(x, y, size):
                color = (1.0, 1.0, 0.0)
                coins.append({'position': (x, y), 'size': size, 'color': color})
                break
    return coins

obstacles = generate_obstacles()
coins = generate_coins()

def draw_circle(cx, cy, radius, color, segments=32):
    theta = 2 * 3.14159 / segments
    glColor3f(*color)
    glBegin(GL_POLYGON)
    for i in range(segments):
        x = radius * cos(i * theta)
        y = radius * sin(i * theta)
        glVertex2f(x + cx, y + cy)
    glEnd()

def draw_platform(x, y, width, height, color):
    glBegin(GL_QUADS)
    glColor3f(*color)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()

def check_collision_and_update_position():
    if game_lost or game_won:
        return
    
    global char_x, char_y, char_radius, is_on_platform, fall_speed, score, jump_velocity

    is_on_platform = False

    for platform in platforms:
        px, py = platform['position']
        pw, ph = platform['size']

        platform_top = py
        platform_bottom = py + ph
        platform_left = px
        platform_right = px + pw

        circle_bottom = char_y + char_radius
        circle_top = char_y - char_radius
        circle_left = char_x - char_radius
        circle_right = char_x + char_radius

        if platform_left <= char_x and char_x <= platform_right:
            if platform_top <= circle_top and circle_top <= platform_bottom:
                char_y = platform_bottom + char_radius
                fall_speed = 0 
                jump_velocity = 0 
                break

            if platform_top <= circle_bottom and circle_bottom <= platform_bottom:
                char_y = platform_top - char_radius
                is_on_platform = True
                fall_speed = 0  
                jump_velocity = 0 
                break
            
        if platform_top <= char_y and char_y <= platform_bottom:
            if platform_left <= circle_left and circle_left <= platform_right:
                char_x = platform_right + char_radius
                break
            if platform_left <= circle_right and circle_right <= platform_right:
                char_x = platform_left - char_radius
                break


    for obstacle in obstacles:
        ox, oy = obstacle['position']
        size = obstacle['size']

        if (ox - char_x) ** 2 + (oy - char_y) ** 2 <= (size + char_radius) ** 2:
            game_over()
            return


    for coin in coins[:]:
        cx, cy = coin['position']
        size = coin['size']

        if (cx - char_x) ** 2 + (cy - char_y) ** 2 <= (size + char_radius) ** 2:
            coins.remove(coin)
            score += 1
            print(f"Score: {score}")

    # Check for collision with the goal platform
    goal_x, goal_y = goal_platform['position']
    goal_w, goal_h = goal_platform['size']
    if goal_x <= char_x <= goal_x + goal_w and goal_y <= char_y <= goal_y + goal_h:
        you_win()

def apply_physics(window):
    global char_x, char_y, is_jumping, jump_velocity, fall_speed, gravity, max_fall_speed, move_speed, is_on_platform

    if key_state[glfw.KEY_LEFT]:
        char_x -= move_speed
    if key_state[glfw.KEY_RIGHT]:
        char_x += move_speed

    if key_state[glfw.KEY_SPACE] and is_on_platform and not is_jumping:
        is_jumping = True
        jump_velocity = 5
        is_on_platform = False

    if is_jumping:
        char_y -= jump_velocity
        jump_velocity -= gravity 
        if jump_velocity <= 0:
            is_jumping = False 
            fall_speed = 0 
    else:
        if not is_on_platform:
            fall_speed += gravity
            if fall_speed > max_fall_speed:
                fall_speed = max_fall_speed
            char_y += fall_speed

    check_collision_and_update_position()

    if char_y - char_radius > HEIGHT:
        game_over()

def render():
    global game_won, game_lost

    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(0.1, 0.1, 0.1, 1)
    draw_circle(char_x, char_y, char_radius, (0, 1, 0))
    for platform in platforms:
        x, y = platform['position']
        width, height = platform['size']
        color = platform['color']
        draw_platform(x, y, width, height, color)
    for obstacle in obstacles:
        x, y = obstacle['position']
        size = obstacle['size']
        color = obstacle['color']
        draw_circle(x, y, size, color)
    for coin in coins:
        x, y = coin['position']
        size = coin['size']
        color = coin['color']
        draw_circle(x, y, size, color)

    render_text(10, 20, 20, f"Score: {score}")

    if game_won:
        render_text(WIDTH // 2 - 50, HEIGHT // 2, 40, "You Win!")
    if game_lost:
        render_text(WIDTH // 2 - 50, HEIGHT // 2, 40, "You Lose")

    if game_won or game_lost:
        render_text(WIDTH // 2 - 100, HEIGHT // 2 + 50, 30, "Press R to Restart")

def main():
    window = init_window()
    init_opengl()
    glfw.set_key_callback(window, key_input)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        apply_physics(window)
        render()
        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()
