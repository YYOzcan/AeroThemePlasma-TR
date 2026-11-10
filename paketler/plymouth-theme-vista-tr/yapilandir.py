#!/usr/bin/env python3
"""PlymouthVista kaynağını Windows 7 kipi + Türkçe metinler için yapılandır."""
import re, sys
kok = sys.argv[1]
AYAR = {
    'UseLegacyBootScreen': '0', 'UseShadow': '1', 'AuthuiStyle': '"7"',
    'Pref': '2', 'UseHibernation': '0', 'DisableWall': '1', 'BootSlowdown': '8',
    'OldPlymouthTheme': '"cachyos"',
    'StartingText': '"Windows Başlatılıyor"',
    'ResumingText': '"Windows Sürdürülüyor"',
    'CopyrightText': '"© Microsoft Corporation"',
    'ShutdownText': '"Kapatılıyor..."',
    'RebootText': '"Yeniden başlatılıyor..."',
    'LogoffText': '"Oturum kapatılıyor..."',
    'UpdateTextMTL': r'"Windows güncelleştirmeleri yapılandırılıyor\n%%%i tamamlandı\nBilgisayarınızı kapatmayın."',
    'PasswordTitle': '"Windows Önyükleme Yöneticisi"',
    'AnswerTitle': '"Windows Önyükleme Yöneticisi"',
    'PasswordText': '"Parola"', 'AnswerText': '"Yanıt"',
    'NoGuiResumeText': '"Windows sürdürülüyor..."',
}
p = kok + '/src/plymouth_config.sp'
s = open(p, encoding='utf-8').read()
for k, v in AYAR.items():
    s, n = re.subn(r'^global\.' + k + r'\s*=.*;$', lambda m: f'global.{k} = {v};', s, flags=re.M)
    assert n == 1, k
open(p, 'w', encoding='utf-8').write(s)
p = kok + '/src/bootmgr.sp'
s = open(p, encoding='utf-8').read().replace('"ENTER - Continue"', '"ENTER - Devam"')
open(p, 'w', encoding='utf-8').write(s)
# Plymouth initramfs kancası Font= / MonospaceFont= satırlarını fc-match ile çözer
p = kok + '/PlymouthVista.plymouth'
s = open(p, encoding='utf-8').read()
if 'Font=' not in s:
    s = s.replace('ModuleName=script', 'ModuleName=script\nFont=Segoe UI\nMonospaceFont=Lucida Console')
s = s.replace('Description=PlymouthVista is a boot screen which re-creates the Windows Vista start-up sequence.',
              'Description=PlymouthVista is a boot screen which re-creates the Windows Vista start-up sequence.\nDescription[tr]=Windows 7 açılış ekranı (Windows Başlatılıyor)')
open(p, 'w', encoding='utf-8').write(s)
# gen_blur.sh: ImageMagick "Segoe-UI" adını tanımıyor; fontconfig'in çözdüğü dosya yolunu kullan
p = kok + '/gen_blur.sh'
s = open(p, encoding='utf-8').read().replace('FONT="Segoe-UI"', 'FONT="$(fc-match -f \'%{file}\' \'Segoe UI\')"')
# Bu ImageMagick derlemesinde info: kodlayıcısı yüklenmiyor; boyut ölçmeden doğrudan label: ile çiz
s = re.sub(r'    dimensions=\$\(magick .*?"\./images/text\$key\.png"\n',
           '    magick -density 96 -background none -font "$FONT" -pointsize "$FONT_SIZE" -fill white -gravity center label:"$value" "./images/text$key.png"\n',
           s, flags=re.S)
assert 'label:"$value" "./images/text$key.png"' in s
open(p, 'w', encoding='utf-8').write(s)
print('PlymouthVista yapılandırıldı')
