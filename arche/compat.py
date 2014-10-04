
import logging
log = logging.getLogger("R.Compat")

try:
    from pygame import freetype
except:
    from pygame import font as pyfont
    pyfont.init()

def freetypeFont(font, size):
    try:
        return freetype.Font(font, ptsize = size)
    except(TypeError):
        pass
    except(NameError):
        return pyfont.Font(font, size)
    try:
        return freetype.Font(font, size = size)
    except(TypeError):
        pass

def freetypeRender(freetypeFont, value, color, rotation=0, size=0):
    try:
        return freetypeFont.render(
            text = value, fgcolor = color, bgcolor = None,
            rotation = rotation, size = size)
    except(Exception) as e:
        log.debug("layer 1 compat on freetypeRender: " + e.message)
    try:
        return freetypeFont.render(value, color, None, rotation, ptsize = size)
    except(Exception) as e:
        log.debug("layer 2 compat on freetypeRender: " + e.message)
    try:
        surface = freetypeFont.render(value, True, (255,255,255))
        return surface, surface.get_rect()
    except(Exception) as e:
        log.debug("layer 3 compat on font render: " + e.message)
