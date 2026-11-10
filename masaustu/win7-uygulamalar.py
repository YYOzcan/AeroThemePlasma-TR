#!/usr/bin/env python3
"""Sistem uygulamalarına Windows 7 (Türkçe) adları ve simgeleri ver.

Kullanıcı düzeyinde geçersiz kılma: ~/.local/share/applications/<id>.desktop ve
~/.local/share/desktop-directories/<ad>.directory. Oluşturulan dosyalar LISTE dosyasına yazılır
(aero-kaldir.sh bunları siler).
"""
import os, re, subprocess

EV = os.path.expanduser('~')
UYG = EV + '/.local/share/applications'
DIZ = EV + '/.local/share/desktop-directories'
LISTE = EV + '/AeroKurulum/win7-uygulamalar.liste'

# id: (Ad, Simge, Açıklama[tr] ya da None, ekstra anahtarlar)
UYGULAMALAR = {
    # Windows Gezgini artık linux-explorer-tr (Türkçe paket); Dolphin gizlenir, Win+E Explorer'a geçer
    'org.kde.dolphin': ('Dolphin', None, None, {'NoDisplay': 'true', 'X-KDE-Shortcuts': ''}),
    'org.kde.konsole': ('Komut İstemi', 'utilities-terminal', 'Metin tabanlı (komut satırı) işlevleri gerçekleştirir.', {}),
    # Denetim Masası artık linux-explorer-tr'nin Denetim Masası; KDE Sistem Ayarları menüden gizlenir
    # (ayar modülleri Denetim Masası bağlantılarından ve simgelerden açılmaya devam eder)
    'systemsettings': ('Sistem Ayarları', 'preferences-system', None, {'NoDisplay': 'true'}),
    'kdesystemsettings': ('Sistem Ayarları', 'preferences-system', None, {'NoDisplay': 'true'}),
    'org.kde.kcalc': ('Hesap Makinesi', 'accessories-calculator', 'Hesap makinesi kullanarak temel aritmetik işlemleri gerçekleştirir.', {}),
    'org.kde.kwrite': ('Not Defteri', 'accessories-text-editor', 'Basit biçimlendirme kullanarak metin dosyaları oluşturur ve düzenler.', {}),
    'org.kde.spectacle': ('Ekran Alıntısı Aracı', 'spectacle', 'Ekranın bir bölümünün görüntüsünü yakalar; kaydeder ya da paylaşır.', {}),
    'org.kde.gwenview': ('Windows Fotoğraf Görüntüleyicisi', 'multimedia-photo-viewer', 'Resimleri görüntüleyin, döndürün ve yazdırın.', {}),
    'org.kde.haruna': ('Windows Media Player', 'multimedia-video-player', 'Dijital ortam dosyalarını oynatın ve düzenleyin.', {}),
    # Görev Yöneticisi artık TuxManager (tux-manager-tr); Plasma Sistem İzleyicisi menüden gizlenir
    'io.github.benapetr.TuxManager': ('Windows Görev Yöneticisi', 'utilities-system-monitor', 'Bilgisayarınızda çalışan programları ve işlemleri görüntüler.', {}),
    'org.kde.plasma-systemmonitor': ('Sistem İzleyicisi', 'utilities-system-monitor', None, {'NoDisplay': 'true'}),
    'linux-devmgmt': ('Aygıt Yöneticisi', None, 'Donanım aygıtlarını görüntüleyin ve sürücü ayarlarını değiştirin.', {}),
    'linux-minesweeper': ('Mayın Tarlası', None, 'Gizli mayınlardan kaçınarak mayın tarlasını temizleyin.', {}),
    'org.kde.kinfocenter': ('Sistem Bilgileri', 'hwinfo', 'Bilgisayarınızın donanımı ve yazılımı hakkındaki ayrıntıları görüntüler.', {}),
    'org.kde.partitionmanager': ('Disk Yönetimi', 'partitionmanager', 'Sabit diskleri ve bölümleri yönetin.', {}),
    'org.kde.kwalletmanager': ('Kimlik Bilgileri Yöneticisi', None, 'Kayıtlı kullanıcı adlarını ve parolaları yönetin.', {}),
    'system-config-printer': ('Aygıtlar ve Yazıcılar', 'printer', 'Aygıtları, yazıcıları ve yazdırma işlerini görüntüleyin ve yönetin.', {}),
    'org.pulseaudio.pavucontrol': ('Ses', 'multimedia-volume-control', 'Ses aygıtlarının ayarlarını değiştirin.', {}),
    'arch-update': ('Windows Update', 'system-software-update', 'Güncelleştirmeleri denetleyin ve yükleyin.', {}),
    'cachyos-pi': ('Programlar ve Özellikler', 'system-software-install', 'Programları yükleyin veya kaldırın.', {}),
    'btrfs-assistant': ('Yedekle ve Geri Yükle', 'timeshift', 'Dosyalarınızı yedekleyin ve geri yükleyin.', {}),
    'limine-snapper-restore': ('Sistem Geri Yükleme', 'timeshift', 'Bilgisayarınızın sistem dosyalarını önceki bir noktaya geri yükleyin.', {}),
    'firefox': ('Mozilla Firefox', None, None, {}),
}

# Tüm Programlar klasörleri (Windows 7 adları)
KLASORLER = {
    'kf5-utilities': 'Donatılar',
    'kf5-system': 'Sistem Araçları',
    'kf5-utilities-accessibility': 'Erişim Kolaylığı',
    'kf5-help': 'Yardım ve Destek',
}

YEREL_ANAHTAR = re.compile(r'^(Name|GenericName|Comment)(\[[^\]]+\])?=')


