import pygame

class Cooldown:
    def __init__(self, time_long: int) -> None:
        self.time_long = time_long
        self.can_perform = True
        self.last_used_time = 0
    
    def timer(self) -> None:
        current_time = pygame.time.get_ticks()
        if self.can_perform: return
        if current_time - self.last_used_time < self.time_long: return
        self.can_perform = True
    
    def __call__(self):
        return self.can_perform

