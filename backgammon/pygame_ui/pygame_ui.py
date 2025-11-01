# pygame_ui.py
import sys
import pygame
from ..core.game import BackgammonGame

WIDTH, HEIGHT = 1000, 700
MARGIN_X, MARGIN_Y = 40, 40
BG_COLOR = (245, 239, 230)
BOARD_COLOR = (230, 220, 200)
TRI_A = (170, 120, 90)
TRI_B = (210, 170, 130)
LINE = (60, 60, 60)
WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
TEXT = (25, 25, 25)
STATE_ROLL = 0
STATE_SELECT_START = 1
STATE_SELECT_END = 2
STATE_END_TURN = 3

MAX_VISIBLE_STACK = 5


def render_ui_elements(surface, game, font):
    dice_values = game.dice.get_values()
    dice_x = WIDTH // 2 - 100
    dice_y = MARGIN_Y + 10  

    txt_turn = font.render(f"Turno de: {game.current_player.name} ({game.current_player.color.upper()})", True, TEXT)
    surface.blit(txt_turn, (dice_x - 100, dice_y))

    for i, die_val in enumerate(dice_values):
        rect = pygame.Rect(dice_x + i * 50, dice_y + 30, 40, 40)
        pygame.draw.rect(surface, LINE, rect, 1)
        txt = font.render(str(die_val), True, TEXT)
        surface.blit(txt, txt.get_rect(center=rect.center))

    end_turn_rect = pygame.Rect(WIDTH - MARGIN_X - 150, MARGIN_Y, 150, 40)
    pygame.draw.rect(surface, (200, 50, 50), end_turn_rect, border_radius=5)
    txt_end = font.render("TERMINAR TURNO", True, WHITE)
    surface.blit(txt_end, txt_end.get_rect(center=end_turn_rect.center))

    return end_turn_rect


def point_index_to_display(idx):
    if 0 <= idx <= 11:
        return 'top', 11 - idx
    else:
        return 'bottom', idx - 12


def draw_triangle(surface, board_rect, col_vis, row, color):
    x0 = board_rect.left + col_vis * (board_rect.width / 12.0)
    x1 = x0 + (board_rect.width / 12.0)
    x_mid = (x0 + x1) / 2.0

    if row == 'top':
        tip_y = board_rect.top + board_rect.height * 0.42
        pts = [(x0, board_rect.top), (x1, board_rect.top), (x_mid, tip_y)]
    else:
        tip_y = board_rect.bottom - board_rect.height * 0.42
        pts = [(x0, board_rect.bottom), (x1, board_rect.bottom), (x_mid, tip_y)]
    pygame.draw.polygon(surface, color, pts)


def draw_checker(surface, center, radius, color_rgb, label=None, font=None):
    pygame.draw.circle(surface, color_rgb, center, radius)
    pygame.draw.circle(surface, LINE, center, radius, 1)
    if label and font:
        txt_color = LINE if color_rgb == WHITE else WHITE
        txt = font.render(str(label), True, txt_color)
        rect = txt.get_rect(center=center)
        surface.blit(txt, rect)


