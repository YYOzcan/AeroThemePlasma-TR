"""Minimal PO okuma/yazma (polib yok)."""
import re

def _unq(s):
    s = s.strip()
    assert s.startswith('"') and s.endswith('"'), s
    return bytes(s[1:-1], 'utf-8').decode('unicode_escape').encode('latin-1').decode('utf-8')

def _q(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t') + '"'

def oku(yol):
    girdiler = []
    cur = None; alan = None
    def bitir():
        nonlocal cur
        if cur and ('msgid' in cur):
            girdiler.append(cur)
        cur = None
    for satir in open(yol, encoding='utf-8'):
        satir = satir.rstrip('\n')
        if not satir.strip():
            bitir(); continue
        if cur is None:
            cur = {'yorum': [], 'msgctxt': None, 'msgid_plural': None, 'msgstr': {}}
        if satir.startswith('#'):
            if satir.startswith('#~'): continue
            cur['yorum'].append(satir); continue
        m = re.match(r'^(msgctxt|msgid_plural|msgid|msgstr(?:\[(\d+)\])?)\s+(".*")$', satir)
        if m:
            k = m.group(1); deger = _unq(m.group(3))
            if k.startswith('msgstr'):
                idx = int(m.group(2)) if m.group(2) else 0
                cur['msgstr'][idx] = deger; alan = ('msgstr', idx)
            else:
                cur[k] = deger; alan = (k, None)
        elif satir.startswith('"'):
            d = _unq(satir)
            if alan[0] == 'msgstr': cur['msgstr'][alan[1]] += d
            else: cur[alan[0]] += d
    bitir()
    return girdiler

def yaz(yol, girdiler, baslik):
    with open(yol, 'w', encoding='utf-8') as f:
        f.write('msgid ""\nmsgstr ""\n')
        for k, v in baslik.items():
            f.write(_q(f'{k}: {v}\n') + '\n')
        f.write('\n')
        for g in girdiler:
            if g['msgid'] == '': continue
            for y in g.get('yorum', []):
                if y.startswith('#:') or y.startswith('#,') or y.startswith('#.'):
                    f.write(y + '\n')
            if g.get('msgctxt') is not None: f.write('msgctxt ' + _q(g['msgctxt']) + '\n')
            f.write('msgid ' + _q(g['msgid']) + '\n')
            if g.get('msgid_plural') is not None:
                f.write('msgid_plural ' + _q(g['msgid_plural']) + '\n')
                for i in sorted(g['msgstr']) or [0, 1]:
                    f.write(f'msgstr[{i}] ' + _q(g['msgstr'].get(i, '')) + '\n')
            else:
                f.write('msgstr ' + _q(g['msgstr'].get(0, '')) + '\n')
            f.write('\n')
