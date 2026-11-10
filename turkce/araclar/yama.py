#!/usr/bin/env python3
"""AeroThemePlasma kaynak ağaçlarına Türkçe yerelleştirme yamaları.

Kullanım: yama.py <bilesen> <kaynak_dizini>
bilesen: aerothemeplasma | aeroshell-workspace | aeroshell-kwin-components | smod |
         aeroshell-sddm-kcm | aerothemeplasma-icons | aerothemeplasma-sounds
Betik idempotenttir; aynı ağaca iki kez uygulanabilir.
"""
import json, os, re, sys

KOK = os.path.dirname(os.path.abspath(__file__))
W = 'io.gitgud.wackyideas.'
YABANCI = ('plasma_shell_org.kde.plasma.desktop', 'plasma_lookandfeel_org.kde.lookandfeel', 'kscreenlocker_greet',
           'libplasma5', 'libplasma6', 'plasma_applet_org.kde.plasma.showdesktop', 'kwin_effects',
           'plasma_applet_org.kde.plasma.notifications', 'okular')


def oku(p):
    return open(p, encoding='utf-8').read()


def yaz(p, s):
    open(p, 'w', encoding='utf-8').write(s)


# Otomatik güncellemede (AERO_YAMA_ESNEK=1) üst kaynak değişmişse yama atlanır, derleme durmaz.
ESNEK = os.environ.get('AERO_YAMA_ESNEK') == '1'
UYARILAR = []


def uyar(mesaj):
    UYARILAR.append(mesaj)
    print('UYARI (yama atlandı): ' + mesaj, file=sys.stderr)


def degistir(p, eski, yeni, zorunlu=True):
    if not os.path.exists(p):
        if ESNEK or not zorunlu:
            return uyar(f'dosya yok: {p}')
        raise SystemExit(f'YAMA DOSYASI YOK: {p}')
    s = oku(p)
    if yeni in s and eski not in s:
        return
    if eski not in s:
        if zorunlu and not ESNEK:
            raise SystemExit(f'YAMA BULUNAMADI: {p}: {eski!r}')
        if zorunlu:
            uyar(f'{p}: {eski[:70]!r}')
        return
    yaz(p, s.replace(eski, yeni))


def alan_yonlendir(dizin, hedef, tum_i18n=False):
    """Dizin altındaki QML/JS dosyalarında yabancı KDE alanlarını ve (istenirse) düz i18n çağrılarını hedef alana çevir."""
    yab = re.compile(r'\b(x?i18nd(?:c|p|cp)?)\s*\(\s*"(' + '|'.join(map(re.escape, YABANCI)) + r')"')
    duz = re.compile(r'(?<![\w.])(x?)i18n(c|p|cp)?\s*\(')
    for kok, _, fs in os.walk(dizin):
        for f in fs:
            if not f.endswith(('.qml', '.js')):
                continue
            p = os.path.join(kok, f)
            s = oku(p)
            y = yab.sub(lambda m: f'{m.group(1)}("{hedef}"', s)
            if tum_i18n:
                y = duz.sub(lambda m: f'{m.group(1)}i18nd{m.group(2) or ""}("{hedef}", ', y)
            if y != s:
                yaz(p, y)


def metadata(p, ad=None, aciklama=None):
    if not os.path.exists(p):
        if ESNEK:
            return uyar(f'metadata yok: {p}')
        raise SystemExit(f'METADATA YOK: {p}')
    d = json.loads(oku(p))
    k = d.setdefault('KPlugin', {})
    if ad:
        k['Name[tr]'] = ad
    if aciklama:
        k['Description[tr]'] = aciklama
    yaz(p, json.dumps(d, ensure_ascii=False, indent=4) + '\n')