def render_board(surface, game, font):
    surface.fill(BG_COLOR)

    board_rect = pygame.Rect(
        MARGIN_X,
        MARGIN_Y + 20,
        WIDTH - 2 * MARGIN_X,
        HEIGHT - 2 * MARGIN_Y - 40
    )
    pygame.draw.rect(surface, BOARD_COLOR, board_rect, border_radius=12)
    pygame.draw.rect(surface, LINE, board_rect, 2, border_radius=12)

    for col_vis in range(12):
        draw_triangle(surface, board_rect, col_vis, 'top', TRI_A if col_vis % 2 == 0 else TRI_B)
        draw_triangle(surface, board_rect, col_vis, 'bottom', TRI_B if col_vis % 2 == 0 else TRI_A)

    tri_w = board_rect.width / 12.0
    radius = int(tri_w * 0.38)
    radius = max(12, min(radius, 22))
    vgap = 4
    step = radius * 2 + vgap

    top_labels = [str(i) for i in range(12, 0, -1)]
    for col_vis, lbl in enumerate(top_labels):
        x = int(board_rect.left + col_vis * tri_w + tri_w / 2)
        y = board_rect.top - 14
        img = font.render(lbl, True, TEXT)
        rect = img.get_rect(center=(x, y))
        surface.blit(img, rect)

    bottom_labels = [str(i) for i in range(13, 25)]
    for col_vis, lbl in enumerate(bottom_labels):
        x = int(board_rect.left + col_vis * tri_w + tri_w / 2)
        y = board_rect.bottom + 14
        img = font.render(lbl, True, TEXT)
        rect = img.get_rect(center=(x, y))
        surface.blit(img, rect)

    pygame.draw.line(surface, LINE, (board_rect.left, board_rect.centery),
                     (board_rect.right, board_rect.centery), 1)

    hitmap = {} 
    
    for idx in range(24):
        point_number = idx + 1 
        row, col_vis = point_index_to_display(idx)
        tri_w = board_rect.width / 12.0
        tri_h = board_rect.height * 0.42 
        x0 = board_rect.left + col_vis * tri_w

        if row == 'top':
            point_rect = pygame.Rect(x0, board_rect.top, tri_w, tri_h)
        else:
            point_rect = pygame.Rect(x0, board_rect.bottom - tri_h, tri_w, tri_h)

        hitmap[point_number] = {'rect': point_rect, 'checkers': []}
        
        cell = game.board.pos[idx]
        if not cell:
            continue
        color_name, count = cell
        cx = int(board_rect.left + col_vis * tri_w + tri_w / 2)
        color_rgb = WHITE if color_name == 'white' else BLACK

        if row == 'top':
            start_y = int(board_rect.top + radius + 6)
            visibles = min(count, MAX_VISIBLE_STACK)
            extras = max(0, count - (MAX_VISIBLE_STACK - 1)) if count > MAX_VISIBLE_STACK else 0
            for i in range(visibles):
                cy = start_y + i * step
                label = extras if (extras and i == visibles - 1) else None  
                draw_checker(surface, (cx, cy), radius, color_rgb, label, font)
                hitmap[point_number]['checkers'].append((cx, cy, radius)) 
        else:
            start_y = int(board_rect.bottom - radius - 6)
            visibles = min(count, MAX_VISIBLE_STACK)
            extras = max(0, count - (MAX_VISIBLE_STACK - 1)) if count > MAX_VISIBLE_STACK else 0
            for i in range(visibles):
                cy = start_y - i * step
                label = extras if (extras and i == visibles - 1) else None 
                draw_checker(surface, (cx, cy), radius, color_rgb, label, font)
                hitmap[point_number]['checkers'].append((cx, cy, radius)) 

    bar_x = board_rect.centerx

    black_bar_count = len(game.board.bar.get('black', []))
    bar_y_start_bottom = board_rect.bottom - radius - 6 
    bar_rect_black = pygame.Rect(bar_x - radius, board_rect.centery, 2 * radius, board_rect.bottom - board_rect.centery)
    hitmap[25] = {'rect': bar_rect_black, 'checkers': []}
    for i in range(min(black_bar_count, MAX_VISIBLE_STACK)):
        cy = bar_y_start_bottom - i * step
        label = max(0, black_bar_count - (
                    MAX_VISIBLE_STACK - 1)) if black_bar_count > MAX_VISIBLE_STACK and i == MAX_VISIBLE_STACK - 1 else None
        draw_checker(surface, (bar_x, cy), radius, BLACK, label, font)
        hitmap[25]['checkers'].append((bar_x, cy, radius))

    white_bar_count = len(game.board.bar.get('white', []))
    bar_y_start_top = board_rect.top + radius + 6
    bar_rect_white = pygame.Rect(bar_x - radius, board_rect.top, 2 * radius, board_rect.centery - board_rect.top)
    hitmap[0] = {'rect': bar_rect_white, 'checkers': []}
    for i in range(min(white_bar_count, MAX_VISIBLE_STACK)):
        cy = bar_y_start_top + i * step
        label = max(0, white_bar_count - (
                    MAX_VISIBLE_STACK - 1)) if white_bar_count > MAX_VISIBLE_STACK and i == MAX_VISIBLE_STACK - 1 else None
        draw_checker(surface, (bar_x, cy), radius, WHITE, label, font)
        hitmap[0]['checkers'].append((bar_x, cy, radius))

    off_w = 120
    off_h = 30
    off_x_right = board_rect.right + 10 

    off_b_count = len(game.board.off_board.get('black', []))
    off_b_rect = pygame.Rect(off_x_right, board_rect.top, off_w, off_h) 
    pygame.draw.rect(surface, LINE, off_b_rect, 1, border_radius=4)
    txt_b = font.render(f"Black Off: {off_b_count:2d}", True, TEXT)
    rect_b = txt_b.get_rect(center=off_b_rect.center)
    surface.blit(txt_b, rect_b)
    hitmap[0]['off_rect'] = off_b_rect 

    off_w_count = len(game.board.off_board.get('white', []))
    off_w_rect = pygame.Rect(off_x_right, board_rect.bottom - off_h, off_w, off_h) 
    pygame.draw.rect(surface, LINE, off_w_rect, 1, border_radius=4)
    txt_w = font.render(f"White Off: {off_w_count:2d}", True, TEXT)
    rect_w = txt_w.get_rect(center=off_w_rect.center)
    surface.blit(txt_w, rect_w)
    hitmap[25]['off_rect'] = off_w_rect 

    return hitmap

