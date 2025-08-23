import pygame
import sys

pygame.init()

# Tamanho da tela
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("rush")

# Carregando o cenário
cenario = pygame.image.load("Assets/cenari.png").convert_alpha()
CENARIO_WIDTH, CENARIO_HEIGHT = cenario.get_size()

# Jogador
player_pos = [100, 100]
player_radius = 10
player_speed = 4
player_color = (255, 0, 0)

# Física
vel_y = 0
gravidade = 0.2
velocidade_maxima_queda = 10
pulo_forca = -10
no_chao = False

clock = pygame.time.Clock()

def is_transparent(x, y):
    if 0 <= x < CENARIO_WIDTH and 0 <= y < CENARIO_HEIGHT:
        pixel = cenario.get_at((int(x), int(y)))
        return pixel.a == 0
    return False

def get_camera_offset(player_pos):
    offset_x = player_pos[0] - SCREEN_WIDTH // 2
    offset_y = player_pos[1] - SCREEN_HEIGHT // 2
    offset_x = max(0, min(offset_x, CENARIO_WIDTH - SCREEN_WIDTH))
    offset_y = max(0, min(offset_y, CENARIO_HEIGHT - SCREEN_HEIGHT))
    return offset_x, offset_y

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimento lateral
    keys = pygame.key.get_pressed()
    nova_x = player_pos[0]
    if keys[pygame.K_LEFT]:
        nova_x -= player_speed
    if keys[pygame.K_RIGHT]:
        nova_x += player_speed

    if is_transparent(nova_x, player_pos[1]):
        player_pos[0] = nova_x

    # Verifica se está no chão olhando 1 pixel abaixo do personagem
    if not is_transparent(player_pos[0], player_pos[1] + player_radius + 1):
        no_chao = True
        vel_y = 0
    else:
        no_chao = False
        vel_y += gravidade
        vel_y = min(vel_y, velocidade_maxima_queda)

    # Pulo
    if keys[pygame.K_SPACE] and no_chao:
        vel_y = pulo_forca

    # Movimento vertical
    nova_y = player_pos[1] + vel_y
    if is_transparent(player_pos[0], nova_y + player_radius):
        player_pos[1] = nova_y
    else:
        # Parar no chão
        while is_transparent(player_pos[0], player_pos[1] + player_radius + 1):
            player_pos[1] += 1
        vel_y = 0

    # Câmera
    camera_offset = get_camera_offset(player_pos)

    # Desenho
    screen.fill((0, 0, 0))
    screen.blit(cenario, (-camera_offset[0], -camera_offset[1]))
    player_screen_pos = (
        int(player_pos[0] - camera_offset[0]),
        int(player_pos[1] - camera_offset[1])
    )
    pygame.draw.circle(screen, player_color, player_screen_pos, player_radius)

    pygame.display.flip()
    clock.tick(60)
