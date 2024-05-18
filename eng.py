from OpenGL.GL import *
import random

# Define a bitmap font for rendering text
font = {
    'A': [
        0b01110,
        0b10001,
        0b10001,
        0b11111,
        0b10001,
        0b10001,
        0b10001,
    ],
    'B': [
        0b11110,
        0b10001,
        0b10001,
        0b11110,
        0b10001,
        0b10001,
        0b11110,
    ],
    'C': [
        0b01111,
        0b10000,
        0b10000,
        0b10000,
        0b10000,
        0b10000,
        0b01111,
    ],
    'D': [
        0b11110,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b11110,
    ],
    'E': [
        0b11111,
        0b10000,
        0b10000,
        0b11110,
        0b10000,
        0b10000,
        0b11111,
    ],
    'F': [
        0b11111,
        0b10000,
        0b10000,
        0b11110,
        0b10000,
        0b10000,
        0b10000,
    ],
    'G': [
        0b01111,
        0b10000,
        0b10000,
        0b10011,
        0b10001,
        0b10001,
        0b01111,
    ],
    'H': [
        0b10001,
        0b10001,
        0b10001,
        0b11111,
        0b10001,
        0b10001,
        0b10001,
    ],
    'I': [
        0b11111,
        0b00100,
        0b00100,
        0b00100,
        0b00100,
        0b00100,
        0b11111,
    ],
    'J': [
        0b00001,
        0b00001,
        0b00001,
        0b00001,
        0b00001,
        0b10001,
        0b01110,
    ],
    'K': [
        0b10001,
        0b10010,
        0b10100,
        0b11000,
        0b10100,
        0b10010,
        0b10001,
    ],
    'L': [
        0b10000,
        0b10000,
        0b10000,
        0b10000,
        0b10000,
        0b10000,
        0b11111,
    ],
    'M': [
        0b10001,
        0b11011,
        0b10101,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
    ],
    'N': [
        0b10001,
        0b10001,
        0b11001,
        0b10101,
        0b10011,
        0b10001,
        0b10001,
    ],
    'O': [
        0b01110,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b01110,
    ],
    'P': [
        0b11110,
        0b10001,
        0b10001,
        0b11110,
        0b10000,
        0b10000,
        0b10000,
    ],
    'Q': [
        0b01110,
        0b10001,
        0b10001,
        0b10001,
        0b10101,
        0b10010,
        0b01101,
    ],
    'R': [
        0b11110,
        0b10001,
        0b10001,
        0b11110,
        0b10100,
        0b10010,
        0b10001,
    ],
    'S': [
        0b01111,
        0b10000,
        0b10000,
        0b01110,
        0b00001,
        0b00001,
        0b11110,
    ],
    'T': [
        0b11111,
        0b00100,
        0b00100,
        0b00100,
        0b00100,
        0b00100,
        0b00100,
    ],
    'U': [
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b01110,
    ],
    'V': [
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b01010,
        0b00100,
    ],
    'W': [
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10101,
        0b10101,
        0b01010,
    ],
    'X': [
        0b10001,
        0b10001,
        0b01010,
        0b00100,
        0b01010,
        0b10001,
        0b10001,
    ],
    'Y': [
        0b10001,
        0b10001,
        0b10001,
        0b01010,
        0b00100,
        0b00100,
        0b00100,
    ],
    'Z': [
        0b11111,
        0b00001,
        0b00010,
        0b00100,
        0b01000,
        0b10000,
        0b11111,
    ],
    '0': [
        0b01110,
        0b10001,
        0b10011,
        0b10101,
        0b11001,
        0b10001,
        0b01110,
    ],
    '1': [
        0b00100,
        0b01100,
        0b00100,
        0b00100,
        0b00100,
        0b00100,
        0b11111,
    ],
    '2': [
        0b01110,
        0b10001,
        0b00001,
        0b00110,
        0b01000,
        0b10000,
        0b11111,
    ],
    '3': [
        0b11110,
        0b00001,
        0b00001,
        0b01110,
        0b00001,
        0b00001,
        0b11110,
    ],
    '4': [
        0b00010,
        0b00110,
        0b01010,
        0b10010,
        0b11111,
        0b00010,
        0b00010,
    ],
    '5': [
        0b11111,
        0b10000,
        0b11110,
        0b00001,
        0b00001,
        0b10001,
        0b01110,
    ],
    '6': [
        0b01110,
        0b10000,
        0b11110,
        0b10001,
        0b10001,
        0b10001,
        0b01110,
    ],
    '7': [
        0b11111,
        0b00001,
        0b00010,
        0b00100,
        0b01000,
        0b01000,
        0b01000,
    ],
    '8': [
        0b01110,
        0b10001,
        0b10001,
        0b01110,
        0b10001,
        0b10001,
        0b01110,
    ],
    '9': [
        0b01110,
        0b10001,
        0b10001,
        0b01111,
        0b00001,
        0b10001,
        0b01110,
    ],
    ':': [
        0b00000,
        0b01100,
        0b01100,
        0b00000,
        0b01100,
        0b01100,
        0b00000,
    ],
    '.': [
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b01100,
        0b01100,
        0b00000,
    ],
    '\'': [
        0b00100,
        0b00100,
        0b01000,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
    ],
    '!': [
        0b00100,
        0b00100,
        0b00100,
        0b00100,
        0b00100,
        0b00000,
        0b00100,
    ],
    '(': [
        0b00110,
        0b01000,
        0b10000,
        0b10000,
        0b10000,
        0b01000,
        0b00110,
    ],
    ')': [
        0b01100,
        0b00010,
        0b00001,
        0b00001,
        0b00001,
        0b00010,
        0b01100,
    ]
}

