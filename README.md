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
Rekap nilai & submission tugas mahasiswa sebagai halaman web (dapat disortir & difilter). Halaman hanya menampilkan tabel; seluruh data dibaca dari satu berkas CSV:
- `homework/grades.csv` — **sumber data tunggal** (nama, skor, URL repo/live, catatan per minggu, nilai UAS). Untuk memperbarui konten, cukup edit berkas ini.
- `homework/table.js` — parser CSV + perender tabel bersama
- `homework/results.html` — rekap nilai gabungan (Week 7, Week 11, UAS)
- `homework/week-7.html` — tugas Mini WebGIS (ditautkan dari kartu *Web GIS Development*)
- `homework/week-11.html` — tugas Visualisasi WMS & WFS (ditautkan dari kartu *OGC Services*)

### `tugas/`
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

## Rekap Tugas & Nilai

Seluruh data nilai dan submission tersimpan di `homework/grades.csv` (satu baris per mahasiswa). Halaman `homework/*.html` membaca berkas ini lewat `fetch` lalu merender tabelnya. Untuk memperbarui nama, skor, URL, atau catatan, cukup edit `homework/grades.csv` — semua halaman ikut ter-update.

Karena memakai `fetch`, halaman rekap perlu dibuka lewat web server (lihat di atas), bukan `file://`.

## Teknologi yang Dipakai

- OpenLayers
- HTML/CSS/JavaScript vanilla
- Marp CLI untuk slide
- Mermaid untuk diagram

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
