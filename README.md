# Donut ASCII Animation

This is a Python-based ASCII donut animation that uses the `curses` module to render a rotating 3D donut in the terminal. The animation features dynamic lighting, shading, and optional color support (if your terminal supports colors).

## Features

- **3D Donut Rendering:** Uses a torus parametric equation to create the donut shape.
- **Dynamic Shading:** Computes surface normals and uses a dot product with a fixed light vector for realistic shading.
- **Color Support:** If your terminal supports it, the animation uses a color gradient to enhance the visual effect.
- **Smooth Animation:** Gradually updates rotation angles to give continuous, smooth motion.
- **Non-Blocking Input:** Press any key to exit the animation.

## Requirements

- **Python 3.x**
- **curses module:**
  - On Linux and macOS, `curses` is usually available by default.
  - On Windows, you must install the `windows-curses` package:
    ```bash
    pip install windows-curses
    ```

## How to Run

1. **Clone or Download** the repository containing `donut.py`.

2. **Open your Terminal or Command Prompt.**

3. **Navigate to the directory** containing `donut.py`.

4. **Run the script:**
    ```bash
    python donut.py
    ```

   The animation will start immediately. **Press any key** to exit the animation.

## Customization

- **Geometry Parameters:**  
  You can tweak the values of `R1`, `R2`, and `K2` in the source code to change the shape and size of the donut.

- **Rotation Speed:**  
  Adjust the increments for angles `A` and `B` (in the main loop) to change the spinning speed.

- **Angular Resolution:**  
  Modify the step size in the `for` loops iterating over `theta` and `phi` to improve smoothness or performance.

- **Color and Shading:**  
  The code uses an ASCII gradient (`luminance_chars`) for shading. You can customize this string to experiment with different visual effects.

## Notes

- This version does not include any fullscreen or auto-maximization functionality. To run the animation, simply maximize your terminal window manually if desired.
- Modern terminal emulators support colors and dynamic resizing, so the donut scales to your terminal size automatically.
