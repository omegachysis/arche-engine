
from pygame import freetype

def freetypeFont(font, size):
    try:
        return freetype.Font(font, ptsize = size)
    except(TypeError):
        pass
    try:
        return freetype.Font(font, size = size)
    except(TypeError):
        pass

def freetypeRender(freetypeFont, value, color, rotation, size):
    try:
        return freetypeFont.render(value, color, None, rotation, size = size)
    except:
        pass
    try:
        return freetypeFont.render(value, color, None, rotation, ptsize = size)
    except:
        pass
