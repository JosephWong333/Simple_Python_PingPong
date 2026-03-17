import pygame, sys, random

pygame.init()

W, H = 800, 500
win = pygame.display.set_mode((W, H))
pygame.display.set_caption("pong")

clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 40)
small = pygame.font.SysFont("monospace", 18)

BLACK  = (10, 10, 10)
WHITE  = (230, 230, 230)
ACCENT = (80, 200, 120)

PAD_W, PAD_H = 12, 70
BALL  = 10
SPEED = 5

lx, ly = 20, H//2 - PAD_H//2
rx, ry = W - 20 - PAD_W, H//2 - PAD_H//2
ls, rs = 0, 0

bx, by = W//2, H//2
bdx = SPEED * random.choice([-1, 1])
bdy = SPEED * random.choice([-1, 1])

def launch():
    global bx, by, bdx, bdy
    bx, by = W//2, H//2
    bdx = SPEED * random.choice([-1, 1])
    bdy = random.uniform(-SPEED, SPEED)

def draw():
    win.fill(BLACK)

    for y in range(0, H, 20):
        pygame.draw.rect(win, (40, 40, 40), (W//2 - 1, y, 2, 10))

    pygame.draw.rect(win, WHITE, (lx, ly, PAD_W, PAD_H), border_radius=4)
    pygame.draw.rect(win, WHITE, (rx, ry, PAD_W, PAD_H), border_radius=4)
    pygame.draw.circle(win, ACCENT, (int(bx), int(by)), BALL)

    win.blit(font.render(str(ls), True, WHITE), (W//4, 16))
    win.blit(font.render(str(rs), True, WHITE), (3*W//4 - 20, 16))
    win.blit(small.render("W/S   arrows", True, (60, 60, 60)), (W//2 - 55, H - 22))

    pygame.display.flip()

while True:
    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
            ls = rs = 0
            launch()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and ly > 0:           ly -= 6
    if keys[pygame.K_s] and ly < H - PAD_H:   ly += 6
    if keys[pygame.K_UP]   and ry > 0:        ry -= 6
    if keys[pygame.K_DOWN] and ry < H - PAD_H: ry += 6

    bx += bdx
    by += bdy

    if by - BALL <= 0 or by + BALL >= H:
        bdy *= -1

    lpad = pygame.Rect(lx, ly, PAD_W, PAD_H)
    rpad = pygame.Rect(rx, ry, PAD_W, PAD_H)
    ball = pygame.Rect(bx - BALL, by - BALL, BALL*2, BALL*2)

    if ball.colliderect(lpad):
        bdx = abs(bdx) + 0.3
        bdy += random.uniform(-1, 1)
    if ball.colliderect(rpad):
        bdx = -(abs(bdx) + 0.3)
        bdy += random.uniform(-1, 1)

    if bx < 0:
        rs += 1; launch()
    if bx > W:
        ls += 1; launch()

    draw()
