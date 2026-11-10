#!/usr/bin/env python3
"""linux-explorer C++ kaynağındaki dize sabitlerini (yorumları atlayarak) bulur.

Bitişik sabitler ("a" "b") tek mantıksal metin olarak birleştirilir. Her grup için:
  bas, son (dosyadaki karakter aralığı), metin (çözülmüş), onek (u8/u/L/R), sonek (_L1/_s...), once/sonra bağlamı.
"""
import re

KACIS = {'n': '\n', 't': '\t', '"': '"', "'": "'", '\\': '\\', 'r': '\r', '0': '\0', 'a': '\a'}


def coz(govde):
    out, i = [], 0
    while i < len(govde):
        c = govde[i]
        if c == '\\' and i + 1 < len(govde):
            n = govde[i + 1]
            if n in KACIS:
                out.append(KACIS[n]); i += 2; continue
            if n == 'x':
                m = re.match(r'[0-9a-fA-F]+', govde[i + 2:])
                out.append(chr(int(m.group(0), 16))); i += 2 + len(m.group(0)); continue
            if n == 'u':
                out.append(chr(int(govde[i + 2:i + 6], 16))); i += 6; continue
            out.append(n); i += 2; continue
        out.append(c); i += 1
    return ''.join(out)


def kacis(metin):
    return (metin.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            .replace('\t', '\\t').replace('\r', '\\r'))


def sabitler(kaynak, tek=False):
    """(bas, son, govde, onek, ham) listesi; yorumlar ve karakter sabitleri atlanır."""
    i, n, out = 0, len(kaynak), []
    while i < n:
        c = kaynak[i]
        if kaynak.startswith('//', i):
            j = kaynak.find('\n', i); i = n if j < 0 else j; continue
        if kaynak.startswith('/*', i):
            j = kaynak.find('*/', i + 2); i = n if j < 0 else j + 2; continue
        if c == "'" and tek:
            j = i + 1
            while j < n and kaynak[j] != "'" and kaynak[j] != '\n':
                j += 2 if kaynak[j] == '\\' else 1
            out.append((i, j + 1, kaynak[i + 1:j], "'", False))
            i = j + 1; continue
        if c == "'":
            j = i + 1
            while j < n and kaynak[j] != "'":
                j += 2 if kaynak[j] == '\\' else 1
            i = j + 1; continue
        if c == '"':
            # önek: u8, u, U, L, R, u8R ...
            k = i
            while k > 0 and (kaynak[k - 1].isalnum() or kaynak[k - 1] == '_'):
                k -= 1
            onek = kaynak[k:i]
            if not re.fullmatch(r'(u8|u|U|L)?R?', onek):
                onek = ''; k = i
            if onek.endswith('R'):
                m = re.match(r'"([^(\s]*)\(', kaynak[i:])
                ayrac = ')' + m.group(1) + '"'
                j = kaynak.find(ayrac, i)
                out.append((k, j + len(ayrac), kaynak[i + len(m.group(0)):j], onek, True))
                i = j + len(ayrac); continue
            j = i + 1
            while j < n and kaynak[j] != '"':
                j += 2 if kaynak[j] == '\\' else 1
            out.append((k, j + 1, kaynak[i + 1:j], onek, False))
            i = j + 1; continue
        i += 1
    return out


def gruplar(kaynak, tek=False):
    """Bitişik sabitleri (aralarında yalnızca boşluk) mantıksal gruplara birleştir."""
    s = sabitler(kaynak, tek)
    grp, out = [], []
    for t in s:
        if grp and not t[4] and not grp[-1][4] and kaynak[grp[-1][1]:t[0]].strip() == '' and t[3] == grp[-1][3]:
            grp.append(t); continue
        if grp:
            out.append(grp)
        grp = [t]
    if grp:
        out.append(grp)
    sonuc = []
    for g in out:
        bas, son = g[0][0], g[-1][1]
        ham = g[0][4]
        metin = g[0][2] if ham else ''.join(coz(x[2]) for x in g)
        m = re.match(r'(_[A-Za-z0-9]+)', kaynak[son:son + 6])
        sonek = m.group(1) if m else ''
        sonuc.append({'bas': bas, 'son': son, 'metin': metin, 'onek': g[0][3], 'ham': ham, 'sonek': sonek,
                      'once': kaynak[max(0, bas - 60):bas], 'sonra': kaynak[son:son + 40],
                      'satir': kaynak.count('\n', 0, bas) + 1})
    return sonuc
