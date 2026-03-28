---
marp: true
theme: default
paginate: true
size: 16:9
author: Ismail Sunni
date: April 2026
---

# Pembangunan SIG Web
## WebGIS vs Desktop GIS & Maps API

Program Sarjana Terapan Teknologi Survei dan Pemetaan Dasar
Departemen Teknologi Kebumian
Sekolah Vokasi, UGM

<hr>

**Ismail Sunni** | Geospatial Software Engineer | Camptocamp DE

---

# Presentasi Ini

[https://github.com/ismailsunni/web-gis-2026](https://github.com/ismailsunni/web-gis-2026)

![QR code](https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://github.com/ismailsunni/web-gis-2026)

---

# Tujuan Pembelajaran

Setelah sesi ini, mahasiswa mampu:

✅ Membandingkan **WebGIS vs Desktop GIS**
✅ Menjelaskan **keunggulan WebGIS**
✅ Mengenal **ragam Maps API** (Leaflet, Google Maps, OpenLayers)
✅ Memahami **strategi publikasi** peta interaktif
✅ Membangun **peta web pertama** menggunakan Maps API

---

# Outline

1. **WebGIS vs Desktop GIS** — Perbandingan & evolusi
2. **Keunggulan WebGIS** — Mengapa beralih ke web?
3. **Arsitektur WebGIS** — Bagaimana data sampai ke browser?
4. **Maps API** — Leaflet, Google Maps, OpenLayers
5. **Hands-on** — Peta interaktif pertama
6. **Strategi Publikasi** — Deploy ke web
7. **Refleksi & Tugas**

---

# 1️⃣ WebGIS vs Desktop GIS
## Perbandingan & Evolusi

---

# Desktop GIS

## Contoh: QGIS, ArcGIS Desktop

- Install di komputer lokal
- Data disimpan di hard drive
- Analisis berat (geoprocessing)
- Satu pengguna per instalasi
- Update manual

![bg right:35% 80%](https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/QGIS_logo_new.svg/1200px-QGIS_logo_new.svg.png)

---

# Web GIS

## Contoh: Google Maps, OpenStreetMap, Mapbox

- Akses via browser — **tanpa install**
- Data di server / cloud
- Visualisasi & interaksi ringan
- **Multi-user** secara bersamaan
- Update otomatis

![bg right:35% 80%](https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Google_Maps_Logo_2020.svg/512px-Google_Maps_Logo_2020.svg.png)

---

# Perbandingan

| Aspek | Desktop GIS | Web GIS |
|---|---|---|
| **Akses** | Install lokal | Browser saja |
| **Data** | Lokal / LAN | Server / Cloud |
| **Analisis** | Lengkap & berat | Ringan & terbatas |
| **Pengguna** | 1 per lisensi | Multi-user |
| **Kolaborasi** | Sulit | Mudah (real-time) |
| **Distribusi** | Kirim file | Share URL |
| **Biaya** | Lisensi mahal* | Gratis / murah |

\* *kecuali QGIS — free & open source!*

---

# Evolusi: Desktop → Web

```
1990s: Desktop GIS (ArcView, MapInfo)
         ↓
2000s: Server GIS (ArcIMS, MapServer)
         ↓
2005+: Web Map Services (WMS, WFS, Google Maps API)
         ↓
2010+: Modern WebGIS (Leaflet, OpenLayers, Mapbox GL)
         ↓
2020+: Cloud-native GIS (STAC, COG, PMTiles)
```

---

# Kapan Pakai Desktop vs Web?

## 🖥️ Desktop GIS:
- Analisis spasial kompleks (buffer, overlay, routing berat)
- Editing data besar
- Cartographic production

## 🌐 Web GIS:
- Visualisasi & sharing
- Dashboard publik
- Monitoring real-time
- Kolaborasi tim

**Keduanya saling melengkapi!**

---

# 2️⃣ Keunggulan WebGIS
## Mengapa Beralih ke Web?

---

# 7 Keunggulan WebGIS

1. **Aksesibilitas** — Cukup browser, tanpa install
2. **Cross-platform** — Desktop, tablet, HP
3. **Kolaborasi** — Banyak user bersamaan
4. **Real-time** — Data update otomatis
5. **Distribusi mudah** — Share link, bukan file
6. **Biaya rendah** — Open source tools tersedia
7. **Integrasi** — Gabung dengan web app lain

---

# Contoh Penggunaan Nyata

| Use Case | Contoh |
|---|---|
| Peta bencana | BNPB Geoportal, InaSAFE |
| Monitoring hutan | Global Forest Watch |
| Transportasi | Google Maps, Grab |
| Smart city | Dashboard kota |
| Pariwisata | Peta wisata daerah |
| Survei lahan | Peta bidang tanah BPN |

---

# 3️⃣ Arsitektur WebGIS
## Bagaimana Data Sampai ke Browser?

---

# Arsitektur Umum

```
┌─────────┐     HTTP Request      ┌──────────┐     SQL Query     ┌──────────┐
│ Browser  │  ──────────────────→  │  Server  │  ──────────────→  │ Database │
│ (Client) │  ←──────────────────  │ (GeoServer│  ←──────────────  │(PostGIS) │
└─────────┘     JSON / Tiles      └──────────┘     Spatial Data   └──────────┘
```

---

# Komponen Client-Side

```
Browser
├── HTML          → Struktur halaman
├── CSS           → Tampilan & layout
├── JavaScript    → Logika & interaksi
└── Maps Library  → Render peta
    ├── Leaflet
    ├── OpenLayers
    └── Mapbox GL JS
```

---

# Data yang Ditampilkan

| Tipe | Format | Contoh |
|---|---|---|
| **Base map** | Raster tiles (PNG/JPG) | OSM, Google, Bing |
| **Vector** | GeoJSON, WFS | Batas wilayah, jalan |
| **Raster** | WMS, COG | Citra satelit |
| **Marker** | Lat/Lon dari API | Lokasi tempat |

---

# 4️⃣ Maps API
## Leaflet, Google Maps, OpenLayers

---

# Apa itu Maps API?

**Maps API** = Library JavaScript yang menyediakan:
- Render peta di browser
- Pan, zoom, interaksi
- Marker, popup, layer
- Akses tile server

**Kita tidak perlu menulis rendering engine dari nol!**

---

# 3 Maps API Utama

| | Leaflet | Google Maps | OpenLayers |
|---|---|---|---|
| **Lisensi** | Open source (BSD) | Proprietary | Open source (BSD) |
| **Ukuran** | ~40 KB | N/A (hosted) | ~180 KB |
| **Kompleksitas** | Simpel | Medium | Lengkap |
| **Terbaik untuk** | Peta ringan | Integrasi Google | GIS profesional |
| **API key?** | Tidak | Ya (berbayar) | Tidak |
| **Mobile** | Baik | Sangat baik | Baik |

---

# Leaflet 🍃

## Ringan, simpel, populer

```html
<link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

<div id="map" style="height: 400px;"></div>

<script>
    let map = L.map('map').setView([-7.79, 110.36], 13);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap'
    }).addTo(map);

    L.marker([-7.79, 110.36])
        .addTo(map)
        .bindPopup('<b>Yogyakarta</b>')
        .openPopup();
</script>
```

---

# Leaflet — Kelebihan

✅ Sangat ringan (~40 KB)
✅ API intuitif — mudah dipelajari
✅ Ekosistem plugin besar (500+ plugin)
✅ Mobile-friendly
✅ Dokumentasi bagus

❌ Terbatas untuk GIS kompleks
❌ Tidak mendukung CRS selain Web Mercator (tanpa plugin)

---

# Google Maps API 🗺️

## Familiar, kuat, tapi berbayar

```html
<script src="https://maps.googleapis.com/maps/api/js?key=YOUR_KEY"></script>

<div id="map" style="height: 400px;"></div>

<script>
    let map = new google.maps.Map(
        document.getElementById('map'), {
            center: { lat: -7.79, lng: 110.36 },
            zoom: 13
        }
    );

    new google.maps.Marker({
        position: { lat: -7.79, lng: 110.36 },
        map: map,
        title: 'Yogyakarta'
    });
</script>
```

---

# Google Maps — Kelebihan

✅ Data lengkap (Street View, traffic, transit)
✅ Geocoding & routing built-in
✅ Familiar bagi pengguna
✅ 3D maps & indoor mapping

❌ **Berbayar** setelah free tier ($200/bulan)
❌ API key wajib
❌ Tidak open source — vendor lock-in
❌ Tidak bisa custom tile server

---

# OpenLayers 🌍

## Lengkap, profesional, GIS-grade

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ol/dist/ol.css" />
<script src="https://cdn.jsdelivr.net/npm/ol/dist/ol.js"></script>

<div id="map" style="height: 400px;"></div>

<script>
    let map = new ol.Map({
        target: 'map',
        layers: [
            new ol.layer.Tile({
                source: new ol.source.OSM()
            })
        ],
        view: new ol.View({
            center: ol.proj.fromLonLat([110.36, -7.79]),
            zoom: 13
        })
    });
</script>
```

---

# OpenLayers — Kelebihan

✅ Mendukung semua CRS (EPSG:4326, EPSG:32749, dll)
✅ WMS, WFS, WMTS, WPS native
✅ Vektor, raster, dan 3D
✅ Fitur editing & drawing tools
✅ Production-ready untuk enterprise

❌ Lebih kompleks dari Leaflet
❌ Learning curve lebih tinggi

---

# Perbandingan Kode: Menambah Marker

## Leaflet
```javascript
L.marker([-7.79, 110.36]).addTo(map).bindPopup('Yogya');
```

## Google Maps
```javascript
new google.maps.Marker({position: {lat: -7.79, lng: 110.36}, map: map});
```

## OpenLayers
```javascript
let marker = new ol.Feature({
    geometry: new ol.geom.Point(ol.proj.fromLonLat([110.36, -7.79]))
});
vectorSource.addFeature(marker);
```

**Leaflet = paling ringkas, OpenLayers = paling eksplisit**

---

# Kapan Pakai Yang Mana?

## 🍃 Leaflet — jika:
- Peta sederhana, cepat
- Prototype / demo
- Proyek kecil

## 🗺️ Google Maps — jika:
- Butuh Street View / routing
- Budget tersedia
- Target: end-user umum

## 🌍 OpenLayers — jika:
- Butuh WMS/WFS/OGC
- Multi-CRS
- Proyek enterprise / pemerintah

---

# 5️⃣ Hands-on
## Peta Interaktif Pertama dengan Leaflet

---

# 🔨 Live Coding: Peta Leaflet

Kita akan membuat peta interaktif Yogyakarta dengan:
- Base map OSM
- Beberapa marker
- Popup informasi
- Layer control

---

# Step 1: Struktur HTML

```html
<!DOCTYPE html>
<html>
<head>
    <title>Peta Yogyakarta</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
    <style>
        #map { height: 100vh; width: 100%; }
    </style>
</head>
<body>
    <div id="map"></div>
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    <script src="app.js"></script>
</body>
</html>
```

---

# Step 2: Inisialisasi Peta

```javascript
// app.js
let map = L.map('map').setView([-7.7956, 110.3695], 14);

// Base map: OpenStreetMap
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);
```

**3 baris kode = peta interaktif!**

---

# Step 3: Menambahkan Marker

```javascript
let landmarks = [
    { name: "Tugu Yogyakarta",   lat: -7.7828, lng: 110.3672, desc: "Ikon kota Yogyakarta" },
    { name: "Malioboro",         lat: -7.7925, lng: 110.3655, desc: "Jalan belanja terkenal" },
    { name: "Kraton Yogyakarta", lat: -7.8053, lng: 110.3642, desc: "Istana Kesultanan" },
    { name: "Taman Sari",        lat: -7.8098, lng: 110.3590, desc: "Taman air kerajaan" },
    { name: "UGM",               lat: -7.7703, lng: 110.3780, desc: "Universitas Gadjah Mada" },
];

landmarks.forEach(lm => {
    L.marker([lm.lat, lm.lng])
        .addTo(map)
        .bindPopup(`<b>${lm.name}</b><br>${lm.desc}`);
});
```

---

# Step 4: Layer Control

```javascript
// Base maps
let osmLayer = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png');
let satellite = L.tileLayer(
    'https://server.arcgisonline.com/ArcGIS/rest/services/' +
    'World_Imagery/MapServer/tile/{z}/{y}/{x}'
);

let map = L.map('map', { layers: [osmLayer] }).setView([-7.7956, 110.3695], 14);

// Marker group
let markerGroup = L.layerGroup();
landmarks.forEach(lm => {
    L.marker([lm.lat, lm.lng]).bindPopup(`<b>${lm.name}</b>`).addTo(markerGroup);
});
markerGroup.addTo(map);

// Control
L.control.layers(
    { "OSM": osmLayer, "Satelit": satellite },
    { "Landmarks": markerGroup }
).addTo(map);
```

---

# Step 5: GeoJSON Data

```javascript
// Data GeoJSON — bisa dari file atau API
let geojsonData = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": { "nama": "Area Malioboro" },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[110.364, -7.790], [110.367, -7.790],
                                 [110.367, -7.795], [110.364, -7.795],
                                 [110.364, -7.790]]]
            }
        }
    ]
};

