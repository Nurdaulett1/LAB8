import pygame
import sys
pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simple paint')

white = (255, 255, 255)
black = (0, 0 , 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
gray = (200, 200, 200)

mode = 'BRUSH'
drawing = False
brush_color = black
start_pos = None

class Button:
    def __init__(self, x, y, width, height, text, color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text= text
        self.color = color
        self.action = action
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, white)
        screen.blit(text_surface, (self.rect.x + 8, self.rect.y + 8))
    def check_action(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()

def set_brush():
    global mode
    mode = 'BRUSH'
def set_rect():
    global mode
    mode = 'RECT'
def set_circle():
    global mode
    mode = 'CIRCLE'
def set_eraser():
    global mode
    mode = 'ERASER'
def set_black():
    global brush_color
    brush_color = black
def set_green():
    global brush_color
    brush_color = green
def set_red():
    global brush_color
    brush_color = red
def set_blue():
    global brush_color
    brush_color = blue
def clear_screen():
    screen.fill(white)
def exit_app():
    pygame.quit()
    sys.exit()

buttons = [
    Button(10, 10, 60, 30, 'Brush', black, set_brush),
    Button(80, 10, 60, 30, 'Rect', black, set_rect),
    Button(150, 10, 60, 30, 'Circle', black, set_circle),
    Button(220, 10, 60, 30, 'Eraser', gray, set_eraser),
    Button(290, 10, 60, 30, 'Clear', gray, clear_screen),
    Button(360, 10, 60, 30, 'Exit', gray, exit_app),
    Button(430, 10, 60, 30, 'Black', black, set_black),
    Button(500, 10, 60, 30, 'Green', green, set_green),
    Button(570, 10, 60, 30, 'Red', red, set_red),
    Button(640, 10, 60, 30, 'Blue', blue, set_blue),
]

clear_screen()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawing = True
                start_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                end_pos = event.pos
                if start_pos and end_pos and end_pos[1] > 50:
                    if mode == 'RECT':
                        x, y = start_pos
                        w, h = end_pos[0] - x, end_pos[1] - y
                        pygame.draw.rect(screen, brush_color, pygame.Rect(x, y, w, h), 2)
                    elif mode == 'CIRCLE':
                        x1, y1 = start_pos
                        x2, y2 = end_pos
                        radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
                        pygame.draw.circle(screen, brush_color, start_pos, radius, 2)
                drawing = False
                start_pos = None
        for button in buttons:
            button.check_action(event)

    if drawing and mode == 'BRUSH':
        x, y = pygame.mouse.get_pos()
        if y > 50:
            pygame.draw.circle(screen, brush_color, (x, y), 5)
    if drawing and mode == 'ERASER':
        x, y = pygame.mouse.get_pos()
        if y > 50:
            pygame.draw.circle(screen, white, (x, y), 10)

    pygame.draw.rect(screen, gray, (0, 0, width, 50))
    for button in buttons:
        button.draw(screen)

    pygame.display.flip()
