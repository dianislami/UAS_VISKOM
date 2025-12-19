# Object Tracking Piano Tiles

**Object Tracking Piano Tiles** adalah proyek game interaktif berbasis visi komputer yang menggabungkan deteksi objek dan pelacakan (pose estimation) dengan gameplay mirip Piano Tiles. Pemain memilih objek yang ingin dilacak melalui kamera, dan game akan menyesuaikan tile dengan posisi objek secara real-time. Audio diputar sinkron dengan beat lagu, menciptakan pengalaman bermain yang interaktif dan menyenangkan.

---

## Fitur Utama
- **Pelacakan Objek Real-time**: Memanfaatkan ORB feature detection dan FLANN matcher untuk melacak objek yang dipilih melalui kamera.
- **Region of Interest (ROI)**: Pemain dapat menandai objek yang ingin dilacak menggunakan mouse.
- **Gameplay Interaktif**: Tile muncul sesuai beat lagu dan dapat ditekan dengan menggerakkan objek ke lane yang tepat.
- **Sinkronisasi Audio**: Lagu diputar sesuai BPM, dan tile muncul sinkron dengan musik.
- **Interface Intuitif**: Menu pemilihan lagu, pemilihan objek, gameplay, dan skor akhir ditampilkan dengan jelas.
- **Responsif dan Stabil**: Sistem berjalan lancar dengan tampilan real-time.

---

## Cara Menggunakan

### 1. Clone Repository
```bash
git clone https://github.com/dianislami/UAS_VISKOM.git
cd object-tracking-piano-tiles
````

### 2. Install Dependencies

Pastikan Python 3.x sudah terpasang. Gunakan pip untuk menginstal library yang dibutuhkan:

```bash
pip install -r requirements.txt
```

**Isi `requirements.txt`:**

```
pygame
opencv-python
mediapipe
numpy
```

### 3. Persiapan Audio

* Masukkan file audio `.wav` ke folder proyek.
* Pastikan nama file sesuai dengan yang tercantum di `main.py` pada variabel `SONGS`.

### 4. Menjalankan Game

Jalankan modul utama:

```bash
python main.py
```

---

## Kontrol Game

* **Mouse**: Drag untuk menentukan objek yang ingin dilacak (ROI).
* **Keyboard**:

  * **UP/DOWN** atau **W/S** → Pilih lagu di menu
  * **ENTER** → Konfirmasi pilihan lagu
  * **SPACE** → Mulai game setelah objek dipilih
  * **ESC** → Keluar dari game

---

## Struktur Folder

```
object-tracking-piano-tiles/
│
├─ main.py                 # Modul utama game
├─ pose_estimation.py      # Modul deteksi dan pelacakan objek
├─ requirements.txt        # Dependencies Python
├─ README.md
├─ audio1
└─ audio2                  
```

---

## Teknologi yang Digunakan

* **Python 3.x** – Bahasa pemrograman utama
* **OpenCV** – Untuk pengolahan gambar dan tracking objek
* **NumPy** – Untuk perhitungan numerik
* **Pygame** – Untuk audio dan gameplay interaktif

---
