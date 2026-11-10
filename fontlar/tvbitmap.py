from fontTools.ttLib import TTFont
from fontTools.pens.pointInsidePen import PointInsidePen
PX = 128
YS = list(range(1408, -512, -PX))  # satır alt kenarları (üstten alta)
def bitmap(f, ad):
    gs = f.getGlyphSet()
    satirlar = []
    for y in YS:
        r = ''
        for x in range(0, 1024, PX):
            pen = PointInsidePen(gs, (x + PX/2, y + PX/2))
            gs[ad].draw(pen)
            r += '#' if pen.getResult() else '.'
        satirlar.append(r)
    return satirlar
