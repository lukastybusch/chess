import pygame
import sys
from map import create_map, field_to_index
from engine import is_valid_move, make_move

# Pygame initialisieren
pygame.init()

# Konstanten
BOARD_SIZE = 640
SQUARE_SIZE = BOARD_SIZE // 8
WHITE_SQUARE = (240, 217, 181)
BLACK_SQUARE = (181, 136, 99)
HIGHLIGHT = (255, 255, 0, 128)  # Gelb mit Transparenz
SELECTED = (0, 255, 0, 128)     # Grün mit Transparenz

# Farben für Figuren
WHITE_PIECE = (255, 255, 255)   # Weiße Figuren
BLACK_PIECE = (0, 0, 0)         # Schwarze Figuren
PIECE_OUTLINE = (50, 50, 50)    # Umrandung für bessere Sichtbarkeit

# Figuren-Symbole - Text-basiert für bessere Kompatibilität
PIECE_SYMBOLS = {
    # Weiße Figuren
    'K': 'K', 'Q': 'Q', 'R': 'R', 'B': 'B', 'N': 'N', 'P': 'P',
    # Schwarze Figuren  
    'k': 'k', 'q': 'q', 'r': 'r', 'b': 'b', 'n': 'n', 'p': 'p'
}

# Alternative Unicode-Symbole (falls verfügbar)
UNICODE_SYMBOLS = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
}

class ChessGUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE + 100))
        pygame.display.set_caption("Schach GUI - Klicke und ziehe Figuren")
        
        self.clock = pygame.time.Clock()
        
        # Schriftarten für Figuren
        self.piece_font = pygame.font.SysFont('Arial', 48, bold=True)  # Für Text-Figuren
        self.unicode_font = None
        
        # Versuche Unicode-Schrift zu laden
        try:
            self.unicode_font = pygame.font.SysFont('Apple Symbols', 60)  # macOS Unicode Font
            if not self.unicode_font:
                self.unicode_font = pygame.font.SysFont('Arial Unicode MS', 60)
        except:
            pass
            
        self.text_font = pygame.font.SysFont('Arial', 28)  # Für Text
        self.use_unicode = self.test_unicode_support()
        
        self.board = create_map()
        self.current_player = "white"
        self.selected_square = None
        self.valid_moves = []
    
    def test_unicode_support(self):
        """Teste ob Unicode-Schachsymbole unterstützt werden"""
        if not self.unicode_font:
            return False
        
        try:
            # Teste ob das Unicode-Symbol korrekt gerendert wird
            test_surface = self.unicode_font.render('♔', True, (0, 0, 0))
            return test_surface.get_width() > 10  # Wenn zu schmal, wahrscheinlich kein Symbol
        except:
            return False
        
    def pos_to_square(self, pos):
        """Konvertiert Maus-Position zu Schachfeld-Koordinaten"""
        x, y = pos
        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            col = x // SQUARE_SIZE
            row = y // SQUARE_SIZE
            return (row, col)
        return None
    
    def square_to_pos(self, square):
        """Konvertiert Schachfeld-Koordinaten zu Pixel-Position"""
        row, col = square
        x = col * SQUARE_SIZE
        y = row * SQUARE_SIZE
        return (x, y)
    
    def get_valid_moves_for_piece(self, square):
        """Findet alle gültigen Züge für eine Figur"""
        valid_moves = []
        piece = self.board[square[0]][square[1]]
        
        # Überprüfe alle möglichen Zielfelder
        for row in range(8):
            for col in range(8):
                target = (row, col)
                if target != square:
                    if is_valid_move(self.board, square, target, piece):
                        valid_moves.append(target)
        
        return valid_moves
    
    def draw_board(self):
        """Zeichnet das Schachbrett mit Koordinaten"""
        for row in range(8):
            for col in range(8):
                color = WHITE_SQUARE if (row + col) % 2 == 0 else BLACK_SQUARE
                rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)
                
                # Zeichne Koordinaten in die Ecke der Felder
                if col == 0:  # Zahlen links
                    number = str(8 - row)
                    coord_color = BLACK_SQUARE if (row + col) % 2 == 0 else WHITE_SQUARE
                    coord_text = pygame.font.Font(None, 24).render(number, True, coord_color)
                    self.screen.blit(coord_text, (col * SQUARE_SIZE + 5, row * SQUARE_SIZE + 5))
                
                if row == 7:  # Buchstaben unten
                    letter = chr(ord('a') + col)
                    coord_color = BLACK_SQUARE if (row + col) % 2 == 0 else WHITE_SQUARE
                    coord_text = pygame.font.Font(None, 24).render(letter, True, coord_color)
                    text_rect = coord_text.get_rect()
                    self.screen.blit(coord_text, (col * SQUARE_SIZE + SQUARE_SIZE - text_rect.width - 5, 
                                                row * SQUARE_SIZE + SQUARE_SIZE - text_rect.height - 5))
    
    def draw_highlights(self):
        """Zeichnet Hervorhebungen für ausgewähltes Feld und mögliche Züge"""
        # Hervorhebung für ausgewähltes Feld
        if self.selected_square:
            x, y = self.square_to_pos(self.selected_square)
            highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            highlight_surface.fill(SELECTED)
            self.screen.blit(highlight_surface, (x, y))
        
        # Hervorhebung für mögliche Züge
        for move in self.valid_moves:
            x, y = self.square_to_pos(move)
            highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            highlight_surface.fill(HIGHLIGHT)
            self.screen.blit(highlight_surface, (x, y))
            
            # Kleiner Kreis in der Mitte für leere Felder
            if self.board[move[0]][move[1]] == ".":
                center_x = x + SQUARE_SIZE // 2
                center_y = y + SQUARE_SIZE // 2
                pygame.draw.circle(self.screen, (0, 0, 0), (center_x, center_y), 10)
    
    def draw_pieces(self):
        """Zeichnet die Schachfiguren mit unterschiedlichen Darstellungen"""
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != ".":
                    # Wähle Symbol und Schrift
                    if self.use_unicode and self.unicode_font:
                        symbol = UNICODE_SYMBOLS.get(piece, piece)
                        font = self.unicode_font
                    else:
                        symbol = PIECE_SYMBOLS.get(piece, piece)
                        font = self.piece_font
                    
                    # Bestimme Farben basierend auf Figur
                    if piece.isupper():  # Weiße Figuren
                        piece_color = WHITE_PIECE
                        bg_color = (220, 220, 220)  # Hellgrauer Hintergrund
                        border_color = BLACK_PIECE
                    else:  # Schwarze Figuren
                        piece_color = BLACK_PIECE
                        bg_color = (60, 60, 60)  # Dunkelgrauer Hintergrund
                        border_color = WHITE_PIECE
                    
                    center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                    center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                    
                    # Wenn Unicode nicht funktioniert, zeichne einen farbigen Kreis mit Buchstaben
                    if not self.use_unicode:
                        # Zeichne Hintergrund-Kreis
                        pygame.draw.circle(self.screen, bg_color, (center_x, center_y), 30)
                        pygame.draw.circle(self.screen, border_color, (center_x, center_y), 30, 3)
                    
                    # Zeichne das Symbol/den Buchstaben
                    text = font.render(symbol, True, piece_color)
                    text_rect = text.get_rect()
                    text_rect.center = (center_x, center_y)
                    self.screen.blit(text, text_rect)
    
    def draw_ui(self):
        """Zeichnet Benutzeroberfläche (Spieler-Info, etc.)"""
        # Hintergrund für UI
        ui_rect = pygame.Rect(0, BOARD_SIZE, BOARD_SIZE, 100)
        pygame.draw.rect(self.screen, (50, 50, 50), ui_rect)
        
        # Aktueller Spieler
        text = f"Am Zug: {'Weiß' if self.current_player == 'white' else 'Schwarz'}"
        player_text = self.text_font.render(text, True, (255, 255, 255))
        self.screen.blit(player_text, (10, BOARD_SIZE + 10))
        
        # Darstellungsart
        display_mode = "Unicode-Symbole" if self.use_unicode else "Text-Modus"
        mode_text = self.text_font.render(f"Modus: {display_mode}", True, (180, 180, 180))
        self.screen.blit(mode_text, (350, BOARD_SIZE + 10))
        
        # Anweisungen
        if self.selected_square:
            instruction = "Klicke auf ein Zielfeld oder klicke die Figur erneut ab"
        else:
            instruction = "Klicke auf eine Figur zum Auswählen"
        
        instruction_text = self.text_font.render(instruction, True, (200, 200, 200))
        self.screen.blit(instruction_text, (10, BOARD_SIZE + 40))
    
    def handle_click(self, pos):
        """Behandelt Mausklicks"""
        square = self.pos_to_square(pos)
        if not square:
            return
        
        row, col = square
        piece = self.board[row][col]
        
        # Wenn kein Feld ausgewählt ist
        if not self.selected_square:
            # Wähle Figur aus, wenn sie dem aktuellen Spieler gehört
            if piece != ".":
                is_white_piece = piece.isupper()
                is_current_player = (self.current_player == "white" and is_white_piece) or \
                                  (self.current_player == "black" and piece.islower())
                
                if is_current_player:
                    self.selected_square = square
                    self.valid_moves = self.get_valid_moves_for_piece(square)
        
        # Wenn ein Feld bereits ausgewählt ist
        else:
            # Wenn das gleiche Feld geklickt wird, Auswahl aufheben
            if square == self.selected_square:
                self.selected_square = None
                self.valid_moves = []
            
            # Wenn ein gültiger Zug geklickt wird
            elif square in self.valid_moves:
                # Zug ausführen
                selected_piece = self.board[self.selected_square[0]][self.selected_square[1]]
                if is_valid_move(self.board, self.selected_square, square, selected_piece):
                    self.board = make_move(self.board, self.selected_square, square)
                    
                    # Spieler wechseln
                    self.current_player = "black" if self.current_player == "white" else "white"
                
                # Auswahl zurücksetzen
                self.selected_square = None
                self.valid_moves = []
            
            # Wenn eine andere eigene Figur geklickt wird
            elif piece != ".":
                is_white_piece = piece.isupper()
                is_current_player = (self.current_player == "white" and is_white_piece) or \
                                  (self.current_player == "black" and piece.islower())
                
                if is_current_player:
                    self.selected_square = square
                    self.valid_moves = self.get_valid_moves_for_piece(square)
                else:
                    self.selected_square = None
                    self.valid_moves = []
    
    def run(self):
        """Hauptspiel-Schleife"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Linke Maustaste
                        self.handle_click(event.pos)
            
            # Zeichnen
            self.screen.fill((60, 60, 60))
            self.draw_board()
            self.draw_highlights()
            self.draw_pieces()
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = ChessGUI()
    game.run()