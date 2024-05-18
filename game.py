# 1. Anika Tabassum (Roll: 61)
# 2. Bholanath Das Niloy (Roll: 22)
# Please Read the README.md/README.pdf file for more details 
import glfw
from OpenGL.GL import *
from math import cos, sin
import random
from eng import render_text, render_text_with_random_colors, render_text_with_density

# Constants for window dimensions and high scores
WIDTH, HEIGHT = 1920, 1080
TITLE_BAR_HEIGHT = 50
HIGH_SCORES_FILE = 'high_scores.txt'
MAX_HIGH_SCORES = 5

class Button:
    def __init__(self, x, y, width, height, label):
        """Initialize a button with position, size, and label."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.state = 'normal'  # States: 'normal', 'hovered', 'clicked'
    
    def is_hovered(self, mouse_x, mouse_y):
        """Check if the button is hovered by the mouse cursor."""
        return self.x <= mouse_x <= self.x + self.width and self.y - self.height // 2 <= mouse_y <= self.y + self.height // 2
    
    def draw(self):
        """Render the button based on its state."""
        if self.state == 'normal':
            glColor3f(0.5, 0.5, 0.5)  # Gray color for normal state
        elif self.state == 'hovered':
            glColor3f(0.7, 0.7, 0.7)  # Light gray for hovered state
        elif self.state == 'clicked':
            glColor3f(0.3, 0.3, 0.3)  # Dark gray for clicked state
        
        # Draw the button as a rectangle
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x + self.width, self.y + self.height)
        glVertex2f(self.x, self.y + self.height)
        glEnd()

        # Render the button label
        glColor3f(1.0, 1.0, 1.0)  # White color for text
        render_text(self.x + 10, self.y + 10, self.height - 20, self.label)

class Game:
    def __init__(self, level):
        """Initialize the game with the specified difficulty level."""
        self.level = level
        self.char_radius = 15
        self.char_x = 30
        self.char_y = (HEIGHT - TITLE_BAR_HEIGHT) // 2 - self.char_radius
        self.move_speed = 2
        self.is_jumping = False
        self.jump_velocity = 5
        self.gravity = 0.1
        self.fall_speed = 0
        self.max_fall_speed = 10
        self.is_on_platform = False
        self.current_platform = None
        self.platform_velocity = 0
        self.key_state = {glfw.KEY_LEFT: False, glfw.KEY_RIGHT: False, glfw.KEY_UP: False}
        self.score = 0
        self.game_won = False
        self.game_lost = False

        # Load platforms based on difficulty level
        if self.level == 'easy':
            self.platforms = self.load_platforms('platforms_level1.txt')
        else:
            self.platforms = self.load_platforms('platforms_level2.txt')
        
        self.obstacles = []
        self.coins = []
        self.generate_obstacles_and_coins()

    def load_platforms(self, filename):
        """Load platform data from a file."""
        platforms = []
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                x, y, w, h = map(int, parts[:4])
                color = tuple(map(float, parts[4:7]))
                move = bool(int(parts[7])) if len(parts) > 7 else False 
                direction = int(parts[8]) if len(parts) > 8 else 1 
                move_distance = int(parts[9]) if len(parts) > 9 else 10 
                platforms.append({'position': [x, y], 'size': (w, h), 'color': color, 'direction': direction, 'move_offset': 0, 'move': move, 'move_distance': move_distance, 'velocity': 0})
        return platforms

    def update_platform_positions(self):
        """Update the positions of moving platforms."""
        for platform in self.platforms:
            if platform['move']: 
                px, py = platform['position']
                direction = platform['direction']
                move_offset = platform['move_offset']
                move_distance = platform['move_distance']

                if direction == 1:  # Move right
                    px += 1
                    move_offset += 1
                    platform['velocity'] = 1
                    if move_offset >= move_distance:
                        platform['direction'] = -1
                else:  # Move left
                    px -= 1
                    move_offset -= 1
                    platform['velocity'] = -1
                    if move_offset <= -move_distance:
                        platform['direction'] = 1

                platform['position'] = [px, py]
                platform['move_offset'] = move_offset
            else:
                platform['velocity'] = 0

    def is_overlapping(self, x, y, size, objects):
        """Check if a point is overlapping with any object."""
        for obj in objects:
            ox, oy = obj['position']
            osize = obj['size']
            if (ox - size <= x <= ox + osize + size) and (oy - size <= y <= oy + osize + size):
                return True
        return False

    def is_overlapping_platforms(self, x, y, size):
        """Check if a point is overlapping with any platform."""
        for platform in self.platforms:
            px, py = platform['position']
            pw, ph = platform['size']
            if (px - size <= x <= px + pw + size) and (py - size <= y <= py + ph + size):
                return True
        return False

    def generate_obstacles_and_coins(self):
        """Generate obstacles and coins for the game."""
        self.obstacles = self.generate_objects(5, 20, (1.0, 0.0, 0.0), [])
        self.coins = self.generate_objects(10, 10, (1.0, 1.0, 0.0), self.obstacles)

    def generate_objects(self, count, size, color, other_objects):
        """Generate objects (obstacles or coins) avoiding overlap."""
        objects = []
        for _ in range(count):
            while True:
                x = random.randint(0, WIDTH - size)
                y = random.randint(0, HEIGHT - size)
                if not self.is_overlapping(x, y, size, objects) and not self.is_overlapping(x, y, size, other_objects) and not self.is_overlapping_platforms(x, y, size):
                    objects.append({'position': (x, y), 'size': size, 'color': color})
                    break
        return objects

    def reset_game(self):
        """Reset the game to its initial state."""
        self.char_x = 30
        self.char_y = (HEIGHT - TITLE_BAR_HEIGHT) // 2 - self.char_radius
        self.is_jumping = False
        self.jump_velocity = 5
        self.fall_speed = 0
        self.is_on_platform = False
        self.current_platform = None
        self.platform_velocity = 0
        self.score = 0
        self.game_won = False
        self.game_lost = False
        self.generate_obstacles_and_coins()

    def game_over(self):
        """Handle game over condition."""
        if self.game_won or self.game_lost:
            return
        print("Game Over")
        self.game_lost = True

    def you_win(self):
        """Handle winning the game."""
        if self.game_won or self.game_lost:
            return
        print("You Win!!")
        self.game_won = True
        app.menu.save_high_score(self.score, self.level)

    def key_input(self, window, key, scancode, action, mods):
        """Handle keyboard input."""
        if action == glfw.PRESS:
            if key in self.key_state:
                self.key_state[key] = True
            if key == glfw.KEY_UP and self.is_on_platform and not self.is_jumping:
                self.is_jumping = True
                self.jump_velocity = 5
                self.is_on_platform = False
                self.platform_velocity = self.current_platform['velocity'] if self.current_platform else 0
                self.current_platform = None
            if key == glfw.KEY_ESCAPE:
                glfw.set_window_should_close(window, True)
            if key == glfw.KEY_R:
                self.reset_game()
            if key == glfw.KEY_M:
                app.current_screen = 'menu' 
            if key == glfw.KEY_P:
                if app.current_screen == 'game':
                    app.current_screen = 'paused'
                elif app.current_screen == 'paused':
                    app.current_screen = 'game'

        if action == glfw.RELEASE:
            if key in self.key_state:
                self.key_state[key] = False

    def check_collision_and_update_position(self):
        """Check for collisions and update character's position."""
        if self.game_lost or self.game_won:
            return

        self.is_on_platform = False

        goal_x, goal_y = self.platforms[-1]['position']
        goal_w, goal_h = self.platforms[-1]['size']

        circle_bottom = self.char_y + self.char_radius
        circle_top = self.char_y - self.char_radius
        circle_left = self.char_x - self.char_radius
        circle_right = self.char_x + self.char_radius

        if goal_x <= circle_right <= goal_x + goal_w and (goal_y <= circle_bottom <= goal_y + goal_h or goal_y <= circle_top <= goal_y + goal_h):
            self.you_win()

        for platform in self.platforms:
            px, py = platform['position']
            pw, ph = platform['size']

            platform_top = py
            platform_bottom = py + ph
            platform_left = px
            platform_right = px + pw

            if platform_left < self.char_x < platform_right:
                if platform_top < circle_top < platform_bottom:
                    self.char_y = platform_bottom + self.char_radius
                    self.fall_speed = 0
                    self.jump_velocity = 0
                    break

                if platform_top < circle_bottom < platform_bottom:
                    self.char_y = platform_top - self.char_radius
                    self.is_on_platform = True
                    self.current_platform = platform
                    self.fall_speed = 0
                    self.jump_velocity = 0
                    break

            if platform_top < self.char_y < platform_bottom:
                if platform_left < circle_left < platform_right:
                    self.char_x = platform_right + self.char_radius
                    break
                if platform_left < circle_right < platform_right:
                    self.char_x = platform_left - self.char_radius
                    break

        for obstacle in self.obstacles:
            ox, oy = obstacle['position']
            size = obstacle['size']

            if (ox - self.char_x) ** 2 + (oy - self.char_y) ** 2 <= (size + self.char_radius) ** 2:
                self.game_over()
                return

        for coin in self.coins[:]:
            cx, cy = coin['position']
            size = coin['size']

            if (cx - self.char_x) ** 2 + (cy - self.char_y) ** 2 <= (size + self.char_radius) ** 2:
                self.coins.remove(coin)
                self.score += 1
                print(f"Score: {self.score}")

    def apply_physics(self):
        """Apply game physics including movement, jumping, and gravity."""
        if self.key_state[glfw.KEY_LEFT]:
            self.char_x -= self.move_speed
        if self.key_state[glfw.KEY_RIGHT]:
            self.char_x += self.move_speed

        if self.key_state[glfw.KEY_UP] and self.is_on_platform and not self.is_jumping:
            self.is_jumping = True
            self.jump_velocity = 5
            self.is_on_platform = False
            self.platform_velocity = self.current_platform['velocity'] if self.current_platform else 0
            self.current_platform = None

        if self.is_jumping:
            self.char_y -= self.jump_velocity
            self.jump_velocity -= self.gravity
            if self.jump_velocity <= 0:
                self.is_jumping = False
                self.fall_speed = 0
        else:
            if not self.is_on_platform:
                self.fall_speed += self.gravity
                if self.fall_speed > self.max_fall_speed:
                    self.fall_speed = self.max_fall_speed
                self.char_y += self.fall_speed

        if self.is_on_platform and self.current_platform and self.current_platform['velocity'] != 0:
            self.char_x += 2 * self.current_platform['velocity']

        self.check_collision_and_update_position()
        self.update_platform_positions()

        if self.char_y - self.char_radius > HEIGHT:
            self.game_over()
        
    def draw_circle(self, cx, cy, radius, color, segments=32):
        """Draw a circle using OpenGL."""
        theta = 2 * 3.14159 / segments
        glColor3f(*color)
        glBegin(GL_POLYGON)
        for i in range(segments):
            x = radius * cos(i * theta)
            y = radius * sin(i * theta)
            glVertex2f(x + cx, y + cy)
        glEnd()

    def draw_platform(self, x, y, width, height, color):
        """Draw a platform using OpenGL."""
        glBegin(GL_QUADS)
        glColor3f(*color)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()

    def render(self):
        """Render the game screen."""
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0.1, 0.1, 0.1, 1)
        self.draw_circle(self.char_x, self.char_y, self.char_radius, (0, 1, 0))
        for platform in self.platforms:
            x, y = platform['position']
            width, height = platform['size']
            color = platform['color']
            self.draw_platform(x, y, width, height, color)
        for obstacle in self.obstacles:
            x, y = obstacle['position']
            size = obstacle['size']
            color = obstacle['color']
            self.draw_circle(x, y, size, color)
        for coin in self.coins:
            x, y = coin['position']
            size = coin['size']
            color = coin['color']
            self.draw_circle(x, y, size, color)

        render_text(10, 20, 20, f"Score: {self.score}")
        render_text(10, HEIGHT - 60, 20, "Press 'M' to go back to Menu")
        render_text(10, HEIGHT - 90, 20, "Press 'P' to Pause/Resume")

        if self.game_won:
            render_text_with_random_colors(WIDTH // 2 - 100, HEIGHT // 2, 80, "You Win!", density=3)
        if self.game_lost:
            render_text_with_density(WIDTH // 2 - 100, HEIGHT // 2, 80, "You Lose", density=3)

        if self.game_won or self.game_lost:
            render_text_with_density(WIDTH // 2 - 150, HEIGHT // 2 + 100, 40, "Press R to Restart", density=2)

class Menu:
    def __init__(self):
        """Initialize the game menu and load high scores."""
        self.high_scores_easy = self.load_high_scores('high_scores_easy.txt')
        self.high_scores_hard = self.load_high_scores('high_scores_hard.txt')
        self.selected_level = None
        button_width, button_height = 270, 50
        self.buttons = {
            'easy': Button(WIDTH // 2 - button_width // 2 + 280, HEIGHT // 2 - 150, button_width, button_height, "Easy Level"),
            'hard': Button(WIDTH // 2 - button_width // 2 + 600, HEIGHT // 2 - 150, button_width, button_height, "Hard Level"),
        }

    def load_high_scores(self, filename):
        """Load high scores from a file."""
        try:
            with open(filename, 'r') as file:
                scores = [int(line.strip()) for line in file.readlines()]
            scores.sort(reverse=True)
            return scores[:MAX_HIGH_SCORES]
        except FileNotFoundError:
            return []

    def save_high_score(self, score, level):
        """Save a high score for the specified level."""
        if level == 'easy':
            self.high_scores_easy.append(score)
            self.high_scores_easy.sort(reverse=True)
            self.high_scores_easy = self.high_scores_easy[:MAX_HIGH_SCORES]
            self.save_scores_to_file(self.high_scores_easy, 'high_scores_easy.txt')
        else:
            self.high_scores_hard.append(score)
            self.high_scores_hard.sort(reverse=True)
            self.high_scores_hard = self.high_scores_hard[:MAX_HIGH_SCORES]
            self.save_scores_to_file(self.high_scores_hard, 'high_scores_hard.txt')

    def save_scores_to_file(self, scores, filename):
        """Save high scores to a file."""
        with open(filename, 'w') as file:
            for score in scores:
                file.write(f"{score}\n")

    def render(self):
        """Render the menu screen."""
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0.1, 0.1, 0.1, 1)
        START = WIDTH // 2 + 200
        END = HEIGHT // 2 - 200

        render_text_with_random_colors(START - 50, END - 100, 40, "Pixel Platformer")
        render_text(START - 50, END, 30, "Choose Your Difficulty!")

        for button in self.buttons.values():
            button.draw()

        render_text(START - 50, END + 150, 30, "High Scores (Easy):")
        for i, score in enumerate(self.high_scores_easy):
            render_text(START - 50, END + 200 + i * 40, 30, f"{i + 1}. {score}")
        
        render_text(START - 50, END + 400, 30, "High Scores (Hard):")
        for i, score in enumerate(self.high_scores_hard):
            render_text(START - 50, END + 450 + i * 40, 30, f"{i + 1}. {score}")

        instructions_start_x = 50
        instructions_start_y = 250
        render_text(instructions_start_x, instructions_start_y, 30, "Instructions:")
        render_text(instructions_start_x, instructions_start_y + 40, 20, "1. Use LEFT and RIGHT arrow keys to move.")
        render_text(instructions_start_x, instructions_start_y + 80, 20, "2. Use UP arrow key to jump.")
        render_text(instructions_start_x, instructions_start_y + 120, 20, "3. Collect coins to increase score.")
        render_text(instructions_start_x, instructions_start_y + 160, 20, "4. Avoid obstacles to stay alive.")
        render_text(instructions_start_x, instructions_start_y + 200, 20, "5. Reach the goal platform to win.")
        render_text(instructions_start_x, instructions_start_y + 240, 20, "6. Press 'M' to go back to the menu at any time.")
        render_text(instructions_start_x, instructions_start_y + 280, 20, "7. Press 'P' to Pause/Resume the game.")

    def mouse_input(self, window, button, action, mods):
        """Handle mouse input for the menu."""
        if action == glfw.PRESS and button == glfw.MOUSE_BUTTON_LEFT:
            xpos, ypos = glfw.get_cursor_pos(window)
            ypos = ypos

            for key, button in self.buttons.items():
                if button.is_hovered(xpos, ypos):
                    button.state = 'clicked'
                    self.selected_level = key
                    app.current_screen = 'game'
                    app.start_game()
                    break

    def key_input(self, window, key, scancode, action, mods):
        """Handle keyboard input for the menu."""
        if action == glfw.PRESS and key == glfw.KEY_ENTER:
            app.current_screen = 'game'
            app.game.reset_game()
        if action == glfw.PRESS and key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)

    def mouse_move(self, window, xpos, ypos):
        """Handle mouse movement for the menu."""
        ypos = ypos
        for button in self.buttons.values():
            if button.is_hovered(xpos, ypos):
                button.state = 'hovered'
            else:
                button.state = 'normal'

class App:
    def __init__(self):
        """Initialize the application and set up the game menu."""
        self.menu = Menu()
        self.current_screen = 'menu'
        self.window = self.init_window()
        self.init_opengl()

    def init_window(self):
        """Initialize the GLFW window."""
        if not glfw.init():
            raise Exception("glfw can not be initialized!")
        
        window = glfw.create_window(WIDTH, HEIGHT + TITLE_BAR_HEIGHT, "Pixel Platformer", None, None)
        if not window:
            glfw.terminate()
            raise Exception("glfw window can not be created!")
        glfw.make_context_current(window)
        glfw.swap_interval(1)

        screen_width = glfw.get_video_mode(glfw.get_primary_monitor()).size.width
        screen_height = glfw.get_video_mode(glfw.get_primary_monitor()).size.height
        glfw.set_window_pos(window, (screen_width - WIDTH) // 2, (screen_height - HEIGHT) // 2)

        glfw.set_key_callback(window, self.key_input_callback)
        glfw.set_mouse_button_callback(window, self.mouse_input_callback)
        glfw.set_cursor_pos_callback(window, self.mouse_move_callback)
        return window

    def key_input_callback(self, window, key, scancode, action, mods):
        """Handle global key input events."""
        if self.current_screen == 'menu':
            self.menu.key_input(window, key, scancode, action, mods)
        elif self.current_screen == 'paused':
            if action == glfw.PRESS and key == glfw.KEY_P:
                self.current_screen = 'game'
            elif action == glfw.PRESS and key == glfw.KEY_M:
                self.current_screen = 'menu'
            elif action == glfw.PRESS and key == glfw.KEY_ESCAPE:
                glfw.set_window_should_close(window, True)
        else:
            self.game.key_input(window, key, scancode, action, mods)

    def mouse_input_callback(self, window, button, action, mods):
        """Handle global mouse input events."""
        if self.current_screen == 'menu':
            self.menu.mouse_input(window, button, action, mods)

    def mouse_move_callback(self, window, xpos, ypos):
        """Handle global mouse movement events."""
        if self.current_screen == 'menu':
            self.menu.mouse_move(window, xpos, ypos)

    def init_opengl(self):
        """Initialize OpenGL settings."""
        glViewport(0, 0, WIDTH, HEIGHT)
        glOrtho(0, WIDTH, HEIGHT, 0, -1, 1)

    def start_game(self):
        """Start the game with the selected difficulty level."""
        level = self.menu.selected_level
        self.game = Game(level)

    def main_loop(self):
        """Main loop to render the current screen and handle events."""
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            if self.current_screen == 'menu':
                self.menu.render()
            elif self.current_screen == 'paused':
                self.render_pause_screen()
            else:
                self.game.apply_physics()
                self.game.render()
            glfw.swap_buffers(self.window)
        glfw.terminate()

    def render_pause_screen(self):
        """Render the pause screen."""
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0.1, 0.1, 0.1, 1)
        render_text(WIDTH // 2 - 50, HEIGHT // 2 - 100, 40, "Game Paused")
        render_text(WIDTH // 2 - 50, HEIGHT // 2, 30, "Press 'P' to Resume")
        render_text(WIDTH // 2 - 50, HEIGHT // 2 + 50, 30, "Press 'M' to Go to Menu")

if __name__ == "__main__":
    app = App()
    app.main_loop()
