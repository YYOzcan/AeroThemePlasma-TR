#!/bin/bash
# AeroThemePlasma: ilk ATP oturumunda bir kez yapılacak işler. Her iş bitince işaret dosyası bırakır;
# hepsi tamamlanınca kendi autostart girdisini siler.
[[ "$PLASMA_DEFAULT_SHELL" == io.gitgud.wackyideas.desktop || "$XDG_CONFIG_DIRS" == */etc/xdg/aerothemeplasma* ]] || exit 0
D=$HOME/AeroKurulum/ilk-giris
mkdir -p "$D"
exec >> "$D/gunluk.log" 2>&1
echo "=== $(date '+%F %T') ilk giriş betiği"
sleep 8

# 1) Masaüstü arka planı: Windows 7 oturum açma arka planı (ATP ile gelir)
if [[ ! -e "$D/duvar-kagidi" ]]; then
    plasma-apply-wallpaperimage /usr/share/sddm/themes/sddm-theme-mod/background && touch "$D/duvar-kagidi"
fi

# 2) Firefox: Geckium + Aero UserChrome (Firefox kapalıyken kurulmalı)
if [[ ! -e "$D/geckium" ]]; then
    if pgrep -f /usr/lib/firefox/firefox >/dev/null; then
        notify-send -a "AeroThemePlasma" -i firefox "Geckium kurulamadı" "Firefox açıktı. Bir sonraki girişte yeniden denenecek."
    elif bash $HOME/AeroKurulum/firefox/geckium-kur.sh; then
        touch "$D/geckium"
    fi
fi

if [[ -e "$D/duvar-kagidi" && -e "$D/geckium" ]]; then
    rm -f $HOME/.config/autostart/aero-ilk-giris.desktop
    echo "tamamlandı"
fi
