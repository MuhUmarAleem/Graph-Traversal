import pygame
from circle import Circle
from line import Line
from button import Button
from algo.A_star import A_star
from algo.Dijkstra import Dijkstra
from algo.Best_first import Greedy_Best_First
from algo.DFS import DFS
from algo.BFS import BFS
from algo.Backward_BFS import backward_BFS
from algo.DFID import DF_ID
import math
from time import sleep

def graphWithCost(linesList: list[Line], circlesList: list[Circle]):
    graph: dict[int, list[tuple[int, int]]] = {}
    for i, line in enumerate(linesList):
        cir1Index = circlesList.index(line.circle[0])
        cir2Index = circlesList.index(line.circle[1])
        if cir1Index in graph:
            graph[cir1Index].append((float(line.getCost()), cir2Index))
        else:
            graph[cir1Index] = [(float(line.getCost()), cir2Index)]

        if cir2Index in graph:
            graph[cir2Index].append((float(line.getCost()), cir1Index))
        else:
            graph[cir2Index] = [(float(line.getCost()), cir1Index)]
    
    return graph

def graphWithNoCost(linesList: list[Line], circlesList: list[Circle]):
    graph: dict[int, list[int]] = {}
    for i, line in enumerate(linesList):
        cir1Index = circlesList.index(line.circle[0])
        cir2Index = circlesList.index(line.circle[1])
        if cir1Index in graph:
            graph[cir1Index].append(cir2Index)
        else:
            graph[cir1Index] = [cir2Index]

        if cir2Index in graph:
            graph[cir2Index].append(cir1Index)
        else:
            graph[cir2Index] = [cir1Index]
    
    return graph

def getHue(circlesList: list[Circle]):
    hue:float = []
    last = circlesList[-1]
    ecu = lambda x1, y1, x2, y2: math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    for circle in circlesList:
        hue.append(ecu(circle.circlePos.x, circle.circlePos.y, last.circlePos.x, last.circlePos.y))
    return hue

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

radius = 30
circlesList = [Circle(radius=radius, screen=screen, name="1")]
linesList: list[Line] = []
algoButtonList = [
    Button("A Star", pygame.Vector2(20, 20), 150, 30, lambda: A_star(graphWithCost(linesList, circlesList), getHue(circlesList), 0, len(circlesList) - 1)),
    Button("DFS", pygame.Vector2(190, 20), 150, 30, lambda: DFS(graphWithNoCost(linesList, circlesList), 0, len(circlesList) - 1, None)),
    Button("BFS", pygame.Vector2(360, 20), 150, 30, lambda: BFS(graphWithNoCost(linesList, circlesList), 0, len(circlesList) - 1)),
    Button("Dijkstra", pygame.Vector2(530, 20), 150, 30, lambda: Dijkstra(graphWithCost(linesList, circlesList), 0, len(circlesList) - 1)),
    Button("GBFS", pygame.Vector2(700, 20), 150, 30, lambda: Greedy_Best_First(graphWithNoCost(linesList, circlesList), getHue(circlesList), 0, len(circlesList) - 1)),
    Button("Backward BFS", pygame.Vector2(870, 20), 150, 30, lambda: backward_BFS(graphWithNoCost(linesList, circlesList), 0, len(circlesList) - 1))
]

drag = False
dragCircleIndex = 0
selected = False
selectedCircleIndex = 0
lineSelected = False
selectedLineIndex = 0

graph: dict[str, list[str]] = {"1": []}

