import mario_class
from pico2d import *


pico2d.open_canvas(background_Width, background_Height)
backgraund = Backgraund()
mario = Mario()

running = True

while running:
    clear_canvas()

    backgraund.draw()
    mario.draw()
    mario.update()

    update_canvas()
    handle_events()

    delay(0.03)