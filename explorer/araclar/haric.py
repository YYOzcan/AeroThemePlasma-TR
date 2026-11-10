# -*- coding: utf-8 -*-
"""Çevrilmemesi gereken tekrarlar: dış veriyle (sysfs, pactl/pacman/timedatectl çıktısı, .desktop/JSON anahtarı) karşılaştırılanlar."""
HARIC = set()          # (dosya_adı, metin)
HARIC_SATIR = {
    # sysfs power_supply/type ve capacity_level değerleri
    ('src/model/control/SysfsScanner.cpp', 1484), ('src/model/control/SysfsScanner.cpp', 1634),
    ('src/model/control/SysfsScanner.cpp', 1752), ('src/model/control/SysfsScanner.cpp', 2318),
    ('src/model/control/SysfsScanner.cpp', 1517), ('src/model/control/SysfsScanner.cpp', 1710),
    # pactl (LC_ALL=C) çıktısı
    ('src/ui/control/dialogs/SoundDialog.cpp', 138), ('src/ui/control/dialogs/SoundDialog.cpp', 141),
    # .desktop anahtarları, AUR JSON alanı, pacman -Qi (LC_ALL=C) alanı
    ('src/ui/control/pages/ProgramsFeaturesPage.cpp', 267), ('src/ui/control/pages/ProgramsFeaturesPage.cpp', 271),
    ('src/ui/control/pages/ProgramsFeaturesPage.cpp', 275), ('src/ui/control/pages/ProgramsFeaturesPage.cpp', 443),
    ('src/ui/control/pages/ProgramsFeaturesPage.cpp', 609),
}
