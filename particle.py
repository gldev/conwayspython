import pygame


pygame.init()

w, h = 800, 600

screen = pygame.display.set_mode( (w, h) )

screen.fill( (0 ,0,0))

# Particle structure will be [ pos, vel, size ]
# no oop because is bad
particles = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill((0,0,0))
    pygame.display.flip()
