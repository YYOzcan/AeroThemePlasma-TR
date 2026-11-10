#!/usr/bin/env python3
"""Genel Türkçeleştirici (yerinde dize değiştirme): C++/QML/JS dize sabitleri ve Qt Designer .ui dosyaları.

  cevir.py aday <proje> <kaynak>        çevrilmesi olası metinleri listele (sozluk/<proje>.aday.json)
  cevir.py uygula <proje> <kaynak> [--rapor]   sözlüğü uygula (sozluk/<proje>.py: T, HARIC_SATIR, DESKTOP, METADATA, OZEL)
  cevir.py eksik <proje> <kaynak>       sözlükte olmayan ve bilinen-teknik listesinde de olmayan yeni metin sayısı
"""
import glob, html, importlib.util, json, os, re, sys
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
from metin import gruplar

UZANTI = ('.cpp', '.h', '.hpp', '.qml', '.js', '.ui')
ATLA = ('/.git/', '/build/', '/tests/', '/autotests/', '/debian/', '/packaging/', '/docs/')
UI_RE = re.compile(r'(<string(?![^>]*notr="true")(?![^>]*/>)[^>]*>)(.*?)(</string>)', re.S)
RISK = re.compile(r'(==|!=)\s*(QStringLiteral\(|QLatin1String\(|u)?\s*$|(startsWith|endsWith|contains|indexOf|value|readEntry|insert|setValue|'
                  r'writeEntry|section|split)\([^()]*$|\bcase\s+$')


ATLA_DOSYA = []   # sozluk yüklenince doldurulur (fnmatch, kaynak köküne göreli)


def dosyalar(kok):
    import fnmatch
    out = []
    for p in glob.glob(kok + '/**/*', recursive=True):
        goreli = os.path.relpath(p, kok)
        if any(fnmatch.fnmatch(goreli, d) for d in ATLA_DOSYA):
            continue
        if p.endswith(UZANTI) and not any(a in p.replace(kok, '') + '/' for a in ATLA) and os.path.isfile(p):
            out.append(p)
    return sorted(out)


def teknik(t):
    s = t.strip()
    if not re.search(r'[A-Za-z]{2}', s):
        return True
    if re.search(r'[{};]|qlineargradient|rgba?\(|px\b|::|stop:\d|\bimport\b', s) and not re.search(r'[A-Za-z]{3,} [a-z]{2,} [a-z]{3,}', s):
        return True
    if re.fullmatch(r'[a-z0-9_.\-/+:*%@=#~$]+', s): return True
    if re.fullmatch(r'[A-Za-z0-9_]+(\.[A-Za-z0-9_]+)+', s): return True
    if re.fullmatch(r'[A-Z0-9_]+', s): return True
    if re.fullmatch(r'[a-z]+[A-Z][A-Za-z0-9]*', s): return True
    if re.fullmatch(r'[A-Z][a-z]+([A-Z][a-z0-9]*)+', s): return True
    if re.fullmatch(r'[A-Za-z][A-Za-z0-9_\-]*(/[A-Za-z0-9_+.\-]+)+/?', s): return True
    if re.fullmatch(r'[A-Za-z0-9_./ ()\-]+\.(h|cpp|png|svg|ogg|wav|conf|desktop|json|ini|qml|js|ico|bmp|qm)', s): return True
    if s.startswith(('/', '--', 'file:', 'http', 'qrc:', 'org.', 'application/', 'inode/', 'x-', '*.', '#', '<?xml', '[Desktop')): return True
    if s.startswith(('\\b', '^')) or '(?' in s: return True
    return False


# i18nc bağlamı / tr() çevirmen notu: ekranda görünmez, çevrilmemeli
BAGLAM = re.compile(r'(\b(i18nc|i18ncp|kli18nc|kli18ncp|ki18nc|ki18ncp|xi18nc|xi18ncp|I18NC_NOOP)\s*\(\s*$)|'
                    r'(\b(i18ndc|i18ndcp)\s*\(\s*(["\'])(?:[^"\'\\\n]|\\.)*\5\s*,\s*$)|'
                    r'(\b(tr|qsTr|translate)\s*\(\s*(["\'])(?:[^"\'\\\n]|\\.)*\8\s*,\s*$)')