L.geoJSON(geojsonData, {
    style: { color: "#ff7800", weight: 2, fillOpacity: 0.3 }
}).addTo(map);
```

---

# Hasil Demo

Dalam ~30 baris kode, kita punya:

✅ Peta interaktif
✅ Multiple marker dengan popup
✅ Layer control (OSM / Satelit)
✅ GeoJSON overlay

**Bayangkan butuh berapa lama di Desktop GIS untuk berbagi ini!**

---

# 6️⃣ Strategi Publikasi
## Deploy Peta ke Web

---

# Cara Mempublikasi WebGIS

| Metode | Gratis? | Kompleksitas | Cocok untuk |
|---|---|---|---|
| **GitHub Pages** | ✅ | Mudah | Peta statis, portfolio |
| **Netlify** | ✅ | Mudah | Peta statis, preview |
| **Vercel** | ✅ | Mudah | React/Next.js apps |
| **VPS (DigitalOcean)** | ❌ | Menengah | Full backend + DB |
| **Cloud (AWS/GCP)** | ❌ | Tinggi | Enterprise, scaling |

---

# Deploy ke GitHub Pages

## Langkah:

1. Buat repository di GitHub
2. Upload file HTML + JS + CSS
3. Settings → Pages → Source: `main` branch
4. Akses di `https://username.github.io/repo-name`

