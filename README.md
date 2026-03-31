# Web GIS 2026

Materi kuliah dan demo praktikum untuk topik Web GIS pada Program Sarjana Terapan Teknologi Survei dan Pemetaan Dasar, Sekolah Vokasi UGM.

Repositori GitHub:
- https://github.com/ismailsunni/web-gis-2026

Repositori ini berisi:
- slide presentasi mingguan dalam format Markdown
- demo WebGIS sederhana berbasis HTML, CSS, dan JavaScript
- contoh implementasi peta dengan pendekatan client-side tanpa backend penuh

## Highlight Materi

Topik utama yang dibahas dalam repositori ini:
- perbandingan WebGIS vs Desktop GIS
- pemilihan Maps API: Leaflet, Google Maps, OpenLayers
- strategi publikasi dan akses peta interaktif di web
- contoh WebGIS sederhana berbasis OpenLayers

## File Penting

- `web-gis-development/web-gis-development.md` — sumber slide utama
- `web-gis-development/web-gis-development.html` — hasil build slide HTML
- `web-gis-development/web-gis-development.pdf` — hasil build slide PDF
- `web-gis-development/index.html` — demo WebGIS OpenLayers
- `web-gis-development/app.js` — logika demo peta

## Struktur Repo

### `internet-programming/`
Materi pengantar JavaScript dan mini WebGIS tanpa library pemetaan.

### `web-gis-development/`
Materi utama tentang:
- perbandingan WebGIS vs Desktop GIS
- ragam Maps API: Leaflet, Google Maps, OpenLayers
- strategi publikasi dan akses peta interaktif di web
- demo WebGIS berbasis OpenLayers

### `examples/`
Contoh minimal dan eksperimen kecil terkait tampilan peta.

## Menjalankan Demo

Semua demo dapat dibuka langsung di browser.

- `examples/index.html`
- `internet-programming/index.html`
- `web-gis-development/index.html`

Jika browser membatasi akses file lokal untuk beberapa aset, jalankan lewat web server sederhana, misalnya:

```bash
python3 -m http.server 8000
```

Lalu buka `http://localhost:8000/`.

## Membangun Slide

Folder `web-gis-development/` memiliki `Makefile` untuk membangun slide HTML dan PDF.

Masuk ke folder tersebut lalu jalankan:

```bash
make all
```

Target yang tersedia:

- `make html` — build slide HTML
- `make pdf` — build slide PDF
- `make diagrams` — render diagram Mermaid di folder `diagrams/`
- `make clean` — hapus hasil build HTML/PDF

Catatan: `make all` hanya membangun slide presentasi, bukan demo `index.html` dan `app.js`.

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
- publikasi peta interaktif ke web
- integrasi data spasial sederhana untuk demo dan tugas mandiri

## Pengampu

- Ismail Sunni
- Geospatial Software Engineer
- Camptocamp DE

## Lisensi dan Atribusi

Repositori ini digunakan untuk keperluan pembelajaran. Jika memakai data, basemap, atau library dari pihak ketiga, pastikan tetap mencantumkan atribusi dan mengikuti lisensi masing-masing.
