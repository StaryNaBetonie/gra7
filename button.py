import pygame
from settings import colors

class Button():
    def __init__(self, pos: tuple, head: str, font: pygame.font.Font) -> None:

        self.font = font
        self.text = self.font.render(head, True, colors.black)
        self.text_rect = self.text.get_rect(center = pos)

        self.background = pygame.Surface((800, 250))
        self.background_rect = self.background.get_rect(center = pos)
    
    def is_mouse_in(self) -> bool:
        mousex, mousey = pygame.mouse.get_pos()
        if not mousex in range(self.background_rect.left, self.background_rect.right): return False
        if not mousey in range(self.background_rect.top, self.background_rect.bottom): return False
        return True

    def get_color(self):
        color = colors.lighter_gray if self.is_mouse_in() else colors.light_gray
        self.background.fill(color)

    def update(self):
        self.get_color()
    
    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.background, self.background_rect)
        screen.blit(self.text, self.text_rect)