def ui_metinleri(s):
    for m in UI_RE.finditer(s):
        yield m, html.unescape(m.group(2))


CEVIRI_CAGRI = re.compile(r'\b(tr|qsTr|kli18n|kli18nc|kli18np|kli18ncp|I18N_NOOP|I18NC_NOOP|i18n|i18nc|i18np|i18ncp|i18nd|i18ndc|i18ndp|i18ndcp|ki18n|ki18nc|xi18n|xi18nc|translate)\s*\(\s*'
                          r'((["\'])(?:[^"\'\\\n]|\\.)*\3\s*,\s*)*$')


def oto(proje, kok, refler):
    """i18n/tr çağrısı içindeki adayları KDE Türkçe kataloglarından doldur -> sozluk/<proje>.oto.json"""
    import gettext
    def katalog(ad):
        p = f'/usr/share/locale/tr/LC_MESSAGES/{ad}.mo'
        try:
            return gettext.GNUTranslations(open(p, 'rb'))._catalog
        except OSError:
            return {}
    def bagsiz(kat):
        o = {}
        for k, v in kat.items():
            if v and isinstance(k, str):
                o.setdefault(k.split('\x04')[-1], v)
            elif v and isinstance(k, tuple) and k[1] == 0:
                o.setdefault(k[0].split('\x04')[-1], v)
        return o
    kats = [bagsiz(katalog(r)) for r in refler]
    genel = {}
    for mo in glob.glob('/usr/share/locale/tr/LC_MESSAGES/*.mo'):
        try:
            for k, v in bagsiz(gettext.GNUTranslations(open(mo, 'rb'))._catalog).items():
                genel.setdefault(k, v)
        except Exception:
            pass
    cagri_ici = set()
    for p in dosyalar(kok):
        if p.endswith('.ui'):
            continue
        s = open(p, encoding='utf-8', errors='ignore').read()
        for g in gruplar(s, tek=p.endswith(('.qml', '.js'))):
            if CEVIRI_CAGRI.search(s[max(0, g['bas'] - 200):g['bas']]):
                cagri_ici.add(g['metin'])
    out = {}
    for x in aday(proje, kok):
        t = x['metin']
        if t not in cagri_ici:
            continue
        for kat in kats + [genel]:
            if kat.get(t):
                out[t] = kat[t]; break
    json.dump(out, open(os.path.join(D, 'sozluk', proje + '.oto.json'), 'w'), ensure_ascii=False, indent=0)
    return out


class DesenliSozluk(dict):
    """T sözlüğü + DESEN [(regex, yerine)]: sürüm numarası gibi değişen dizeleri de yakalar."""
    desen = ()

    def _bul(self, k):
        if isinstance(k, str):
            for d, y in self.desen:
                if d.fullmatch(k):
                    return d.sub(y, k)
        return None

    def __contains__(self, k):
        return dict.__contains__(self, k) or self._bul(k) is not None

    def __getitem__(self, k):
        if dict.__contains__(self, k):
            return dict.__getitem__(self, k)
        v = self._bul(k)
        if v is None:
            raise KeyError(k)
        return v

    def get(self, k, v=None):
        return self[k] if k in self else v


