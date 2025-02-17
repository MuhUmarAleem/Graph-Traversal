import pygame

class Button:
    def __init__(self, text: str, pos: pygame.Vector2, width: int, height: int, action) -> None:
        self.algo = text
        self.action = action
        self.rect = pygame.Rect(pos.x, pos.y, width, height)
        font = pygame.font.Font('freesansbold.ttf', 20)
        self.text = font.render(self.algo, True, "black")
        self.textRect = self.text.get_rect()
        self.textRect.center = (self.rect.center[0], self.rect.center[1])

    def drawRect(self):
        return ["green", self.rect]
    
    def drawText(self):
        return [self.text, self.textRect]
    
    def getAlgo(self):
        return self.algo
    
    def isColliding(self, mousePos: tuple[int, int]) -> bool:
        width = self.rect.width
        height = self.rect.height
        x = self.rect.left
        y = self.rect.top
        within = lambda x, low, high: low <= x <= high
        return within(mousePos[0], x, x + width)\
            and within(mousePos[1], y, y + height)