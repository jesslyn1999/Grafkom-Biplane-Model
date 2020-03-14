#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Place a button on the screen.
Russell Jeffery
18 December 2018
'''

import pyglet

class Button():
    '''
    Place a button on the screen.
    rect_color and text_color are specified as tuples containing RGBA values--
    in other words, red, green, blue, and alpha (0 is transparent, 255 is
    opaque).
    '''

    def __init__(self, x, y, l, h, text, rect_color=(255, 255, 255, 255),
                 text_color=(0, 0, 0, 255)):
        # Rectangle info.
        self.x = x
        self.y = y
        self.l = l
        self.h = h
        self.rect_color = rect_color

        # Text info.
        self.x_mid = x + l // 2
        self.y_mid = y + h // 2
        self.text = text
        self.text_color = text_color
        self.font_size = int(round(h // 4 * 3 * 0.8))  # 4px = 3pt

    def draw_rect(self):
        '''
        Draw a rectangle.
        '''
        # "4" specifies how many verticies will be defined.
        # "pyglet.gl.GL_QUADS" tells OpenGL what to draw from the verticies.
        # "'v2i'" means that the next info will be verticies denoted by two
        # integer coordinates.
        # "'c3B'" means that, for each vertex, a color will be specified with a
        # 3-byte, unsigned value. I want the whole rectangle to be a solid
        # color, so I just multiplied 'color' by four, creating four identical
        # tuples.
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ('v2i', (
                                 self.x, self.y,
                                 self.x + self.l, self.y,
                                 self.x + self.l, self.y + self.h,
                                 self.x, self.y + self.h)),
                             ('c4B', self.rect_color * 4))

    def draw_text(self):
        '''
        Draw some text on the screen.
        '''
        label = pyglet.text.Label(self.text, font_name="Times New Roman",
                                  font_size=self.font_size, bold=True, color=self.text_color,
                                  x=self.x_mid, y=self.y_mid, width=self.l, height=self.h,
                                  anchor_x="center", anchor_y="center", align="center")
        label.draw()

    def draw_button(self):
        '''
        Draw a rectangle with text on it.
        '''
        self.draw_rect()
        self.draw_text()

    def mouseover(self, mouse_x, mouse_y):
        '''
        Returns "True" (bool) if mouse is over the button.
        '''
        # Calculate the sides of the button.
        left = self.x
        right = self.x + self.l
        bottom = self.y
        top = self.y + self.h

        if (left < mouse_x < right) and (bottom < mouse_y < top):
            return True
        else:
            return False

def draw_background(WINDOW_WIDTH, WINDOW_HEIGHT):
    '''
    Define what the background will look like.
    '''
    horizon = int(round(WINDOW_HEIGHT * 0.8))

    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                         ('v2i', (
                             0, 0,
                             WINDOW_WIDTH, 0,
                             WINDOW_WIDTH, horizon,
                             0, horizon)),
                         ('c4B',
                          (0, 0, 0, 255,
                           0, 0, 0, 255,
                           0, 0, 200, 255,
                           0, 0, 200, 255)
                          )
                         )

    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                         ('v2i', (
                             0, horizon,
                             WINDOW_WIDTH, horizon,
                             WINDOW_WIDTH, WINDOW_HEIGHT,
                             0, WINDOW_HEIGHT)),
                         ('c4B',
                          (255, 255, 255, 255,
                           255, 255, 255, 255,
                           100, 100, 255, 255,
                           100, 100, 255, 255)
                          )
                         )

def main():
    '''The main function'''
    # Set up the window.
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, caption='Game')

    @window.event
    def on_draw():
        window.clear()

        draw_background(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Set the dimensions and postions of the buttons, and draw five buttons
        # at different y-positions.
        button_len = 200
        button_hei = 50
        button_x = WINDOW_WIDTH // 2 - button_len // 2
        button_y = 60
        for i in range(5):
            button = Button(button_x, button_y, button_len, button_hei,
                            text='Button {}'.format(i),
                            rect_color=(200, 200, 200, 255), text_color=(0, 0, 0, 255))
            button.draw_button()
            button_y += 100

    pyglet.app.run()

# Only call main if program is run directly (not if imported).
if __name__ == "__main__":
    main()