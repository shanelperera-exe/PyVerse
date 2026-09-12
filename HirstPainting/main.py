# Painting a Hirst Spot painting using Turtle

from colorgram import extract
import turtle
import random

def main():
    tim = turtle.Turtle()
    screen = turtle.Screen()

    turtle.colormode(255)
    tim.penup()
    tim.hideturtle()
    tim.speed("fastest")
    tim.goto(-220, -220)

    rgb_colors = extract_colors()

    x_coordinate = -220
    y_coordinate = -220

    for i in range(10):
        for j in range(10):
            random_color = random.choice(rgb_colors)
            tim.dot(20, random_color)
            tim.forward(50)
        y_coordinate += 50
        tim.goto(x_coordinate, y_coordinate)

    screen.exitonclick()


def extract_colors():
    """Extract colors from a Hirst spot painting"""
    rgb_colors = []
    colors = extract('image.jpg', 50)
    for color in colors:
        r = color.rgb.r
        g = color.rgb.g
        b = color.rgb.b
        rgb_colors.append((r, g, b))

    # Removing background colors safely
    for bg_color in [(245, 243, 238), (246, 242, 244), (240, 245, 241)]:
        if bg_color in rgb_colors:
            rgb_colors.remove(bg_color)

    return rgb_colors


if __name__ == "__main__":
    main()