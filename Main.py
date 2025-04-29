import os
import math
import time
import threading
import shutil

# Function to clear the console screen
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Donut constants
A = 0  # Rotation angle around X-axis
B = 0  # Rotation angle around Y-axis
R1 = 1.5  # Smaller tube radius (adjusted for better appearance)
R2 = 3    # Larger body radius (adjusted for proportion)
K2 = 7    # Distance constant
running = True  # Flag to control the loop

def get_terminal_size():
    """Get the size of the terminal window."""
    size = shutil.get_terminal_size()
    return size.columns, size.lines

def render_frame(A, B, width, height):
    output = [[' ' for _ in range(width)] for _ in range(height)]
    zbuffer = [[0 for _ in range(width)] for _ in range(height)]

    cos_A, sin_A = math.cos(A), math.sin(A)
    cos_B, sin_B = math.cos(B), math.sin(B)

    K1 = min(width, height) // 2.2  # Dynamically adjust scaling for proportion

    for theta in range(0, 628, 3):  # Finer resolution for smoother edges
        for phi in range(0, 628, 3):
            # Torus parametric equations
            sin_theta, cos_theta = math.sin(theta / 100), math.cos(theta / 100)
            sin_phi, cos_phi = math.sin(phi / 100), math.cos(phi / 100)

            x = (R2 + R1 * cos_theta) * cos_phi
            y = (R2 + R1 * cos_theta) * sin_phi
            z = R1 * sin_theta

            # Rotate around X and Y axes
            x_rot = cos_B * x + sin_B * (sin_A * y + cos_A * z)
            y_rot = cos_A * y - sin_A * z
            z_rot = K2 + cos_B * (sin_A * y + cos_A * z) - sin_B * x

            # Perspective projection
            ooz = 1 / z_rot
            xp = int(width / 2 + K1 * ooz * x_rot)  # Center the donut horizontally
            yp = int(height / 2 - K1 * ooz * y_rot)  # Center the donut vertically

            # Calculate luminance for shading
            L = cos_phi * cos_theta * sin_B - cos_A * cos_theta * sin_phi - sin_A * sin_theta + cos_B * (cos_A * sin_theta - cos_theta * sin_phi)

            if L > 0:  # Only render visible surfaces
                if 0 <= xp < width and 0 <= yp < height and ooz > zbuffer[yp][xp]:
                    zbuffer[yp][xp] = ooz
                    luminance_index = int(L * 8)
                    luminance_index = min(max(luminance_index, 0), len(".,-~:;=!*#$@") - 1)
                    luminance = ".,-~:;=!*#$@"[luminance_index]
                    output[yp][xp] = luminance

    # Render the frame
    clear_console()
    for row in output:
        print(''.join(row))

def animation_loop():
    global A, B, running
    width, height = get_terminal_size()  # Get terminal dimensions
    while running:
        render_frame(A, B, width, height)
        A += 0.03  # Smooth rotation speed around X-axis
        B += 0.06  # Smooth rotation speed around Y-axis
        time.sleep(0.03)  # Delay for smoother animation

# Graceful exit on user input
def listen_for_exit():
    global running
    input("Press Enter to stop the animation...\n")
    running = False

# Run the animation in a separate thread to allow user input
threading.Thread(target=listen_for_exit, daemon=True).start()
animation_loop()