**Gratis, otomatis, HTTPS!**

---

# Tips Publikasi

- **Gunakan CDN** untuk library (tidak perlu upload Leaflet/OL)
- **Optimasi ukuran** — compress gambar, minify JS
- **Responsive design** — test di mobile
- **CORS** — perhatikan akses data cross-origin
- **HTTPS** — wajib untuk geolocation API
- **README** — dokumentasi cara menggunakan

---

# 7️⃣ Refleksi & Tugas

---

# Refleksi

🤔 Kapan sebaiknya pakai WebGIS vs Desktop GIS?
🤔 Library mana yang paling cocok untuk proyek Anda?
🤔 Apa tantangan utama WebGIS?
🤔 Bagaimana cara memilih base map yang tepat?

---

# Key Takeaways

1. WebGIS = **aksesibilitas + kolaborasi**
2. Desktop GIS tetap diperlukan untuk **analisis berat**
3. Leaflet → simpel, OpenLayers → lengkap, Google Maps → familiar
4. Maps API **mempercepat development** drastis
5. GitHub Pages = cara termudah **publikasi gratis**

---

# 📋 Tugas

Buat peta web interaktif dengan ketentuan:

1. Pilih **salah satu Maps API** (Leaflet / OpenLayers)
2. Tampilkan **minimal 5 lokasi** di Yogyakarta (atau kota lain)
3. Setiap marker memiliki **popup dengan informasi**
4. Tambahkan **layer control** (minimal 2 base map)
5. *(Bonus)* Tambahkan data **GeoJSON** (polygon / polyline)
6. **Deploy** ke GitHub Pages
7. Kumpulkan **link GitHub repo + link demo**

