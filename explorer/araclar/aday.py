#!/usr/bin/env python3
"""Çevrilecek aday metinleri listele (teknik olanları ele). Çıktı: aday.json + okunabilir liste."""
import os, re, sys, json, collections
sys.path.insert(0, os.path.dirname(__file__))
from metin import gruplar
KOK = sys.argv[1]

def teknik(t, g):
    if g['ham'] or not re.search(r'[A-Za-z]{2}', t): return True
    if g['sonek'] in ('_L1',) and ' ' not in t: return True
    s = t.strip()
    if re.search(r'[{};]|qlineargradient|rgba?\(|px\b|:hover|::|stop:\d', s) and not re.search(r'[a-z]{3,} [a-z]{3,} [a-z]{3,}', s): return True
    if re.fullmatch(r'[a-z0-9_.\-/+:*%@=]+', s): return True              # anahtar, simge adı, yol, mime
    if re.fullmatch(r'[A-Za-z0-9_]+(\.[A-Za-z0-9_]+)+', s): return True   # org.kde.x
    if re.fullmatch(r'[A-Z][A-Za-z0-9]+[A-Z][A-Za-z0-9]*', s) and ' ' not in s: return True  # CamelCaseAnahtar
    if re.fullmatch(r'[A-Z0-9_]+', s): return True                         # SABIT, ENV
    if re.fullmatch(r'[A-Z][A-Za-z_\-]*(/[A-Za-z0-9_+\-]+)+', s): return True   # Europe/Berlin, General/LogoPath
    if re.fullmatch(r'[A-Za-z0-9_./ ()\-]+\.(h|cpp|png|svg|ogg|wav|conf|desktop|json|ini)', s): return True
    if re.fullmatch(r'[A-Za-z]+/', s): return True                           # ayar grubu
    if s.startswith(('[Desktop Entry]', 'Type=', 'Name=', 'Hidden=', 'X-')): return True
    if re.fullmatch(r'[a-z]+[A-Z][A-Za-z]*', s): return True               # camelCase anahtar
    if s.startswith('\\b') or s.startswith('^') or '(?' in s: return True    # düzenli ifade
    if s.startswith(('/', '--', 'file:', 'http', 'org.', 'application/', 'inode/', 'x-', '*.', '#', '<?xml', 'Exec=', 'Icon=')) and ' ' not in s: return True
    if re.match(r'^(sh|bash|pkexec|systemctl|ufw|pacman|yay|paru|flatpak|kioclient|xdg-|gsettings|kwriteconfig|qdbus|lpstat|lpadmin|nmcli|localectl|timedatectl|hostnamectl|ip |lsblk|udisksctl)\b', s): return True
    return False

adaylar = collections.OrderedDict()
for kok, _, fs in os.walk(KOK + '/src'):
    for f in sorted(fs):
        if not f.endswith(('.cpp', '.h')): continue
        p = os.path.join(kok, f)
        for g in gruplar(open(p, encoding='utf-8').read()):
            t = g['metin']
            if teknik(t, g): continue
            a = adaylar.setdefault(t, {'metin': t, 'konum': [], 'baglam': (g['once'][-45:] + '⟦' + t[:30] + '⟧' + g['sonra'][:20]).replace('\n', '⏎')})
            a['konum'].append(f'{os.path.relpath(p, KOK)}:{g["satir"]}')
json.dump(list(adaylar.values()), open(os.path.join(os.path.dirname(__file__), '..', 'aday.json'), 'w'), ensure_ascii=False, indent=0)
print(len(adaylar))
