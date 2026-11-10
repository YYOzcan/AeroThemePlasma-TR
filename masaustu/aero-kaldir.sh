#!/bin/bash
# AeroThemePlasma (Windows 7) dönüşümünü geri alır ve önceki KDE yedeğine döner.
#
#   bash ~/KDE-Yedek/aero-kaldir.sh            -> sistem tarafını geri alır, kullanıcı yedeğini bir sonraki girişe hazırlar
#   bash ~/KDE-Yedek/aero-kaldir.sh --kuru     -> yalnızca ne yapılacağını gösterir
#
# Alternatif (yalnızca kök dosya sistemi): kurulumdan önce alınan snapper anlık görüntüsü.
set -uo pipefail

KURU=0; [[ "${1:-}" == "--kuru" ]] && KURU=1
YEDEK=$(ls -t "$HOME"/KDE-Yedek/kde-yedek-*.run 2>/dev/null | head -1)
calistir() { echo "+ $*"; [[ $KURU == 1 ]] || "$@"; }

[[ $EUID -ne 0 ]] || { echo "Root olarak değil, kendi kullanıcınızla çalıştırın (sudo gerektiğinde sorulur)."; exit 1; }
[[ -f "$YEDEK" ]] || { echo "Yedek bulunamadı: $YEDEK"; exit 1; }
calistir bash "$YEDEK" dogrula || { echo "Yedek doğrulanamadı, durduruldu."; exit 1; }

echo "== 1) Ekran yöneticisi: SDDM -> Plasma Login Manager"
calistir sudo systemctl disable sddm.service
calistir sudo systemctl enable plasmalogin.service
calistir sudo rm -f /etc/sddm.conf.d/kde_settings.conf

echo "== 2) Plymouth: PlymouthVista -> cachyos"
calistir sudo systemctl disable plymouth-vista-slow-boot-animation.service plymouth-vista-no-wall.service
calistir sudo plymouth-set-default-theme cachyos

echo "== 3) Yerel ATP paketlerini kaldır, özgün libplasma'yı geri kur"
PAKETLER=$(pacman -Qgq aerothemeplasma-yerel 2>/dev/null | grep -vx aeroshell-libplasma | tr '\n' ' ')
[[ -n "$PAKETLER" ]] && calistir sudo pacman -Rns --noconfirm $PAKETLER
if pacman -Q aeroshell-libplasma >/dev/null 2>&1; then
    echo "+ yes e | sudo pacman -S libplasma   (aeroshell-libplasma yerine)"
    [[ $KURU == 1 ]] || { yes e | sudo pacman -S libplasma; }
fi
pacman -Q ksysguard6-git >/dev/null 2>&1 && calistir sudo pacman -Rns --noconfirm ksysguard6-git

echo "== 4) Sistem geneli varsayılan imleç"
calistir sudo sed -i 's/^Inherits=.*/Inherits=Adwaita/' /usr/share/icons/default/index.theme

echo "== 5) initramfs + Limine girdileri"
calistir sudo limine-mkinitcpio

echo "== 6) Kullanıcı tarafı artıkları"
calistir rm -rf $HOME/.themes/Windows-7-Better
calistir rm -f $HOME/.local/bin/aero-ilk-giris.sh $HOME/.config/autostart/aero-ilk-giris.desktop
calistir rm -f "$HOME/.local/share/konsole/Komut İstemi.profile" $HOME/.local/share/konsole/WindowsKomutIstemi.colorscheme
calistir sed -i '/^# Windows 7 Komut İstemi görünümü/,/^fi$/d' $HOME/.bashrc
calistir rm -f $HOME/.config/aerothemeplasmarc
calistir sudo rm -f /var/log/aerothemeplasma-guncelle.log
# Windows 7 uygulama adı/simge geçersiz kılmaları ve masaüstü Geri Dönüşüm Kutusu
if [[ -f $HOME/AeroKurulum/win7-uygulamalar.liste ]]; then
    while IFS= read -r f; do [[ -n "$f" ]] && calistir rm -f "$f"; done < $HOME/AeroKurulum/win7-uygulamalar.liste
fi

# Windows Gezgini (linux-explorer-tr) yerine yeniden Dolphin
calistir xdg-mime default org.kde.dolphin.desktop inode/directory x-directory/normal inode/mount-point
[[ -f $HOME/KDE-Yedek/user-places-oncesi.xbel ]] && calistir cp $HOME/KDE-Yedek/user-places-oncesi.xbel $HOME/.local/share/user-places.xbel

echo "== 7) KDE yedeğini geri yükle (Firefox dahil; Klassy vb. eksik paketler de kurulur)"
calistir bash "$YEDEK" geri-yukle --paketleri-kur --oturumu-kapatma

echo
echo "Bitti. Bilgisayarı yeniden başlatın: Plasma Login Manager ve eski KDE masaüstü gelecek."
