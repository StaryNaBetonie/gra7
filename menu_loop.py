import pygame
from button import Button
from settings import colors

class MenuLoop:
    def __init__(self, game) -> None:
        self.game = game

        self.font = pygame.font.Font(None, 150)
    
        self.play_button = Button((960, 380), 'Play', self.font)
        self.controls_button = Button((960, 580), 'Controls', self.font)
        self.credits_button = Button((960, 780), 'Credits', self.font)
        self.exit_button = Button((960, 980), 'Exit', self.font)

        self.head = self.font.render('enter the gungeon chinese edition', True, colors.white)
        self.head_rect = self.head.get_rect(center = (960, 200))

    def render(self):
        self.game.screen.fill(colors.black)
        self.game.screen.blit(self.head, self.head_rect)
        self.play_button.render(self.game.screen)
        self.controls_button.render(self.game.screen)
        self.credits_button.render(self.game.screen)
        self.exit_button.render(self.game.screen)
        pygame.display.update()
    
    def update(self):
        self.play_button.update()
        self.credits_button.update()
        self.controls_button.update()
        self.exit_button.update()
    
    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.play_button.is_mouse_in():
                        self.game.current_loop_is_gameplay()
                    elif self.exit_button.is_mouse_in():
                        self.game.running = False
                    elif self.controls_button.is_mouse_in():
                        self.game.current_loop_is_controls()
                    elif self.credits_button.is_mouse_in():
                        self.game.current_loop_is_credits()