---

# Contoh Referensi

- 🗺️ [Leaflet Quick Start](https://leafletjs.com/examples/quick-start/)
- 🌍 [OpenLayers Quick Start](https://openlayers.org/doc/quickstart.html)
- 📊 [Peta dari Google Sheet](https://ismailsunni.id/map/sheet-map/)
- 🛣️ [Route Finder Yogyakarta](https://ismailsunni.id/map/route-finder/)
- 📝 [GeoJSON.io](https://geojson.io/) — Buat GeoJSON interaktif
- 🚀 [GitHub Pages Docs](https://pages.github.com/)

---

# Final Thought

Desktop GIS = **alat analisis**
Web GIS = **media komunikasi**

## Keduanya saling melengkapi.
## Yang penting: **data sampai ke yang membutuhkan.**

---

# 📚 Referensi

- [Leaflet Documentation](https://leafletjs.com/reference.html)
- [OpenLayers Examples](https://openlayers.org/en/latest/examples/)
- [MDN: JavaScript Basics](https://developer.mozilla.org/docs/Learn/Getting_started_with_the_web/JavaScript_basics)
- [This presentation](https://github.com/ismailsunni/web-gis-2026)
- [Map Collection](https://ismailsunni.id/map/)

> Silakan eksplorasi dan bawa pertanyaan ke sesi berikutnya!
