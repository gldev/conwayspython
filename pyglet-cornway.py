import pyglet
import sys, numpy

window = pyglet.window.Window(500, 500)

cell_width, cell_height = 10, 10

pixel_width, pixel_height = int(500/cell_width), int(500/cell_height)

batch = pyglet.graphics.Batch()
bat = pyglet.graphics.Batch()

white = [255]*4
black = [0]*4

state = numpy.zeros(( cell_width, cell_height ))

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
def on_draw():
    window.clear()
    batch.draw()

def update(dt):
    global state
    vertex_list = pyglet.graphics.vertex_list(4, 'v2f', 'c3B')
    statecpy = numpy.copy(state)
    for y in range(0, cell_height):
        for x in range(0, cell_width):
            vertex = [
                (x)* pixel_width, (y+1) * pixel_height,#top left
                (x+1) * pixel_width, (y + 1) * pixel_height,#top right
                (x+1) * pixel_width, y,#bottom right
                x * pixel_width, y,#bottom left 
            ]
            n = neigh(x, y, state, cell_width, cell_height)
            
            if state[x, y] == 0 and n == 3:
                statecpy[x, y] = 1
            elif state[x, y] == 1 and (n < 2 or n > 3):
                statecpy[x, y] = 0

            if statecpy[x, y] == 0:
                batch.add(4, pyglet.gl.GL_QUADS, None, ('v2i',vertex), ('c4B', white*4))
                #batch.add_indexed(4, pyglet.gl.GL_QUADS, None, [0, 1, 2, 3, 4], ('c4B', white*4))
            else:
                batch.add(4, pyglet.gl.GL_QUADS, None, ('v2i',vertex), ('c4B', black*4))
                #batch.add_indexed(4, pyglet.gl.GL_QUADS, None, [0, 1, 2, 3, 4], ('c4B', black*4))
            vertex_list.vertices = vertex
    state = numpy.copy(statecpy)

if __name__ == "__main__":
    state[2, 3] = 1
    state[2, 4] = 1
    state[2, 5] = 1
    state[1, 4] = 1
    pyglet.clock.schedule_interval(update, 1 / 5.0)
    pyglet.app.run()