def hit_test(hitmap, pos):
    """
    Detecta si el clic del ratón impactó en una ficha, en el área de una punta, en la barra o en el área de Off-Board.
    Retorna el índice (0, 1-24, 25) o None.
    """
    mx, my = pos
    
    for idx, data in hitmap.items():
        for (cx, cy, r) in data['checkers']:
            dx, dy = mx - cx, my - cy
            if dx * dx + dy * dy <= r * r:
                return idx 
    
    for idx, data in hitmap.items():
        if 'rect' in data and data['rect'].collidepoint(pos):
            return idx 
        if 'off_rect' in data and data['off_rect'].collidepoint(pos):
            return idx 
            
    return None

def main():
    pygame.init()
    pygame.display.set_caption("Backgammon (Pygame)")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 20)
    font_large = pygame.font.SysFont(None, 50, bold=True) 

    game = BackgammonGame("Player1", "Player2")
    game.start_game()

    game_state = STATE_ROLL
    selected_start_point = None  

    running = True
    while running:
        hitmap = render_board(screen, game, font)
        end_turn_rect = render_ui_elements(screen, game, font)

        is_over, winner_color = game.check_game_over()
        if is_over:
            game_state = STATE_END_TURN 
            
            winner_name = game.player1.name if winner_color == 'white' else game.player2.name
            final_msg = font_large.render(f"¡JUEGO TERMINADO! GANADOR: {winner_name.upper()}", True, (0, 150, 0))
            screen.blit(final_msg, final_msg.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            
            pygame.display.flip()
            pygame.time.wait(5000) 
            running = False 
            break

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mouse_pos = e.pos

                if game_state == STATE_ROLL:
                    game.roll_dice()
                    game_state = STATE_SELECT_START
                    print(f"Dados lanzados: {game.dice.get_values()}")

                elif game_state == STATE_SELECT_START or game_state == STATE_SELECT_END:
                    if end_turn_rect.collidepoint(mouse_pos):
                        game_state = STATE_END_TURN
                        print("Turno terminado manualmente.")
                        break

                    idx = hit_test(hitmap, mouse_pos)
                    point_number = idx 
                    
                    if point_number is not None and point_number in range(26):
                        
                        if game_state == STATE_SELECT_START:
                            
                            is_reentry_required = game.board_has_captured_checkers(game.current_player.color)

                            if point_number in [0, 25]:
                                bar_color = 'white' if point_number == 0 else 'black'
                                
                                if bar_color == game.current_player.color and is_reentry_required:
                                    selected_start_point = point_number
                                    game_state = STATE_SELECT_END
                                    print(f"✅ BARRA de {bar_color.upper()} seleccionada como inicio.")
                                else:
                                    print("❌ La barra no tiene tus fichas o no es obligatoria la reentrada.")
                                    
                            elif 1 <= point_number <= 24:
                                
                                if is_reentry_required:
                                    print("❌ Debes mover las fichas de la barra (reentrada) primero.")
                                    continue
                                
                                point_obj = game.board.points[point_number]
                                if point_obj.count() > 0 and point_obj.top_color() == game.current_player.color:
                                    selected_start_point = point_number
                                    game_state = STATE_SELECT_END
                                    print(f"✅ Punto de inicio seleccionado: {selected_start_point}")
                                else:
                                    print("❌ No es posible iniciar el movimiento desde aquí.")

                        elif game_state == STATE_SELECT_END:
                            end_point = point_number
                            die_used = 0
                            move_successful = False
                            
                            valid_moves = game.get_valid_moves()
                            
                            for start, end, die_val in valid_moves:
                                if start == selected_start_point and end == end_point:
                                    die_used = die_val 
                                    print(f"DEBUG: Movimiento válido encontrado: {start} -> {end} (usando {die_used})")
                                    break
                            
                            if die_used > 0:
                                move_successful = game.make_move(selected_start_point, end_point, die_used)
                                
                                if move_successful:
                                    print(f"✅ Movimiento: {selected_start_point} -> {end_point} (usando {die_used})")
                                    selected_start_point = None 
                                    
                                    if game.dice.rolls_left == 0:
                                        game_state = STATE_END_TURN 
                                    else:
                                        game_state = STATE_SELECT_START 
                                else:
                                    print("❌ Movimiento inválido (falló game.make_move).")
                            else:
                                print(f"❌ Movimiento inválido. El movimiento de {selected_start_point} a {end_point} no es legal con los dados restantes.")

                            if not move_successful:
                                selected_start_point = None
                                game_state = STATE_SELECT_START 

        if game_state == STATE_END_TURN and running:
            game.switch_turn()
            game_state = STATE_ROLL
            print(f"\n--- CAMBIO DE TURNO --- Ahora juega {game.current_player.name}")

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()