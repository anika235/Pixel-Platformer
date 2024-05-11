import glfw
from OpenGL.GL import *
from math import cos, sin

# Window dimensions
WIDTH, HEIGHT = 800, 600
char_radius = 15  # Character's radius
char_x = 30
char_y = HEIGHT/ 2 - char_radius  # Adjust initial y-coordinate
move_speed = 5
is_jumping = False  # Indicates if the character is currently jumping
jump_height = 0  # The remaining height the character has to jump


def init_window():
    if not glfw.init():
        raise Exception("glfw can not be initialized!")
    window = glfw.create_window(WIDTH, HEIGHT, "Pixel Platformer", None, None)
    if not window:
        glfw.terminate()
        raise Exception("glfw window can not be created!")
    glfw.set_window_pos(window, 400, 200)
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    return window

def init_opengl():
    glViewport(0, 0, WIDTH, HEIGHT)
    glOrtho(0, WIDTH, HEIGHT, 0, -1, 1)

def game_over(window):
    print("Game Over")
    glfw.set_window_should_close(window, True)

def you_win(window):
    print("You Win!!")
    glfw.set_window_should_close(window, True)

def key_input(window, key, scancode, action, mods):
    global char_x, char_y
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_LEFT:
            char_x -= move_speed
        if key == glfw.KEY_RIGHT:
            char_x += move_speed
        if key == glfw.KEY_UP:
            char_y -= move_speed
        if key == glfw.KEY_DOWN:
            char_y += move_speed
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)

# Platforms defined by bottom-left corner, width, and height
platforms = [
    {'position': (500, 100), 'size': (120, 20), 'color': (0.6, 0.3, 0.1)},
    {'position': (580, 200), 'size': (120, 20), 'color': (0.5, 0.5, 0.1)},
    {'position': (680, 50), 'size': (120, 20), 'color': (0.0, 0.0, 1.0)},
    {'position': (100, 100), 'size': (150, 20), 'color': (0.2, 0.5, 0.4)},
    {'position': (300, 150), 'size': (180, 20), 'color': (0.5, 0.4, 0.2)},
    {'position': (50, 250), 'size': (110, 20), 'color': (0.3, 0.6, 0.7)},
    {'position': (450, 300), 'size': (160, 20), 'color': (0.7, 0.2, 0.5)},
    {'position': (200, 350), 'size': (140, 20), 'color': (0.4, 0.7, 0.3)},
    {'position': (550, 400), 'size': (130, 20), 'color': (0.5, 0.5, 0.1)},
    {'position': (400, 450), 'size': (170, 20), 'color': (0.1, 0.5, 0.6)},
    {'position': (150, 500), 'size': (100, 20), 'color': (0.2, 0.6, 0.3)},
    {'position': (680, 500), 'size': (100, 20), 'color': (0.2, 0.6, 0.3)},
    {'position': (0, 560), 'size': (100, 20), 'color': (0.4, 0.8, 0.2)},
    {'position': (280, 550), 'size': (120, 20), 'color': (0.3, 0.4, 0.5)}
]

# Adding the goal platform
goal_platform = {'position': (780, 0), 'size': (20, 50), 'color': (1.0, 1.0, 0.0)}  # Yellow color
platforms.append(goal_platform)


def draw_circle(cx, cy, radius, color, segments=32):
    theta = 2 * 3.14159 / segments  # The angle between vertices
    glColor3f(*color)  # Set the color of the circle
    glBegin(GL_POLYGON)  # Start drawing a filled circle
    for i in range(segments):
        x = radius * cos(i * theta)  # X coordinate
        y = radius * sin(i * theta)  # Y coordinate
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

def check_collision_and_update_position(window):
    global char_y, move_speed, char_radius

    # Assume gravity pulls the character down each frame
    new_y = char_y + move_speed

    # Detect collision with each platform
    for platform in platforms:
        px, py = platform['position']
        pw, ph = platform['size']

        # Calculate platform edges
        platform_top = py
        platform_bottom = py + ph
        platform_left = px
        platform_right = px + pw

        # Calculate circle edges
        circle_bottom = new_y + char_radius
        circle_top = new_y - char_radius
        circle_left = char_x - char_radius
        circle_right = char_x + char_radius

        # Check horizontal and vertical bounds
        if (circle_right > platform_left and circle_left < platform_right and
            circle_bottom > platform_top and circle_top < platform_bottom):

            # Check if this is the goal platform
            if platform == goal_platform:
                you_win(window)
                return  # Stop further processing since game is won

            # Circle is intersecting the platform, adjust position
            if circle_bottom > platform_top and char_y + char_radius <= platform_top:
                # The character is landing on the platform
                new_y = platform_top - char_radius
                break  # Correct the position and stop checking further

    # Update the character's position only if there's no intersection
    char_y = new_y



def key_input(window, key, scancode, action, mods):
    global char_x, char_y, is_jumping, jump_height
    if action == glfw.PRESS:  # Trigger on the initial press to avoid repeating the jump due to key repeat
        if key == glfw.KEY_LEFT:
            char_x -= move_speed
        if key == glfw.KEY_RIGHT:
            char_x += move_speed
        if key == glfw.KEY_SPACE and not is_jumping:  # Start jumping only if not already jumping
            is_jumping = True
            jump_height = 80  # Set how high the jump should be
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)


def apply_physics(window):
    global char_y, is_jumping, jump_height

    if is_jumping:
        if jump_height > 0:
            char_y -= 10  # Move up by 10 pixels per frame
            jump_height -= 10
        else:
            is_jumping = False
    else:
        # Apply gravity if not jumping and check for goal collision
        check_collision_and_update_position(window)

    if char_y - char_radius > HEIGHT:
        game_over(window)


def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(0.1, 0.1, 0.1, 1)
    # Draw character as a circle
    draw_circle(char_x, char_y, char_radius, (1, 0, 0))
    # Draw platforms
    for platform in platforms:
        x, y = platform['position']
        width, height = platform['size']
        color = platform['color']
        draw_platform(x, y, width, height, color)


def main():
    window = init_window()
    init_opengl()
    glfw.set_key_callback(window, key_input)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        apply_physics(window)  # Pass the window to the function
        render()
        glfw.swap_buffers(window)
    glfw.terminate()



if __name__ == "__main__":
    main()
