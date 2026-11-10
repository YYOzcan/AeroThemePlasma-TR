#!/usr/bin/env python3
"""ATP kaynaklarından çeviri alanı başına .pot üret, KDE Türkçe kataloglarından doldur."""
import os, re, subprocess, sys, glob, gettext, json, xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(__file__))
import pofmt

K = os.path.expanduser('~/AeroKurulum')
A = K + '/aerothemeplasma/plasma'
R = K + '/repos'
P = 'plasma_applet_'
W = 'io.gitgud.wackyideas.'

def tr_katalog(alan):
    yol = f'/usr/share/locale/tr/LC_MESSAGES/{alan}.mo'
    if not os.path.exists(yol): return {}
    return gettext.GNUTranslations(open(yol, 'rb'))._catalog

def anahtar(g):
    return (g['msgctxt'] + '\x04' if g['msgctxt'] else '') + g['msgid']

def doldur(g, kat):
    k = anahtar(g)
    if g['msgid_plural']:
        if (k, 0) in kat and kat[(k, 0)]:
            g['msgstr'] = {0: kat[(k, 0)], 1: kat.get((k, 1), kat[(k, 0)])}; return True
    elif k in kat and kat[k]:
        g['msgstr'] = {0: kat[k]}; return True
    return False

KUM = None
def kuresel():
    global KUM
    if KUM is None:
        KUM = {}
        for mo in glob.glob('/usr/share/locale/tr/LC_MESSAGES/*.mo'):
            try:
                for k, v in gettext.GNUTranslations(open(mo, 'rb'))._catalog.items():
                    if k and v: KUM.setdefault(k, v)
            except Exception: pass
    return KUM

