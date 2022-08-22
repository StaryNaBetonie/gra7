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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.current_loop_is_menu()
                elif event.key == pygame.K_w:
                    self.gameplay.actions['up'] = True
                elif event.key == pygame.K_a:
                    self.gameplay.actions['left'] = True
                elif event.key == pygame.K_s:
                    self.gameplay.actions['down'] = True
                elif event.key == pygame.K_d:
                    self.gameplay.actions['right'] = True
                elif event.key == pygame.K_r:
                    self.gameplay.player.gun.reload()
                elif event.key == pygame.K_2:
                    self.gameplay.player.change_item_slot(True)
                elif event.key == pygame.K_1:
                    self.gameplay.player.change_item_slot(False)
                elif event.key == pygame.K_e:
                    self.gameplay.player.interact_with_objects(self.gameplay)
                elif event.key == pygame.K_F9:
                    self.gameplay.player.inventory.all_weapons()
                    self.gameplay.player.gun = self.gameplay.player.inventory.selected_gun
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.gameplay.actions['up'] = False
                elif event.key == pygame.K_a:
                    self.gameplay.actions['left'] = False
                elif event.key == pygame.K_s:
                    self.gameplay.actions['down'] = False
                elif event.key == pygame.K_d:
                    self.gameplay.actions['right'] = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.gameplay.actions['fire'] = True
                elif event.button == 3:
                    self.gameplay.player.make_dodge()
            elif event.type == pygame.MOUSEBUTTONUP:
               if event.button == 1:
                    self.gameplay.actions['fire'] = False