from math import sin, pi

# Code to generate block shadows
def getColorFromNumber(n, numColors):
    red = int(min(max(100 * (sin((n + numColors * (90 / 360)) * pi / 180) + 1), 44), 162))
    green = int(min(max(100 * (sin((n + numColors * (210 / 360)) * pi / 180) + 1), 44), 162))
    blue = int(min(max(100 * (sin((n + numColors * (330 / 360)) * pi / 180) + 1), 44), 162))
    return (red, green, blue)


# Code to generate block colors
def getLightFromNumber(n, numColors):
    red = int(min(max(125 * (sin((n + numColors * (90 / 360)) * pi / 180) + 1), 55), 204))
    green = int(min(max(125 * (sin((n + numColors * (210 / 360)) * pi / 180) + 1), 55), 204))
    blue = int(min(max(125 * (sin((n + numColors * (330 / 360)) * pi / 180) + 1), 55), 204))
    return (red, green, blue)
