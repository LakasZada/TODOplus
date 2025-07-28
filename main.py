import pygame
import sys
import time

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TODO plus")

font = pygame.font.Font("assets/fixedsys.ttf", 28)
small_font = pygame.font.Font("assets/fixedsys.ttf", 20)

bg_color = (50, 50, 50)
white = (255, 255, 255)
green = (0, 255, 0)
gray = (100, 100, 100)
red = (255, 100, 100)
blue = (100, 100, 255)

alarm_sound = pygame.mixer.Sound("assets/alarm.wav")

input_active = False
input_text = ""
input_box = pygame.Rect(10, HEIGHT - 50, 480, 32)

slider_rect = pygame.Rect(300, HEIGHT - 90, 180, 8)
slider_handle = pygame.Rect(470, HEIGHT - 96, 10, 20)
slider_dragging = False

use_timer = False
timer_toggle_box = pygame.Rect(10, HEIGHT - 90, 20, 20)

tasks = []

clock = pygame.time.Clock()
running = True
while running:
    screen.fill(bg_color)
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                input_active = True
            else:
                input_active = False

            if slider_handle.collidepoint(event.pos):
                slider_dragging = True

            if timer_toggle_box.collidepoint(event.pos):
                use_timer = not use_timer

            y = 20
            for task in tasks:
                box = pygame.Rect(10, y, 20, 20)
                if box.collidepoint(event.pos):
                    task["done"] = not task["done"]
                y += 60

        if event.type == pygame.MOUSEBUTTONUP:
            slider_dragging = False

        if event.type == pygame.MOUSEMOTION and slider_dragging:
            slider_handle.x = max(min(event.pos[0], slider_rect.right), slider_rect.left)

        if event.type == pygame.KEYDOWN and input_active:
            if event.key == pygame.K_RETURN and input_text.strip() != "":
                task_minutes = round((slider_handle.x - slider_rect.left) / slider_rect.width * 60)
                if task_minutes < 1:
                    task_minutes = 1

                new_task = {
                    "name": input_text,
                    "done": False,
                    "alarm_played": False
                }

                if use_timer:
                    new_task["start_time"] = time.time()
                    new_task["duration"] = task_minutes * 60

                tasks.append(new_task)
                input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                if len(input_text) < 25:
                    input_text += event.unicode

    pygame.draw.rect(screen, gray, input_box)
    input_surface = font.render(input_text, True, white)
    screen.blit(input_surface, (input_box.x + 10, input_box.y + 2))

    pygame.draw.rect(screen, white, slider_rect)
    pygame.draw.rect(screen, green, slider_handle)

    minutes = round((slider_handle.x - slider_rect.left) / slider_rect.width * 60)
    if minutes < 1:
        minutes = 1
    min_text = small_font.render(f"{minutes} min", True, white)
    screen.blit(min_text, (slider_rect.x, slider_rect.y - 25))

    pygame.draw.rect(screen, white, timer_toggle_box, 2)
    if use_timer:
        check = font.render("✔", True, green)
        screen.blit(check, (timer_toggle_box.x, timer_toggle_box.y - 6))
    toggle_label = small_font.render("Timer", True, white)
    screen.blit(toggle_label, (timer_toggle_box.x + 30, timer_toggle_box.y - 2))

    y = 20
    now = time.time()
    for task in tasks:
        checkbox = pygame.Rect(10, y, 20, 20)
        pygame.draw.rect(screen, white, checkbox, 2)

        if task["done"]:
            pygame.draw.line(screen, green, (12, y + 10), (18, y + 16), 3)
            pygame.draw.line(screen, green, (18, y + 16), (28, y + 4), 3)


        label = font.render(task["name"], True, white)
        screen.blit(label, (40, y))

        if "duration" in task:
            remaining = max(0, int(task["start_time"] + task["duration"] - now))
            minutes = remaining // 60
            seconds = remaining % 60
            timer_label = small_font.render(f"{minutes:02}:{seconds:02}", True, red)
            screen.blit(timer_label, (400, y))

            if remaining == 0 and not task["alarm_played"]:
                alarm_sound.play()
                task["alarm_played"] = True

        y += 60

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
