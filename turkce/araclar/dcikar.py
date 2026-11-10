#!/usr/bin/env python3
"""i18nd*("ALAN", ...) çağrılarını alan bazında çıkar; yabancı (KDE) alanlarda Türkçe karşılığı olmayanları raporla."""
import os, re, sys, subprocess, tempfile, json, shutil
sys.path.insert(0, os.path.dirname(__file__))
import pofmt
from cikar_ortak import *

DKEY = re.compile(r'\b(x?i18nd(?:c|p|cp)?)\s*\(\s*"([^"]+)"\s*,')
SUFFIX = {'i18nd': ':1', 'i18ndc': ':1c,2', 'i18ndp': ':1,2', 'i18ndcp': ':1c,2,3', 'xi18nd': ':1', 'xi18ndc': ':1c,2', 'xi18ndp': ':1,2', 'xi18ndcp': ':1c,2,3'}

def main():
    dizinler = [A, R + '/aeroshell-workspace', R + '/aeroshell-kwin-components', R + '/smod', R + '/aeroshell-sddm-kcm']
    alanlar = {}
    tmp = tempfile.mkdtemp()
    dosyalar = []
    for d in dizinler:
        for kok, _, fs in os.walk(d):
            if any(x in kok for x in ('/autotests', '/tests', '/build', '/.git')): continue
            for f in fs:
                if not f.endswith(('.qml', '.js', '.cpp', '.h')): continue
                yol = os.path.join(kok, f)
                s = open(yol, encoding='utf-8', errors='ignore').read()
                if not DKEY.search(s): continue
                def rep(m):
                    i = alanlar.setdefault(m.group(2), len(alanlar))
                    return f'{m.group(1).upper()}_{i}('
                yeni = DKEY.sub(rep, s)
                hedef = os.path.join(tmp, os.path.relpath(yol, K).replace('/', '__'))
                open(hedef, 'w').write(yeni); dosyalar.append(hedef)
    sonuc = {}
    for alan, i in alanlar.items():
        kw = [f'-k{fn.upper()}_{i}{suf}' for fn, suf in SUFFIX.items()]
        o = os.path.join(tmp, f'out{i}.pot')
        subprocess.run(['xgettext', '--from-code=UTF-8', '-L', 'C++', '--no-wrap', '-k', '-o', o] + kw + dosyalar, check=True, stderr=subprocess.DEVNULL)
        g = pofmt.oku(o) if os.path.exists(o) else []
        g = [x for x in g if x['msgid']]
        for x in g:
            x['yorum'] = [y.replace('__', '/') for y in x['yorum']]
        sonuc[alan] = g
    shutil.rmtree(tmp)
    json.dump(sonuc, open(K + '/turkce/pot/_d_cagrilari.json', 'w'), ensure_ascii=False, indent=1)
    for alan, g in sonuc.items():
        kat = tr_katalog(alan)
        eksik = [x for x in g if not doldur(dict(x, msgstr={}), kat)]
        print(f'{alan}: {len(g)} metin, Türkçe katalogda olmayan: {len(eksik)}')
        for x in eksik: print('    -', repr(x['msgctxt']), repr(x['msgid'][:90]), x['yorum'][-1][:90] if x['yorum'] else '')
main()
