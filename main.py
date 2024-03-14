import pygame
import math
import random

pygame.init()

width, height = 1500, 800
WINDOW = pygame.display.set_mode((width, height))
pygame.display.set_caption("Solar System")
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
LIGHT_BROWN = (139, 69, 19)


class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600 * 24  # 1 day

    def __init__(self, x, y, radius, colour, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.mass = mass
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + width / 2
        y = self.y * self.SCALE + height / 2
        pygame.draw.circle(win, self.colour, (x, y), self.radius)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x, distance_y = other_x - self.x, other_y - self.y
        distance = math.sqrt((distance_x**2) + (distance_y**2))
        if other.sun:
            self.distance_to_sun = distance
        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


class StaticAsteroid:
    def __init__(self, radius, angle, size, colour):
        self.radius = radius
        self.angle = angle
        self.size = size
        self.colour = colour
        self.x = self.radius * math.cos(self.angle)
        self.y = self.radius * math.sin(self.angle)

    def draw(self, win):
        x = self.x * Planet.SCALE + width / 2
        y = self.y * Planet.SCALE + height / 2
        pygame.draw.circle(win, self.colour, (x, y), self.size)


class MovingAsteroid(StaticAsteroid):
    def __init__(self, radius, angle, size, colour):
        super().__init__(radius, angle, size, colour)
        self.x_vel = random.uniform(-0.1, 0.1) * 1000
        self.y_vel = random.uniform(-0.1, 0.1) * 1000

    def update_position(self):
        self.x += self.x_vel * Planet.TIMESTEP
        self.y += self.y_vel * Planet.TIMESTEP


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    jupiter = Planet(-5.2 * Planet.AU, 0, 20, LIGHT_BROWN, 1.898 * 10**27)
    jupiter.y_vel = 13.07 * 1000

    planets = [sun, earth, mars, mercury, venus, jupiter]

    moving_asteroids = [MovingAsteroid(random.uniform(
        1.5, 2.5) * Planet.AU, random.uniform(0, 2*math.pi), 2, DARK_GREY) for _ in range(200)]

    while run:
        clock.tick(60)
        WINDOW.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    Planet.SCALE *= 1.1
                elif event.button == 5:
                    Planet.SCALE *= 0.9

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WINDOW)
        for asteroid in moving_asteroids:
            asteroid.update_position()
            asteroid.draw(WINDOW)
        pygame.display.update()


main()
