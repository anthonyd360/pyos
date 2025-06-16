import pygame
import sys
import os

# Debug: Print current working directory and check images folder
print(f"Current working directory: {os.getcwd()}")
print(f"Images folder exists: {os.path.exists('images')}")
if os.path.exists('images'):
    print("Contents of images folder:", os.listdir('images'))

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (245, 245, 245)
GRAY = (120, 120, 120)
GREEN = (118, 150, 86)
BEIGE = (238, 238, 210)

# Load piece images
PIECES = {}
piece_names = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wP']
missing_pieces = []

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# Debug logging
import logging
logging.basicConfig(filename='chess_debug.log', level=logging.DEBUG)
logging.info("Starting chess game...")

try:
    for name in piece_names:
        image_path = get_resource_path(os.path.join('images', f"{name}.png"))
        logging.info(f"Attempting to load: {image_path}")
        if not os.path.exists(image_path):
            logging.error(f"Image file not found: {image_path}")
            print(f"Warning: Image file {image_path} not found")
            missing_pieces.append(name)
            continue
        
        # Load and resize the image
        original_image = pygame.image.load(image_path)
        PIECES[name] = pygame.transform.smoothscale(original_image, (SQUARE_SIZE, SQUARE_SIZE))
        logging.info(f"Successfully loaded: {name}.png")

    if missing_pieces:
        print("\nMissing piece images:", missing_pieces)
        print("\nPlease ensure all piece images are in the images folder")
        pygame.quit()
        sys.exit(1)

except Exception as e:
    logging.error(f"Error loading chess pieces: {str(e)}")
    print(f"Error loading chess pieces: {e}")
    pygame.quit()
    sys.exit(1)

# Set up display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess 2 Player")

# Initial board state
board = [
    ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
    ['bP'] * 8,
    [''] * 8,
    [''] * 8,
    [''] * 8,
    [''] * 8,
    ['wP'] * 8,
    ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
]

selected = None
turn = 'w'  # w = white, b = black

def draw_board(win):
    for row in range(ROWS):
        for col in range(COLS):
            # Draw board squares
            color = BEIGE if (row + col) % 2 == 0 else GREEN
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            # Draw pieces
            piece = board[row][col]
            if piece and piece in PIECES:
                win.blit(PIECES[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))
    
    # Draw highlights for selected piece and valid moves
    if selected:
        sx, sy = selected
        # Highlight selected square with yellow
        pygame.draw.rect(win, (255, 255, 0), 
                        (sy * SQUARE_SIZE, sx * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
        # Highlight valid moves with red circles
        valid_moves = get_valid_moves(selected)
        for move in valid_moves:
            row, col = move
            pygame.draw.circle(win, (255, 0, 0), 
                             (col * SQUARE_SIZE + SQUARE_SIZE//2, 
                              row * SQUARE_SIZE + SQUARE_SIZE//2), 10)

def get_square(pos):
    x, y = pos
    return y // SQUARE_SIZE, x // SQUARE_SIZE

def get_valid_moves(start):
    valid_moves = []
    sx, sy = start
    piece = board[sx][sy]
    
    if not piece or piece[0] != turn:
        return []
    
    piece_type = piece[1]
    piece_color = piece[0]
    
    # Pawn movement
    if piece_type == 'P':
        direction = 1 if piece_color == 'b' else -1  # Black moves down, White moves up
        
        # Forward move
        if 0 <= sx + direction < 8 and not board[sx + direction][sy]:
            valid_moves.append((sx + direction, sy))
            # Initial two-square move
            if ((piece_color == 'w' and sx == 6) or (piece_color == 'b' and sx == 1)) and \
               not board[sx + 2*direction][sy]:
                valid_moves.append((sx + 2*direction, sy))
        
        # Capture moves
        for dy in [-1, 1]:  # Check diagonal captures
            if 0 <= sx + direction < 8 and 0 <= sy + dy < 8:
                target = board[sx + direction][sy + dy]
                if target and target[0] != piece_color:  # Enemy piece
                    valid_moves.append((sx + direction, sy + dy))
    
    # Knight movement
    elif piece_type == 'N':
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                       (1, -2), (1, 2), (2, -1), (2, 1)]
        for dx, dy in knight_moves:
            new_x, new_y = sx + dx, sy + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                target = board[new_x][new_y]
                if not target or target[0] != piece_color:
                    valid_moves.append((new_x, new_y))
    
    # Bishop, Rook, and Queen movements
    elif piece_type in ['B', 'R', 'Q']:
        directions = []
        if piece_type in ['B', 'Q']:  # Diagonal movements
            directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        if piece_type in ['R', 'Q']:  # Horizontal and vertical movements
            directions += [(-1, 0), (1, 0), (0, -1), (0, 1)]
            
        for dx, dy in directions:
            new_x, new_y = sx + dx, sy + dy
            while 0 <= new_x < 8 and 0 <= new_y < 8:
                target = board[new_x][new_y]
                if not target:  # Empty square
                    valid_moves.append((new_x, new_y))
                elif target[0] != piece_color:  # Enemy piece
                    valid_moves.append((new_x, new_y))
                    break
                else:  # Friendly piece
                    break
                new_x, new_y = new_x + dx, new_y + dy
    
    # King movement
    elif piece_type == 'K':
        king_moves = [(-1, -1), (-1, 0), (-1, 1),
                     (0, -1),           (0, 1),
                     (1, -1),  (1, 0),  (1, 1)]
        for dx, dy in king_moves:
            new_x, new_y = sx + dx, sy + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                target = board[new_x][new_y]
                if not target or target[0] != piece_color:
                    valid_moves.append((new_x, new_y))
    
    return valid_moves

def is_valid_move(start, end):
    return end in get_valid_moves(start)

def main():
    global selected, turn
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        draw_board(WIN)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_square(pygame.mouse.get_pos())

                if selected:
                    if is_valid_move(selected, (row, col)):
                        sx, sy = selected
                        piece = board[sx][sy]
                        board[row][col] = piece
                        board[sx][sy] = ''
                        turn = 'b' if turn == 'w' else 'w'
                    selected = None
                else:
                    if board[row][col] and board[row][col][0] == turn:
                        selected = (row, col)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error in chess game: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to close...")
        sys.exit(1)