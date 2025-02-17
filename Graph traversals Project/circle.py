import pygame

class Circle:
    def __init__(self, screen: pygame.Surface, radius: int, name: str):
        self.circlePos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        self.radius = radius
        self.color = "red"
        self.name = name
        font = pygame.font.Font('freesansbold.ttf', 25)
        self.text = font.render(name, True, (255, 255, 255))
        self.textRect = self.text.get_rect()
        self.textRect.center = (self.circlePos[0], self.circlePos[1])

    def drawCircle(self) -> list:
        return [self.color, self.circlePos, self.radius]
    
    def drawText(self) -> list:
        return [self.text, self.textRect] 

    def setSelected(self, selected):
        if selected:
            self.color = "blue"
        else:
            self.color = "red"

    def circleCollision(self, mousePos: tuple[int, int]) -> bool:
        within = lambda x, low, high: low <= x <= high
        return within(mousePos[0], self.circlePos.x - self.radius, self.circlePos.x + self.radius)\
            and within(mousePos[1], self.circlePos.y - self.radius, self.circlePos.y + self.radius)
    
    def addPosition(self, x, y):
        self.circlePos[0] += x
        self.circlePos[1] += y
        self.textRect.center = (self.circlePos[0], self.circlePos[1])