from player   import Hero
from game_map import Atlas
from view     import Animator
from mob      import Enemies

import controller

import pyglet


if __name__ == "__main__":
    window     = pyglet.window.Window()
    atlas      = Atlas()
    hero       = Hero(hero_type="ghost")
    animator   = Animator()
    event_loop = pyglet.app.EventLoop()
    enemies    = Enemies()
    @window.event
    def on_key_press(symbol, modifiers):
        if controller.check_quit(symbol, modifiers):
            window.close()
        controller.move_hero(symbol, modifiers, hero)
        controller.move_enemies(enemies)

    @window.event
    def on_draw():
        window.clear()
        animator.draw_tiles(atlas)
        animator.draw_hero(hero)
        animator.draw_enemies(enemies)

    pyglet.app.run()