def sozluk(proje):
    p = os.path.join(D, 'sozluk', proje + '.py')
    spec = importlib.util.spec_from_file_location('sozluk_' + proje.replace('-', '_'), p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    for ad, v in (('T', {}), ('HARIC_SATIR', set()), ('DESKTOP', {}), ('METADATA', {}), ('OZEL', []), ('ATLA', set())):
        if not hasattr(m, ad):
            setattr(m, ad, v)
    ATLA_DOSYA[:] = list(getattr(m, 'ATLA_DOSYA', []))
    otop = os.path.join(D, 'sozluk', proje + '.oto.json')
    if os.path.exists(otop):
        birlesik = {k: v for k, v in json.load(open(otop)).items() if k not in m.ATLA}
        birlesik.update(m.T)
        m.T = birlesik
    t = DesenliSozluk(m.T)
    t.desen = [(re.compile(d, re.S), y) for d, y in getattr(m, 'DESEN', [])]
    m.T = t
    return m


def aday(proje, kok):
    sozluk(proje)
    adaylar = {}
    for p in dosyalar(kok):
        s = open(p, encoding='utf-8', errors='ignore').read()
        goreli = os.path.relpath(p, kok)
        if p.endswith('.ui'):
            liste = [(t, s.count('\n', 0, m.start()) + 1) for m, t in ui_metinleri(s)]
        else:
            liste = [(g['metin'], g['satir']) for g in gruplar(s, tek=p.endswith(('.qml', '.js')))
                     if not g['ham'] and not BAGLAM.search(s[max(0, g['bas'] - 300):g['bas']])]
        for t, satir in liste:
            if teknik(t):
                continue
            adaylar.setdefault(t, []).append(f'{goreli}:{satir}')
    out = [{'metin': t, 'konum': k} for t, k in adaylar.items()]
    json.dump(out, open(os.path.join(D, 'sozluk', proje + '.aday.json'), 'w'), ensure_ascii=False, indent=0)
    return out


def kacis(t, tirnak):
    t = t.replace('\\', '\\\\').replace('\n', '\\n').replace('\t', '\\t')
    return t.replace(tirnak, '\\' + tirnak)


def uygula(proje, kok, rapor_iste=False):
    S = sozluk(proje)
    T = S.T
    say, risk, haric = 0, [], 0
    for p in dosyalar(kok):
        s = open(p, encoding='utf-8', errors='ignore').read()
        goreli = os.path.relpath(p, kok)
        yeni = s
        if p.endswith('.ui'):
            parcalar, son = [], 0
            for m, t in ui_metinleri(s):
                tr = T.get(t)
                satir = s.count('\n', 0, m.start()) + 1
                if tr is None or (goreli, satir) in S.HARIC_SATIR:
                    continue
                parcalar += [s[son:m.start(2)], html.escape(tr, quote=False)]
                son = m.end(2); say += 1
            yeni = ''.join(parcalar) + s[son:]
        else:
            duzen = []
            for g in gruplar(s, tek=p.endswith(('.qml', '.js'))):
                if g['ham'] or g['metin'] not in T:
                    continue
                if BAGLAM.search(s[max(0, g['bas'] - 300):g['bas']]):
                    continue
                if (goreli, g['satir']) in S.HARIC_SATIR:
                    haric += 1; continue
                tr, bas, son = T[g['metin']], g['bas'], g['son']
                once = s[max(0, bas - 40):bas]
                if g['onek'] == "'":
                    lit = "'" + kacis(tr, "'") + "'"
                else:
                    lit = g['onek'] + '"' + kacis(tr, '"') + '"'
                m = re.search(r'(QLatin1String(?:View)?)\(\s*$', once)
                if g['sonek'] == '_L1':
                    lit, son = 'QString::fromUtf8(' + lit + ')', son + 3
                elif m:
                    bas -= len(once) - m.start(); lit = 'QString::fromUtf8(' + lit
                if RISK.search(once):
                    risk.append(f'{goreli}:{g["satir"]}: {g["metin"]!r} ⟵ …{once[-30:]!r}')
                duzen.append((bas, son, lit)); say += 1
            for bas, son, lit in sorted(duzen, reverse=True):
                yeni = yeni[:bas] + lit + yeni[son:]
        if yeni != s:
            open(p, 'w', encoding='utf-8').write(yeni)
    for dosya, eski, yeni in S.OZEL:
        p = os.path.join(kok, dosya)
        icerik = open(p, encoding='utf-8').read() if os.path.exists(p) else ''
        if eski.startswith('re:'):   # düzenli ifade (DOTALL): büyük ham dize blokları için
            desen = re.compile(eski[3:], re.S)
            if desen.search(icerik):
                open(p, 'w', encoding='utf-8').write(desen.sub(lambda _m: yeni, icerik, count=1))
                continue
            print(f'UYARI: özel düzeltme atlandı: {dosya}')
        elif eski in icerik:
            open(p, 'w', encoding='utf-8').write(icerik.replace(eski, yeni))
        else:
            print(f'UYARI: özel düzeltme atlandı: {dosya}')
    # QT_TR = (main.cpp, QApplication satırı): Qt'nin kendi metinleri (Tamam/İptal/Evet/Hayır, dosya
    # iletişim kutuları) için qtbase_tr kataloğunu yükle
    if getattr(S, 'QT_TR', None):
        dosya, capa = S.QT_TR
        p = os.path.join(kok, dosya)
        icerik = open(p, encoding='utf-8').read() if os.path.exists(p) else ''
        if capa in icerik and 'qtbase_tr' not in icerik:
            ek = ('\n    { auto *qtTr = new QTranslator(qApp);'
                  ' if (qtTr->load(QLocale(), QStringLiteral("qtbase"), QStringLiteral("_"),'
                  ' QLibraryInfo::path(QLibraryInfo::TranslationsPath))) qApp->installTranslator(qtTr); } // qtbase_tr')
            icerik = icerik.replace(capa, capa + ek, 1)
            icerik = '#include <QTranslator>\n#include <QLocale>\n#include <QLibraryInfo>\n' + icerik
            open(p, 'w', encoding='utf-8').write(icerik)
        else:
            print(f'UYARI: Qt Türkçe kataloğu eklenemedi: {dosya}')
    # .desktop: Name[tr] / GenericName[tr] / Comment[tr] / Keywords[tr]
    for dosya, anahtarlar in S.DESKTOP.items():
        for p in glob.glob(os.path.join(kok, dosya)):
            satirlar = [x for x in open(p, encoding='utf-8').read().split('\n') if not re.match(r'^(Name|GenericName|Comment|Keywords)\[tr\]=', x)]
            out, bolum = [], None
            for x in satirlar:
                if x.startswith('['):
                    bolum = x.strip()
                out.append(x)
                k = x.split('=', 1)[0]
                if bolum == '[Desktop Entry]' and f'{k}[tr]' in anahtarlar:
                    out.append(f'{k}[tr]={anahtarlar[k + "[tr]"]}')
            open(p, 'w', encoding='utf-8').write('\n'.join(out))
    # Plasma metadata.json: Name[tr] / Description[tr]
    for dosya, (ad, ac) in S.METADATA.items():
        p = os.path.join(kok, dosya)
        if os.path.exists(p):
            d = json.load(open(p, encoding='utf-8'))
            if ad: d.setdefault('KPlugin', {})['Name[tr]'] = ad
            if ac: d.setdefault('KPlugin', {})['Description[tr]'] = ac
            open(p, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=4) + '\n')
    print(f'{proje}: {say} dize Türkçeleştirildi, {haric} bilerek atlandı.')
    if rapor_iste:
        for r in risk:
            print('  RISK', r)


