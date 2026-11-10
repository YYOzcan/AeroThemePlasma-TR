# -*- coding: utf-8 -*-
"""Windows 7 Mayın Tarlası Türkçe sözlüğü (Windows 7 Türkçe Mayın Tarlası metinleri)."""
T = {
    'Appearance': 'Görünüm',
    'View Help': 'Yardımı Görüntüle',
    'About': 'Hakkında',
    'Change Appearance': 'Görünümü Değiştir',
    'Select Game Style': 'Oyun Stilini Seçin',
    'Minesweeper': 'Mayın Tarlası',
    'Flower Garden': 'Çiçek Bahçesi',
    'Select Board': 'Tahta Seçin',
    'Silver and Blue': 'Gümüş ve Mavi',
    'Green': 'Yeşil',
    'Randomly choose game style and board': 'Oyun stilini ve tahtayı rastgele seç',
    'Not implemented': 'Henüz uygulanmadı',
    'Minesweeper Help': 'Mayın Tarlası Yardımı',
    '&Game': '&Oyun',
    '&New Game': '&Yeni Oyun',
    '&Statistics': '&İstatistikler',
    '&Options': '&Seçenekler',
    '&Change Appearance': '&Görünümü Değiştir',
    'E&xit': 'Çı&kış',
    '&Help': '&Yardım',
    '&View Help': 'Yardımı &Görüntüle',
    '&About Minesweeper': 'Mayın Tarlası &Hakkında',
    'About Minesweeper': 'Mayın Tarlası Hakkında',
    'Clear the minefield without detonating any of the hidden mines. Left-click a square to uncover it, right-click to flag a mine.':
        'Gizli mayınlardan hiçbirini patlatmadan mayın tarlasını temizleyin. Bir kareyi açmak için sol tıklatın, mayını işaretlemek için sağ tıklatın.',
    '%1 mines': '%1 mayın',
    '%1 x %2 tile grid': '%1 x %2 karelik tahta',
    'Options': 'Seçenekler',
    'Difficulty': 'Zorluk',
    '&Beginner': '&Başlangıç',
    '&Intermediate': '&Orta düzey',
    '&Advanced': '&İleri düzey',
    'Bo&snia': 'Bo&sna',
    '&Custom': 'Ö&zel',
    'Height (9-24):': 'Yükseklik (9-24):',
    'Width (9-30):': 'Genişlik (9-30):',
    'Mines (10-668):': 'Mayınlar (10-668):',
    '&Display animations': 'Animasyonları &göster',
    '&Play sounds': 'Sesleri ç&al',
    'Show tips': 'İpuçlarını göster',
    'Always continue saved game': 'Kaydedilen oyuna her zaman devam et',
    'Always save game on exit': 'Çıkışta oyunu her zaman kaydet',
    'Allow &question marks (on double right-click)': '&Soru işaretlerine izin ver (çift sağ tıklatmada)',
    'Game Won': 'Oyunu Kazandınız',
    'Game Lost': 'Oyunu Kaybettiniz',
    'Congratulations, you won the game!': 'Tebrikler, oyunu kazandınız!',
    'Sorry, you lost this game. Better luck next time!': 'Üzgünüz, bu oyunu kaybettiniz. Bir dahaki sefere bol şans!',
    'Time: %1 seconds': 'Süre: %1 saniye',
    'A new record!': 'Yeni rekor!',
    'Games played: %1': 'Oynanan oyunlar: %1',
    'Games won: %1': 'Kazanılan oyunlar: %1',
    'Percentage: %1%': 'Yüzde: %%1',
    'Get More Games Online': 'Çevrimiçi Daha Fazla Oyun Edinin',
    'Exit': 'Çık',
    'Restart this game': 'Bu oyunu yeniden başlat',
    'Play again': 'Yeniden oyna',
    'Statistics': 'İstatistikler',
    'Beginner': 'Başlangıç',
    'Intermediate': 'Orta düzey',
    'Advanced': 'İleri düzey',
    'Bosnia': 'Bosna',
    'Games played:': 'Oynanan oyunlar:',
    'Games won:': 'Kazanılan oyunlar:',
    'Win percentage:': 'Kazanma yüzdesi:',
    'Best time:': 'En iyi süre:',
    'Longest winning streak:': 'En uzun kazanma serisi:',
    'Longest losing streak:': 'En uzun kaybetme serisi:',
    'Reset': 'Sıfırla',
    'Reset Statistics': 'İstatistikleri Sıfırla',
    'Erase all saved statistics for every difficulty?': 'Tüm zorluk düzeyleri için kaydedilen bütün istatistikler silinsin mi?',
    '%1 seconds': '%1 saniye',
    "Recreated in Linux with Qt6, using the original Windows 7 artwork, animations and sounds, extracted from the game's own executable and DLL (frame backdrop via the Lmy0217/Minesweeper project). Best enjoyed with AeroThemePlasma. Any Microsoft branding is used solely for referential use only, and does not aim to usurp copyrights from Microsoft.":
        "Oyunun kendi yürütülebilir dosyasından ve DLL'inden çıkarılan özgün Windows 7 çizimleri, animasyonları ve sesleri kullanılarak Qt6 ile Linux'ta yeniden oluşturuldu (çerçeve arka planı Lmy0217/Minesweeper projesinden). En iyi AeroThemePlasma ile kullanılır. Microsoft markaları yalnızca atıf amacıyla kullanılmıştır; Microsoft'un telif haklarını gasp etme amacı taşımaz.",
}
DESKTOP = {'linux-minesweeper.desktop': {'Name[tr]': 'Mayın Tarlası', 'GenericName[tr]': 'Mayın Tarlası',
                                         'Comment[tr]': 'Gizli mayınlardan kaçınarak mayın tarlasını temizleyin'}}

