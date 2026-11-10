# -*- coding: utf-8 -*-
"""win-gadgets Türkçe sözlüğü. Hava durumu C++/motor kodu yerinde değiştirilmez (anahtarlar servis verisiyle eşleşir);
onun yerine KDE'nin Türkçe hava katalogları gadget alanına .mo olarak kurulur (PKGBUILD)."""
ATLA_DOSYA = ['plasmoids/src/weather_src/weather/*.cpp', 'plasmoids/src/weather_src/weather/*.h',
              'plasmoids/src/weather_src/weather/*/*.cpp', 'plasmoids/src/weather_src/weather/*/*.h',
              'plasmoids/src/weather_src/weather/*/*/*.cpp', 'plasmoids/src/weather_src/weather/*/*/*.h',
              'plasmoids/src/slideshow_src/*.cpp', 'plasmoids/src/slideshow_src/*.h']
# Saat stili adları klasör anahtarıdır (clocks/<ad>); ekranda "%1 (yerleşik)" ile görünür
HARIC_SATIR = {('plasmoids/io.gitgud.catpswin56.gadgets.clock/contents/ui/StylesSystem.qml', 11)}

T = {
    '%1 (built-in)': '%1 (yerleşik)',
    'Appearance': 'Görünüm',
    'Show seconds hand': 'Saniye ibresini göster',
    'Show timezone': 'Saat dilimini göster',
    'Skin': 'Kaplama',
    'Failed to load theme %1 properly!': '%1 teması düzgün yüklenemedi!',
    'Example text': 'Örnek metin',
    'Preset:': 'Hazır ayar:',
    'Lightness:': 'Açıklık:',
    'HEX:': 'HEX:',
    'Current font:': 'Geçerli yazı tipi:',
    'Colorization mode:': 'Renklendirme modu:',
    'Automatic': 'Otomatik',
    'Choose a Font': 'Yazı Tipi Seçin',
    'Font': 'Yazı tipi',
    'Use Markdown': 'Markdown kullan',
    '"Click to Edit" behavior will be used for editing text': 'Metni düzenlemek için "Düzenlemek için tıklatın" davranışı kullanılacak',
    'Size:': 'Boyut:',
    'Expanded': 'Genişletilmiş',
    'Resizable': 'Yeniden boyutlandırılabilir',
    'Remove': 'Kaldır',
    'RSS Feed URL': 'RSS Akışı URL’si',
    'No feed items to display.': 'Görüntülenecek akış öğesi yok.',
    'Open link in browser': 'Bağlantıyı tarayıcıda aç',
    'Paths': 'Klasörler',
    'Duration for each slide (in milliseconds):': 'Her slaytın gösterim süresi (milisaniye):',
    'Choose a folder': 'Klasör seçin',
    'Use expanded variant': 'Genişletilmiş biçimi kullan',
    'Not available': 'Kullanılamıyor',
    'Calm': 'Durgun',
}

METADATA = {
    'plasmoids/io.gitgud.catpswin56.gadgets.clock/metadata.json': ('Saat', 'Saati ve saat dilimini gösteren masaüstü aracı'),
    'plasmoids/io.gitgud.catpswin56.gadgets.cpu/metadata.json': ('CPU Ölçer', 'CPU ve bellek kullanımını gösteren masaüstü aracı'),
    'plasmoids/io.gitgud.catpswin56.gadgets.notes/metadata.json': ('Notlar', 'Masaüstünüze kısa notlar yazın'),
    'plasmoids/io.gitgud.catpswin56.gadgets.rssfeeds/metadata.json': ('Akış Başlıkları', 'En son haber, spor ve eğlence başlıklarını izleyin.'),
    'plasmoids/src/slideshow_src/package/metadata.json': ('Slayt Gösterisi', 'Resimlerinizin sürekli bir gösterisini sunar'),
    'plasmoids/src/weather_src/weather/metadata.json': ('Hava Durumu', 'Hava tahmini ve geçerli hava koşulları'),
}