def get_char_bitmap(char):
    """
    Get the bitmap representation of a character.

    Parameters:
    char (str): The character to get the bitmap for.

    Returns:
    list: A list of integers representing the bitmap of the character.
    """
    return font.get(char.upper(), [0] * 7)  

rev = False

def render_text(x, y, height, text):
    """
    Render text at a specified position with a specified height.

    Parameters:
    x (float): The x-coordinate of the text position.
    y (float): The y-coordinate of the text position.
    height (float): The height of the text.
    text (str): The text to render.
    """
    glColor3ub(255, 255, 255)
    glPointSize(3)
    glBegin(GL_POINTS)
    
    scale = height / 7  # Scale the text height
    start_x = x
    
    for char in text:
        bitmap = get_char_bitmap(char)
        for row in range(7):
            bits = bitmap[row]
            for col in range(5):
                if bits & (1 << (4 - col)):
                    glVertex2f(x + col * scale, y + row * scale)
        x += 6 * scale  # Move to the next character position

    glEnd()
    
def render_text_with_density(x, y, height, text, density=2):
    """
    Render text with specified density.

    Parameters:
    x (float): The x-coordinate of the text position.
    y (float): The y-coordinate of the text position.
    height (float): The height of the text.
    text (str): The text to render.
    density (int): The density of the text rendering.
    """
    glColor3ub(255, 255, 255)  # Set the fixed color to white
    glPointSize(2)
    glBegin(GL_POINTS)
    
    scale = height / 7  # Scale the text height
    start_x = x
    
    for char in text:
        bitmap = get_char_bitmap(char)
        for row in range(7):
            bits = bitmap[row]
            for col in range(5):
                if bits & (1 << (4 - col)):
                    for dy in range(density):
                        for dx in range(density):
                            glVertex2f(x + (col * density + dx) * (scale / density), y + (row * density + dy) * (scale / density))
        x += 6 * scale  # Move to the next character position

    glEnd()

def get_random_color():
    """
    Generate a random color.

    Returns:
    tuple: A tuple containing three integers representing an RGB color.
    """
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def render_text_with_random_colors(x, y, height, text, density=3):
    """
    Render text with random colors for each pixel.

    Parameters:
    x (float): The x-coordinate of the text position.
    y (float): The y-coordinate of the text position.
    height (float): The height of the text.
    text (str): The text to render.
    density (int): The density of the text rendering.
    """
    glPointSize(2)
    glBegin(GL_POINTS)
    
    scale = height / 7  # Scale the text height
    start_x = x
    
    for char in text:
        bitmap = get_char_bitmap(char)
        for row in range(7):
            bits = bitmap[row]
            for col in range(5):
                if bits & (1 << (4 - col)):
                    for dy in range(density):
                        for dx in range(density):
                            r, g, b = get_random_color()
                            glColor3ub(r, g, b)
                            glVertex2f(x + (col * density + dx) * (scale / density), y + (row * density + dy) * (scale / density))
        x += 6 * scale  # Move to the next character position

    glEnd()