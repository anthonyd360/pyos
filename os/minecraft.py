import ursina
from ursina import *
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.first_person_controller import FirstPersonController
import math, random, os

app = Ursina()

# Initialize inventory and icons
inventory = {1: 10, 2: 10, 3: 10, 4: 10, 5: 10, 6: 10, 7: 10}  # Start with 10 of each block type
icons = {1: 'white_cube', 2: 'white_cube', 3: 'white_cube', 4: 'white_cube', 5: 'white_cube', 6: 'white_cube', 7: 'white_cube'}
selected_block = 1  # Currently selected block type

# Initialize hotbar UI elements
hotbar_ui = []
count_ui = []

def get_block_color(block_id):
    """Get the color for a specific block type"""
    block_colors = {
        1: color.rgb(0, 0.7, 0.1),    # Grass - Green
        2: color.rgb(0.5, 0.3, 0),    # Dirt - Brown
        3: color.rgb(0.6, 0.3, 0),    # Wood - Dark Brown
        4: color.rgb(0, 0.5, 0),      # Leaves - Dark Green
        5: color.rgb(0.5, 0.5, 0.5),  # Stone - Gray
        6: color.rgb(0.8, 0.8, 0.8),  # Sand - Light Gray
        7: color.rgb(0.2, 0.2, 0.8),  # Water - Blue
    }
    return block_colors.get(block_id, color.white)

def draw_hotbar():
    global hotbar_ui, count_ui
    
    # Clear existing UI elements
    for ui in hotbar_ui + count_ui:
        destroy(ui)
    hotbar_ui.clear()
    count_ui.clear()
    
    # Draw hotbar background
    hotbar_bg = Entity(
        parent=camera.ui,
        model='quad',
        color=color.dark_gray,
        position=Vec3(0, -0.45, -0.01),
        scale=(1.8, 0.2)
    )
    hotbar_ui.append(hotbar_bg)
      # Draw slots and items
    for i in range(1, 8):  # Slots 1-7
        slot_x = -0.6 + (i-1) * 0.2
        
        # Draw slot background
        slot_color = color.yellow if i == selected_block else color.gray
        
        slot = Entity(
            parent=camera.ui,
            model='quad',
            color=slot_color,
            position=Vec3(slot_x, -0.45, 0),
            scale=0.15
        )
        hotbar_ui.append(slot)
        
        # Always draw item icon (even if count is 0, but dimmed)
        icon_color = get_block_color(i) if inventory.get(i, 0) > 0 else color.dark_gray
        icon = Entity(
            parent=camera.ui,
            model='quad',
            texture=icons[i],
            color=icon_color,
            position=Vec3(slot_x, -0.45, 0.01),
            scale=0.12
        )
        hotbar_ui.append(icon)
        
        # Draw count text - ALWAYS show the count (moved higher)
        count = inventory.get(i, 0)
        count_color = color.white if count > 0 else color.red
        count_text = Text(
            text=str(count),
            position=Vec3(slot_x, -0.32, 0.02),  # Centered above the slot
            origin=(0, 0),
            color=count_color,
            scale=2.0  # Made bigger for better visibility
        )
        count_ui.append(count_text)

class Voxel(Button):
    def __init__(self, position=(0,0,0), block_id=1):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            color=get_block_color(block_id),
            texture=icons[block_id],
            scale=1.0,
            collider='box'
        )
        self.block_id = block_id

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                # Break block and add to inventory
                if self.block_id in inventory:
                    inventory[self.block_id] += 1
                else:
                    inventory[self.block_id] = 1
                destroy(self)
                draw_hotbar()
            
            if key == 'right mouse down':
                # Place selected block type
                if selected_block in inventory and inventory[selected_block] > 0:
                    new_voxel = Voxel(position=self.position + mouse.normal, block_id=selected_block)
                    inventory[selected_block] -= 1  # Reduce inventory count
                    draw_hotbar()

def create_world():
    voxels = []
    # First generate a height map
    heights = {}
    WORLD_SIZE = 10  # Change this value to make the world bigger or smaller
    
    # Generate initial heights
    for x in range(-WORLD_SIZE, WORLD_SIZE + 1):
        for z in range(-WORLD_SIZE, WORLD_SIZE + 1):
            heights[(x,z)] = math.floor(random.uniform(3, 8))
    
    # Smooth the heights
    smoothed_heights = heights.copy()
    for x in range(-WORLD_SIZE, WORLD_SIZE + 1):
        for z in range(-WORLD_SIZE, WORLD_SIZE + 1):
            # Average height with neighbors
            neighbors = []
            for dx in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    if (x+dx,z+dz) in heights:
                        neighbors.append(heights[(x+dx,z+dz)])
            smoothed_heights[(x,z)] = math.floor(sum(neighbors) / len(neighbors))
    
    # Create the world using smoothed heights
    for x in range(-WORLD_SIZE, WORLD_SIZE + 1):
        for z in range(-WORLD_SIZE, WORLD_SIZE + 1):
            height = smoothed_heights[(x,z)]            # Fill from bottom to top
            for y in range(-2, height):
                if y == height - 1:
                    # Top layer (grass)
                    voxel = Voxel(position=(x, y, z), block_id=1)
                elif y > height - 4:
                    # Underground (dirt)
                    voxel = Voxel(position=(x, y, z), block_id=2)
                else:
                    # Deep underground (stone)
                    voxel = Voxel(position=(x, y, z), block_id=5)
                voxels.append(voxel)
    
    # Add trees on flatter areas
    for _ in range(5):
        x = random.randint(-8, 8)
        z = random.randint(-8, 8)
        # Only place trees where the ground is relatively flat
        height = smoothed_heights[(x,z)]
        create_tree(x, height, z)
    
    # Return both voxels and the height at spawn point for proper player positioning
    spawn_height = smoothed_heights.get((0, 0), 5)  # Get height at (0,0) or default to 5
    return voxels, spawn_height

def create_tree(x, y, z):
    # Create trunk (wood blocks)
    for h in range(3):
        voxel = Voxel(position=(x, y + h, z), block_id=3)  # Wood
    
    # Create leaves
    for dx in [-1, 0, 1]:
        for dz in [-1, 0, 1]:
            for dy in [3, 4]:
                voxel = Voxel(position=(x + dx, y + dy, z + dz), block_id=4)  # Leaves

# Set up the game - FIX THE SPAWN POSITION
voxels, spawn_height = create_world()
player = FirstPersonController(position=(0, spawn_height + 2, 0))  # Spawn 2 blocks above ground
draw_hotbar()

def input(key):
    global selected_block
    
    # Block selection (1-7 keys)
    if key in '1234567':
        selected_block = int(key)
        draw_hotbar()
        print(f"Selected block type {selected_block}: {get_block_name(selected_block)}")
    
    if key == 'q':
        # Quit the game
        ursina.application.quit()

def get_block_name(block_id):
    """Get the name of a block type"""
    block_names = {
        1: "Grass",
        2: "Dirt", 
        3: "Wood",
        4: "Leaves",
        5: "Stone",
        6: "Sand",
        7: "Water"
    }
    return block_names.get(block_id, "Unknown")

# Sky
sky = Entity(
    model='sphere',
    texture='sky',
    shader=lit_with_shadows_shader,
    scale=100,
    double_sided=True,
)

def update():
    pass

app.run()