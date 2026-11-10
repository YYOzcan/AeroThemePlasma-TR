#!/bin/bash
# AeroThemePlasma otomatik yeniden derleme (root). pacman hook'u tarafından systemd ile başlatılır.
# Ayarlara (~/.config, /etc) dokunmaz; yalnızca ATP paketlerini yeni KWin/Plasma/Qt'ye göre derleyip kurar.
set -uo pipefail
# Kullanıcı: /etc/aerothemeplasma-otomatik.conf içinde KULLANICI=... ile belirtilebilir; yoksa UID 1000
[[ -f /etc/aerothemeplasma-otomatik.conf ]] && . /etc/aerothemeplasma-otomatik.conf
KULLANICI=${KULLANICI:-$(getent passwd 1000 | cut -d: -f1)}
EV=$(getent passwd "$KULLANICI" | cut -d: -f6)
K=$EV/AeroKurulum
UID_K=$(id -u $KULLANICI)
GUNLUK=/var/log/aerothemeplasma-guncelle.log
touch "$GUNLUK" && chmod 644 "$GUNLUK"
exec > >(tee -a "$GUNLUK") 2>&1

kul() { runuser -u "$KULLANICI" -- env HOME=$EV LANG=tr_TR.UTF-8 "$@"; }
bildir() {  # başlık, metin, simge
    runuser -u "$KULLANICI" -- env DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$UID_K/bus \
        notify-send -a "AeroThemePlasma" -i "${3:-system-software-update}" "$1" "$2" 2>/dev/null || true
}

echo "===== $(date '+%F %T') AeroThemePlasma yeniden derleme"

# 1) pacman / paru / yay / makepkg işleri bitene ve 30 sn boyunca sessiz kalana kadar bekle (en çok 2 saat)
sessiz=0; bekleme=0
while (( sessiz < 30 )); do
    if [[ -e /var/lib/pacman/db.lck ]] || pgrep -x 'pacman|paru|yay|makepkg' >/dev/null; then
        sessiz=0
    else
        sessiz=$((sessiz + 5))
    fi
    sleep 5; bekleme=$((bekleme + 5))
    (( bekleme > 7200 )) && { echo "Paket yöneticisi 2 saattir meşgul; vazgeçildi."; bildir "AeroThemePlasma güncellenemedi" "Paket yöneticisi uzun süre meşgul kaldı. Elle başlatmak için: aerothemeplasma-guncelle" dialog-warning; exit 1; }
done

PLASMA=$(pacman -Q plasma-workspace | awk '{print $2}')
DAL="Plasma/$(cut -d. -f1,2 <<< "$PLASMA")"
echo "Plasma $PLASMA, KWin $(pacman -Q kwin | awk '{print $2}'), Qt $(pacman -Q qt6-base | awk '{print $2}') -> ATP dalı $DAL"
bildir "AeroThemePlasma güncelleniyor" "KDE/Qt güncellendi ($PLASMA). ATP arka planda yeniden derleniyor; ayarlarınız ve Türkçe korunuyor."

# 2) Kaynaklar
KAYNAK_CIKTI=$(kul bash "$K/otomatik/kullanici.sh" kaynak "$DAL")
echo "$KAYNAK_CIKTI"
DAL_UYARI=$(grep -c 'dalı yok' <<< "$KAYNAK_CIKTI")

# 3) Türkçe (yamalar + kataloglar)
CEVIRI_CIKTI=$(kul bash "$K/otomatik/kullanici.sh" ceviri 2>&1)
echo "$CEVIRI_CIKTI" | tail -15
EKSIK=$(sed -n 's/^EKSIK=//p' <<< "$CEVIRI_CIKTI" | tail -1)
ATLANAN=$(grep -c 'yama atlandı)' <<< "$CEVIRI_CIKTI")
EKSIK_EX=$(sed -n 's/^EKSIK_EXPLORER=//p' <<< "$CEVIRI_CIKTI" | tail -1)

# 4) Derle + kur (sıra önemli: libplasma önce, masaüstü sonra)
SIRA=(aeroshell-libplasma uac-polkit-agent aeroshell-smod aeroshell-workspace aeroshell-kwin-components aeroshell-sddm-kcm)
grep -q 'DEGISTI aerothemeplasma-icons' <<< "$KAYNAK_CIKTI" && SIRA+=(aerothemeplasma-icons)
grep -q 'DEGISTI aerothemeplasma-sounds' <<< "$KAYNAK_CIKTI" && SIRA+=(aerothemeplasma-sounds)
# Windows 7 Gezgini/Denetim Masası (Türkçe) masaüstünden önce: ATP yamaları kurulu olup olmadığına bakar
[[ -d $K/pkg/linux-explorer-tr ]] && SIRA+=(linux-explorer-tr)
SIRA+=(aerothemeplasma-desktop aerothemeplasma-tr)
for p in "${SIRA[@]}"; do
    echo "--- $p"
    dosya=$(kul bash "$K/otomatik/kullanici.sh" derle "$p" | tail -1)
    if [[ ! -f "$dosya" ]]; then
        echo "$dosya"
        bildir "AeroThemePlasma derlemesi başarısız" "$p derlenemedi; önceki sürüm yerinde kaldı. Günlük: $K/pkg/$p.log — Claude'a gösterin." dialog-error
        exit 1
    fi
    if ! pacman -U --noconfirm "$dosya"; then
        bildir "AeroThemePlasma kurulamadı" "$p paketi kurulamadı. Günlük: $GUNLUK" dialog-error
        exit 1
    fi
done

# 5) Sonuç bildirimi
mesaj="Tamamlandı. Yeni KWin efektlerinin yüklenmesi için oturumu kapatıp açın."
(( ${EKSIK:-0} > 0 )) && mesaj+=" Not: $EKSIK yeni metin henüz çevrilmedi (İngilizce görünebilir); Claude'a 'ATP çevirilerini tamamla' deyin."
(( ${EKSIK_EX:-0} > 0 )) && mesaj+=" Windows Gezgini’nde $EKSIK_EX yeni metin henüz çevrilmedi; Claude’a 'Gezgin çevirilerini tamamla' deyin."
(( ${ATLANAN:-0} > 0 )) && mesaj+=" Bazı Türkçe yamalar üst kaynak değiştiği için atlandı."
(( ${DAL_UYARI:-0} > 0 )) && mesaj+=" Uyarı: ATP henüz $DAL dalını yayımlamamış, mevcut dal ile derlendi."
echo "$mesaj"
bildir "AeroThemePlasma güncellendi" "$mesaj" system-software-update
