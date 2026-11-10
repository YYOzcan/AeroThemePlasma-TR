#!/usr/bin/env python3
"""Yamalı ATP kaynaklarından alan başına çeviri girdileri çıkar ve KDE Türkçe kataloglarından ön doldur.

Çıktı: turkce/pot/<alan>.json  (her girdi: msgctxt, msgid, msgid_plural, msgstr, kaynak, yorum)
"""
import os, re, subprocess, sys, glob, gettext, json, tempfile, shutil, xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(__file__))
import pofmt

K = os.path.expanduser('~/AeroKurulum')
T = K + '/turkce/kaynak'
A = T + '/aerothemeplasma/plasma'
P = 'plasma_applet_'
W = 'io.gitgud.wackyideas.'
# alan: (düz i18n çağrılarının tarandığı dizinler, referans KDE katalogları)
ALANLAR = {
    P+W+'battery':            ([A+'/plasmoids/'+W+'battery'], [P+'org.kde.plasma.battery', P+'org.kde.plasma.brightness', 'powerdevil']),
    P+W+'desktopcontainment': ([A+'/plasmoids/'+W+'desktopcontainment', A+'/plasmoids/src/desktopcontainment'], [P+'org.kde.desktopcontainer', P+'org.kde.plasma.folder']),
    P+W+'digitalclocklite':   ([A+'/plasmoids/'+W+'digitalclocklite'], [P+'org.kde.plasma.digitalclock', 'libplasma6', P+'org.kde.plasma.calendar']),
    P+W+'keyboardlayout':     ([A+'/plasmoids/'+W+'keyboardlayout'], [P+'org.kde.plasma.keyboardlayout']),
    P+W+'networkmanagement':  ([A+'/plasmoids/'+W+'networkmanagement'], [P+'org.kde.plasma.networkmanagement', 'plasmanetworkmanagement-libs', 'plasmanetworkmanagement-kcm']),
    P+W+'panel':              ([A+'/plasmoids/'+W+'panel'], [P+'org.kde.panel', 'plasma_shell_org.kde.plasma.desktop']),
    P+W+'SevenStart':         ([A+'/plasmoids/'+W+'SevenStart', A+'/plasmoids/src/sevenstart_src'], [P+'org.kde.plasma.kickoff', P+'org.kde.plasma.kicker', P+'org.kde.plasma.lock_logout']),
    P+W+'seventasks':         ([A+'/plasmoids/'+W+'seventasks', A+'/plasmoids/src/seventasks_src'], [P+'org.kde.plasma.taskmanager', 'libtaskmanager']),
    P+W+'volume':             ([A+'/plasmoids/'+W+'volume', A+'/plasmoids/src/volume_src'], [P+'org.kde.plasma.volume', 'kcm_pulseaudio']),
    P+W+'win7showdesktop':    ([A+'/plasmoids/'+W+'win7showdesktop'], [P+'org.kde.plasma.showdesktop', P+'org.kde.plasma.minimizeall', 'kwin']),
    P+W+'notifications':      ([A+'/plasmoids/src/notifications_src'], [P+'org.kde.plasma.notifications', 'libnotificationmanager']),
    P+W+'systemtray':         ([A+'/plasmoids/src/systemtray_src'], [P+'org.kde.plasma.systemtray']),
    'plasma_shell_'+W+'desktop': ([], ['plasma_shell_org.kde.plasma.desktop', 'plasmashell', 'kscreenlocker_greet', 'plasma_lookandfeel_org.kde.lookandfeel', 'libplasma6', 'plasmashellprivateplugin', 'kcm_lookandfeel']),
    'plasma_lookandfeel_authui7': ([], ['plasma_lookandfeel_org.kde.lookandfeel']),
    'aerothemeplasma-sddm-theme': ([], ['plasma-desktop-sddm-theme', 'plasma_lookandfeel_org.kde.lookandfeel', 'kscreenlocker_greet']),
    'atpootb':                ([A+'/atpootb'], ['kcm_kwin_effects', 'kcm_lookandfeel']),
    'smod_deco':              ([T+'/smod'], ['breeze_kwin_deco', 'kcm_kwindecoration']),
    'kcm_aeroshellsddm':      ([T+'/aeroshell-sddm-kcm'], ['kcm_sddm']),
    'aeroshell-libtaskmanager': ([T+'/aeroshell-workspace/libtaskmanager'], ['libtaskmanager']),
    'aeroshell-kwin-components': ([T+'/aeroshell-kwin-components'], ['kcm_kwin_effects', 'kwin', 'kwin_effects', 'kcm_kwintabbox']),
    'uac-polkit-agent':       ([T+'/uac-polkit-agent'], ['polkit-kde-authentication-agent-1', 'polkit-1']),
}
ANAHTAR = ['-ki18n:1', '-ki18nc:1c,2', '-ki18np:1,2', '-ki18ncp:1c,2,3', '-kki18n:1', '-kki18nc:1c,2',
           '-kki18np:1,2', '-kki18ncp:1c,2,3', '-kxi18n:1', '-kxi18nc:1c,2', '-kxi18np:1,2', '-kxi18ncp:1c,2,3',
           '-kkxi18n:1', '-kkxi18nc:1c,2', '-kI18N_NOOP:1', '-kI18NC_NOOP:1c,2', '-kI18N_NOOP2:1c,2', '-ktr2i18n:1', '-ktr2xi18n:1']
