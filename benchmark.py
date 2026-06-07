import time
import random
import copy
import tracemalloc
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# ALGORİTMALAR

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def insertion_sort(arr):
    for i in range(1, len(arr)):
        anahtar = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > anahtar:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = anahtar
    return arr



# ÖLÇÜM FONKSİYONLARI


def sure_olc(algoritma, dizi):
    # Çalışma süresini milisaniye cinsinden döndürür.
    dizi_kopyasi = copy.copy(dizi)
    baslangic = time.perf_counter()
    algoritma(dizi_kopyasi)
    bitis = time.perf_counter()
    return (bitis - baslangic) * 1000  # ms


def bellek_olc(algoritma, dizi):
    # Algoritmanın çalışması sırasında kullandığı EK belleği KB cinsinden döndürür.

    dizi_kopyasi = copy.copy(dizi)
    tracemalloc.start()
    algoritma(dizi_kopyasi)
    guncel, tepe = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return tepe / 1024  # KB



# TEST PARAMETRELERİ


boyutlar = [100, 500, 1000, 3000, 5000, 10000]

algoritmalar = {
    "Bubble Sort":    bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
}

senaryolar = {
    "Ortalama Durum\n(Rastgele)":    lambda n: random.sample(range(n * 10), n),
    "En İyi Durum\n(Sıralı)":        lambda n: list(range(n)),
    "En Kötü Durum\n(Ters Sıralı)":  lambda n: list(range(n, 0, -1)),
}

renkler = {
    "Bubble Sort":    "#E24B4A",
    "Selection Sort": "#378ADD",
    "Insertion Sort": "#1D9E75",
}


# TESTLER


sure_sonuclar   = {s: {a: [] for a in algoritmalar} for s in senaryolar}
bellek_sonuclar = {a: [] for a in algoritmalar}

print("Testler çalıştırılıyor...\n")

# Süre testleri (3 senaryo)
for senaryo_adi, veri_uret in senaryolar.items():
    print(f"  Senaryo: {senaryo_adi.replace(chr(10), ' ')}")
    for boyut in boyutlar:
        dizi = veri_uret(boyut)
        for alg_adi, alg_fonk in algoritmalar.items():
            sure = sure_olc(alg_fonk, dizi)
            sure_sonuclar[senaryo_adi][alg_adi].append(sure)
            print(f"    {alg_adi:18s} | n={boyut:6d} | {sure:8.2f} ms")
    print()

# Bellek testleri (rastgele dizi, senaryo bağımsız)
print("  Bellek ölçümleri (rastgele dizi):")
for boyut in boyutlar:
    dizi = random.sample(range(boyut * 10), boyut)
    for alg_adi, alg_fonk in algoritmalar.items():
        kb = bellek_olc(alg_fonk, dizi)
        bellek_sonuclar[alg_adi].append(kb)
        print(f"    {alg_adi:18s} | n={boyut:6d} | {kb:.3f} KB")

print("\nTestler tamamlandı. Grafikler oluşturuluyor...\n")



# GRAFİKLER


fig = plt.figure(figsize=(18, 10))
fig.suptitle(
    "Bubble Sort · Selection Sort · Insertion Sort\nPerformans Analizi",
    fontsize=15, fontweight="bold", y=1.01
)

# Zaman grafikleri 
senaryo_listesi = list(senaryolar.keys())
for col, senaryo_adi in enumerate(senaryo_listesi):
    ax = fig.add_subplot(2, 4, col + 1)
    for alg_adi, sureler in sure_sonuclar[senaryo_adi].items():
        ax.plot(boyutlar, sureler,
                label=alg_adi, color=renkler[alg_adi],
                marker="o", linewidth=2, markersize=4)
    ax.set_title(senaryo_adi, fontsize=10, pad=6)
    ax.set_xlabel("Dizi boyutu (n)", fontsize=9)
    ax.set_ylabel("Süre (ms)", fontsize=9)
    ax.legend(fontsize=8)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.1f"))
    ax.tick_params(labelsize=8)