def ini_anahtar(p, anahtarlar, grup='Desktop Entry'):
    """INI/.desktop dosyasında [grup] içine Anahtar[tr]=değer ekle/değiştir."""
    if not os.path.exists(p):
        if ESNEK:
            return uyar(f'dosya yok: {p}')
        raise SystemExit(f'DOSYA YOK: {p}')
    satirlar = oku(p).split('\n')
    cikti, ici, eklendi = [], False, set()

    def ekle_eksik():
        for k, v in anahtarlar.items():
            if k not in eklendi:
                cikti.append(f'{k}={v}')
                eklendi.add(k)

    for s in satirlar:
        if s.startswith('['):
            if ici:
                ekle_eksik()
            ici = (s.strip() == f'[{grup}]')
        if ici:
            m = re.match(r'^([A-Za-z]+\[tr\])\s*=', s)
            if m and m.group(1) in anahtarlar:
                if m.group(1) not in eklendi:
                    cikti.append(f'{m.group(1)}={anahtarlar[m.group(1)]}')
                    eklendi.add(m.group(1))
                continue
        cikti.append(s)
    if ici:
        while cikti and cikti[-1] == '':
            cikti.pop()
        ekle_eksik()
        cikti.append('')
    yaz(p, '\n'.join(cikti))


def aerothemeplasma(d):
    P = d + '/plasma'
    pl = P + '/plasmoids/'
    # 1) Alan yönlendirme
    alan_yonlendir(P + '/shells/' + W + 'desktop', 'plasma_shell_' + W + 'desktop', tum_i18n=True)
    alan_yonlendir(P + '/sddm/sddm-theme-mod', 'aerothemeplasma-sddm-theme', tum_i18n=True)
    alan_yonlendir(P + '/look-and-feel/authui7', 'plasma_lookandfeel_authui7', tum_i18n=True)
    for ad in ('battery', 'desktopcontainment', 'digitalclocklite', 'keyboardlayout', 'networkmanagement', 'panel',
               'SevenStart', 'seventasks', 'volume', 'win7showdesktop'):
        alan_yonlendir(pl + W + ad, 'plasma_applet_' + W + ad)
    alan_yonlendir(pl + 'src/notifications_src', 'plasma_applet_' + W + 'notifications')
    alan_yonlendir(pl + 'src/systemtray_src', 'plasma_applet_' + W + 'systemtray')

    # 2) Sabit metinler
    ss = pl + W + 'SevenStart/contents/ui/'
    degistir(ss + 'NavGrid.qml', 'text: "No items match your search."', 'text: i18n("No items match your search.")')
    degistir(ss + 'MenuRepresentation.qml', 'text: "    All Programs"', 'text: "    " + i18n("All Programs")')
    degistir(ss + 'MenuRepresentation.qml', 'text: "    Back"', 'text: "    " + i18n("Back")')
    s = oku(ss + 'IconPicker.qml')
    m = re.search(r'text: ("Customize the way the menu orb looks like[^\n]*")', s)
    if m:
        yaz(ss + 'IconPicker.qml', s.replace('text: ' + m.group(1), 'text: i18n(' + m.group(1) + ')'))
    dc = pl + W + 'desktopcontainment/contents/ui/'
    degistir(dc + 'WatermarkConfigure.qml', 'property string text: "New watermark"', 'property string text: i18n("New watermark")')
    nm = pl + W + 'networkmanagement/contents/ui/'
    for metin in ('General', 'Speed', 'Close'):
        degistir(nm + 'DetailsWindow.qml', f'text: "{metin}"', f'text: i18n("{metin}")')
    degistir(nm + 'PopupDialog.qml', 'text: "Back"', 'text: i18n("Back")')
    for metin in ('Graph', 'Status'):
        degistir(nm + 'TrafficMonitor.qml', f'text: "{metin}"', f'text: i18n("{metin}")')
    degistir(nm + 'main.qml', 'Plasmoid.title: "Open Network and Sharing Center"', 'Plasmoid.title: i18n("Open Network and Sharing Center")')
    for metin in ('Sign in required', 'No network access', 'Internet access', 'No Internet access'):
        degistir(nm + 'ConnectionItem.qml', f'return "{metin}";', f'return i18n("{metin}");')
    st = pl + W + 'seventasks/contents/ui/'
    degistir(st + 'TasksMenu.qml', 'text: "Pin program to taskbar"', 'text: i18n("Pin program to taskbar")')
    degistir(st + 'TasksMenu.qml', '? "Close all windows" : "Close window"', '? i18n("Close all windows") : i18n("Close window")')
    degistir(st + 'Task.qml', '? "Close all windows" : "Close window"', '? i18n("Close all windows") : i18n("Close window")')
    vo = pl + W + 'volume/contents/ui/'
    degistir(vo + 'MixerWindow.qml', 'title: "Volume Mixer" +', 'title: i18n("Volume Mixer") +')
    degistir(vo + 'MixerWindow.qml', 'title: "Device"', 'title: i18n("Device")')
    degistir(vo + 'MixerWindow.qml', 'title: "Applications"', 'title: i18n("Applications")')
    degistir(vo + 'main.qml', 'Plasmoid.title: "Mixer"', 'Plasmoid.title: i18n("Mixer")')
    # Qt 6.12: parola alanında placeholderText de maskeleniyor ("Parola" nokta olarak görünüyor).
    # İpucu metnini maskelenmeyen ayrı bir Text katmanıyla çiz.
    def parola_ipucu(dosya, alan, renk):
        eski = f'placeholderText: i18nd("{alan}", "Password")'
        katman = (f'placeholderText: ""\n'
                  f'                        Text {{\n'
                  f'                            anchors.fill: parent\n'
                  f'                            leftPadding: password.leftPadding\n'
                  f'                            rightPadding: password.rightPadding\n'
                  f'                            verticalAlignment: Text.AlignVCenter\n'
                  f'                            elide: Text.ElideRight\n'
                  f'                            font: password.font\n'
                  f'                            color: "{renk}"\n'
                  f'                            text: i18nd("{alan}", "Password")\n'
                  f'                            visible: password.text.length === 0 && password.preeditText.length === 0\n'
                  f'                        }}')
        degistir(dosya, eski, katman)
    parola_ipucu(P + '/sddm/sddm-theme-mod/Main.qml', 'aerothemeplasma-sddm-theme', '#555555')
    parola_ipucu(P + '/shells/' + W + 'desktop/contents/lockscreen/AuthUI.qml', 'plasma_shell_' + W + 'desktop', '#6d6d6d')
    # Yan panel (Belgeler, Resimler, Bilgisayar...): görünürlük yapılandırmadaki İngilizce anahtarlarla
    # eşleştiriliyor ama 'name' alanı i18n ile çevriliyor; çeviri devreye girince öğeler gizleniyordu.
    # Çevrilmeyen ayrı bir 'anahtar' alanı ekle ve eşleştirmede onu kullan.
    spm = ss + 'SidePanelModels.qml'
    s = oku(spm)
    if 'anahtar:' not in s:
        s = re.sub(r'(\n(\s*)name: i18n\("([^"]+)"\),)', lambda m: f'{m.group(1)}\n{m.group(2)}anahtar: "{m.group(3)}",', s)
        s = s.replace('name: "Donate",', 'name: "Donate",\n            anahtar: "Donate",')
        yaz(spm, s)
    for kat in ('firstCategory', 'secondCategory', 'thirdCategory'):
        degistir(ss + 'MenuRepresentation.qml', f'sidePanelVisibility[sidePanelModels.{kat}[index].name]',
                 f'sidePanelVisibility[sidePanelModels.{kat}[index].anahtar]')
        degistir(ss + 'ConfigSidepanel.qml', f'text: sidePanelModels.{kat}[index].name\n',
                 f'property string anahtar: sidePanelModels.{kat}[index].anahtar\n'
                 f'						text: sidePanelModels.{kat}[index].name\n')
    s = oku(ss + 'ConfigSidepanel.qml')
    for fn in ('getItem', 'addItem', 'removeItem'):
        s = s.replace(f'visibilityManager.{fn}(text)', f'visibilityManager.{fn}(anahtar)')
    yaz(ss + 'ConfigSidepanel.qml', s)

    # Windows (Meta) tuşu / Alt+F1: Plasma, başlatıcıyı "org.kde.plasma.launchermenu" sağlayan uygulamacıkta arar
    mp = pl + W + 'SevenStart/metadata.json'
    meta = json.loads(oku(mp))
    meta['X-Plasma-Provides'] = ['org.kde.plasma.launchermenu']
    yaz(mp, json.dumps(meta, ensure_ascii=False, indent=4) + '\n')

    # Windows 7 Gezgini / Denetim Masası (linux-explorer-tr) kuruluysa ATP bağlantılarını ona yönlendir.
    # computer:/// ve controlpanel:///<sayfa> adreslerini linux-explorer-adres.desktop işler.
    import shutil
    if shutil.which('explorer'):
        degistir(ss + 'SidePanelModels.qml', 'executableString: "file:///.",', 'executableString: "computer:///",')
        degistir(ss + 'SidePanelModels.qml', 'executableString: "systemsettings",', 'executableString: "explorer --control-panel",')
        degistir(ss + 'SidePanelModels.qml', 'executableString: "systemsettings kcm_printer_manager",',
                 'executableString: "explorer \'controlpanel:///Donanım ve Ses/Aygıtlar ve Yazıcılar\'",')
        degistir(ss + 'FloatingIcon.qml', 'KCM.KCMLauncher.openSystemSettings("kcm_users")',
                 'Qt.openUrlExternally("controlpanel:///Kullanıcı Hesapları ve Aile Güvenliği/Kullanıcı Hesapları")')
        degistir(pl + W + 'networkmanagement/contents/ui/main.qml', 'onTriggered: KCMUtils.KCMLauncher.openSystemSettings(kcm)',
                 'onTriggered: Qt.openUrlExternally("controlpanel:///Ağ ve Internet/Ağ ve Paylaşım Merkezi")')
        degistir(pl + W + 'battery/contents/ui/main.qml', 'KCMUtils.KCMLauncher.openSystemSettings("kcm_powerdevilprofilesconfig");',
                 'Qt.openUrlExternally("controlpanel:///Sistem ve Güvenlik/Güç Seçenekleri");')

    # Görev Yöneticisi: ksysguard (KF6 portu) kuruluysa onu, değilse Plasma Sistem İzleyicisi'ni aç
    gy = '"(command -v ksysguard >/dev/null && kstart ksysguard) || kstart plasma-systemmonitor"'
    degistir(ss + 'main.qml', 'menu_executable.exec("kstart ksysguard")', 'menu_executable.exec(' + gy + ')')
    degistir(pl + W + 'seventasks/contents/ui/main.qml', 'menu_executable.exec("kstart ksysguard")', 'menu_executable.exec(' + gy + ')')
    degistir(P + '/shells/' + W + 'desktop/contents/logout/Logout.qml', 'executable.exec("kstart ksysguard")', 'executable.exec(' + gy + ')')
    sh = P + '/shells/' + W + 'desktop/contents/applet/AppletError.qml'
    hedef = 'i18nd("plasma_shell_' + W + 'desktop", "No error information.")'
    s = oku(sh)
    yaz(sh, s.replace('"No error information."', hedef) if hedef not in s else s)

    # 3) metadata.json
    md = [
        ('/desktoptheme/Seven-Black', 'Seven Black', 'Cam efekti ve yansımalar içeren Seven Black teması'),
        ('/layout-templates/' + W + 'taskbar', 'AeroThemePlasma Görev Çubuğu', 'Uygulama başlatıcı, görev çubuğu ve sistem tepsisi içeren varsayılan panel'),
        ('/look-and-feel/authui7', 'Windows 7 stili', 'Windows 7 tarzı açılış ekranı'),
        ('/plasmoids/' + W + 'SevenStart', 'Başlat Menüsü', 'Uygulama menüsünü açar'),
        ('/plasmoids/' + W + 'battery', 'Güç ve Pil', None),
        ('/plasmoids/' + W + 'desktopcontainment', 'Masaüstü (Windows 7)', 'Temiz ve basit bir masaüstü yerleşimi'),
        ('/plasmoids/' + W + 'digitalclocklite', 'Dijital Saat Lite', None),
        ('/plasmoids/' + W + 'keyboardlayout', 'Klavye Yerleşimi Değiştirici', None),
        ('/plasmoids/' + W + 'networkmanagement', 'Ağ', 'Ağ durumu ve denetimi'),
        ('/plasmoids/' + W + 'panel', 'Panel', 'Görev çubuğu paneli'),
        ('/plasmoids/' + W + 'seventasks', 'Görev Çubuğu', 'Simgeleri ve metni gösteren Windows 7 tarzı görev çubuğu'),
        ('/plasmoids/' + W + 'volume', 'Ses Düzeyi Karıştırıcısı', 'Aygıtların ve uygulamaların ses düzeyini ayarlayın'),
        ('/plasmoids/' + W + 'win7showdesktop', 'Masaüstünü Göster (Aero)', 'Masaüstünü gösterir'),
        ('/plasmoids/src/notifications_src/notifications', 'Eylem Merkezi', 'Bildirimleri ve işleri görüntüler'),
        ('/plasmoids/src/systemtray_src/systemtray', 'Bildirim Alanı', 'Sistem özelliklerine ve uygulama durum simgelerine hızlı erişim'),
        ('/plasmoids/src/systemtray_src/systemtray/package', 'Bildirim Alanı', None),
        ('/shells/' + W + 'desktop', 'Masaüstü', 'Windows 7 tarzı masaüstü kabuğu'),
    ]
    for yol, ad, ac in md:
        metadata(P + yol + '/metadata.json', ad, ac)

    # 4) .desktop dosyaları
    ini_anahtar(P + '/sddm/sddm-theme-mod/metadata.desktop', {'Name[tr]': 'SMOD', 'Description[tr]': 'SDDM için Windows 7 benzeri tema'}, 'SddmGreeterTheme')
    ini_anahtar(P + '/sddm/login-sessions/aerothemeplasma.desktop.cmake', {'Name[tr]': 'AeroThemePlasma', 'Comment[tr]': 'AeroThemePlasma ile çalışan KDE Plasma'})
    ini_anahtar(d + '/misc/xdg/autostart/x-atpootb.desktop', {'Name[tr]': 'AeroThemePlasma İlk Kurulum Sihirbazı'})
    ini_anahtar(d + '/misc/shortcuts/computer.desktop', {'Name[tr]': 'Bilgisayar', 'GenericName[tr]': 'Dosya Yöneticisi'})
    ini_anahtar(d + '/misc/shortcuts/Desktop Widget Gallery.desktop', {'Name[tr]': 'Masaüstü Gadget Galerisi'})
    # 5) Marka bilgisi (Sistem Bilgisi sayfası)
    br = d + '/misc/branding/kcm-about-distrorc'
    if os.path.exists(br):
        s = oku(br)
        yaz(br, s)


