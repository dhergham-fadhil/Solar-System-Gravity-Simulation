import math

import pygame
import random

# تشغيل pygame
pygame.init()

# حجم النافذة
WIDTH = 800
HEIGHT = 600

# إنشاء النافذة
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

# عنوان النافذة
pygame.display.set_caption("Physics Simulation")

# متغير تشغيل البرنامج
running = True

earth_x = 550
earth_y = 300

velocity_x = 0
velocity_y = -5.77

acceleration_x = 0
acceleration_y = 0

orbit_points = []

G = 5000
sun_mass = 10000
earth_mass = 1
time = 0

stars = []

for i in range(150):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    stars.append([
        x,
        y,
        random.uniform(0, 2 * math.pi)  # phase (للتذبذب)
    ])



# الحلقة الرئيسية
while running:

    clock.tick(60)
    time += 0.05

    # قراءة الأحداث
    for event in pygame.event.get():

        # إذا ضغط المستخدم زر الإغلاق
        if event.type == pygame.QUIT:
            running = False

    dx = 400 - earth_x
    dy = 300 - earth_y

    distance = (dx ** 2 + dy ** 2) ** 0.5

    softening = 10
    distance = max(distance, 1)

    dx /= distance
    dy /= distance

    gravity = 5000 / ((distance + softening) ** 2)

    acceleration_x = dx * gravity
    acceleration_y = dy * gravity

    dt = 1 / 60
    time_scale = 5

    scaled_dt = dt * time_scale

    velocity_x += acceleration_x * scaled_dt
    velocity_y += acceleration_y * scaled_dt
    # السرعة
    speed = (velocity_x ** 2 + velocity_y ** 2) ** 0.5

    # الطاقة الحركية
    kinetic = 0.5 * earth_mass * speed ** 2

    # طاقة الوضع الجاذبية (الصحيح)
    potential = - G * sun_mass * earth_mass / distance
    total_energy = kinetic + potential
    print(total_energy)

    # الطاقة الكلية
    total_energy = kinetic + potential

    earth_x += velocity_x * scaled_dt
    earth_y += velocity_y * scaled_dt
    orbit_points.append([earth_x, earth_y, 255])  # 255 = opacity

    # لون الخلفية
    screen.fill((8, 8, 15))

    for star in stars:
        star[0] += 0.05  # حركة خفيفة جدًا

        if star[0] > WIDTH:
            star[0] = 0
            star[1] = random.randint(0, HEIGHT)

        # ✨ twinkle (لمعان)
        brightness = 150 + int(105 * math.sin(time + star[2]))

        pygame.draw.circle(
            screen,
            (brightness, brightness, brightness),
            (int(star[0]), int(star[1])),
            1
        )
    for point in orbit_points:
        pygame.draw.circle(screen, (100, 100, 100), (int(point[0]), int(point[1])), 2)
    pulse = int(2 * math.sin(time * 2))  # نبض خفيف جدًا

    pygame.draw.circle(
        screen,
        (255, 230, 80),  # نيون أصفر
        (400, 300),
        30 + pulse
    )

    pygame.draw.circle(
        screen,
        (80, 180, 255),  # Neon blue
        (int(earth_x), int(earth_y)),
        10
    )
    # تحديث الشاشة
    pygame.display.update()

# إغلاق pygame
pygame.quit()