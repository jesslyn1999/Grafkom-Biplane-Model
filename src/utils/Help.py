#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import pyglet
from colors import *
import os


class Help():
    '''
    Displays the help documentation.
    '''
    def __init__(self):
        '''Help screen initializer'''
        # Load the help document.
        self.doc = pyglet.text.load(os.path.join(os.getcwd(), "src/utils/Help.html"))
        self.help_label = pyglet.text.DocumentLabel(self.doc,
                y=(WINDOW_HEIGHT - 80), x=100, width=600, multiline=True)

        # Make the button list.
        self.button_list = []

        # Add buttons to the list.

    def show(self, window):
        '''
        Set up and display the help screen.
        '''
        @window.event
        def on_draw():
            # Draw the background and buttons.
            self.draw_background()
            self.help_label.draw()

        @window.event
        def on_mouse_motion(x, y, dx, dy):
            # If the mouse is moved over one of the buttons, highlight it.
            # Otherwise, return it to its original color.
            pass

            #print(x, y) # Helpful for troubleshooting

        @window.event
        def on_mouse_press(x, y, click, modifiers):
            # If a button is clicked, darken it.
            pass

        @window.event
        def on_mouse_release(x, y, click, modifiers):
            # When the mouse click is released, undo the click-highlight.
            pass


    def draw_background(self):
        '''
        Define what the background will look like.
        '''
        horizon = int(round(WINDOW_HEIGHT * 0.8))

        # Draw the sea.
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ('v2i', (
                                 0, 0,
                                 WINDOW_WIDTH, 0,
                                 WINDOW_WIDTH, WINDOW_HEIGHT,
                                 0, horizon)),
                             ('c4B', (LIGHT_BLUE + LIGHT_BLUE + WHITE + WHITE))
                             )

        # Draw the sky.
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
            ('v2i', (
                0, horizon,
                WINDOW_WIDTH, horizon,
                WINDOW_WIDTH, WINDOW_HEIGHT,
                0, WINDOW_HEIGHT)),
            ('c4B', (WHITE + WHITE + LIGHT_BLUE + LIGHT_BLUE))
            )




def main():
    ''' Main method '''
    # Create the window manager.
    global WINDOW_WIDTH
    WINDOW_WIDTH = 800
    global WINDOW_HEIGHT
    WINDOW_HEIGHT = 600

    window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT,
            caption='Submarine Game')

    # Show the help screen.
    help = Help()
    help.show(window)
    # Start the game!
    pyglet.app.run()
    # pyglet.app.exit()

# Only call main if program is run directly (not if imported).
if __name__ == "__main__":
    main()