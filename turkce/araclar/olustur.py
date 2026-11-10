#!/usr/bin/env python3
"""pot/*.json + ceviriler.py -> po/<alan>.po ve mo/<alan>.mo"""
import os, sys, json, glob, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import pofmt, ceviriler
K = os.path.expanduser('~/AeroKurulum/turkce')
os.makedirs(K + '/po', exist_ok=True); os.makedirs(K + '/mo', exist_ok=True)
BASLIK = {'Project-Id-Version': 'aerothemeplasma-tr', 'PO-Revision-Date': '2026-11-07 01:00+0300',
          'Last-Translator': 'Yerel kurulum', 'Language': 'tr', 'MIME-Version': '1.0',
          'Content-Type': 'text/plain; charset=UTF-8', 'Content-Transfer-Encoding': '8bit',
          'Plural-Forms': 'nplurals=2; plural=(n > 1);'}

def bul(sozluk, x):
    for k in ((x['msgctxt'], x['msgid']), x['msgid']):
        if k in sozluk: return sozluk[k]
    return None

toplam_eksik = 0
for f in sorted(glob.glob(K + '/pot/*.json')):
    alan = os.path.basename(f)[:-5]
    g = json.load(open(f))
    eksik = []
    for x in g:
        x['msgstr'] = {int(k): v for k, v in x['msgstr'].items()}
        for sozluk in (ceviriler.GENEL, ceviriler.ALAN.get(alan, {})):
            v = bul(sozluk, x)
            if v is None: continue
            if x['msgid_plural']:
                x['msgstr'] = {0: v[0], 1: v[1]} if isinstance(v, tuple) else {0: v, 1: v}
            else:
                x['msgstr'] = {0: v[0] if isinstance(v, tuple) else v}
        if not x['msgstr'].get(0): eksik.append(x)
    po = f'{K}/po/{alan}.po'
    pofmt.yaz(po, g, BASLIK)
    r = subprocess.run(['msgfmt', '--check', '-o', f'{K}/mo/{alan}.mo', po], capture_output=True, text=True)
    durum = 'OK' if r.returncode == 0 else 'MSGFMT HATASI:\n' + r.stderr
    print(f'{len(g):4d} metin, eksik {len(eksik):3d}  {alan}  {durum}')
    for x in eksik: print('      EKSİK:', repr(x['msgctxt']), repr(x['msgid']))
    toplam_eksik += len(eksik)
print('Toplam eksik:', toplam_eksik)
