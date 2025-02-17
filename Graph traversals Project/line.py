import pygame
from circle import Circle

class Line:
    def __init__(self, circle: list[Circle]):
        self.circle = circle
        self.startPos = self.circle[0].circlePos
        self.endPos = self.circle[1].circlePos
        self.color = "red"
        self.cost = "0"
        font = pygame.font.Font('freesansbold.ttf', 20)
        self.text = font.render(self.cost, True, "white")
        self.textRect = self.text.get_rect()
        self.textRect.center = (
            (self.startPos[0] + self.endPos[0]) // 2,
            (self.startPos[1] + self.endPos[1]) // 2,
        )

    def drawLine(self) -> list:
        return [self.color, self.startPos, self.endPos]
    
    def checkCollision(self, mousePos: tuple[int, int]) -> bool:
        width = (len(self.color) // 2) * 20 + 10
        within = lambda x, low, high: low <= x <= high
        return within(mousePos[0], self.textRect.center[0] - width, self.textRect.center[0] + width)\
            and within(mousePos[1], self.textRect.center[1] - width, self.textRect.center[1] + width)
    
    def setSelected(self, selected: bool):
        font = pygame.font.Font('freesansbold.ttf', 20)
        if selected:
            self.text = font.render(self.cost, True, "green")
        else:
            self.text = font.render(self.cost, True, "white")
        self.textRect = self.text.get_rect()
        self.textRect.center = (
            (self.startPos[0] + self.endPos[0]) // 2,
            (self.startPos[1] + self.endPos[1]) // 2,
        )

    def getCost(self) -> str:
        return self.cost

    def setCost(self, cost):
        self.cost = cost
        font = pygame.font.Font('freesansbold.ttf', 20)
        self.text = font.render(cost, True, "green")
        self.textRect = self.text.get_rect()
        self.textRect.center = (
            (self.startPos[0] + self.endPos[0]) // 2,
            (self.startPos[1] + self.endPos[1]) // 2,
        )

    def drawText(self) -> list:
        self.textRect.center = (
            (self.startPos[0] + self.endPos[0]) // 2,
            (self.startPos[1] + self.endPos[1]) // 2,
        )
        return [self.text, self.textRect] 