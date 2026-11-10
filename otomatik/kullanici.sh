#!/bin/bash
# AeroThemePlasma otomatik güncelleme — kullanıcı tarafı. Root betiği runuser ile çağırır.
#   kullanici.sh kaynak <Plasma/X.Y>   kaynakları güncelle; değişen depoları "DEGISTI <ad>" olarak yaz
#   kullanici.sh ceviri                Türkçe yamaları uygula, katalogları yeniden üret; "EKSIK=<n>" yaz
#   kullanici.sh derle <paket>         paketi temiz kaynakla derle; son satırda paket dosyasının yolu
set -uo pipefail

K=$HOME/AeroKurulum
PKG=$K/pkg
export AERO_YAMA_ESNEK=1 LANG=tr_TR.UTF-8

# depo dizini | PKGBUILD paketi | dal türü (plasma = Plasma/X.Y dalı, master = sabit)
DEPOLAR=(
  "$K/repos/libplasma|aeroshell-libplasma|plasma"
  "$K/repos/uac-polkit-agent|uac-polkit-agent|plasma"
  "$K/repos/smod|aeroshell-smod|plasma"
  "$K/repos/aeroshell-workspace|aeroshell-workspace|plasma"
  "$K/repos/aeroshell-kwin-components|aeroshell-kwin-components|plasma"
  "$K/repos/aeroshell-sddm-kcm|aeroshell-sddm-kcm|master"
  "$K/repos/aerothemeplasma-icons|aerothemeplasma-icons|master"
  "$K/repos/aerothemeplasma-sounds|aerothemeplasma-sounds|master"
  "$K/aerothemeplasma|aerothemeplasma-desktop|plasma"
)

# Windows 7 uygulamaları: kaynak dizini (uygulamalar/ altında) | PKGBUILD paketi | etiket ya da dal adı
UYGULAMALAR=(
  "linux-devmgmt|linux-devmgmt-tr|etiket"
  "linux-minesweeper|linux-minesweeper-tr|etiket"
  "TuxManager|tux-manager-tr|etiket"
  "win-gadgets|aeroshell-gadgets-tr|master"
  "execbin|execbin-tr|master"
  "linver|linver-tr|master"
)

kaynak() {
    local dal=$1 satir dizin paket tur hedef eski yeni
    for satir in "${DEPOLAR[@]}"; do
        IFS='|' read -r dizin paket tur <<< "$satir"
        cd "$dizin" || { echo "UYARI depo yok: $dizin"; continue; }
        eski=$(git rev-parse HEAD 2>/dev/null)
        if [[ $tur == plasma ]]; then
            if git ls-remote --exit-code --heads origin "$dal" >/dev/null 2>&1; then
                hedef=$dal
            else
                hedef=$(git rev-parse --abbrev-ref HEAD)
                echo "UYARI $paket: uzak depoda $dal dalı yok (ATP bu Plasma sürümünü henüz desteklemiyor); $hedef ile devam"
            fi
        else
            hedef=$(git rev-parse --abbrev-ref HEAD)
        fi
        if git fetch -q --depth 1 origin "+refs/heads/$hedef:refs/remotes/origin/$hedef" 2>/dev/null; then
            git checkout -q -B "$hedef" "origin/$hedef" && git reset -q --hard "origin/$hedef"
        else
            echo "UYARI $paket: git fetch başarısız (ağ?); mevcut kaynakla devam"
        fi
        yeni=$(git rev-parse HEAD)
        [[ "$eski" != "$yeni" ]] && echo "DEGISTI $paket"
        sed -i -E "s|(git\+file://$dizin)#branch=[^\"]*\"|\1#branch=$hedef\"|" "$PKG/$paket/PKGBUILD"
    done
    # linux-explorer (Windows 7 Gezgini/Denetim Masası): en son yayımlanan sürüm etiketi
    local ex=$K/explorer/kaynak etiket
    if [[ -d $ex/.git ]]; then
        cd "$ex" && eski=$(git rev-parse HEAD)
        git fetch -q --tags origin 2>/dev/null || echo "UYARI linux-explorer-tr: git fetch başarısız; mevcut sürümle devam"
        etiket=$(git tag -l 'v[0-9]*' | sort -V | tail -1)
        if [[ -n $etiket ]]; then
            git checkout -q "$etiket"
            sed -i -E "s|(explorer/kaynak)#tag=[^\"]*\"|\1#tag=$etiket\"|; s/^pkgver=.*/pkgver=${etiket#v}/" "$PKG/linux-explorer-tr/PKGBUILD"
        fi
        [[ "$eski" != "$(git rev-parse HEAD)" ]] && echo "DEGISTI linux-explorer-tr"
    fi
    # Windows 7 uygulamaları: etiketli olanlar en son v* sürümü, diğerleri ana dal
    local u dizin paket tur
    for u in "${UYGULAMALAR[@]}"; do
        IFS='|' read -r dizin paket tur <<< "$u"
        dizin=$K/uygulamalar/$dizin
        [[ -d $dizin/.git ]] || { echo "UYARI depo yok: $dizin"; continue; }
        cd "$dizin" || continue
        eski=$(git rev-parse HEAD)
        if [[ $tur == etiket ]]; then
            git fetch -q --tags origin 2>/dev/null || echo "UYARI $paket: git fetch başarısız; mevcut sürümle devam"
            etiket=$(git tag -l 'v[0-9]*' | sort -V | tail -1)
            if [[ -n $etiket ]]; then
                git checkout -q "$etiket"
                sed -i -E "s|(uygulamalar/[^#\"]+)#tag=[^\"]*\"|\1#tag=$etiket\"|; s/^pkgver=.*/pkgver=${etiket#v}/" "$PKG/$paket/PKGBUILD"
            fi
        else
            if git fetch -q origin "+refs/heads/$tur:refs/remotes/origin/$tur" 2>/dev/null; then
                git checkout -q -B "$tur" "origin/$tur" && git reset -q --hard "origin/$tur"
            else
                echo "UYARI $paket: git fetch başarısız; mevcut kaynakla devam"
            fi
        fi
        [[ "$eski" != "$(git rev-parse HEAD)" ]] && echo "DEGISTI $paket"
    done
}