def aeroshell_workspace(d):
    cm = d + '/libtaskmanager/CMakeLists.txt'
    s = oku(cm)
    if 'TRANSLATION_DOMAIN' not in s:
        yaz(cm, 'add_definitions(-DTRANSLATION_DOMAIN=\\"aeroshell-libtaskmanager\\")\n' + s)
    ini_anahtar(d + '/aeroshell.desktop', {'Name[tr]': 'AeroShell Tercihleri'})
    mx = d + '/mimetype/x-ms-win.xml'
    s = oku(mx)
    for en, tr in (('Windows or DOS program', 'Windows veya DOS programı'), ('16-bit Windows program', '16 bit Windows programı'),
                   ('Windows or EFI program', 'Windows veya EFI programı'), ('Dynamic link library file', 'Dinamik bağlantı kitaplığı dosyası')):
        satir = f'<comment>{en}</comment>'
        ek = f'<comment xml:lang="tr">{tr}</comment>'
        if satir in s and ek not in s:
            s = s.replace(satir, satir + '\n        ' + ek)
    yaz(mx, s)


def aeroshell_kwin_components(d):
    md = [
        ('/effects_cpp/aeroglide/src', 'Aero Süzülme', 'Pencereler açılıp kapanırken Aero cam efektini koruyarak süzülmelerini sağlar'),
        ('/effects_cpp/kde-effects-aeroglassblur/src', 'Aero Cam Bulanıklığı', 'Pencerelerin arkasını Windows 7 ve Vista tarzında bulanıklaştırır. Özgün bulanıklık efektiyle çakışır!'),
        ('/effects_cpp/kwin-effect-smodsnap-v2/src', 'Aero Snap (SMOD)', 'Yeniden boyutlandırılabilir bir pencere ekran kenarına sürüklendiğinde animasyon gösterir'),
        ('/effects_cpp/startupfeedback/src', 'Başlangıç Geri Bildirimi', None),
        ('/kwin/effects/aeroshell-thumbnails', 'Görev Çubuğu Küçük Resim Animasyonları', 'Görev çubuğu küçük resimlerindeki pencere önizlemelerine animasyon ekler'),
        ('/kwin/effects/dimscreenaero', 'Yönetici Modu için Ekranı Karart', None),
        ('/kwin/effects/fadingpopupsaero', 'Solan Açılır Pencereler (Aero)', None),
        ('/kwin/effects/loginaero', 'Oturum Açma (Aero)', 'Oturum açılırken masaüstüne yumuşak geçiş yapar'),
        ('/kwin/effects/smodpeekeffect', 'Aero Peek', 'Masaüstünü göstermek için pencereleri saydamlaştırır'),
        ('/kwin/effects/squashaero', 'Aero Simge Durumuna Küçültme', 'Pencereler simge durumuna küçültülürken sıkıştırma animasyonu oynatır'),
        ('/kwin/scripts/smodpeekscript', 'Aero Peek', 'Aero Peek betiği'),
        ('/kwin/tabbox/flip3d', 'Flip 3D', None),
        ('/kwin/tabbox/thumbnail_aero', 'Aero Küçük Resimler', 'Küçük resim ızgarası kullanan pencere değiştirici'),
    ]
    for yol, ad, ac in md:
        metadata(d + yol + '/metadata.json', ad, ac)
    # po/tr çeviri dosyası (ki18n_install(po) ile derlenir)
    kaynak = os.path.join(KOK, '..', 'po', 'aeroshell-kwin-components.po')
    if os.path.exists(kaynak):
        os.makedirs(d + '/po/tr', exist_ok=True)
        yaz(d + '/po/tr/aeroshell-kwin-components.po', oku(kaynak))