def kaynak_bul(uid):
    kullanici = f'{UYG}/{uid}.desktop'
    if os.path.exists(kullanici) and not open(kullanici, encoding='utf-8').read().startswith('# win7-uygulamalar'):
        return kullanici
    for d in ('/usr/share/applications', '/usr/local/share/applications'):
        if os.path.exists(f'{d}/{uid}.desktop'):
            return f'{d}/{uid}.desktop'
    return None


def uygula(uid, ad, simge, aciklama, ekstra):
    yol = kaynak_bul(uid)
    if not yol:
        return None
    satirlar = open(yol, encoding='utf-8').read().splitlines()
    cikti, giris = [], False
    eklenecek = {'Name': ad, 'Name[tr]': ad}
    if aciklama:
        eklenecek['Comment'] = aciklama
        eklenecek['Comment[tr]'] = aciklama
    if simge:
        eklenecek['Icon'] = simge
    eklenecek.update(ekstra)
    for s in satirlar:
        if s.startswith('# win7-uygulamalar'):
            continue
        if s.startswith('['):
            if giris:
                cikti += [f'{k}={v}' for k, v in eklenecek.items()]
            giris = (s.strip() == '[Desktop Entry]')
            cikti.append(s)
            continue
        if giris:
            if s.startswith(('Name=', 'Name[')) or (aciklama and s.startswith(('Comment=', 'Comment['))) \
                    or s.startswith('GenericName') or (simge and s.startswith('Icon=')) \
                    or any(s.startswith(k + '=') for k in ekstra):
                continue
        cikti.append(s)
    if giris:
        cikti += [f'{k}={v}' for k, v in eklenecek.items()]
    hedef = f'{UYG}/{uid}.desktop'
    yedek = None
    if yol == hedef:
        yedek = f'{EV}/KDE-Yedek/uygulama-oncesi-{uid}.desktop'
        if not os.path.exists(yedek):
            open(yedek, 'w', encoding='utf-8').write('\n'.join(satirlar) + '\n')
    open(hedef, 'w', encoding='utf-8').write('# win7-uygulamalar: Windows 7 adı/simgesi (AeroThemePlasma)\n' + '\n'.join(cikti) + '\n')
    return hedef


def main():
    os.makedirs(UYG, exist_ok=True); os.makedirs(DIZ, exist_ok=True)
    yazilan = []
    for uid, (ad, simge, ac, ek) in UYGULAMALAR.items():
        h = uygula(uid, ad, simge, ac, ek)
        print(('✓ ' if h else '– (kurulu değil) ') + f'{uid} -> {ad}')
        if h:
            yazilan.append(h)
    for ad, tr in KLASORLER.items():
        kaynak = f'/usr/share/desktop-directories/{ad}.directory'
        if not os.path.exists(kaynak):
            continue
        satirlar = [s for s in open(kaynak, encoding='utf-8').read().splitlines() if not YEREL_ANAHTAR.match(s)]
        i = satirlar.index('[Desktop Entry]') + 1
        satirlar[i:i] = [f'Name={tr}', f'Name[tr]={tr}']
        h = f'{DIZ}/{ad}.directory'
        open(h, 'w', encoding='utf-8').write('\n'.join(satirlar) + '\n')
        yazilan.append(h)
        print(f'✓ klasör {ad} -> {tr}')
    # D-Bus: "Klasörde göster" (org.freedesktop.FileManager1) isteklerini Explorer karşılasın
    dbus = EV + '/.local/share/dbus-1/services/org.freedesktop.FileManager1.service'
    os.makedirs(os.path.dirname(dbus), exist_ok=True)
    open(dbus, 'w').write('[D-BUS Service]\nName=org.freedesktop.FileManager1\nExec=/usr/bin/explorer\n')
    yazilan.append(dbus)
    # Masaüstü: Bilgisayar -> Explorer'ın Bilgisayar görünümü
    masaustu = subprocess.run(['xdg-user-dir', 'DESKTOP'], capture_output=True, text=True).stdout.strip()
    for ad, icerik in (('Bilgisayar.desktop',
                        '[Desktop Entry]\nType=Application\nName=Bilgisayar\nName[tr]=Bilgisayar\n'
                        'Comment=Bilgisayarınıza bağlı disk sürücülerini ve diğer donanımları görün.\n'
                        'Exec=explorer computer:///\nIcon=computer\nOnlyShowIn=KDE;\n'),
                       ('Geri Dönüşüm Kutusu.desktop',
                        '[Desktop Entry]\nType=Link\nName=Geri Dönüşüm Kutusu\nName[tr]=Geri Dönüşüm Kutusu\n'
                        'Comment=Silinen dosya ve klasörleri içerir.\nIcon=user-trash-full\nEmptyIcon=user-trash\n'
                        'URL=trash:/\nOnlyShowIn=KDE;\n')):
        h = f'{masaustu}/{ad}'
        open(h, 'w').write(icerik)
        os.chmod(h, 0o755)
        yazilan.append(h)
    open(LISTE, 'w').write('\n'.join(yazilan) + '\n')
    # Varsayılan uygulamalar: klasörler ve computer:/controlpanel: adresleri Explorer'da açılsın
    for mime in ('inode/directory', 'x-directory/normal', 'inode/mount-point'):
        subprocess.run(['xdg-mime', 'default', 'linux-explorer.desktop', mime])
    for mime in ('x-scheme-handler/computer', 'x-scheme-handler/controlpanel'):
        subprocess.run(['xdg-mime', 'default', 'linux-explorer-adres.desktop', mime])
    subprocess.run(['kbuildsycoca6'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


main()
