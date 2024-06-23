import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys

# Function to create the cube's vertices, edges, and surfaces based on size
def create_cube_vertices_and_edges(size):
    half_size = size / 2
    vertices = (
        ( half_size, -half_size, -half_size),
        ( half_size,  half_size, -half_size),
        (-half_size,  half_size, -half_size),
        (-half_size, -half_size, -half_size),
        ( half_size, -half_size,  half_size),
        ( half_size,  half_size,  half_size),
        (-half_size, -half_size,  half_size),
        (-half_size,  half_size,  half_size)
    )

    edges = (
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7)
    )

    surfaces = (
        (0, 1, 2, 3),
        (3, 2, 7, 6),
        (6, 7, 5, 4),
        (4, 5, 1, 0),
        (1, 5, 7, 2),
        (4, 0, 3, 6)
    )

    return vertices, edges, surfaces

# Function to draw the cube
def draw_cube(vertices, edges, surfaces, colors):
    glBegin(GL_QUADS)
    for surface in surfaces:
        for i, vertex in enumerate(surface):
            glColor3fv(colors[i % len(colors)])
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_LINES)
    glColor3fv((0, 0, 0))
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Main function
def main():
    # Predefined color options
    color_options = {
        'red': (1, 0, 0),
        'green': (0, 1, 0),
        'blue': (0, 0, 1),
        'yellow': (1, 1, 0),
        'cyan': (0, 1, 1),
        'magenta': (1, 0, 1),
        'white': (1, 1, 1),
        'black': (0, 0, 0)
    }

    # Get user inputs for color and dimensions
    print("Available colors: red, green, blue, yellow, cyan, magenta, white, black")
    color_name = input("Enter the color name or custom RGB values (comma-separated, e.g., '1,0,0' for red): ").strip().lower()

    # Determine the color based on user input
    if color_name in color_options:
        color = color_options[color_name]
    else:
        try:
            color = tuple(map(float, color_name.split(',')))
            if len(color) != 3 or not all(0 <= v <= 1 for v in color):
                raise ValueError
        except ValueError:
            print("Invalid color input. Using default color (white).")
            color = (1, 1, 1)

    dimensions_input = input("Enter the dimensions of the cube (single float value for all sides): ")

    # Parse user input for size
    try:
        size = float(dimensions_input)
    except ValueError:
        print("Invalid dimensions input. Using default size (2.0).")
        size = 2.0

    angle_input = input("Enter the angle at which you want to rotate the cube: ")

    # Parse user input for angle
    try:
        rotation_angle = float(angle_input)
    except ValueError:
        print("Invalid angle input. Using default angle (1.0).")
        rotation_angle = 1.0

    speed_input = input("Enter the speed of the rotation (higher value for faster rotation): ")

    # Parse user input for speed
    try:
        rotation_speed = float(speed_input)
    except ValueError:
        print("Invalid speed input. Using default speed (1.0).")
        rotation_speed = 1.0

    # Create vertices, edges, and surfaces based on the given size
    vertices, edges, surfaces = create_cube_vertices_and_edges(size)
    colors = [color] * 6  # Same color for all faces

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    angle_x, angle_y = 0, 0
    rotating = False  # Flag to control rotation

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_SPACE:
                    rotating = not rotating  # Toggle rotation on/off

        if rotating:
            glRotatef(rotation_angle * rotation_speed, 3, 1, 1)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_cube(vertices, edges, surfaces, colors)
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
