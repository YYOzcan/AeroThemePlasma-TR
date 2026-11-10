#!/bin/bash
# Geckium + Aero UserChrome'u varsayılan Firefox profiline kurar (Firefox kapalıyken çalıştırın).
set -euo pipefail

INDIR=$HOME/AeroKurulum/firefox/indir
PROFIL_KOK=$HOME/.config/mozilla/firefox
[[ -f $PROFIL_KOK/profiles.ini ]] || PROFIL_KOK=$HOME/.mozilla/firefox
# Varsayılan profil: [Install...] bölümündeki Default=
PROFIL_AD=$(awk -F= '/^\[Install/{f=1} f&&/^Default=/{print $2; exit}' "$PROFIL_KOK/profiles.ini")
P="$PROFIL_KOK/$PROFIL_AD"
ESKI=$HOME/KDE-Yedek/firefox-chrome-oncesi-$(date +%Y%m%d-%H%M%S)

if pgrep -x firefox >/dev/null || pgrep -f /usr/lib/firefox/firefox >/dev/null; then
    echo "HATA: Firefox açık. Önce Firefox'u kapatın." >&2
    exit 1
fi
[[ -d "$P" ]] || { echo "HATA: profil bulunamadı: $P" >&2; exit 1; }

# 1) Eski chrome klasörünü kenara al (tam yedek ayrıca ~/KDE-Yedek/*.run içinde)
mkdir -p "$ESKI"
[[ -d "$P/chrome" ]] && mv "$P/chrome" "$ESKI/chrome"
cp -a "$P/user.js" "$ESKI/user.js" 2>/dev/null || true

# 2) Geckium profil dosyaları
cp -r "$INDIR/geckium/Profile Folder/chrome" "$P/chrome"
[[ -d "$P/chrThemes" ]] || cp -r "$INDIR/geckium/Profile Folder/chrThemes" "$P/chrThemes"

# 3) Aero UserChrome (Aero, CSS, JS, GTK klasörleri chrome içine birleştirilir)
for d in Aero CSS JS GTK; do
    mkdir -p "$P/chrome/$d"
    cp -r "$INDIR/aero-uc/$d/." "$P/chrome/$d/"
done
grep -qxF '@import url("Aero/Geckium.css");' "$P/chrome/userChrome.css" || printf '\n@import url("Aero/Geckium.css");\n' >> "$P/chrome/userChrome.css"

# 4) Zorunlu tercihler (user.js her açılışta uygulanır)
touch "$P/user.js"
sed -i '/browser\.tabs\.inTitlebar/d;/toolkit\.legacyUserProfileCustomizations\.stylesheets/d;/widget\.gtk\.rounded-bottom-corners\.enabled/d' "$P/user.js"
cat >> "$P/user.js" <<'EOF'
user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);
user_pref("widget.gtk.rounded-bottom-corners.enabled", true);
user_pref("browser.tabs.inTitlebar", 1);
EOF

# 5) Geckium'un ilk ayarları (prefs.js'e bir kez yazılır; sonradan Geckium Ayarları'ndan değiştirilebilir)
cat >> "$P/prefs.js" <<'EOF'
user_pref("Geckium.appearance.choice", 11);
user_pref("Geckium.appearance.titlebarStyle", "win");
user_pref("Geckium.appearance.titlebarNative", 1);
user_pref("Geckium.firstRun.complete", true);
EOF

# 6) Başlangıç önbelleğini temizle (README: "Clear startup cache")
rm -rf "$HOME/.cache/mozilla/firefox/$PROFIL_AD/startupCache"

# 7) profile-sync-daemon kullanılıyorsa değişiklikleri diske yaz
if systemctl --user is-active --quiet psd 2>/dev/null; then
    profile-sync-daemon resync >/dev/null 2>&1 || true
fi
echo "Geckium + Aero UserChrome kuruldu. Eski chrome: $ESKI"
