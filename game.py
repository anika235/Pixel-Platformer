import glfw
from OpenGL.GL import *
from math import cos, sin
import random
from eng import render_text


WIDTH, HEIGHT = 1920, 1080

class Game:
    def __init__(self):
        self.char_radius = 15
        self.char_x = 30
        self.char_y = HEIGHT // 2 - self.char_radius
        self.move_speed = 2
        self.is_jumping = False
        self.jump_velocity = 5
        self.gravity = 0.1
        self.fall_speed = 0
        self.max_fall_speed = 10
        self.is_on_platform = False
        self.key_state = {glfw.KEY_LEFT: False, glfw.KEY_RIGHT: False, glfw.KEY_SPACE: False}
        self.score = 0
        self.game_won = False
        self.game_lost = False
        self.platforms = self.load_platforms('platforms.txt')
        self.obstacles = self.generate_obstacles()
        self.coins = self.generate_coins()

    def load_platforms(self, filename):
        platforms = []
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                x, y, w, h = map(int, parts[:4])
                color = tuple(map(float, parts[4:]))
                platforms.append({'position': (x, y), 'size': (w, h), 'color': color})
        return platforms

    def generate_obstacles(self):
        obstacles = []
        for _ in range(5):
            while True:
                x = random.randint(0, WIDTH - 50)
                y = random.randint(0, HEIGHT - 50)
                size = 20
                if not self.is_overlapping(x, y, size):
                    color = (1.0, 0.0, 0.0)
                    obstacles.append({'position': (x, y), 'size': size, 'color': color})
                    break
        return obstacles

    def generate_coins(self):
        coins = []
        for _ in range(10):
            while True:
                x = random.randint(0, WIDTH - 20)
                y = random.randint(0, HEIGHT - 20)
                size = 10
                if not self.is_overlapping(x, y, size):
                    color = (1.0, 1.0, 0.0)
                    coins.append({'position': (x, y), 'size': size, 'color': color})
                    break
        return coins

    def is_overlapping(self, x, y, size):
        for platform in self.platforms:
            px, py = platform['position']
            pw, ph = platform['size']
            if (px - size <= x <= px + pw + size) and (py - size <= y <= py + ph + size):
                return True
        return False

    def reset_game(self):
        self.char_x = 30
        self.char_y = HEIGHT // 2 - self.char_radius
        self.is_jumping = False
        self.jump_velocity = 5
        self.fall_speed = 0
        self.is_on_platform = False
        self.score = 0
        self.game_won = False
        self.game_lost = False
        self.obstacles = self.generate_obstacles()
        self.coins = self.generate_coins()

    def game_over(self):
        if self.game_won or self.game_lost:
            return
        print("Game Over")
        self.game_lost = True

    def you_win(self):
        if self.game_won or self.game_lost:
            return
        print("You Win!!")
        self.game_won = True

    def key_input(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            if key in self.key_state:
                self.key_state[key] = True
            if key == glfw.KEY_SPACE and self.is_on_platform and not self.is_jumping:
                self.is_jumping = True
                self.jump_velocity = 5
                self.is_on_platform = False
            if key == glfw.KEY_ESCAPE:
                glfw.set_window_should_close(window, True)
            if key == glfw.KEY_R:
                self.reset_game()

        if action == glfw.RELEASE:
            if key in self.key_state:
                self.key_state[key] = False

    def check_collision_and_update_position(self):
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
        if self.key_state[glfw.KEY_LEFT]:
            self.char_x -= self.move_speed
        if self.key_state[glfw.KEY_RIGHT]:
            self.char_x += self.move_speed

        if self.key_state[glfw.KEY_SPACE] and self.is_on_platform and not self.is_jumping:
            self.is_jumping = True
            self.jump_velocity = 5
            self.is_on_platform = False

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

        self.check_collision_and_update_position()

        if self.char_y - self.char_radius > HEIGHT:
            self.game_over()

    def draw_circle(self, cx, cy, radius, color, segments=32):
        theta = 2 * 3.14159 / segments
        glColor3f(*color)
        glBegin(GL_POLYGON)
        for i in range(segments):
            x = radius * cos(i * theta)
            y = radius * sin(i * theta)
            glVertex2f(x + cx, y + cy)
        glEnd()

    def draw_platform(self, x, y, width, height, color):
        glBegin(GL_QUADS)
        glColor3f(*color)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()

    def render(self):
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

        if self.game_won:
            render_text(WIDTH // 2 - 50, HEIGHT // 2, 40, "You Win!")
        if self.game_lost:
            render_text(WIDTH // 2 - 50, HEIGHT // 2, 40, "You Lose")

        if self.game_won or self.game_lost:
            render_text(WIDTH // 2 - 100, HEIGHT // 2 + 50, 30, "Press R to Restart")

class App:
    def __init__(self):
        self.game = Game()
        self.window = self.init_window()
        self.init_opengl()

    def init_window(self):
        if not glfw.init():
            raise Exception("glfw can not be initialized!")
        
        window = glfw.create_window(WIDTH, HEIGHT, "Pixel Platformer", None, None)
        if not window:
            glfw.terminate()
            raise Exception("glfw window can not be created!")
        glfw.make_context_current(window)
        glfw.swap_interval(1)

        screen_width = glfw.get_video_mode(glfw.get_primary_monitor()).size.width
        screen_height = glfw.get_video_mode(glfw.get_primary_monitor()).size.height
        glfw.set_window_pos(window, (screen_width - WIDTH) // 2, (screen_height - HEIGHT) // 2)
        
        glfw.set_key_callback(window, self.game.key_input)
        
        return window

    def init_opengl(self):
        glViewport(0, 0, WIDTH, HEIGHT)
        glOrtho(0, WIDTH, HEIGHT, 0, -1, 1)

    def main_loop(self):
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.game.apply_physics()
            self.game.render()
            glfw.swap_buffers(self.window)
        glfw.terminate()

if __name__ == "__main__":
    app = App()
    app.main_loop()
