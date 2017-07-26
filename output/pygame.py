import pygame

def render(animation, scale=16, gap=1):
  pygame.init()
  screen = pygame.display.set_mode((53 * gap * scale, 1 * scale))
  for colors in animation:
    rect = pygame.rect.Rect(0, 0, scale, scale)
    for idx, color in enumerate(colors):
      screen.fill(color, rect)
      rect.x += scale * gap
    pygame.display.update()
    time.sleep(0.05)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        return
