import pygame
from gameplay import GamePlay

class GameplyLoop:
    def __init__(self, game) -> None:
        self.game = game
        self.gameplay = GamePlay()
        self.running = True

    def render(self):
        self.game.screen.fill(self.gameplay.key_color())
        self.gameplay.render(self.game.screen)
        pygame.display.update()
    
    def new_gameplay(self):
        if self.gameplay.player.hp <= 0:
            self.gameplay = GamePlay()
            self.game.current_loop_is_menu()
    
    def update(self):
        self.gameplay.update()
        self.new_gameplay()
    
    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False          
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.current_loop_is_menu()
                if event.key == pygame.K_w:
                    self.gameplay.actions['up'] = True
                if event.key == pygame.K_a:
                    self.gameplay.actions['left'] = True
                if event.key == pygame.K_s:
                    self.gameplay.actions['down'] = True
                if event.key == pygame.K_d:
                    self.gameplay.actions['right'] = True
                if event.key == pygame.K_r:
                    self.gameplay.player.gun.reload()
                if event.key == pygame.K_2:
                    self.gameplay.player.change_item_slot(True)
                if event.key == pygame.K_1:
                    self.gameplay.player.change_item_slot(False)
                if event.key == pygame.K_e:
                    self.gameplay.player.interact_with_objects(self.gameplay)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.gameplay.actions['up'] = False
                if event.key == pygame.K_a:
                    self.gameplay.actions['left'] = False
                if event.key == pygame.K_s:
                    self.gameplay.actions['down'] = False
                if event.key == pygame.K_d:
                    self.gameplay.actions['right'] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.gameplay.actions['fire'] = True
                if event.button == 3:
                    self.gameplay.player.make_dodge()
            if event.type == pygame.MOUSEBUTTONUP:
               if event.button == 1:
                    self.gameplay.actions['fire'] = False