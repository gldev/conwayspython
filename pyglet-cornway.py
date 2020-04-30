import pyglet
import sys, numpy

window = pyglet.window.Window(500, 500)

cell_width, cell_height = 10, 10

pixel_width, pixel_height = int(500/cell_width), int(500/cell_height)

@window.event
def on_draw():
    window.clear()

def update(dt):
    #game logic
    vertex_list = pyglet.graphics.vertex_list(4, 'v2f', 'c3B')
    for y in range(0, cell_height):
        for x in range(0, cell_width):
			vertex = [
				x * pixel_width, y,
				(x + 1 ) * pixel_width, y,
				(x) * pixel_width, (y + 1) * pixel_height,
				(x+1)* pixel_width, (y+1) * pixel_height
			]
			vertex_list.colors = [
				0, 0, 0,
				0, 0, 0,
				0, 0, 0,
				0, 0, 0,
			]
			vertex_list.vertices = vertex
	vertex_list.draw(pyglet.gl.GL_QUADS)

    pass

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1 / 60.0)
    pyglet.app.run()