def smod(d):
    metadata(d + '/gloweffect/metadata.json', 'SMOD Parıltı', 'İmleçle üzerine gelindiğinde başlık düğmelerinin parlamasını sağlar')


def aeroshell_sddm_kcm(d):
    cm = d + '/src/CMakeLists.txt'
    s = oku(cm)
    if 'TRANSLATION_DOMAIN' not in s:
        yaz(cm, 'add_definitions(-DTRANSLATION_DOMAIN=\\"kcm_aeroshellsddm\\")\n' + s)
    for f in os.listdir(d + '/src'):
        if f.endswith('.json'):
            metadata(d + '/src/' + f, 'SDDM Teması', 'AeroShell SDDM teması ayarlarını yönetin')


def aerothemeplasma_icons(d):
    ini_anahtar(d + '/Windows 7 Aero/index.theme', {'Name[tr]': 'Windows 7 Aero', 'Comment[tr]': 'Windows 7 Aero simge teması'}, 'Icon Theme')
    ini_anahtar(d + '/aero-drop/index.theme', {'Comment[tr]': 'Windows 7 Aero imleç teması'}, 'Icon Theme')


SES = {'Windows 7': 'Windows Varsayılanı', 'Windows 7 Afternoon': 'Öğleden Sonra', 'Windows 7 Calligraphy': 'Hat Sanatı',
       'Windows 7 Characters': 'Karakterler', 'Windows 7 Cityscape': 'Şehir Manzarası', 'Windows 7 Delta': 'Delta',
       'Windows 7 Festival': 'Festival', 'Windows 7 Garden': 'Bahçe', 'Windows 7 Heritage': 'Miras',
       'Windows 7 Landscape': 'Manzara', 'Windows 7 Quirky': 'Tuhaf', 'Windows 7 Raga': 'Raga',
       'Windows 7 Savanna': 'Savan', 'Windows 7 Sonata': 'Sonat'}


