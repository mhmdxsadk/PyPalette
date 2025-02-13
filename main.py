from random import randint as ri
from threading import Thread
import pyperclip
import requests
import pygame
import sys
import os

def getRandomColor():
    while True:
        r = ri(0, 255)
        g = ri(0, 255)
        b = ri(0, 255)

        if r >= 100 and g >= 100 and b >= 100:
            break

    return r, g, b

def colorToHex(color):
    return "#{:02X}{:02X}{:02X}".format(*color)

def darkenColor(color, factor=0.8):
    return tuple(int(c * factor) for c in color)

def getColorName(hexCode, callback):
    hexCode = hexCode[1:]
    try:
        url = f"https://www.thecolorapi.com/id?hex={hexCode}"
        response = requests.get(url, timeout=5)
        data = response.json()
        colorName = data.get('name', {}).get("value", "Unknown Color")
        colorRgb = data.get('rgb', {}).get("value", "Unknown RGB")
        callback(colorName, colorRgb)
    except requests.exceptions.RequestException:
        colorName = "Unknown Color"

def renderStylizedText(font, text, color, pos, shadowColor=(0, 0, 0)):
    textSurface = font.render(text, True, color)
    shadowSurface = pygame.Surface((textSurface.get_width(), textSurface.get_height()), pygame.SRCALPHA)

    if shadowColor:
        shadowSurface.blit(font.render(text, True, shadowColor), (1, 1))

    shadowSurface.blit(textSurface, (0, 0))
    screen.blit(shadowSurface, pos)

def getColorNameThreaded(hexCode, colIndex):
    def target(colorName, colorRgb):
        colorNames[colIndex] = f"{colorName}"

    thread = Thread(target=getColorName, args=(hexCode, target))
    thread.start()

pygame.init()

width, height = 1280, 720
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF, pygame.SCALED, vsync=True)
pygame.display.set_caption("PyPalette")

columns = 8
columnWidth = (width / columns) 

colors = [getRandomColor() for _ in range(columns)]
colorNames = ["" for _ in range(columns)]

for col in range(columns):
    colorHex = colorToHex(colors[col])
    getColorNameThreaded(colorHex, col)

clock = pygame.time.Clock()
fps = 24

fontSize = 16
font = pygame.font.Font('./assets/fonts/montserrat.ttf', fontSize)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouseX, mouseY = event.pos
                for col in range(columns):
                    columnRect = pygame.Rect(col * columnWidth, 0, columnWidth, height)
                    if columnRect.collidepoint(mouseX, mouseY):
                        colorHex = colorToHex(colors[col])
                        pyperclip.copy(colorHex)
                        getColorNameThreaded(colorHex, col)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                colors = [getRandomColor() for _ in range(columns)]
                colorNames = ["" for _ in range(columns)]
                for col in range(columns):
                    colorHex = colorToHex(colors[col])
                    getColorNameThreaded(colorHex, col)

        elif event.type == pygame.USEREVENT:
            colorName = event.dict.get('colorName', 'Unknown Color')
            colorRgb = event.dict.get('colorRgb', 'Unknown RGB')
            colorNames[event.dict['colIndex']] = f"{colorName} | Hex: {colorHex} | RGB: {colorRgb}"

    screen.fill((255, 255, 255))

    for col in range(columns):
        color = colors[col]
        columnRect = pygame.Rect(col * columnWidth, 0, columnWidth, height)

        if columnRect.collidepoint(pygame.mouse.get_pos()):
            columnSurface = pygame.Surface((columnWidth, height), pygame.SRCALPHA)
            alpha = int(0.8 * 255)
            colorWithAlpha = (*color[:3], alpha)
            columnSurface.fill(colorWithAlpha)
            screen.blit(columnSurface, columnRect.topleft)
        else:
            pygame.draw.rect(screen, color, columnRect)

        textCol = darkenColor(color)
        rgbText = font.render(f"RGB: {color}", True, textCol)
        hexText = font.render(f"Hex: {colorToHex(color)}", True, textCol)
        colorNameText = font.render(f"{colorNames[col]}", True, textCol)

        leftPadding = 3

        screen.blit(rgbText, (col * columnWidth + leftPadding, height - 60))
        screen.blit(hexText, (col * columnWidth + leftPadding, height - 40))
        screen.blit(colorNameText, (col * columnWidth + leftPadding, height - 20))

        textCol = darkenColor(color)
        outlineCol = darkenColor(darkenColor(darkenColor(darkenColor(color))))
        renderStylizedText(font, f"RGB: {color}", textCol, (col * columnWidth + leftPadding, height - 60))
        renderStylizedText(font, f"Hex: {colorToHex(color)}", textCol, (col * columnWidth + leftPadding, height - 40))
        renderStylizedText(font, f"{colorNames[col]}", textCol, (col * columnWidth + leftPadding, height - 20))

    pygame.display.flip()
    clock.tick(fps)
