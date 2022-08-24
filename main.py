import pygame
from controls_loop import ControlsLoop
from gameplay_loop import GameplyLoop
from menu_loop import MenuLoop

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN|pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.running = True

        self.menu_loop = MenuLoop(self)
        self.gameplay_loop = GameplyLoop(self)
        self.controls_loop = ControlsLoop(self)
        self.current_loop = self.menu_loop
    
    def current_loop_is_gameplay(self):
        self.current_loop = self.gameplay_loop
    
    def current_loop_is_menu(self):
        self.current_loop = self.menu_loop
        
    def current_loop_is_controls(self):
        self.current_loop = self.controls_loop
    
    def main_loop(self):
        while self.running:
            self.clock.tick(60)
            self.current_loop.get_events()
            self.current_loop.update()
            self.current_loop.render()
            
if __name__ == '__main__':
    game = Game()
    game.main_loop()