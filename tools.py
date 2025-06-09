import pygame

pygame.init()


def draw_line(screen, start_point, end_point):
    pygame.draw.line(screen, (255, 255, 255), start_point, end_point)
    return "Drawn line from " + str(start_point) + " to " + str(end_point)

def draw_circle(screen, center, radius):
    pygame.draw.circle(screen, (255, 255, 255), center, radius,10)
    return "Drawn circle at " + str(center) + " with radius " + str(radius) 

def draw_rectangle(screen, top_left, width, height):
    pygame.draw.rect(screen, (255, 255, 255), (top_left[0], top_left[1], width, height),10)
    return "Drawn rectangle at " + str(top_left) + " with width " + str(width) + " and height " + str(height)