def animate(entire_path: list[list[int]]):
    global running
    for i, path in enumerate(entire_path):
        for j, node in enumerate(path):
            circlesList[node].setSelected(True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not running:
            break

        screen.fill((18, 18, 18))
        for line in linesList:
            pygame.draw.line(screen, *line.drawLine())
            screen.blit(*line.drawText())
        for circle in reversed(circlesList):
            pygame.draw.circle(screen, *circle.drawCircle())
            screen.blit(*circle.drawText())
        for button in algoButtonList:
            pygame.draw.rect(screen, *button.drawRect())
            screen.blit(*button.drawText())
        pygame.display.flip()
        for j, node in enumerate(path):
            circlesList[node].setSelected(False)
        sleep(1)

rightMouseClickOnce = False
mousePosLastFrame = pygame.mouse.get_pos()
while running:
    mousePos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not drag:
            leftClick = event.dict['button'] == 1
            if leftClick:
                for i, button in enumerate(algoButtonList):
                    if not button.isColliding(pygame.mouse.get_pos()):
                        continue
                    entire_path = button.action()
                    print(entire_path)
                    animate(entire_path)
                    break

        if event.type == pygame.KEYDOWN:
            unicode = event.dict['unicode']
            if unicode == ' ':
                circlesList.append(Circle(radius=radius, screen=screen, name=str(len(circlesList) + 1)))
                graph[circlesList[-1].name] = []
            if unicode >= '0' and unicode <= '9' and lineSelected:
                cost = linesList[selectedLineIndex].getCost()
                if cost == "0":
                    cost = unicode
                else:
                    cost += unicode
                linesList[selectedLineIndex].setCost(cost)
            if unicode == '.' and lineSelected:
                cost = linesList[selectedLineIndex].getCost()
                if not unicode in cost:
                    cost += unicode
                linesList[selectedLineIndex].setCost(cost)
            if event.dict['key'] == pygame.K_BACKSPACE and lineSelected:
                cost = linesList[selectedLineIndex].getCost()
                if len(cost) != 0:
                    cost = cost[0: -1]
                    linesList[selectedLineIndex].setCost(cost)
            if event.dict['key'] == pygame.K_RETURN and lineSelected:
                cost = linesList[selectedLineIndex].getCost()
                if len(cost) == 0 or cost == ".":
                    linesList[selectedLineIndex].setCost("0")
                lineSelected = False
                linesList[selectedLineIndex].setSelected(False)
                selectedLineIndex = 0

    if pygame.mouse.get_pressed()[0]:
        if not drag:
            for i, circle in enumerate(circlesList):
                if circle.circleCollision(mousePos):
                    drag = True
                    dragCircleIndex = i
                    break

            for i, line in enumerate(linesList):
                if line.checkCollision(mousePos):
                    if lineSelected:
                        if selectedLineIndex == i:
                            break
                    else:
                        line.setSelected(True)
                        lineSelected = True
                        selectedLineIndex = i
                        break
            else:
                if lineSelected:
                    cost = linesList[selectedLineIndex].getCost()
                    if len(cost) == 0 or cost == ".":
                        linesList[selectedLineIndex].setCost("0")
                    lineSelected = False
                    linesList[selectedLineIndex].setSelected(False)
                    selectedLineIndex = 0
    else:
        drag = False
        dragCircleIndex = 0

    if pygame.mouse.get_pressed()[2] and not rightMouseClickOnce:
        rightMouseClickOnce = True
        for i, circle in enumerate(circlesList):
            if circle.circleCollision(mousePos):
                if not selected:
                    selected = True
                    selectedCircleIndex = i
                    circle.setSelected(True)
                    break
                else:
                    if i == selectedCircleIndex:
                        break
                    else:
                        if not circlesList[i].name in graph[circlesList[selectedCircleIndex].name]:
                            linesList.append(Line([circlesList[selectedCircleIndex], circlesList[i]]))
                            graph[circlesList[selectedCircleIndex].name].append(circlesList[i].name)
                            graph[circlesList[i].name].append(circlesList[selectedCircleIndex].name)
                        circlesList[selectedCircleIndex].setSelected(False)
                        selectedCircleIndex = 0
                        selected = False
                        break
        else:
            if selected:
                circlesList[selectedCircleIndex].setSelected(False)
            selected = False
            selectedCircleIndex = 0
    elif not pygame.mouse.get_pressed()[2]:
        rightMouseClickOnce = False
                
    if drag:
        if mousePos[1] > 100:
            yDiff = mousePos[1] - mousePosLastFrame[1]
        else:
            yDiff = 0
        xDiff = mousePos[0] - mousePosLastFrame[0]
        circlesList[dragCircleIndex].addPosition(xDiff, yDiff)

    screen.fill((18, 18, 18))
    for line in linesList:
        pygame.draw.line(screen, *line.drawLine())
        screen.blit(*line.drawText())
    for circle in reversed(circlesList):
        pygame.draw.circle(screen, *circle.drawCircle())
        screen.blit(*circle.drawText())
    for button in algoButtonList:
        pygame.draw.rect(screen, *button.drawRect())
        screen.blit(*button.drawText())
    pygame.display.flip()
    
    dt = clock.tick(60) / 1000
    mousePosLastFrame = mousePos

pygame.quit()