"""A small Pygame visualization of an Earth-like body orbiting a fixed Sun.

The simulation uses scaled, illustrative parameters instead of real astronomical
values. It is meant as a visual demonstration of Newtonian gravity, not as a
precision ephemeris.
"""

import math
import random
from collections import deque

import pygame

# Display
WIDTH = 800
HEIGHT = 600
FPS = 60

# Simulation constants (scaled units, chosen for a stable-looking orbit)
G = 5000.0
SUN_MASS = 1.0
EARTH_MASS = 1.0
SOFTENING = 10.0
DT = 1 / FPS
TIME_SCALE = 5
ORBIT_TRAIL_LENGTH = 600
STAR_COUNT = 150

# Colors
BACKGROUND = (8, 8, 15)
SUN_COLOR = (255, 230, 80)
EARTH_COLOR = (80, 180, 255)
TRAIL_COLOR = (100, 100, 100)


def create_stars():
    """Return a list of stars: [x, y, twinkle phase]."""
    stars = []
    for _ in range(STAR_COUNT):
        stars.append([
            random.randint(0, WIDTH),
            random.randint(0, HEIGHT),
            random.uniform(0, 2 * math.pi),
        ])
    return stars


def draw_stars(screen, stars, elapsed):
    """Scroll and twinkle the star field."""
    for star in stars:
        star[0] += 0.05

        if star[0] > WIDTH:
            star[0] = 0
            star[1] = random.randint(0, HEIGHT)

        brightness = 150 + int(105 * math.sin(elapsed + star[2]))
        pygame.draw.circle(
            screen,
            (brightness, brightness, brightness),
            (int(star[0]), int(star[1])),
            1,
        )


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Earth–Sun Gravity Simulation")
    clock = pygame.time.Clock()

    sun_x = WIDTH // 2
    sun_y = HEIGHT // 2

    earth_x = 550.0
    earth_y = 300.0
    velocity_x = 0.0
    velocity_y = -5.77

    stars = create_stars()
    orbit_points = deque(maxlen=ORBIT_TRAIL_LENGTH)
    elapsed = 0.0
    running = True

    while running:
        clock.tick(FPS)
        elapsed += 0.05

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Gravitational acceleration toward the Sun
        dx = sun_x - earth_x
        dy = sun_y - earth_y
        distance = max(math.hypot(dx, dy), 1.0)
        direction_x = dx / distance
        direction_y = dy / distance

        gravity = G * SUN_MASS / ((distance + SOFTENING) ** 2)
        acceleration_x = direction_x * gravity
        acceleration_y = direction_y * gravity

        # Semi-implicit Euler integration
        scaled_dt = DT * TIME_SCALE
        velocity_x += acceleration_x * scaled_dt
        velocity_y += acceleration_y * scaled_dt
        earth_x += velocity_x * scaled_dt
        earth_y += velocity_y * scaled_dt
        orbit_points.append((earth_x, earth_y))

        # Energy readout: kinetic + gravitational potential
        speed_squared = velocity_x ** 2 + velocity_y ** 2
        kinetic = 0.5 * EARTH_MASS * speed_squared
        potential = -G * SUN_MASS * EARTH_MASS / distance
        total_energy = kinetic + potential
        pygame.display.set_caption(
            f"Earth–Sun Gravity Simulation | Energy: {total_energy:,.1f}"
        )

        # Rendering
        screen.fill(BACKGROUND)
        draw_stars(screen, stars, elapsed)

        for point in orbit_points:
            pygame.draw.circle(
                screen, TRAIL_COLOR, (int(point[0]), int(point[1])), 2
            )

        pulse = int(2 * math.sin(elapsed * 2))
        pygame.draw.circle(screen, SUN_COLOR, (sun_x, sun_y), 30 + pulse)
        pygame.draw.circle(
            screen, EARTH_COLOR, (int(earth_x), int(earth_y)), 10
        )

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
