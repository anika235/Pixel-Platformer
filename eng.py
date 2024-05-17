import glfw
from OpenGL.GL import *
import math
import random

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
}

def get_char_bitmap(char):
    return font.get(char.upper(), [0] * 7)  

rev = False

def render_text(x, y, height, text):
    glColor3ub(255, 255, 255)
    glPointSize(3)
    glBegin(GL_POINTS)
    
    scale = height / 7  
    start_x = x
    
    # if not rev:
    #     for key in font:
    #         font[key] = font[key][::-1]
    
    for char in text:
        bitmap = get_char_bitmap(char)
        for row in range(7):
            bits = bitmap[row]
            for col in range(5):
                if bits & (1 << (4 - col)):
                    glVertex2f(x + col * scale, y + row * scale)
        x += 6 * scale  

    glEnd()