def eksik(proje, kok):
    S = sozluk(proje)
    bilinen_yol = os.path.join(D, 'sozluk', proje + '.bilinen.json')
    bilinen = set(json.load(open(bilinen_yol))) if os.path.exists(bilinen_yol) else set()
    yeni = [x for x in aday(proje, kok) if x['metin'] not in S.T and x['metin'] not in bilinen]
    print(len(yeni))


if __name__ == '__main__':
    komut, proje, kok = sys.argv[1], sys.argv[2], os.path.abspath(sys.argv[3])
    if komut == 'aday':
        print(len(aday(proje, kok)))
    elif komut == 'uygula':
        uygula(proje, kok, '--rapor' in sys.argv)
    elif komut == 'eksik':
        eksik(proje, kok)
    elif komut == 'bilinen':
        # şu anki çevrilmemiş (bilerek İngilizce bırakılan) dizeleri taban çizgisi olarak kaydet
        S = sozluk(proje)
        b = sorted({x['metin'] for x in aday(proje, kok) if x['metin'] not in S.T})
        json.dump(b, open(os.path.join(D, 'sozluk', proje + '.bilinen.json'), 'w'), ensure_ascii=False, indent=0)
        print(len(b))
    elif komut == 'oto':
        print(len(oto(proje, kok, sys.argv[4:])))
    elif komut == 'kalan':
        S = sozluk(proje)
        for x in json.load(open(os.path.join(D, 'sozluk', proje + '.aday.json'))):
            if x['metin'] not in S.T:
                print(x['konum'][0].split('/')[-1].split(':')[0][:26], '|', repr(x['metin'])[:150])
