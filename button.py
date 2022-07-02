import pygame
from settings import colors

class Button():
    def __init__(self, pos: tuple, head: str, font: pygame.font.Font) -> None:

        self.image1 = pygame.image.load('graphics/button/main_menu_button1.png')
        self.image2 = pygame.image.load('graphics/button/main_menu_button2.png')
        self.rect = self.image1.get_rect(center = pos)

        self.font = font
        self.text = self.font.render(head, True, colors.white)
        self.text_rect = self.text.get_rect(center = (self.rect.center + pygame.Vector2(150, 0)))
    
    def is_mouse_in(self) -> bool:
        mousex, mousey = pygame.mouse.get_pos()
        if not mousex in range(self.rect.left, self.rect.right): return False
        if not mousey in range(self.rect.top, self.rect.bottom): return False
        return True     

    def update(self):
        self.image = self.image2 if self.is_mouse_in() else self.image1
    
    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
