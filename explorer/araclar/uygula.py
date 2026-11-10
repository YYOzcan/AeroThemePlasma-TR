#!/usr/bin/env python3
"""linux-explorer kaynağına Türkçe çeviriyi uygular (yerinde dize değiştirme).

Kullanım: uygula.py <kaynak_dizini> [--rapor]
  - ceviri*.py sözlüklerindeki metinleri C++ dize sabitlerinde Türkçesiyle değiştirir.
  - '/' ile birleşik kategori yollarını parça parça çevirir (sayfa anahtarları tutarlı kalsın).
  - HARIC içindeki (dosya, metin) çiftlerine dokunmaz (komut çıktısı ayrıştırma, yapılandırma anahtarı...).
  - main.cpp'ye Qt'nin Türkçe kataloğunu (qtbase_tr) yükleyen kod ekler.
  - .desktop dosyalarına Türkçe ad/açıklama ekler.
"""
import os, re, sys, json, glob
sys.path.insert(0, os.path.dirname(__file__))
from metin import gruplar, kacis
import ceviri1, ceviri2, ceviri3, ceviri4, haric

T = {}
for m in (ceviri1, ceviri2, ceviri3, ceviri4):
    T.update(m.T)

RISK = re.compile(r'(==|!=)\s*(u|QStringLiteral\(|QLatin1String\()?\s*$|(startsWith|endsWith|contains|indexOf|value|readEntry|'
                  r'FieldFrom|insert|remove|setValue|writeEntry)\([^()]*$|\bcase\s+$')


def ceviri_bul(metin):
    if metin in T:
        return T[metin]
    if '/' in metin and ' ' in metin and not metin.startswith('/') and '://' not in metin:
        parcalar = metin.split('/')
        if any(p in T for p in parcalar) and all(p and not p.startswith(' ') for p in parcalar):
            return '/'.join(T.get(p, p) for p in parcalar)
    return None


def dosya_uygula(yol, kok, rapor):
    kaynak = open(yol, encoding='utf-8').read()
    goreli = os.path.relpath(yol, kok)
    duzen = []  # (bas, son, yeni)
    for g in gruplar(kaynak):
        if g['ham']:
            continue
        tr = ceviri_bul(g['metin'])
        if tr is None or tr == g['metin']:
            continue
        if (os.path.basename(yol), g['metin']) in haric.HARIC or (goreli, g['satir']) in haric.HARIC_SATIR:
            rapor['haric'].append(f'{goreli}:{g["satir"]}: {g["metin"]!r}')
            continue
        bas, son = g['bas'], g['son']
        yeni = g['onek'] + '"' + kacis(tr) + '"'
        once = kaynak[max(0, bas - 40):bas]
        m = re.search(r'(QLatin1String(?:View)?|QLatin1StringView)\(\s*$', once)
        if g['sonek'] == '_L1':
            yeni = 'QString::fromUtf8(' + yeni + ')'
            son += 3
        elif m:
            bas = bas - (len(once) - m.start())
            yeni = 'QString::fromUtf8(' + yeni
        if RISK.search(once):
            rapor['risk'].append(f'{goreli}:{g["satir"]}: {g["metin"]!r}  ⟵ …{once[-35:]!r}')
        duzen.append((bas, son, yeni))
        rapor['sayi'] += 1
    for bas, son, yeni in sorted(duzen, reverse=True):
        kaynak = kaynak[:bas] + yeni + kaynak[son:]
    if duzen:
        open(yol, 'w', encoding='utf-8').write(kaynak)


QT_CEVIRMEN = '''
    // Türkçe: Qt'nin standart iletişim kutuları ve düğmeleri için qtbase çevirisi
    {
        auto *qtCevirmen = new QTranslator(&app);
        if (qtCevirmen->load(QLocale::system(), QStringLiteral("qtbase"), QStringLiteral("_"),
                             QLibraryInfo::path(QLibraryInfo::TranslationsPath)))
            QCoreApplication::installTranslator(qtCevirmen);
    }
'''


