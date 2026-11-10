# -*- coding: utf-8 -*-
"""LinVer (Windows Hakkında / winver) Türkçe sözlüğü — Windows 7 Türkçe winver metinleri."""
T = {
    'Version ': 'Sürüm ',
    'Linux is a Registered Trademark of Linus Torvalds. All trademarks are property of their respective owners.':
        'Linux, Linus Torvalds’ın tescilli ticari markasıdır. Tüm ticari markalar ilgili sahiplerine aittir.',
    '<p style="line-height:85%">The ': '<p style="line-height:85%">',
    ' operating system and its user interface are protected by trademark and other pending or existing intellectual property rights in the United States and other countries.</p>':
        ' işletim sistemi ve kullanıcı arabirimi, Amerika Birleşik Devletleri’nde ve diğer ülkelerde ticari marka ve diğer bekleyen ya da mevcut fikri mülkiyet haklarıyla korunmaktadır.</p>',
    'This product is licensed under the <a style="color: #0066cc;" href="https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html">GNU General<br>Public License v2</a> to:':
        'Bu ürün <a style="color: #0066cc;" href="https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html">GNU Genel Kamu<br>Lisansı v2</a> kapsamında şu kişiye lisanslanmıştır:',
    'About Linux': 'Linux Hakkında',
    'About Windows': 'Windows Hakkında',
    'Version 6.0 (Build 6003: Service Pack 2)': 'Sürüm 6.0 (Derleme 6003: Service Pack 2)',
    'Copyright © 2006 Microsoft Corporation.  All rights reserved.': 'Telif Hakkı © 2006 Microsoft Corporation.  Tüm hakları saklıdır.',
    'Physical memory available to Windows®': 'Windows® için kullanılabilir fiziksel bellek',
    'This product is licensed under the <a style="color: #0066cc;" href="https://support.microsoft.com/en-us/windows/microsoft-software-license-terms-e26eedad-97a2-5250-2670-aad156b654bd">Microsoft Software<br>License Terms</a> to:':
        'Bu ürün <a style="color: #0066cc;" href="https://support.microsoft.com/en-us/windows/microsoft-software-license-terms-e26eedad-97a2-5250-2670-aad156b654bd">Microsoft Yazılımı<br>Lisans Koşulları</a> kapsamında şu kişiye lisanslanmıştır:',
    'Version 6.1 (Build 7601: Service Pack 1)': 'Sürüm 6.1 (Derleme 7601: Service Pack 1)',
    'Copyright © 2009 Microsoft Corporation.  All rights reserved.': 'Telif Hakkı © 2009 Microsoft Corporation.  Tüm hakları saklıdır.',
    'Version 6.2 (Build 9200)': 'Sürüm 6.2 (Derleme 9200)',
    '© 2012 Microsoft Corporation.  All rights reserved.': '© 2012 Microsoft Corporation.  Tüm hakları saklıdır.',
    'Version 6.3 (Build 9600)': 'Sürüm 6.3 (Derleme 9600)',
    '© 2013 Microsoft Corporation.  All rights reserved.': '© 2013 Microsoft Corporation.  Tüm hakları saklıdır.',
    'Linver configuration': 'LinVer yapılandırması',
    'Branding style to use:': 'Kullanılacak marka stili:',
    'Custom': 'Özel',
    'Display fake version instead of OS version': 'İşletim sistemi sürümü yerine Windows sürümünü göster',
    'Display full name': 'Tam adı göster',
    'To customize texts, branding image and other options, click customize.': 'Metinleri, marka resmini ve diğer seçenekleri özelleştirmek için Özelleştir’i tıklatın.',
    'Customize...': 'Özelleştir...',
    'Image or ICO file (*.png *.jpg *.bmp *.ico)': 'Resim veya ICO dosyası (*.png *.jpg *.bmp *.ico)',
    'Image file (*.png *.jpg *.bmp)': 'Resim dosyası (*.png *.jpg *.bmp)',
    'Customize Linver': 'LinVer’i Özelleştir',
    'Window': 'Pencere',
    'Size': 'Boyut',
    'Width:': 'Genişlik:',
    'Icon path:': 'Simge yolu:',
    'Branding': 'Marka',
    'Branding image path:': 'Marka resmi yolu:',
    'Product name:': 'Ürün adı:',
    'Copyright:': 'Telif hakkı:',
    'OS name:': 'İşletim sistemi adı:',
    'Details': 'Ayrıntılar',
    'Version:': 'Sürüm:',
    'License (RichText):': 'Lisans (zengin metin):',
    'Memory available text:': 'Kullanılabilir bellek metni:',
    'Tweaks': 'İnce ayarlar',
    'Misc': 'Çeşitli',
    'Show branding separator': 'Marka ayırıcısını göster',
    'Show operating system text': 'İşletim sistemi metnini göster',
    'Show memory available': 'Kullanılabilir belleği göster',
    'Details spacers': 'Ayrıntı boşlukları',
    'Left:': 'Sol:',
    'Height:': 'Yükseklik:',
    'Right:': 'Sağ:',
    'Apply': 'Uygula',
    'Cancel': 'İptal',
    'OK': 'Tamam',
    'Caption': 'Başlık',
    'Title:': 'Başlık:',
}
# "Physical memory available to " + dağıtım + ": " -> "<dağıtım> için kullanılabilir fiziksel bellek: "
OZEL = [
    ('about.cpp', '"Physical memory available to " + distro + ": "', 'distro + " için kullanılabilir fiziksel bellek: "'),
]

QT_TR = ('main.cpp', 'QApplication a(argc, argv);')
