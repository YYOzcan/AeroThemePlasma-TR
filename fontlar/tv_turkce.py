#!/usr/bin/env python3
"""TerminalVector'a Türkçe ğ Ğ İ ekle, bozuk ı'yı düzelt (8x12 piksel ızgara, 128 birim/piksel)."""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
PX = 128
GLIFLER = {
    # ad: (unicode, {satır_alt_y: desen})
    'Gbreve': (0x011E, ['1152 .#...#..', '1024 ..###...', '896 ..####..', '768 .##..##.', '640 ##...##.',
                        '512 ##......', '384 ##..###.', '256 ##...##.', '128 .##..##.', '0 ..#####.']),
    'gbreve': (0x011F, ['1024 .#...#..', '896 ..###...', '640 .###.##.', '512 ##..##..', '384 ##..##..',
                        '256 ##..##..', '128 .#####..', '0 ....##..', '-128 ##..##..', '-256 .####...']),
    'Idotaccent': (0x0130, ['1152 ..##....', '896 .####...', '768 ..##....', '640 ..##....', '512 ..##....',
                            '384 ..##....', '256 ..##....', '128 ..##....', '0 .####...']),
    'dotlessi': (0x0131, ['640 .####...', '512 ...##...', '384 ...##...', '256 ...##...', '128 ...##...', '0 .######.']),
}

def ciz(desen):
    pen = TTGlyphPen(None)
    for satir in desen:
        y, bit = satir.split()
        y = int(y); x = 0
        while x < len(bit):
            if bit[x] == '#':
                b = x
                while x < len(bit) and bit[x] == '#': x += 1
                x0, x1, y0, y1 = b * PX, x * PX, y, y + PX
                pen.moveTo((x0, y0)); pen.lineTo((x0, y1)); pen.lineTo((x1, y1)); pen.lineTo((x1, y0)); pen.closePath()
            else:
                x += 1
    return pen.glyph()

f = TTFont(sys.argv[1])
order = f.getGlyphOrder()
for ad, (cp, desen) in GLIFLER.items():
    g = ciz(desen)
    if ad not in order:
        order.append(ad)
    f['glyf'][ad] = g
    g.recalcBounds(f['glyf'])
    f['hmtx'][ad] = (1024, g.xMin)
    for t in f['cmap'].tables:
        if t.isUnicode():
            t.cmap[cp] = ad
f.setGlyphOrder(order)
f['maxp'].numGlyphs = len(order)
if f['post'].formatType == 2.0:
    f['post'].extraNames = []; f['post'].mapping = {}
# Gömülü 12ppem bitmap katmanı eski/bozuk ı içeriyor ve yeni glifleri kapsamıyor; anahatlar zaten piksel ızgarasında
for t in ('EBDT', 'EBLC'):
    if t in f: del f[t]
f.save(sys.argv[2])
print('yazıldı', sys.argv[2])
