# Web GIS 2026

Materi kuliah dan demo praktikum untuk topik Web GIS pada Program Sarjana Terapan Teknologi Survei dan Pemetaan Dasar, Sekolah Vokasi UGM.

Repositori GitHub:
- https://github.com/ismailsunni/web-gis-2026

Repositori ini berisi:
- halaman utama (`index.html`) yang menautkan seluruh materi dan demo
- slide presentasi mingguan dalam format Markdown beserta hasil build HTML/PDF
- demo WebGIS sederhana berbasis HTML, CSS, dan JavaScript (client-side, tanpa backend penuh)
- rekap submission tugas mahasiswa

## Highlight Materi

Topik utama yang dibahas dalam repositori ini:
- dasar pemrograman internet: HTML, CSS, JavaScript, DOM, dan event
- perbandingan WebGIS vs Desktop GIS serta pemilihan Maps API (Leaflet, Google Maps, OpenLayers)
- konsumsi dan visualisasi layanan OGC (WMS & WFS) dari GeoServer di OpenLayers
- Location-Based Services (LBS) & Mobile GIS: Geolocation API, sumber lokasi, privasi & baterai
- strategi publikasi dan akses peta interaktif di web

## Struktur Repo

- `index.html` — halaman utama yang menautkan demo, slide, dan rekap tugas tiap topik

### `internet-programming/`
Pengantar JavaScript (DOM, event) dan mini WebGIS tanpa library pemetaan.

### `web-gis-development/`
Arsitektur WebGIS, ragam Maps API, dan demo peta interaktif berbasis OpenLayers.

### `ogc-services/`
Standar interoperabilitas OGC — konsumsi WMS & WFS dari GeoServer di OpenLayers.

### `lbs-mobile-gis/`
Location-Based Services & Mobile GIS — Geolocation API, sumber lokasi, alur kerja LBS.

### `examples/`
Contoh minimal penempatan marker pada peta.

### `homework/`
Rekap submission tugas mahasiswa dalam bentuk halaman web (dapat disortir & difilter):
- `homework/week-7.html` — tugas Mini WebGIS (ditautkan dari kartu *Web GIS Development*)
- `homework/week-11.html` — tugas Visualisasi WMS & WFS (ditautkan dari kartu *OGC Services*)

### `tugas/`
Perkakas pembuat rekap:
- `recap_week7.py`, `recap_week11.py` — ekstraksi link GitHub repo & live deployment dari PDF submission, lalu menghasilkan CSV/Markdown dan halaman `homework/week-*.html`
- `week7_recap.csv` / `.md`, `week11_recap.csv` / `.md` — hasil ekspor rekap

PDF submission mentah (`tugas/week-7/`, `tugas/week-11/`) tidak di-commit (lihat `tugas/.gitignore`).

## Menjalankan Demo

Semua demo dapat dibuka langsung di browser, namun sebagian aset lebih stabil dijalankan lewat web server sederhana:

```bash
python3 -m http.server 8000
```

Lalu buka `http://localhost:8000/` untuk halaman utama, atau langsung ke salah satu demo:

- `internet-programming/index.html`
- `examples/index.html`
- `web-gis-development/index.html`
- `ogc-services/index.html`
- `lbs-mobile-gis/index.html`

## Membangun Slide

Folder `web-gis-development/`, `ogc-services/`, dan `lbs-mobile-gis/` masing-masing memiliki `Makefile` untuk membangun slide HTML dan PDF.

Masuk ke folder yang dimaksud lalu jalankan:

```bash
make all
```

Target yang tersedia:

- `make html` — build slide HTML
- `make pdf` — build slide PDF
- `make diagrams` — render diagram Mermaid di folder `diagrams/`
- `make clean` — hapus hasil build HTML/PDF

Catatan: `make all` hanya membangun slide presentasi, bukan demo `index.html` dan `app.js`.

## Rekap Tugas

Untuk membuat ulang rekap submission (CSV, Markdown, dan halaman web):

```bash
cd tugas
python3 recap_week7.py    # atau recap_week11.py
```

Skrip membaca PDF submission, mengekstrak link GitHub repo & live deployment (dari teks maupun anotasi/hyperlink PDF), lalu menulis `week*_recap.csv`, `week*_recap.md`, dan `homework/week-*.html`.

## Teknologi yang Dipakai

- OpenLayers
- HTML/CSS/JavaScript vanilla
- Marp CLI untuk slide
- Mermaid untuk diagram
- Python (`pdftotext`, `qpdf`) untuk perkakas rekap tugas

## Konteks Penggunaan

Repositori ini ditujukan untuk:
- bahan ajar di kelas
- demo saat presentasi atau praktikum
- latihan mandiri mahasiswa untuk eksplorasi WebGIS

## Tujuan Pembelajaran

Materi dalam repositori ini membantu mahasiswa memahami:
- perbedaan peran Desktop GIS dan WebGIS
- pemilihan library pemetaan yang tepat sesuai kebutuhan
- konsumsi layanan OGC (WMS & WFS) dan konsep LBS/Mobile GIS
- publikasi peta interaktif ke web
- integrasi data spasial sederhana untuk demo dan tugas mandiri

## Pengampu

- Ismail Sunni
- Geospatial Software Engineer
- Camptocamp DE

## Lisensi dan Atribusi

Repositori ini digunakan untuk keperluan pembelajaran. Jika memakai data, basemap, atau library dari pihak ketiga, pastikan tetap mencantumkan atribusi dan mengikuti lisensi masing-masing.
