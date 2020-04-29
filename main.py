import pygame, sys
import numpy
import time

width, height = 500, 500

pygame.init()

screen = pygame.display.set_mode([width, height])

screen.fill( (0,0,0) )

gcx, gcy = 20, 20

state = numpy.zeros(( gcx, gcy ))

gsx, gsy = int(width / gcx), (height / gcy)

def neigh(posx, posy, grid, sizex, sizey):
    sm = (
        grid[(posx - 1) % sizex, (y + 1) % sizey] +
        grid[(posx) % sizex, (y+1) % sizey] +
        grid[(posx + 1) % sizex, (y+1) % sizey] +
        grid[(posx-1) % sizex, (y) % sizey] +
        grid[(posx+1) % sizex, (y) % sizey] +
        grid[(posx-1) % sizex, (y-1) % sizey] +
        grid[(posx) % sizex, (y-1) % sizey] +
        grid[(posx+1) % sizex, (y-1) % sizey]
    )
    return sm

state[10, 3] = 1
state[10, 4] = 1
state[10, 5] = 1
state[9, 4] = 1

while True:
    time.sleep(0.2)
    screen.fill((0,0,0))

    statecpy = numpy.copy(state)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            mx, my = int(pos[0] / gsx), int(pos[1] / gsy)
            if state[mx, my] == 1:
                state[mx, my] = 0
            else:
                state[mx, my] = 1

    for y in range(0, gcy):
        for x in range(0, gcx):
            square = [
                    ( x * gsx, y * gsy ),
                    ( (x + 1) * gsx, y * gsy ),
                    ( (x + 1) * gsx, (y + 1) * gsy ),
                    ( (x) * gsx, (y + 1) * gsy )
            ]
            n = neigh(x, y, state, gcx, gcy)
            
            if state[x, y] == 0 and n == 3:
                statecpy[x, y] = 1
            elif state[x, y] == 1 and (n < 2 or n > 3):
                statecpy[x, y] = 0
            
            if statecpy[x, y] == 0:
                pygame.draw.polygon( screen, (255, 255, 255), square, 1)
            else:
                pygame.draw.polygon( screen, (255, 255, 255), square, 0)

    state = numpy.copy(statecpy)

    pygame.display.flip()