def main_cpp(kok):
    p = kok + '/src/main.cpp'
    s = open(p, encoding='utf-8').read()
    if 'qtCevirmen' in s:
        return
    m = re.search(r'\n(\s*)(QApplication|KAboutData|QGuiApplication)\s+app\s*\([^;]*;\n', s) or \
        re.search(r'\n\s*QApplication\s+\w+\s*\([^;]*;\n', s)
    if not m:
        raise SystemExit('main.cpp: QApplication bulunamadı')
    s = s[:m.end()] + QT_CEVIRMEN + s[m.end():]
    s = '#include <QTranslator>\n#include <QLibraryInfo>\n#include <QLocale>\n' + s
    open(p, 'w', encoding='utf-8').write(s)


DESKTOP = {
    'linux-explorer.desktop': {'Name[tr]': 'Windows Gezgini', 'GenericName[tr]': 'Dosya Yöneticisi',
                               'Comment[tr]': 'Dosya ve klasörlere göz atın'},
    'linux-controlpanel.desktop': {'Name[tr]': 'Denetim Masası', 'Comment[tr]': 'Bilgisayarınızın ayarlarını yapın'},
}
EK = {'linux-explorer.desktop': {'X-KDE-Shortcuts': 'Meta+E'}}
EYLEM = {'Open New Window': 'Yeni Pencere Aç', 'Open Home Folder': 'Kişisel Klasörü Aç'}


def desktop(kok):
    for ad, anahtarlar in DESKTOP.items():
        p = f'{kok}/{ad}'
        if not os.path.exists(p):
            continue
        satirlar = open(p, encoding='utf-8').read().split('\n')
        out, bolum = [], None
        for s in satirlar:
            if s.startswith('['):
                bolum = s.strip()
            if re.match(r'^(Name|GenericName|Comment)\[tr\]=', s):
                continue
            out.append(s)
            if bolum == '[Desktop Entry]':
                k = s.split('=', 1)[0]
                if f'{k}[tr]' in anahtarlar:
                    out.append(f'{k}[tr]={anahtarlar[k + "[tr]"]}')
            elif bolum and bolum.startswith('[Desktop Action') and s.startswith('Name='):
                tr = EYLEM.get(s[5:])
                if tr:
                    out.append(f'Name[tr]={tr}')
        # Ek anahtarlar: [Desktop Entry] bölümünün sonuna (yoksa)
        for k, v in EK.get(ad, {}).items():
            if not any(x.startswith(k + '=') for x in out):
                i = next((n for n, x in enumerate(out) if x.startswith('[Desktop Action')), len(out))
                while i > 0 and (out[i - 1].strip() == '' or out[i - 1].startswith('#')):
                    i -= 1
                out.insert(i, f'{k}={v}')
        open(p, 'w', encoding='utf-8').write('\n'.join(out))


# Türkçe söz dizimi için küçük kod düzeltmeleri (eşleşmezse atlanır)
OZEL = [
    ('src/ui/control/pages/ProgramsFeaturesPage.cpp', 'action + " complete"',
     '(reinstall ? QStringLiteral("Onarma tamamlandı") : QStringLiteral("Kaldırma tamamlandı"))'),
]


def ozel(kok):
    for dosya, eski, yeni in OZEL:
        p = f'{kok}/{dosya}'
        if os.path.exists(p):
            s = open(p, encoding='utf-8').read()
            if eski in s:
                open(p, 'w', encoding='utf-8').write(s.replace(eski, yeni))
            else:
                print(f'UYARI: özel düzeltme atlandı: {dosya}: {eski}')


def main():
    kok = os.path.abspath(sys.argv[1])
    rapor = {'sayi': 0, 'risk': [], 'haric': []}
    for yol in sorted(glob.glob(kok + '/src/**/*.cpp', recursive=True) + glob.glob(kok + '/src/**/*.h', recursive=True)):
        dosya_uygula(yol, kok, rapor)
    ozel(kok)
    main_cpp(kok)
    desktop(kok)
    print(f'Türkçe: {rapor["sayi"]} dize değiştirildi, {len(rapor["haric"])} bilerek atlandı.')
    if '--rapor' in sys.argv:
        json.dump(rapor, open(os.path.join(os.path.dirname(__file__), '..', 'rapor.json'), 'w'), ensure_ascii=False, indent=1)
        print(f'Risk (karşılaştırma/anahtar bağlamı): {len(rapor["risk"])}')
        for r in rapor['risk']:
            print('  RISK', r)


main()