def aerothemeplasma_sounds(d):
    for klasor, ad in SES.items():
        p = f'{d}/{klasor}/index.theme'
        if os.path.exists(p):
            ini_anahtar(p, {'Name[tr]': ad, 'Comment[tr]': 'Windows 7 ses düzeni'}, 'Sound Theme')


def uac_polkit_agent(d):
    kaynak = os.path.join(KOK, '..', 'po', 'uac-polkit-agent.po')
    if os.path.exists(kaynak):
        yaz(d + '/po/tr/uac-polkit-agent.po', oku(kaynak))


if __name__ == '__main__':
    bilesen, dizin = sys.argv[1], os.path.abspath(sys.argv[2])
    {'aerothemeplasma': aerothemeplasma, 'aeroshell-workspace': aeroshell_workspace,
     'aeroshell-kwin-components': aeroshell_kwin_components, 'smod': smod,
     'aeroshell-sddm-kcm': aeroshell_sddm_kcm, 'aerothemeplasma-icons': aerothemeplasma_icons,
     'aerothemeplasma-sounds': aerothemeplasma_sounds, 'uac-polkit-agent': uac_polkit_agent}[bilesen](dizin)
    print(f'Türkçe yama uygulandı: {bilesen}' + (f' ({len(UYARILAR)} yama atlandı)' if UYARILAR else ''))
