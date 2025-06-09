import pygame

pygame.init()


def draw_line(screen, start_point, end_point):
    pygame.draw.line(screen, (255, 255, 255), start_point, end_point)

def draw_circle(screen, center, radius):
    pygame.draw.circle(screen, (255, 255, 255), center, radius)

def draw_rectangle(screen, top_left, width, height):
    pygame.draw.rect(screen, (255, 255, 255), (top_left, width, height))




