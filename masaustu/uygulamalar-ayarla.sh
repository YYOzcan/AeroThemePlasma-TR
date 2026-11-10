#!/bin/bash
# Windows 7 uygulamalarını masaüstüne bağlar (kendi kullanıcınızla, Plasma oturumu açıkken çalıştırın).
#   - Başlat menüsü > Çalıştır...  -> execbin (Windows 7 "Çalıştır" penceresi)
#   - execbin için KWin kuralı (simge durumuna küçültülemez; upstream add_rule.sh ile aynı)
#   - Uygulama adları/simgeleri (win7-uygulamalar.py: Görev Yöneticisi -> TuxManager, Aygıt Yöneticisi, Mayın Tarlası)
# Görev Yöneticisi bağlantıları (Başlat menüsü, görev çubuğu, Ctrl+Alt+Del) yama.py ile zaten
# tux-manager'ı tercih eder; Denetim Masası'ndaki "Aygıt Yöneticisi" bağlantıları devmgmt'yi açar.
set -uo pipefail
DIZIN=$(cd "$(dirname "$0")" && pwd)

# 1) SevenStart: Çalıştır uygulaması
if command -v execbin >/dev/null; then
    qdbus6 org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript '
      panels().concat(desktops()).forEach(function (c) {
        c.widgets("io.gitgud.wackyideas.SevenStart").forEach(function (w) {
          w.currentConfigGroup = ["General"];
          w.writeConfig("defaultRunnerApp", "execbin");
        });
      });' && echo "✓ Çalıştır -> execbin"
fi

# 2) KWin kuralı (EXECBIN_RULES), yoksa ekle
C=~/.config/kwinrulesrc
if command -v execbin >/dev/null && ! grep -q 'EXECBIN_RULES' "$C" 2>/dev/null; then
    n=1; while grep -q "^\[$n\]" "$C" 2>/dev/null; do n=$((n + 1)); done
    for kv in Description=EXECBIN_RULES clientmachine=localhost minimizerule=2 wmclass=execbin wmclassmatch=1; do
        kwriteconfig6 --file kwinrulesrc --group "$n" --key "${kv%%=*}" "${kv#*=}"
    done
    sira=$(kreadconfig6 --file kwinrulesrc --group General --key Order)
    kwriteconfig6 --file kwinrulesrc --group General --key Order "${sira:+$sira,}$n"
    sayi=$(kreadconfig6 --file kwinrulesrc --group General --key count)
    [[ -n $sayi ]] && kwriteconfig6 --file kwinrulesrc --group General --key count "$((sayi + 1))"
    qdbus6 org.kde.KWin /KWin reconfigure && echo "✓ KWin kuralı: EXECBIN_RULES"
fi

# 3) Uygulama adları ve simgeleri
python3 "$DIZIN/win7-uygulamalar.py"
