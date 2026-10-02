'''
Created on Oct 2, 2026

@author: bsund
'''
import tkinter as tk
import math

class LogoTurtleCanvas(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Logo Language")
        self.geometry("800x600")

        # Set canvas dimensions
        self.width = 600
        self.height = 600

        # Frame for controls
        control_frame = tk.Frame(self)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Canvas for drawing
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg="white")
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Turtle State (Center of canvas is origin (0, 0))
        self.x = 0.0
        self.y = 0.0
        self.heading = 90.0  # 90 degrees = Facing Up
        self.pen_down = True
        self.pen_color = "black"
        self.pen_width = 2

        # Setup UI Control Panel
        self._build_ui(control_frame)

        # Draw initial turtle
        self.turtle_shape_ids = []
        self._draw_turtle()

    # --- Coordinates System Helper ---
    def _to_canvas_coords(self, x, y):
        """Converts Logo coordinates (0,0 at center, +Y up) to Tkinter Canvas coordinates."""
        cx = (self.width / 2) + x
        cy = (self.height / 2) - y
        return cx, cy

    # --- Core Turtle Movement Commands ---
    def forward(self, distance):
        """Move forward by 'distance' units."""
        rad = math.radians(self.heading)
        new_x = self.x + distance * math.cos(rad)
        new_y = self.y + distance * math.sin(rad)
        self.goto(new_x, new_y)

    def backward(self, distance):
        """Move backward by 'distance' units."""
        self.forward(-distance)

    def turn_left(self, angle):
        """Turn left by 'angle' degrees."""
        self.heading = (self.heading + angle) % 360
        self._draw_turtle()

    def turn_right(self, angle):
        """Turn right by 'angle' degrees."""
        self.heading = (self.heading - angle) % 360
        self._draw_turtle()

    def goto(self, new_x, new_y):
        """Move directly to coordinate (new_x, new_y)."""
        if self.pen_down:
            x1, y1 = self._to_canvas_coords(self.x, self.y)
            x2, y2 = self._to_canvas_coords(new_x, new_y)
            self.canvas.create_line(x1, y1, x2, y2, fill=self.pen_color, width=self.pen_width, capstyle=tk.ROUND)

        self.x = new_x
        self.y = new_y
        self._draw_turtle()

    def circle(self, radius, extent=360, steps=60):
        """Draw a curve or circle with given radius and extent (in degrees)."""
        step_angle = extent / steps
        step_length = (2 * math.pi * radius * (extent / 360)) / steps
        
        # Determine turn direction based on sign of radius
        for _ in range(steps):
            if radius >= 0:
                self.forward(step_length)
                self.turn_left(step_angle)
            else:
                self.forward(step_length)
                self.turn_right(step_angle)

    def reset_turtle(self):
        """Clear canvas and reset turtle to center."""
        self.canvas.delete("all")
        self.x = 0.0
        self.y = 0.0
        self.heading = 90.0
        self.pen_down = True
        self._draw_turtle()

    # --- Turtle Visualization ---
    def _draw_turtle(self):
        """Draws a visual representation of the turtle pointing in 'self.heading' direction."""
        # Clear previous turtle icon
        for shape_id in self.turtle_shape_ids:
            self.canvas.delete(shape_id)
        self.turtle_shape_ids.clear()

        cx, cy = self._to_canvas_coords(self.x, self.y)
        rad = math.radians(self.heading)

        # Define triangular turtle body relative to heading
        size = 12
        points = [
            (size, 0),             # Nose
            (-size / 2, size / 2), # Left tail
            (-size / 3, 0),        # Inner indent
            (-size / 2, -size / 2) # Right tail
        ]

        rotated_points = []
        for px, py in points:
            rx = cx + px * math.cos(rad) - py * math.sin(rad)
            ry = cy - (px * math.sin(rad) + py * math.cos(rad))
            rotated_points.extend([rx, ry])

        turtle_id = self.canvas.create_polygon(rotated_points, fill="forestgreen", outline="black", width=1)
        self.turtle_shape_ids.append(turtle_id)

    # --- UI Elements Setup ---
    def _build_ui(self, frame):
        tk.Label(frame, text="Turtle Controls", font=("Arial", 12, "bold")).pack(pady=5)

        # Step / Turn Controls
        tk.Button(frame, text="Forward 50", command=lambda: self.forward(50), width=15).pack(pady=2)
        tk.Button(frame, text="Backward 50", command=lambda: self.backward(50), width=15).pack(pady=2)
        tk.Button(frame, text="Turn Left 45°", command=lambda: self.turn_left(45), width=15).pack(pady=2)
        tk.Button(frame, text="Turn Right 45°", command=lambda: self.turn_right(45), width=15).pack(pady=2)

        tk.Label(frame, text="Shape Presets", font=("Arial", 10, "bold")).pack(pady=(15, 5))
        tk.Button(frame, text="Draw Square", command=self._draw_square_preset, width=15).pack(pady=2)
        tk.Button(frame, text="Draw Circle", command=lambda: self.circle(50), width=15).pack(pady=2)
        tk.Button(frame, text="Draw Star", command=self._draw_star_preset, width=15).pack(pady=2)

        tk.Label(frame, text="Direct Goto (X, Y)", font=("Arial", 10, "bold")).pack(pady=(15, 5))
        
        entry_frame = tk.Frame(frame)
        entry_frame.pack()
        
        tk.Label(entry_frame, text="X:").grid(row=0, column=0)
        entry_x = tk.Entry(entry_frame, width=5)
        entry_x.insert(0, "100")
        entry_x.grid(row=0, column=1, padx=2)

        tk.Label(entry_frame, text="Y:").grid(row=0, column=2)
        entry_y = tk.Entry(entry_frame, width=5)
        entry_y.insert(0, "100")
        entry_y.grid(row=0, column=3, padx=2)

        def goto_action():
            try:
                x = float(entry_x.get())
                y = float(entry_y.get())
                self.goto(x, y)
            except ValueError:
                pass

        tk.Button(frame, text="Go to Coordinate", command=goto_action, width=15).pack(pady=5)

        tk.Button(frame, text="Clear Canvas", command=self.reset_turtle, bg="coral", width=15).pack(pady=(20, 5))

    # --- Preset Demonstrations ---
    def _draw_square_preset(self):
        for _ in range(4):
            self.forward(100)
            self.turn_right(90)

    def _draw_star_preset(self):
        for _ in range(5):
            self.forward(100)
            self.turn_right(144)

if __name__ == "__main__":
    app = LogoTurtleCanvas()
    app.mainloop()