DKEY = re.compile(r'\b(x?i18nd(?:c|p|cp)?)\s*\(\s*"([^"]+)"\s*,')
DSUF = {'I18ND': ':1', 'I18NDC': ':1c,2', 'I18NDP': ':1,2', 'I18NDCP': ':1c,2,3', 'XI18ND': ':1', 'XI18NDC': ':1c,2', 'XI18NDP': ':1,2', 'XI18NDCP': ':1c,2,3'}
ATLA = ('/autotests', '/tests', '/build', '/.git', '/examples')


def dosyalar(dizinler, uzanti=('.qml', '.js', '.cpp', '.h', '.mjs')):
    out = []
    for d in dizinler:
        for kok, _, fs in os.walk(d):
            if any(x in kok for x in ATLA):
                continue
            out += [os.path.join(kok, f) for f in fs if f.endswith(uzanti)]
    return sorted(out)


def ui_metinleri(dizinler):
    sonuc = []
    for f in dosyalar(dizinler, ('.ui',)):
        for prop in ET.parse(f).iter('property'):
            for el in prop.iter('string'):
                if el.get('notr') == 'true' or not (el.text or '').strip():
                    continue
                sonuc.append({'msgctxt': el.get('comment'), 'msgid': el.text, 'msgid_plural': None, 'msgstr': {},
                              'yorum': ['#: ' + os.path.relpath(f, T)]})
    return sonuc


def xgettext(liste, anahtarlar, dil='C++'):
    if not liste:
        return []
    fd, o = tempfile.mkstemp(suffix='.pot'); os.close(fd); os.remove(o)
    subprocess.run(['xgettext', '--from-code=UTF-8', '-L', dil, '--no-wrap', '-c', '-k', '-o', o] + anahtarlar + liste,
                   check=True, stderr=subprocess.DEVNULL)
    if not os.path.exists(o):
        return []
    g = pofmt.oku(o); os.remove(o)
    return [x for x in g if x['msgid']]


def isaretle(tum):
    """i18nd çağrılarını alan-indeksli işaretçilere çevirip geçici kopyalara yaz."""
    tmp = tempfile.mkdtemp()
    alanlar, kopyalar = {}, {}
    for yol in tum:
        s = open(yol, encoding='utf-8', errors='ignore').read()
        if not DKEY.search(s):
            continue
        def rep(m):
            i = alanlar.setdefault(m.group(2), len(alanlar))
            return f'{m.group(1).upper()}_{i}('
        hedef = os.path.join(tmp, os.path.relpath(yol, T).replace('/', '__'))
        open(hedef, 'w').write(DKEY.sub(rep, s))
        kopyalar[hedef] = yol
    return tmp, alanlar, kopyalar


