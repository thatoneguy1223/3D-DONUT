import math
import time
import curses

def donut_animation(stdscr):
    # Hide the cursor and enable non-blocking input.
    curses.curs_set(0)
    stdscr.nodelay(True)

    # Try to enable color support.
    use_colors = False
    color_pairs = []
    if curses.has_colors():
        curses.start_color()
        try:
            curses.use_default_colors()
        except curses.error:
            pass
        # Define a gradient of colors from dark to light.
        shade_colors = [
            curses.COLOR_BLACK, curses.COLOR_BLUE, curses.COLOR_CYAN,
            curses.COLOR_GREEN, curses.COLOR_YELLOW, curses.COLOR_MAGENTA,
            curses.COLOR_RED, curses.COLOR_WHITE
        ]
        for i, col in enumerate(shade_colors):
            try:
                curses.init_pair(i + 1, col, -1)
                color_pairs.append(curses.color_pair(i + 1))
            except curses.error:
                pass
        use_colors = True

    # Donut geometry parameters.
    R1 = 1.0    # Radius of the tube (the small circle).
    R2 = 2.0    # Distance from the torus center to the tube center.
    K2 = 5.0    # Distance offset for perspective.

    # Initial rotation angles.
    A = 0.0
    B = 0.0

    # ASCII luminance gradient.
    luminance_chars = ".,-~:;=!*#$@"

    while True:
        height, width = stdscr.getmaxyx()
        # Projection constant scaling with the terminal width.
        K1 = width * K2 / (8 * (R1 + R2))

        # Create buffers for output characters and depth (z-buffer).
        output = [[' ' for _ in range(width)] for _ in range(height)]
        zbuffer = [[0.0 for _ in range(width)] for _ in range(height)]
        color_buffer = (
            [[0 for _ in range(width)] for _ in range(height)]
            if use_colors
            else None
        )

        cosA = math.cos(A)
        sinA = math.sin(A)
        cosB = math.cos(B)
        sinB = math.sin(B)

        # Use a fine angular step for better detail.
        for theta in range(0, 628, 2):  # theta in [0, 6.28)
            for phi in range(0, 628, 2):  # phi in [0, 6.28)
                th = theta / 100.0
                ph = phi / 100.0

                cos_th = math.cos(th)
                sin_th = math.sin(th)
                cos_ph = math.cos(ph)
                sin_ph = math.sin(ph)

                # Compute torus parameters.
                circle_x = R2 + R1 * cos_th
                circle_y = R1 * sin_th

                # 3D coordinates before rotation.
                x = circle_x * cos_ph
                y = circle_x * sin_ph
                z = circle_y

                # Apply rotation about the X-axis.
                x1 = x
                y1 = cosA * y - sinA * z
                z1 = sinA * y + cosA * z

                # Apply rotation about the Z-axis.
                x2 = cosB * x1 - sinB * y1
                y2 = sinB * x1 + cosB * y1
                z2 = z1 + K2  # Translate away from viewer.

                if z2 == 0:
                    continue
                ooz = 1 / z2  # "One over z" for perspective scaling.

                # 2D screen projection.
                xp = int(width / 2 + K1 * ooz * x2)
                yp = int(height / 2 - K1 * ooz * y2)

                # Compute the surface normal (for shading determination).
                nx = cos_th * cos_ph
                ny = cos_th * sin_ph
                nz = sin_th

                # Rotate the normal using the same transforms.
                ny_rot = cosA * ny - sinA * nz
                nz_rot = sinA * ny + cosA * nz
                nx_rot = cosB * nx - sinB * ny_rot
                ny_rot2 = sinB * nx + cosB * ny_rot
                nz_rot2 = nz_rot

                # Define a fixed (normalized) light vector.
                Lx, Ly, Lz = 0, 1, -1
                L_len = math.sqrt(Lx**2 + Ly**2 + Lz**2)
                Lx, Ly, Lz = Lx / L_len, Ly / L_len, Lz / L_len

                # Dot product gives the luminance.
                L = nx_rot * Lx + ny_rot2 * Ly + nz_rot2 * Lz

                if L > 0 and 0 <= xp < width and 0 <= yp < height:
                    if ooz > zbuffer[yp][xp]:
                        zbuffer[yp][xp] = ooz
                        luminance_index = int(L * (len(luminance_chars) - 1))
                        luminance_index = max(0, min(luminance_index, len(luminance_chars) - 1))
                        output[yp][xp] = luminance_chars[luminance_index]
                        if use_colors:
                            color_idx = int(
                                luminance_index * (len(color_pairs) - 1) / (len(luminance_chars) - 1)
                            )
                            color_buffer[yp][xp] = color_pairs[color_idx]

        # Render the frame.
        stdscr.erase()
        if not use_colors:
            for r, row in enumerate(output):
                try:
                    stdscr.addstr(r, 0, "".join(row))
                except curses.error:
                    pass
        else:
            for r in range(height):
                for c in range(width):
                    try:
                        ch = output[r][c]
                        attr = color_buffer[r][c]
                        stdscr.addch(r, c, ch, attr)
                    except curses.error:
                        pass
        stdscr.refresh()

        # Update rotation angles for animation.
        A += 0.04
        B += 0.02

        time.sleep(0.02)
        if stdscr.getch() != -1:
            break

def main():
    curses.wrapper(donut_animation)

if __name__ == "__main__":
    main()
