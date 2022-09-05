import pygame
from button import Button

class CreditsLoop:
    def __init__(self, game):
        self.game = game

        self.font = pygame.font.Font(None, 150)
        self.back_button = Button((600, 850), 'Back', self.font)

        self.image = pygame.image.load('graphics/button/credits.png')
    
    def render(self):
        self.game.screen.blit(self.image, (0, 0))
        self.back_button.render(self.game.screen)
        pygame.display.update()
    
    def update(self):
        self.back_button.update()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.back_button.is_mouse_in():
                        self.game.current_loop_is_menu()