# Karmaşıklık tablosu 
ax_tablo = fig.add_subplot(2, 4, 4)
ax_tablo.axis("off")
tablo_veri = [
    ["Algoritma",       "En İyi",  "Ortalama", "En Kötü", "Bellek"],
    ["Bubble Sort",     "O(n)",    "O(n²)",    "O(n²)",   "O(1)"],
    ["Selection Sort",  "O(n²)",   "O(n²)",    "O(n²)",   "O(1)"],
    ["Insertion Sort",  "O(n)",    "O(n²)",    "O(n²)",   "O(1)"],
]
tablo = ax_tablo.table(
    cellText=tablo_veri[1:],
    colLabels=tablo_veri[0],
    cellLoc="center",
    loc="center",
)
tablo.auto_set_font_size(False)
tablo.set_fontsize(8.5)
tablo.scale(1.15, 1.8)

# Başlık satırı rengi
for j in range(5):
    tablo[0, j].set_facecolor("#378ADD")
    tablo[0, j].set_text_props(color="white", fontweight="bold")

# Algoritma sütunu renkleri
satir_renkleri = ["#fde8e8", "#e8f1fd", "#e8f7f2"]
for i, renk in enumerate(satir_renkleri, start=1):
    for j in range(5):
        tablo[i, j].set_facecolor(renk)

ax_tablo.set_title("Teorik Karmaşıklık Tablosu", fontsize=9,
                   fontweight="bold", pad=10)

# Bellek grafiği (geniş) + Zaman karşılaştırması (n=10000) 
ax_bellek = fig.add_subplot(2, 4, (5, 6))
for alg_adi, kb_listesi in bellek_sonuclar.items():
    ax_bellek.plot(boyutlar, kb_listesi,
                   label=alg_adi, color=renkler[alg_adi],
                   marker="s", linewidth=2, markersize=4)
ax_bellek.set_title("Bellek Kullanımı (Ek Alan)", fontsize=10)
ax_bellek.set_xlabel("Dizi boyutu (n)", fontsize=9)
ax_bellek.set_ylim(0, max(max(v) for v in bellek_sonuclar.values()) * 1.5)
ax_bellek.set_ylabel("Tepe bellek kullanımı (KB)", fontsize=9)
ax_bellek.legend(fontsize=8)
ax_bellek.grid(True, linestyle="--", alpha=0.4)
ax_bellek.tick_params(labelsize=8)

# n=10000 çubuk grafik karşılaştırması 
ax_cubuk = fig.add_subplot(2, 4, (7, 8))
en_buyuk_idx = -1  # boyutlar listesinin son elemanı = 10000
x = range(len(senaryolar))
genislik = 0.25
senaryo_etiketleri = [s.replace("\n", " ") for s in senaryo_listesi]

for i, (alg_adi, alg_fonk) in enumerate(algoritmalar.items()):
    degerler = [
        sure_sonuclar[s][alg_adi][en_buyuk_idx]
        for s in senaryo_listesi
    ]
    offset = (i - 1) * genislik
    cubuklar = ax_cubuk.bar(
        [xi + offset for xi in x], degerler,
        width=genislik, label=alg_adi,
        color=renkler[alg_adi], alpha=0.85
    )
    for cubuk, deger in zip(cubuklar, degerler):
        ax_cubuk.text(
            cubuk.get_x() + cubuk.get_width() / 2,
            cubuk.get_height() + 5,
            f"{deger:.0f}",
            ha="center", va="bottom", fontsize=7
        )

ax_cubuk.set_title(f"n = {boyutlar[-1]:,} için Süre Karşılaştırması", fontsize=10)
ax_cubuk.set_xticks(list(x))
ax_cubuk.set_xticklabels(senaryo_etiketleri, fontsize=8)
ax_cubuk.set_ylabel("Süre (ms)", fontsize=9)
ax_cubuk.legend(fontsize=8)
ax_cubuk.grid(True, linestyle="--", alpha=0.4, axis="y")
ax_cubuk.tick_params(labelsize=8)

plt.tight_layout()
plt.savefig("performans_analizi.png", dpi=150, bbox_inches="tight")
print("Grafik 'performans_analizi.png' olarak kaydedildi.")
plt.show()