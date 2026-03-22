import pygame, sys, random

pygame.init()
W, H = 800, 500
win = pygame.display.set_mode((W, H))
pygame.display.set_caption("pong")
clock = pygame.time.Clock()
font  = pygame.font.SysFont("monospace", 40)
small = pygame.font.SysFont("monospace", 18)

BLACK  = (10, 10, 10)
WHITE  = (230, 230, 230)
ACCENT = (80, 200, 120)
DIM    = (40, 40, 40)

PAD_W, PAD_H = 12, 70
BALL_R   = 10
BASE_SPD = 5
MAX_SPD  = 12
WIN_SC   = 7

lx, ly = 20, H // 2 - PAD_H // 2
rx, ry = W - 20 - PAD_W, H // 2 - PAD_H // 2
ls, rs = 0, 0
bx = by = bdx = bdy = 0


def launch():
    global bx, by, bdx, bdy
    bx, by = W / 2, H / 2
    bdx = BASE_SPD * random.choice([-1, 1])
    bdy = random.uniform(-BASE_SPD * 0.8, BASE_SPD * 0.8)


def clamp_speed():
    global bdx, bdy
    spd = (bdx**2 + bdy**2) ** 0.5
    if spd > MAX_SPD:
        bdx = bdx / spd * MAX_SPD
        bdy = bdy / spd * MAX_SPD


def draw():
    win.fill(BLACK)
    for y in range(0, H, 20):
        pygame.draw.rect(win, DIM, (W // 2 - 1, y, 2, 10))
    pygame.draw.rect(win, WHITE, (lx, ly, PAD_W, PAD_H), border_radius=4)
    pygame.draw.rect(win, WHITE, (rx, ry, PAD_W, PAD_H), border_radius=4)
    pygame.draw.circle(win, ACCENT, (int(bx), int(by)), BALL_R)
    win.blit(font.render(str(ls), True, WHITE), (W // 4, 16))
    win.blit(font.render(str(rs), True, WHITE), (3 * W // 4 - 20, 16))
    if ls == WIN_SC or rs == WIN_SC:
        msg = "LEFT WINS!" if ls == WIN_SC else "RIGHT WINS!"
        surf = font.render(msg, True, ACCENT)
        win.blit(surf, surf.get_rect(center=(W // 2, H // 2)))
        win.blit(small.render("R to restart", True, DIM), small.render("R to restart", True, DIM).get_rect(center=(W // 2, H // 2 + 50)))
    else:
        win.blit(small.render("W/S   arrows    R restart", True, (55, 55, 55)), (W // 2 - 100, H - 22))
    pygame.display.flip()


launch()

while True:
    clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
            ls = rs = 0
            launch()

    if ls < WIN_SC and rs < WIN_SC:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and ly > 0:             ly -= 6
        if keys[pygame.K_s] and ly < H - PAD_H:     ly += 6
        if keys[pygame.K_UP]   and ry > 0:          ry -= 6
        if keys[pygame.K_DOWN] and ry < H - PAD_H:  ry += 6

        bx += bdx
        by += bdy

        if by - BALL_R <= 0:
            by = BALL_R; bdy = abs(bdy)
        elif by + BALL_R >= H:
            by = H - BALL_R; bdy = -abs(bdy)

        ball = pygame.Rect(bx - BALL_R, by - BALL_R, BALL_R * 2, BALL_R * 2)
        lpad = pygame.Rect(lx, ly, PAD_W, PAD_H)
        rpad = pygame.Rect(rx, ry, PAD_W, PAD_H)

        if ball.colliderect(lpad) and bdx < 0:
            bx  = lx + PAD_W + BALL_R
            rel = (by - (ly + PAD_H / 2)) / (PAD_H / 2)
            bdx = abs(bdx) + 0.4
            bdy = rel * BASE_SPD + random.uniform(-0.5, 0.5)
            clamp_speed()

        if ball.colliderect(rpad) and bdx > 0:
            bx  = rx - BALL_R
            rel = (by - (ry + PAD_H / 2)) / (PAD_H / 2)
            bdx = -(abs(bdx) + 0.4)
            bdy = rel * BASE_SPD + random.uniform(-0.5, 0.5)
            clamp_speed()

        if bx < 0:
            rs += 1; launch()
        if bx > W:
            ls += 1; launch()

    draw()
