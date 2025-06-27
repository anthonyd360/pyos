import tkinter as tk
from tkinter import ttk

class FrameAnimator:
    def __init__(self, width=600, height=500, fps=2):
        self.root = tk.Tk()
        self.root.title("Frame-by-Frame Animator - Draw Your Animation!")
        
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)
        
        # Canvas for drawing
        self.canvas = tk.Canvas(main_frame, width=width, height=height-100, bg="white", bd=2, relief="sunken")
        self.canvas.pack()
        
        # Control frame
        control_frame = tk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        self.width = width
        self.height = height - 100
        self.fps = fps
        
        # Frame storage - each frame stores a list of drawing commands
        self.frame_data = [[], [], []]  # 3 frames to start
        self.current_frame = 0
        self.is_playing = False
        
        # Drawing variables
        self.last_x = None
        self.last_y = None
        self.pen_color = "black"
        self.pen_size = 3
        
        # Bind mouse events for drawing
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)
        
        # Create controls
        self.create_controls(control_frame)
        
        # Display current frame
        self.display_frame()
        
        self.root.mainloop()

    def create_controls(self, parent):
        # Frame navigation
        nav_frame = tk.Frame(parent)
        nav_frame.pack(side=tk.LEFT, padx=5)
        
        tk.Label(nav_frame, text="Frame:").pack(side=tk.LEFT)
        self.frame_var = tk.StringVar(value=str(self.current_frame + 1))
        self.frame_label = tk.Label(nav_frame, textvariable=self.frame_var, font=("Arial", 12, "bold"))
        self.frame_label.pack(side=tk.LEFT, padx=5)
        
        tk.Button(nav_frame, text="◄ Prev", command=self.prev_frame).pack(side=tk.LEFT, padx=2)
        tk.Button(nav_frame, text="Next ►", command=self.next_frame).pack(side=tk.LEFT, padx=2)
        
        # Animation controls
        anim_frame = tk.Frame(parent)
        anim_frame.pack(side=tk.LEFT, padx=20)
        
        self.play_button = tk.Button(anim_frame, text="▶ Play", command=self.toggle_animation)
        self.play_button.pack(side=tk.LEFT, padx=2)
        
        tk.Label(anim_frame, text="FPS:").pack(side=tk.LEFT, padx=(10,2))
        self.fps_var = tk.IntVar(value=self.fps)
        fps_spin = tk.Spinbox(anim_frame, from_=1, to=10, width=3, textvariable=self.fps_var, command=self.update_fps)
        fps_spin.pack(side=tk.LEFT)
        
        # Drawing tools
        tools_frame = tk.Frame(parent)
        tools_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(tools_frame, text="Pen:").pack(side=tk.LEFT)
        
        # Color buttons
        colors = ["black", "red", "blue", "green", "purple", "orange"]
        for color in colors:
            btn = tk.Button(tools_frame, bg=color, width=2, command=lambda c=color: self.set_color(c))
            btn.pack(side=tk.LEFT, padx=1)
        
        # Pen size
        tk.Label(tools_frame, text="Size:").pack(side=tk.LEFT, padx=(5,2))
        self.size_var = tk.IntVar(value=self.pen_size)
        size_spin = tk.Spinbox(tools_frame, from_=1, to=20, width=3, textvariable=self.size_var, command=self.update_size)
        size_spin.pack(side=tk.LEFT)
        
        # Clear button
        tk.Button(tools_frame, text="Clear Frame", command=self.clear_frame, bg="lightcoral").pack(side=tk.LEFT, padx=(10,0))

    def start_draw(self, event):
        if not self.is_playing:
            self.last_x = event.x
            self.last_y = event.y

    def draw(self, event):
        if not self.is_playing and self.last_x and self.last_y:
            # Draw line on canvas
            line_id = self.canvas.create_line(
                self.last_x, self.last_y, event.x, event.y,
                width=self.pen_size, fill=self.pen_color, capstyle=tk.ROUND, smooth=tk.TRUE
            )
            
            # Store the drawing command
            self.frame_data[self.current_frame].append({
                'type': 'line',
                'coords': [self.last_x, self.last_y, event.x, event.y],
                'width': self.pen_size,
                'fill': self.pen_color
            })
            
            self.last_x = event.x
            self.last_y = event.y

    def stop_draw(self, event):
        self.last_x = None
        self.last_y = None

    def set_color(self, color):
        self.pen_color = color

    def update_size(self):
        self.pen_size = self.size_var.get()
        
    def update_fps(self):
        self.fps = self.fps_var.get()

    def prev_frame(self):
        if not self.is_playing:
            self.current_frame = (self.current_frame - 1) % len(self.frame_data)
            self.display_frame()

    def next_frame(self):
        if not self.is_playing:
            self.current_frame = (self.current_frame + 1) % len(self.frame_data)
            self.display_frame()

    def clear_frame(self):
        if not self.is_playing:
            self.frame_data[self.current_frame] = []
            self.display_frame()

    def display_frame(self):
        # Clear canvas
        self.canvas.delete("all")
        
        # Redraw current frame
        for item in self.frame_data[self.current_frame]:
            if item['type'] == 'line':
                self.canvas.create_line(
                    *item['coords'],
                    width=item['width'],
                    fill=item['fill'],
                    capstyle=tk.ROUND,
                    smooth=tk.TRUE
                )
        
        # Update frame counter
        self.frame_var.set(f"{self.current_frame + 1}/{len(self.frame_data)}")

    def toggle_animation(self):
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.play_button.config(text="⏸ Pause")
            self.animate()
        else:
            self.play_button.config(text="▶ Play")

    def animate(self):
        if self.is_playing:
            self.display_frame()
            # Advance to next frame
            self.current_frame = (self.current_frame + 1) % len(self.frame_data)
            # Schedule next frame
            self.root.after(int(1000 / self.fps), self.animate)

# Run the animator
FrameAnimator()