ceviri() {
    local d
    for d in aerothemeplasma:$K/aerothemeplasma aeroshell-workspace:$K/repos/aeroshell-workspace \
             aeroshell-kwin-components:$K/repos/aeroshell-kwin-components smod:$K/repos/smod \
             aeroshell-sddm-kcm:$K/repos/aeroshell-sddm-kcm uac-polkit-agent:$K/repos/uac-polkit-agent; do
        rsync -a --delete --exclude .git --exclude build "${d#*:}/" "$K/turkce/kaynak/${d%%:*}/"
        python3 "$K/turkce/araclar/yama.py" "${d%%:*}" "$K/turkce/kaynak/${d%%:*}"
    done
    cd "$K/turkce" || return 1
    python3 araclar/cikar.py > /dev/null
    python3 araclar/olustur.py > "$K/otomatik/son-ceviri.txt"
    echo "EKSIK=$(sed -n 's/^Toplam eksik: //p' "$K/otomatik/son-ceviri.txt")"
    [[ -d $K/explorer/kaynak ]] && echo "EKSIK_EXPLORER=$(python3 "$K/explorer/araclar/eksik.py" "$K/explorer/kaynak" 2>/dev/null || echo 0)"
    # Windows 7 uygulamaları: sözlükte olmayan yeni metin sayısı
    local u dizin toplam=0 n
    for u in "${UYGULAMALAR[@]}"; do
        dizin=${u%%|*}
        [[ -d $K/uygulamalar/$dizin ]] || continue
        n=$(python3 "$K/uygulamalar/araclar/cevir.py" eksik "$dizin" "$K/uygulamalar/$dizin" 2>/dev/null || echo 0)
        [[ $n =~ ^[0-9]+$ ]] && (( n > 0 )) && echo "UYARI $dizin: $n yeni çevrilmemiş metin (araclar/sozluk/$dizin.py)"
        [[ $n =~ ^[0-9]+$ ]] && toplam=$((toplam + n))
    done
    echo "EKSIK_UYGULAMA=$toplam"
}

derle() {
    local paket=$1 d=$PKG/$1 surum
    cd "$d" || return 1
    rm -rf kaynak src pkg ./*.pkg.tar.zst
    # pkgrel'i zaman damgası yap (her otomatik derleme yeni sürüm olsun)
    sed -i -E "s/^pkgrel=.*/pkgrel=$(date +%Y%m%d%H%M)/" PKGBUILD
    if [[ $paket == aeroshell-libplasma ]]; then
        surum=$(grep -oP 'set\(PROJECT_VERSION "\K[0-9.]+' "$K/repos/libplasma/CMakeLists.txt")
        sed -i -E "s/^pkgver=.*/pkgver=$surum/; s/^provides=.*/provides=(libplasma=$surum)/" PKGBUILD
    fi
    makepkg -f --noconfirm --nocolor > "$PKG/$paket.log" 2>&1 || { echo "HATA derleme: $paket (günlük: $PKG/$paket.log)"; return 1; }
    ls -1 "$d"/*.pkg.tar.zst | head -1
}

case "${1:-}" in
    kaynak) kaynak "$2" ;;
    ceviri) ceviri ;;
    derle)  derle "$2" ;;
    *) echo "kullanım: $0 kaynak <dal> | ceviri | derle <paket>"; exit 2 ;;
esac
