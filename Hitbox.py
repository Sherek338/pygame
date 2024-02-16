import pygame

_layers = {}

class HB:
    def __init__(self, rect: pygame.Rect, layer: list, mask: list, enter_hitbox = lambda mask, hitbox : None) -> None:
       """Init hitbox

       Args:
           rect (pygame.Rect): hitbox zone
           layer (list): list of that can detect hitbox
           mask (list): list of that hitbox can detect
           enter_hitbox (function): function that calls when hitbox enter
       """
       super().__init__()
       self._hitbox = rect
       self._mask = mask
       self._enter_hitbox = enter_hitbox
       
       for index in layer:
            _layers.setdefault(index, []).append(self)
           
    def update(self, center) -> None:
        """Update hitbox

        Args:
            center (Rect.center): new pose
        """
        self._hitbox.center = center
        for mask in self._mask:
            for hitbox in _layers[mask]:
                if self._hitbox.colliderect(hitbox._hitbox):
                    self._enter_hitbox(mask, hitbox)
