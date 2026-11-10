# AeroThemePlasma TR

**Windows 7 görünümünü KDE Plasma'ya getiren [AeroThemePlasma](https://gitgud.io/wackyideas/aerothemeplasma)'nın tamamen Türkçeleştirilmiş, Arch/CachyOS paketlemesine uyarlanmış bir çatalıdır (fork).**

> Bu depo bağımsız bir topluluk çalışmasıdır. AeroThemePlasma, Linux Explorer, Geckium ve Aero UserChrome'un **orijinal geliştiricileriyle bir bağı yoktur**. Tüm emek ve telif hakları aşağıda listelenen üst projelere aittir; bu depo yalnızca onların üzerine Türkçe çeviri, düzeltme yamaları ve otomatik paketleme ekler.
>
> Microsoft® Windows™, Microsoft Corporation'ın tescilli ticari markasıdır. Bu ad yalnızca atıf amacıyla kullanılmaktadır.

## Neyin çatalı?

| Üst proje | Geliştirici | Lisans | Bu depoda ne var |
|---|---|---|---|
| [AeroThemePlasma](https://gitgud.io/wackyideas/aerothemeplasma) ve [AeroShell bileşenleri](https://gitgud.io/aeroshell) (libplasma çatalı, SMOD, KWin efektleri, çalışma alanı, UAC ajanı, SDDM KCM, simgeler, sesler) | WackyIdeas ve katkıcılar | AGPL-3.0 / GPL / LGPL | Türkçe çeviriler (~1000 metin), kaynak yamaları, PKGBUILD'ler |
| [Linux Explorer](https://github.com/actuallyaridan/linux-explorer) (Windows 7 Gezgini ve Denetim Masası) | actuallyaridan | GPL-3.0 | Türkçe çeviri (~1400 metin), yamalar, PKGBUILD |
| [Geckium](https://github.com/Neo-Kitchenfox/Geckium) | AngelBruni ve katkıcılar | MPL-2.0 | Firefox kurulum betiği (Geckium zaten Türkçe dil dosyası içerir) |
| [Aero UserChrome](https://gitgud.io/souris/aero-userchrome) | Souris | MPL-2.0 | Firefox kurulum betiği |
| [PlymouthVista](https://github.com/furkrn/PlymouthVista) | furkrn | MIT | Windows 7 kipi + Türkçe açılış metinleri ("Windows Başlatılıyor") |
| [Windows 7 Better](https://gitgud.io/Gamer95875/Windows-7-Better) (GTK) | Gamer95875 | — | Yalnızca kurulum adımı |
| [Selawik](https://github.com/microsoft/Selawik), [TerminalVector](https://www.yohng.com/software/terminalvector.html) | Microsoft / George Yohng | OFL-1.1 / kamu malı | Fontconfig eşlemesi; TerminalVector'a Türkçe ğ Ğ İ ı ekleyen betik |

Üst projelerin kaynak kodu ve Microsoft varlıkları (simge, ses, arka plan) **bu depoya kopyalanmamıştır**; PKGBUILD'ler derleme sırasında onları doğrudan üst depolardan alır.

## Neler Türkçe?

- **Başlat menüsü:** Tüm Programlar, Belgeler, Resimler, Denetim Masası, Aygıtlar ve Yazıcılar, Bilgisayarı kapat…
- **Görev çubuğu, bildirim alanı ve uygulamacıklar:** Saat, ses, ağ, pil ve Eylem Merkezi.
- **Kilit ekranı ve SDDM giriş ekranı:** "Kullanıcı Değiştir", "Parola"…
- **Diğer AeroShell bileşenleri:** İlk kurulum sihirbazı, Kullanıcı Hesabı Denetimi (UAC), SMOD dekorasyon ayarları, Aero cam bulanıklığı ve pencere rengi ayarları.
- **Windows Gezgini ve Denetim Masası (Linux Explorer):** Menüler, kopyalama penceresi, Özellikler, Aygıt Yöneticisi, saat dilimleri ve Denetim Masası sayfalarının tamamı.
- **Açılış ve kapanış (PlymouthVista):** "Windows Başlatılıyor", "Kapatılıyor…", "Windows güncelleştirmeleri yapılandırılıyor".
- **Konsole "Komut İstemi" profili:** cmd.exe renkleri, TerminalVector 9 pt, `C:\home\kullanıcı>` istemi.

Terminoloji olarak Windows 7'nin Türkçe sürümü esas alınmıştır.

## Üst projelere göre düzeltmeler

Çeviri sırasında üst projelerde ortaya çıkan ve burada yamalanan sorunlar:

- **Başlat menüsü sağ paneli:** Öğe görünürlüğü çevrilmiş adlarla karşılaştırıldığı için İngilizce dışındaki dillerde panel boş kalıyordu. Bu depoda ayrı bir anahtar alanı eklendi.
- **Windows tuşu:** SevenStart, `org.kde.plasma.launchermenu` sağladığını bildirmediği için Windows (Meta) tuşu ve Alt+F1 Başlat menüsünü açmıyordu.
- **Parola kutusu:** Qt 6.12'de parola kutusunun ipucu metni de maskeleniyor, "Parola" yazısı nokta olarak görünüyordu. SDDM'de ve kilit ekranında düzeltildi.
- **Görev Yöneticisi:** `ksysguard` kurulu değilse `plasma-systemmonitor` açılıyor.
- **Linux Explorer yönlendirmeleri:** Linux Explorer kuruluysa Başlat menüsü (Bilgisayar, Denetim Masası, Aygıtlar ve Yazıcılar), ağ ve güç bağlantıları ile kullanıcı resmi onun Denetim Masası sayfalarına yönlendiriliyor.

## Kurulum (Arch / CachyOS)

> ⚠ Betikler çalışma dizini olarak `~/AeroKurulum` bekler (üst depolar `~/AeroKurulum/repos`, ATP `~/AeroKurulum/aerothemeplasma`, PKGBUILD'ler `~/AeroKurulum/pkg`). Otomatik güncelleme servisi varsayılan olarak UID 1000 kullanıcısını kullanır; farklıysa `/etc/aerothemeplasma-otomatik.conf` içine `KULLANICI=ad` yazın. Kurulumdan önce mutlaka yedek ve snapper anlık görüntüsü alın.

1. Üst depoları klonlayın: AeroThemePlasma'nın `install.sh` dosyasındaki listeye bakın; `Plasma/6.8` dalı kullanılır.
2. Türkçe katalogları üretin:
   ```bash
   python3 turkce/araclar/cikar.py && python3 turkce/araclar/olustur.py
   ```
3. Paketleri sırayla derleyip kurun:
   ```bash
   paketler/derle-kur.sh aeroshell-libplasma uac-polkit-agent aeroshell-smod aeroshell-workspace \
     aeroshell-kwin-components aeroshell-sddm-kcm aerothemeplasma-icons aerothemeplasma-sounds \
     linux-explorer-tr aerothemeplasma-desktop aerothemeplasma-tr
   ```
4. İsteğe bağlı paketler:
   - `aero-yazitipleri`: Segoe UI yerine Selawik ve Türkçe TerminalVector;
   - `plymouth-theme-vista-tr`: Windows 7 açılış ekranı;
   - `geckium-autoconfig`: Geckium için Firefox autoconfig;
   - `aerothemeplasma-otomatik`: otomatik güncelleme.
5. SDDM'i etkinleştirin ve giriş ekranında **AeroThemePlasma** oturumunu seçin.

Paketlerin hepsi `aerothemeplasma-yerel` grubundadır; böylece `pacman` ile tek seferde kaldırılabilir.

## Otomatik güncelleme

`aerothemeplasma-otomatik` paketi bir pacman hook'u kurar. KDE Plasma, KWin, Qt veya libaero-qt güncellendiğinde (örneğin `paru -Syu` ya da Cachy Update ile) şunları yapar:

1. Paket yöneticisi işini bitirince arka planda düşük öncelikle başlar.
2. Kurulu Plasma sürümüne uygun ATP dalını (`Plasma/X.Y`) ve Linux Explorer'ın son sürümünü çeker.
3. Türkçe yamaları yeniden uygular. Değişen satırlar atlanır, derleme durmaz.
4. Paketleri derleyip kurar ve sonucu masaüstü bildirimiyle bildirir. Yeni çevrilmemiş metin varsa sayısını söyler.

Kullanıcı ayarlarına (`~/.config`), SDDM, Plymouth ve Firefox yapılandırmasına dokunmaz.

- Günlük: `/var/log/aerothemeplasma-guncelle.log`
- Elle başlatma: `aerothemeplasma-guncelle`

## Dizin yapısı

```
turkce/      AeroThemePlasma Türkçe araçları (yama.py, çeviri sözlüğü, .po kataloglar)
explorer/    Linux Explorer Türkçe çeviri sözlüğü ve kaynak yamalayıcı
paketler/    PKGBUILD'ler, pacman hook'u ve güncelleme servisi
otomatik/    Güncelleme servisinin kullanıcı tarafı (kaynak / çeviri / derleme)
firefox/     Geckium + Aero UserChrome profil kurulum betiği
masaustu/    Uygulama adlarını Windows 7'ye çeviren betik, Komut İstemi profili, geri dönüş betiği
fontlar/     TerminalVector'a Türkçe harf ekleyen betik
```

## Lisans

Bu depodaki çeviriler, yamalar ve betikler, türetildikleri AeroThemePlasma ile uyumlu olarak **GNU AGPL-3.0 veya sonrası** ile lisanslanmıştır (bkz. `LICENSE`). İstisnalar:

- `explorer/` altındaki çeviriler Linux Explorer'dan türetilmiştir; o projenin **GPL-3.0** lisansına tabidir.
- Geckium, Aero UserChrome ve PlymouthVista'ya ait yapılandırmalar kendi lisanslarına (MPL-2.0 / MIT) tabidir.

## Teşekkürler

Asıl emek üst proje geliştiricilerine aittir:

- WackyIdeas ve AeroShell katkıcıları
- actuallyaridan (Linux Explorer)
- AngelBruni ve Geckium ekibi
- Souris (Aero UserChrome)
- furkrn (PlymouthVista)
- Gamer95875 (Windows 7 Better)
- KDE Türkçe çeviri ekibi: bu depodaki çevirilerin bir kısmı KDE'nin mevcut Türkçe kataloglarından devşirilmiştir.