def katalog(alan):
    yol = alan[1:] if alan.startswith('@') else f'/usr/share/locale/tr/LC_MESSAGES/{alan}.mo'
    if not os.path.exists(yol):
        return {}
    return gettext.GNUTranslations(open(yol, 'rb'))._catalog


def baglamsiz(kat):
    """Bağlamı atılmış anahtar -> çeviri (ilk görülen)."""
    out = {}
    for k, v in kat.items():
        if not v:
            continue
        if isinstance(k, tuple):
            ks, i = k
            out.setdefault((ks.split('\x04')[-1], i), v)
        else:
            out.setdefault(k.split('\x04')[-1], v)
    return out


def dene(g, kat, ctx=True):
    k = ((g['msgctxt'] + '\x04') if (g['msgctxt'] and ctx) else '') + g['msgid']
    if g['msgid_plural']:
        if kat.get((k, 0)):
            g['msgstr'] = {0: kat[(k, 0)], 1: kat.get((k, 1)) or kat[(k, 0)]}
            return True
        return False
    if kat.get(k):
        g['msgstr'] = {0: kat[k]}
        return True
    return False


def main():
    tum = dosyalar([T])
    tmp, dalanlar, kopyalar = isaretle(tum)
    isaretli = sorted(kopyalar)
    kuresel = {}
    for mo in glob.glob('/usr/share/locale/tr/LC_MESSAGES/*.mo'):
        try:
            for k, v in gettext.GNUTranslations(open(mo, 'rb'))._catalog.items():
                if k and v:
                    kuresel.setdefault(k, v)
        except Exception:
            pass
    kuresel_bs = baglamsiz(kuresel)
    for alan, (dizinler, refler) in ALANLAR.items():
        fl = dosyalar(dizinler)
        g = xgettext([f for f in fl if not f.endswith(('.js', '.mjs'))], ANAHTAR)
        g += xgettext([f for f in fl if f.endswith(('.js', '.mjs'))], ANAHTAR, 'JavaScript')
        g += ui_metinleri(dizinler)
        if alan in dalanlar:
            i = dalanlar[alan]
            g += xgettext(isaretli, [f'-k{fn}_{i}{suf}' for fn, suf in DSUF.items()])
        tekil = {}
        for x in g:
            x['yorum'] = [y.replace('__', '/').replace(tmp + '/', '') for y in x.get('yorum', [])]
            tekil.setdefault((x['msgctxt'], x['msgid']), x)
        g = list(tekil.values())
        kats = [katalog(r) for r in refler]
        kats_bs = [baglamsiz(k) for k in kats]
        say = {'ust': 0, 'ust~': 0, 'kuresel': 0, 'kuresel~': 0, 'yok': 0}
        for x in g:
            x['msgstr'] = {}
            if any(dene(x, k) for k in kats):
                x['kaynak'] = 'ust'
            elif any(dene(x, k, ctx=False) for k in kats_bs):
                x['kaynak'] = 'ust~'
            elif dene(x, kuresel):
                x['kaynak'] = 'kuresel'
            elif dene(x, kuresel_bs, ctx=False):
                x['kaynak'] = 'kuresel~'
            else:
                x['kaynak'] = 'yok'
            say[x['kaynak']] += 1
        json.dump(g, open(f'{K}/turkce/pot/{alan}.json', 'w'), ensure_ascii=False, indent=1)
        print(f'{len(g):4d} | ' + ' '.join(f'{k}:{v:3d}' for k, v in say.items()) + f' | {alan}')
    bilinmeyen = set(dalanlar) - set(ALANLAR)
    print('Kapsam dışı i18nd alanları:', sorted(bilinmeyen))
    shutil.rmtree(tmp)


main()