DESEN = [(r'Version: ([0-9][0-9.]*)', r'Sürüm: \1')]

QT_TR = ('src/main.cpp', 'QApplication app(argc, argv);')

T['OK'] = 'Tamam'

# Yardım penceresi: ham dize (R"(...)") olduğundan sözlükle değil, blok olarak değiştirilir
YARDIM = r'''
<style>
  body { background: white; color: #1a1a1a; }
  .link { color: #0066cc; }
  .aside { color: #555555; }
</style>
<body>

<p style="font-size:17pt; color:#333333;">Mayın Tarlası: Nasıl oynanır</p>

<p>Mayın Tarlası, göründüğünden zor bir bellek ve akıl yürütme sınavıdır ve
tüm zamanların en sevilen Windows oyunlarından biridir. Amaç: boş kareleri
bulmak ve mayınlardan kaçınmak.</p>
<p>Kolay görünüyor, değil mi?</p>

<p style="font-size:11pt; color:#1570c4;"><b>&#9660; Oyun başlatmak için</b></p>
<ol>
  <li><span class="link">&#10140; Oyunlar'ı açmak için tıklatın.</span></li>
  <li><b>Mayın Tarlası</b>'nı çift tıklatın.<br>
      <span class="aside">(Göremiyor musunuz? Windows Oyunları'nı açmanız
      gerekebilir. Bkz. <span class="link">Oyunlarım nerede?</span>)</span></li>
  <li>Bir zorluk düzeyi seçin: Başlangıç, Orta düzey veya İleri düzey.</li>
  <li>Başlamak için bir kareyi tıklatın.</li>
</ol>

<p style="font-size:11pt; color:#1570c4;"><b>&#9660; Oyunu kaydetmek için</b></p>
<ul>
  <li>Bir oyunu daha sonra bitirmeniz gerekirse oyundan çıkıp <b>Kaydet</b>'i
      tıklatabilirsiniz. Bir sonraki oynayışınızda son oyununuza devam etmek
      isteyip istemediğiniz sorulur. İstiyorsanız <b>Evet</b>'i tıklatın.</li>
</ul>

<p style="font-size:11pt; color:#1570c4;"><b>&#9660; Oyun seçeneklerini değiştirmek için</b></p>
<p>Zorluk düzeyini ayarlayabilir, animasyonları açıp kapatabilir ve daha
fazlasını yapabilirsiniz.</p>
<ol>
  <li><span class="link">&#10140; Oyunlar'ı açmak için tıklatın.</span></li>
  <li><b>Mayın Tarlası</b>'nı çift tıklatın.<br>
      <span class="aside">(Göremiyor musunuz? Windows Oyunları'nı açmanız
      gerekebilir. Bkz. <span class="link">Oyunlarım nerede?</span>)</span></li>
  <li><b>Oyun</b> menüsünü, ardından <b>Seçenekler</b>'i tıklatın.</li>
  <li>Seçimlerinizi yapın ve <b>Tamam</b>'ı tıklatın.</li>
</ol>

<p style="font-size:11pt; color:#1570c4;"><b>&#9660; Oyunun görünümünü özelleştirmek için</b></p>
<p>Tahtanın rengini ve mayınları mı yoksa çiçekleri mi gizleyeceğini
değiştirebilirsiniz.</p>
<ol>
  <li><span class="link">&#10140; Oyunlar'ı açmak için tıklatın.</span></li>
  <li><b>Mayın Tarlası</b>'nı çift tıklatın.<br>
      <span class="aside">(Göremiyor musunuz? Windows Oyunları'nı açmanız
      gerekebilir. Bkz. <span class="link">Oyunlarım nerede?</span>)</span></li>
  <li><b>Oyun</b> menüsünü, ardından <b>Görünümü Değiştir</b>'i tıklatın.</li>
  <li>Seçimlerinizi yapın ve <b>Tamam</b>'ı tıklatın.</li>
</ol>

<p style="font-size:17pt; color:#333333;">Mayın Tarlası: Kurallar ve temel bilgiler</p>

<p style="font-size:10pt;"><b>Amaç</b></p>
<p>Mayınlardan kaçınarak boş kareleri bulun. Tahtayı ne kadar hızlı
temizlerseniz puanınız o kadar iyi olur.</p>

<p style="font-size:10pt;"><b>Tahta</b></p>
<p>Mayın Tarlası'nda, her biri bir öncekinden zor olan üç standart tahta
vardır.</p>
<ul>
  <li><b>Başlangıç:</b> 81 kare, 10 mayın</li>
  <li><b>Orta düzey:</b> 256 kare, 40 mayın</li>
  <li><b>İleri düzey:</b> 480 kare, 99 mayın</li>
</ul>
<p><b>Oyun</b> menüsünü, ardından <b>Seçenekler</b>'i tıklatarak özel bir
tahta da oluşturabilirsiniz. Mayın Tarlası en çok 720 karelik ve 668
mayınlı tahtaları destekler.</p>

<p style="font-size:10pt;"><b>Nasıl oynanır</b></p>
<p>Mayın Tarlası'nın kuralları basittir:</p>
<ul>
  <li>Bir mayını açarsanız oyun biter.</li>
  <li>Boş bir kareyi açarsanız oynamaya devam edersiniz.</li>
  <li>Bir sayıyı açarsanız, sayı çevredeki sekiz karede kaç mayın gizlendiğini
      söyler. Bu bilgiyi yakındaki hangi karelerin tıklatılması güvenli
      olduğunu çıkarmak için kullanırsınız.</li>
</ul>

<p style="font-size:10pt;"><b>İpuçları ve püf noktaları</b></p>
<ul>
  <li><b>Mayınları işaretleyin.</b> Bir karenin mayın gizlediğinden
      şüpheleniyorsanız kareyi sağ tıklatın. Kareye bir bayrak konur.
      (Emin değilseniz soru işaretine çevirmek için yeniden sağ tıklatın.)</li>
  <li><b>Desenleri inceleyin.</b> Bir sıradaki üç kare 2-3-2 gösteriyorsa, o
      sıranın yanında büyük olasılıkla üç mayın dizilidir. Bir kare 8
      gösteriyorsa çevresindeki tüm karelerde mayın vardır.</li>
  <li><b>Keşfedilmemiş yerleri keşfedin.</b> Sonra nereyi tıklatacağınızdan
      emin değil misiniz? Keşfedilmemiş bir alanı açmayı deneyin. Mayınlı
      olduğundan şüphelendiğiniz bir alan yerine işaretlenmemiş karelerin
      ortasını tıklatmanız daha iyidir.</li>
</ul>

<p align="center"><img src=":/assets/helpBoard.png"></p>

</body>
'''
OZEL = [('src/ui/HelpDialog.cpp', r're:const char \*kHelpHtml = R"\(.*?\)";', 'const char *kHelpHtml = R"(' + YARDIM + ')";')]
