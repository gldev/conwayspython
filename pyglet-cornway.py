import pyglet
import sys, numpy

window = pyglet.window.Window(500, 500)

cell_width, cell_height = 20, 20

pixel_width, pixel_height = int(500/cell_width), int(500/cell_height)

batch = pyglet.graphics.Batch()
bat = pyglet.graphics.Batch()

white = [255]*4
black = [0]*4

global state, mem_cache, statecpy

mem_cache = {}

state = numpy.zeros(( cell_width, cell_height ))
state[2, 3] = 1
state[2, 4] = 1
state[2, 5] = 1
state[1, 4] = 1
possx,possy= 0,0

def neigh(posx, posy, grid, sizex, sizey):
    return (
        grid[(posx - 1) % sizex, (posy + 1) % sizey] +
        grid[(posx) % sizex, (posy+1) % sizey] +
        grid[(posx + 1) % sizex, (posy+1) % sizey] +
        grid[(posx-1) % sizex, (posy) % sizey] +
        grid[(posx+1) % sizex, (posy) % sizey] +
        grid[(posx-1) % sizex, (posy-1) % sizey] +
        grid[(posx) % sizex, (posy-1) % sizey] +
        grid[(posx+1) % sizex, (posy-1) % sizey]
    )

@window.event
def on_mouse_press(x, y, button, modifiers):
    mx, my = int(x / pixel_width), int(y / pixel_height)
    possx, possy = (mx, my)
    if state[mx, my] == 1:
        state[mx, my] = 0
    else:
        state[mx, my] = 1

@window.event
def on_draw():
    window.clear()
    batch.draw()

def update(dt):
    global state, statecpy
    statecpy = numpy.copy(state)
    for y in range(0, cell_height):
        for x in range(0, cell_width):
            vertex = [
                (x)* pixel_width, (y+1) * pixel_height,#top left
                (x+1) * pixel_width, (y + 1) * pixel_height,#top right
                (x+1) * pixel_width, y*pixel_height,#bottom right
                x * pixel_width, y*pixel_height,#bottom left 
            ]
            n = neigh(x, y, state, cell_width, cell_height)
            
            if state[x, y] == 0 and n == 3:
                statecpy[x, y] = 1
            elif state[x, y] == 1 and (n < 2 or n > 3):
                statecpy[x, y] = 0

            square = mem_cache.get((y, x))
            color = ('c4B', white*4)
            if square:
                if statecpy[x, y] != 0:
                    square.colors = black*4
                else:
                    square.colors = white*4
            else:
                if statecpy[x, y] != 0:
                    color = ('c4B', black*4)
                
                mem_cache[y,x] = batch.add(4, pyglet.gl.GL_QUADS, None, ('v2i',vertex), color)
    state = numpy.copy(statecpy)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1 / 5.0)
    pyglet.app.run()
