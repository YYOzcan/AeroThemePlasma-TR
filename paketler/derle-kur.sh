#!/bin/bash
# Sırayla derle ve kur (install.sh sırası)
cd $HOME/AeroKurulum/pkg || exit 1
for p in "$@"; do
  echo "BASLADI $p"
  ( cd $p && rm -f *.pkg.tar.zst && makepkg -f --noconfirm > ../$p.log 2>&1 ) || { echo "HATA_DERLEME $p"; exit 1; }
  ( cd $p && yes e | sudo pacman -U --needed *.pkg.tar.zst >> ../$p.log 2>&1 ) || { echo "HATA_KURULUM $p"; exit 1; }
  pacman -Q $p >/dev/null 2>&1 && echo "TAMAM $p" || { echo "HATA_KURULUM $p"; exit 1; }
done
echo "HEPSI_BITTI"
