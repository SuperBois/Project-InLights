def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    rect = img.get_rect()
    rect.center = (x,y)
    screen.blit(img, rect)


def draw_time(screen, time, font, x, y):
    draw_text(screen, time, font, (255,255,255), x, y)