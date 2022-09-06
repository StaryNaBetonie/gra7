import pygame
from controls_loop import ControlsLoop
from credits_loop import CreditsLoop
from gameplay_loop import GameplyLoop
from menu_loop import MenuLoop
from support import add_date_to_text_file

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN|pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.running = True

        self.menu_loop = MenuLoop(self)
        self.gameplay_loop = GameplyLoop(self)
        self.controls_loop = ControlsLoop(self)
        self.credits_loop = CreditsLoop(self)
        self.current_loop = self.menu_loop
    
    def current_loop_is_gameplay(self):
        self.current_loop = self.gameplay_loop
    
    def current_loop_is_menu(self):
        self.current_loop = self.menu_loop
        
    def current_loop_is_controls(self):
        self.current_loop = self.controls_loop
    
    def current_loop_is_credits(self):
        self.current_loop = self.credits_loop
    
    def main_loop(self):
        while self.running:
            self.clock.tick(60)
            self.current_loop.get_events()
            self.current_loop.update()
            self.current_loop.render()
            
if __name__ == '__main__':
    add_date_to_text_file()
    game = Game()
    game.main_loop()