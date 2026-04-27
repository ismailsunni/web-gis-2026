---
marp: true
theme: default
paginate: true
size: 16:9
author: Ismail Sunni
date: April 2026
---
****
# OGC Services
## Standar Interoperabilitas: WMS & WFS

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

# Recap: Sudah Sampai Mana Kita

**Minggu sebelumnya:**
- WebGIS vs Desktop GIS
- Maps API: Leaflet, Google Maps, OpenLayers
- Publikasi: GitHub Pages, Vercel, GeoServer

**Hari ini (CPMK-3):**
- Bagaimana **server pemetaan** berbicara dengan **client** secara terstandar?
- Kenalan dengan **WMS** dan **WFS** — standar OGC

---

# Tujuan Pembelajaran

Setelah sesi ini, mahasiswa mampu:

✅ Menjelaskan **mengapa** standar OGC diperlukan
✅ Membedakan paradigma **WMS** (raster) vs **WFS** (vektor)
✅ Membaca dan menyusun request **WMS**: `GetCapabilities`, `GetMap`, `GetFeatureInfo`
✅ Membaca dan menyusun request **WFS**: `GetCapabilities`, `DescribeFeatureType`, `GetFeature`
✅ Mengkonsumsi WMS & WFS di OpenLayers

---

# Outline (50 menit)

1. **Mengapa Interoperabilitas?** — masalah & solusi (5')
2. **WMS** — Web Map Service mendalam (12')
3. **WFS** — Web Feature Service mendalam (12')
4. **WMS vs WFS** — kapan pakai yang mana (3')
5. **Selain WMS & WFS** — WMTS, WMS-T, Vector Tiles, OGC API (8')
6. **Demo Langsung** — OpenLayers + GeoServer (7')
7. **Wrap-up** & Q&A (3')

---

# 1️⃣ Mengapa Interoperabilitas?

---

# Masalah: Setiap Vendor Punya Bahasa Sendiri

Bayangkan kondisi tanpa standar:

- Data ESRI hanya bisa dibaca ArcGIS
- Data MapInfo hanya bisa dibaca MapInfo
- Setiap server pakai format request berbeda
- Klien harus tahu detail setiap server

**Akibatnya:**
- Vendor lock-in
- Data silos
- Integrasi mahal & rapuh

---

# Solusi: OGC (Open Geospatial Consortium)

**OGC** = konsorsium internasional yang menetapkan standar terbuka untuk data dan layanan geospasial.

🌐 [ogc.org](https://www.ogc.org/)

**Filosofi:**
- Server berbicara dengan **bahasa standar**
- Klien apa pun (OpenLayers, QGIS, ArcGIS, Leaflet) bisa mengkonsumsinya
- Data bisa dipertukarkan tanpa konversi format

**Standar populer:** WMS, WFS, WMTS, WCS, CSW, SensorThings, OGC API Features (modern)

---

# Service-Oriented GIS

```
┌─────────────┐         OGC Request          ┌──────────────────┐
│   Client    │ ───────────────────────────▶ │   Map Server     │
│ (OL, QGIS,  │                              │ (GeoServer,      │
│  ArcGIS)    │ ◀─────────────────────────── │  MapServer,      │
└─────────────┘     OGC Response             │  QGIS Server)    │
                  (image / GML / GeoJSON)    └──────────────────┘
                                                       │
                                                       ▼
                                              ┌──────────────────┐
                                              │  Data Source     │
                                              │  (PostGIS, SHP,  │
                                              │   GeoTIFF, ...)  │
                                              └──────────────────┘
```

**Server tahu cara membaca data → klien tidak perlu tahu format aslinya.**

---

# 2️⃣ WMS — Web Map Service

---

# WMS: Konsep

**Server me-render data → mengirim gambar (PNG/JPEG) ke klien.**

```
Klien:  "Tolong render layer 'jalan' dalam BBOX X1,Y1,X2,Y2,
         ukuran 800×600 pixel, format PNG"

Server: [renders image] → kirim PNG
```

- Klien tidak perlu tahu data aslinya
- Styling dilakukan di server
- Cocok untuk visualisasi cepat & layer berat

**Output:** raster image (PNG, JPEG, GIF)

---

# WMS: Tiga Operasi Utama

| Operasi | Fungsi |
|---|---|
| **`GetCapabilities`** | Apa saja yang ditawarkan server? (metadata, layer, CRS) |
| **`GetMap`** | Minta gambar peta yang sudah dirender |
| **`GetFeatureInfo`** | Tanya atribut di koordinat tertentu |

Semua diakses via **HTTP GET** dengan query parameter.

---

# WMS: `GetCapabilities`

Cek "menu" layanan yang tersedia.

```
https://geoserver.example.com/wms?
    SERVICE=WMS&
    VERSION=1.3.0&
    REQUEST=GetCapabilities
```

**Respons (XML):**
- Daftar layer + judul + deskripsi
- CRS yang didukung (EPSG:4326, EPSG:3857, ...)
- Bounding box tiap layer
- Format output (image/png, image/jpeg, ...)
- Style yang tersedia

> Selalu mulai eksplorasi server baru dari `GetCapabilities`.

---

# WMS: `GetMap`

Operasi inti — minta gambar peta.

```
https://geoserver.example.com/wms?
    SERVICE=WMS&
    VERSION=1.3.0&
    REQUEST=GetMap&
    LAYERS=topp:states&
    CRS=EPSG:3857&
    BBOX=-13884991,2870341,-7455066,6338219&
    WIDTH=800&
    HEIGHT=600&
    FORMAT=image/png&
    TRANSPARENT=true
```

---

# WMS: Parameter `GetMap`

| Parameter | Penjelasan |
|---|---|
| `LAYERS` | Nama layer (bisa multi, dipisah koma) |
| `CRS` (1.3.0) / `SRS` (1.1.1) | Sistem koordinat output |
| `BBOX` | Area peta: `minX, minY, maxX, maxY` |
| `WIDTH`, `HEIGHT` | Ukuran gambar (pixel) |
| `FORMAT` | `image/png`, `image/jpeg`, ... |
| `TRANSPARENT` | `true`/`false` — latar transparan |
| `STYLES` | Nama style; kosong = default |

---

# ⚠️ Trap: Versi WMS 1.1.1 vs 1.3.0

| | WMS 1.1.1 | WMS 1.3.0 |
|---|---|---|
| Param CRS | `SRS` | `CRS` |
| Axis order EPSG:4326 | `lon, lat` | `lat, lon` ⚠️ |

**Contoh BBOX EPSG:4326:**
- 1.1.1: `BBOX=110.3,-7.8,110.4,-7.7` (lon, lat)
- 1.3.0: `BBOX=-7.8,110.3,-7.7,110.4` (lat, lon!)

> **Penyebab paling umum** "kenapa peta saya kosong / di tempat aneh?".

---

# WMS: `GetFeatureInfo`

Klik satu pixel → server balikkan atribut fitur di sana.

```
https://geoserver.example.com/wms?
    SERVICE=WMS&
    VERSION=1.3.0&
    REQUEST=GetFeatureInfo&
    LAYERS=topp:states&
    QUERY_LAYERS=topp:states&
    CRS=EPSG:3857&
    BBOX=...&
    WIDTH=800&HEIGHT=600&
    I=400&J=300&                 ← pixel diklik
    INFO_FORMAT=application/json
```

**Output:** JSON / HTML / XML berisi properties fitur di koordinat tersebut.

---

# WMS di OpenLayers

```javascript
const wmsLayer = new ol.layer.Tile({
    source: new ol.source.TileWMS({
        url: 'http://localhost:8080/geoserver/wms',
        params: {
            'LAYERS': 'workspace:layer_name',
            'TILED': true
        },
        serverType: 'geoserver'
    })
});
map.addLayer(wmsLayer);
```

OpenLayers otomatis menyusun URL `GetMap` saat user pan/zoom.

---

# WMS: Pro & Con

✅ **Pro:**
- Cepat di klien — server sudah render
- Cocok untuk layer besar (jutaan fitur)
- Styling konsisten — ditentukan server (SLD)

❌ **Con:**
- Hanya gambar — tidak ada data atribut langsung
- Styling sulit diubah di klien
- Tidak bisa analisis spasial di klien
- Untuk query atribut harus pakai `GetFeatureInfo` (extra request)

---

# WMS Publik untuk Dicoba

**Terrestris OSM-WMS** (Jerman, sangat stabil)
```
https://ows.terrestris.de/osm/service?
  SERVICE=WMS&VERSION=1.1.1&REQUEST=GetCapabilities
```
Layer: `OSM-WMS`, `OSM-Overlay-WMS`, `TOPO-OSM-WMS`

**USGS National Map** (citra satelit AS)
```
https://basemap.nationalmap.gov/arcgis/services/USGSImageryOnly/MapServer/WMSServer?
  SERVICE=WMS&REQUEST=GetCapabilities
```

**Indonesia:** [tanahair.indonesia.go.id](https://tanahair.indonesia.go.id/portal-web) (BIG) dan [bmkg.go.id](https://www.bmkg.go.id/) menyediakan WMS publik — periksa endpoint terbaru.

> Tempel URL `GetCapabilities` di tab browser → kalian dapat XML lengkap.

---

# 3️⃣ WFS — Web Feature Service

---

# WFS: Konsep

**Server mengirim data fitur vektor (GML/GeoJSON) ke klien.**

```
Klien:  "Kirim semua fitur layer 'jalan' di area X,Y,
         dalam format GeoJSON"

Server: [query data] → kirim GeoJSON
```

- Klien menerima **geometri + atribut**
- Klien bisa restyle, query, analisis
- Cocok untuk data interaktif & dataset kecil-menengah

**Output:** GML, GeoJSON, Shapefile (zipped), CSV

---

# WFS: Tiga Operasi Utama

| Operasi | Fungsi |
|---|---|
| **`GetCapabilities`** | Apa saja yang ditawarkan? (sama seperti WMS) |
| **`DescribeFeatureType`** | Skema atribut: nama field & tipe data |
| **`GetFeature`** | Ambil data fitur (geometri + atribut) |

Plus **`Transaction`** (WFS-T) — insert/update/delete (advanced).

---

# WFS: `DescribeFeatureType`

Tanya skema layer — ada atribut apa saja, tipenya apa?

```
https://geoserver.example.com/wfs?
    SERVICE=WFS&
    VERSION=2.0.0&
    REQUEST=DescribeFeatureType&
    TYPENAMES=workspace:jalan
```

**Respons (XML Schema):**

```xml
<xsd:element name="nama"     type="xsd:string"/>
<xsd:element name="panjang"  type="xsd:double"/>
<xsd:element name="kelas"    type="xsd:string"/>
<xsd:element name="geom"     type="gml:LineStringPropertyType"/>
```

> Penting saat akan menyusun filter atau popup atribut.

---

# WFS: `GetFeature` (dasar)

Ambil semua fitur sebuah layer dalam GeoJSON.

```
https://geoserver.example.com/wfs?
    SERVICE=WFS&
    VERSION=2.0.0&
    REQUEST=GetFeature&
    TYPENAMES=workspace:jalan&
    OUTPUTFORMAT=application/json&
    SRSNAME=EPSG:4326
```

Hasil: standar GeoJSON `FeatureCollection` — bisa langsung dibaca OpenLayers, Leaflet, QGIS.

---

# WFS: `GetFeature` dengan Filter BBOX

Hanya ambil fitur dalam area tertentu (efisien!).

```
&BBOX=110.3,-7.8,110.4,-7.7,EPSG:4326
```

**Strategi `bbox` di OpenLayers:** server hanya mengirim fitur sesuai viewport — request otomatis berubah saat user pan/zoom.

---

# WFS: `GetFeature` dengan Filter CQL

CQL (Common Query Language) — filter berdasarkan atribut.

```
&CQL_FILTER=kelas='arteri' AND panjang>500
```

Atau pakai **OGC Filter XML** (lebih verbose, tapi standar):

```xml
<Filter>
  <PropertyIsEqualTo>
    <PropertyName>kelas</PropertyName>
    <Literal>arteri</Literal>
  </PropertyIsEqualTo>
</Filter>
```

> CQL = singkat & enak dibaca. OGC Filter = standar resmi.

---

# WFS di OpenLayers

```javascript
const wfsSource = new ol.source.Vector({
    format: new ol.format.GeoJSON(),
    url: (extent) => {
        return 'http://localhost:8080/geoserver/wfs?' +
            'service=WFS&version=2.0.0&request=GetFeature&' +
            'typename=workspace:jalan&' +
            'outputFormat=application/json&' +
            'srsname=EPSG:3857&' +
            `bbox=${extent.join(',')},EPSG:3857`;
    },
    strategy: ol.loadingstrategy.bbox
});

const wfsLayer = new ol.layer.Vector({ source: wfsSource });
```

---

# WFS: Pro & Con

✅ **Pro:**
- Klien dapat **data asli** — bisa restyle, query, analisis
- Interaktivitas tinggi — hover, klik, filter di klien
- Bisa diedit (WFS-T)

❌ **Con:**
- Payload bisa berat — tidak cocok untuk jutaan fitur sekaligus
- Styling jadi tugas klien
- Performa tergantung filter & strategi loading

---

# WFS Publik untuk Dicoba

**ahocevar GeoServer demo** (dipakai contoh resmi OpenLayers)
```
https://ahocevar.com/geoserver/wfs?
  service=WFS&version=2.0.0&request=GetFeature&
  typename=osm:water_areas&
  outputFormat=application/json&
  bbox=110.3,-7.85,110.45,-7.75,EPSG:4326
```

**GeoSolutions demo**
```
https://gs-stable.geosolutionsgroup.com/geoserver/wfs?
  service=WFS&version=2.0.0&request=GetCapabilities
```

> Buka URL `GetFeature` di browser → kalian langsung dapat GeoJSON.
> Coba ubah `bbox` atau tambah `&CQL_FILTER=...`.

---

# Inspeksi Response OGC dengan Tools

Browser cukup, tapi response WMS/WFS sering panjang & berformat XML/JSON yang sulit dibaca mentah.

| Tool | Untuk apa |
|---|---|
| **Hoppscotch** 🌐 | **Rekomendasi utama** — web-based, tanpa install |
| **Browser + JSON Viewer** ext | Cepat untuk GeoJSON/JSON |
| **Postman** 📮 | Alternatif jika kantor/proyek sudah pakai |
| **`curl` + `xmllint`/`jq`** | Power user, scriptable |
| **DevTools → Network** | Lihat request OL kirim |

> Pakai Hoppscotch untuk kelas — buka browser, langsung jalan.

---

# Hoppscotch untuk OGC: Workflow

🔗 [hoppscotch.io](https://hoppscotch.io/) — buka di browser, tidak perlu install.

1. **Method:** `GET`
2. Tempel URL `GetCapabilities`, misal:
   `https://ows.terrestris.de/osm/service?SERVICE=WMS&REQUEST=GetCapabilities`
3. **Send** → response otomatis di-pretty-print (XML/JSON)
4. **Parameters tab** → ubah `BBOX`, `LAYERS`, `CQL_FILTER` tanpa edit URL
5. **Save** ke koleksi → akses cepat lain hari

**Kenapa Hoppscotch (vs Postman)?**
- Open source, sejalan dengan semangat OGC
- Tanpa sign-up untuk fitur dasar
- Berjalan di browser apa pun, termasuk lab tanpa hak install

```bash
# Setara di terminal (untuk yang suka CLI):
curl -s "URL_GETCAPABILITIES" | xmllint --format -    # XML
curl -s "URL_GETFEATURE_JSON" | jq '.features[0]'     # JSON
```

---

# 4️⃣ WMS vs WFS

---

# Perbandingan Inti

| Aspek | WMS | WFS |
|---|---|---|
| **Output** | Gambar (raster) | Fitur vektor (GML/GeoJSON) |
| **Styling** | Di server (SLD) | Di klien (CSS/JS) |
| **Interaktivitas** | Terbatas (`GetFeatureInfo`) | Tinggi (data ada di klien) |
| **Performa data besar** | ✅ Baik | ⚠️ Berat |
| **Analisis di klien** | ❌ Tidak bisa | ✅ Bisa |
| **Editing** | ❌ Tidak | ✅ Bisa (WFS-T) |
| **Bandwidth** | Stabil | Variatif |

---

# Kapan Pakai Yang Mana?

| Skenario | Pilih |
|---|---|
| Basemap, citra satelit, raster besar | **WMS** |
| Layer dengan jutaan fitur | **WMS** |
| Data perlu di-klik untuk lihat atribut | **WMS** + `GetFeatureInfo` |
| Data perlu di-style di klien | **WFS** |
| Data perlu di-filter / dianalisis | **WFS** |
| Data perlu diedit dari web | **WFS-T** |
| Layer kecil-menengah, interaktif | **WFS** |

> Banyak proyek nyata **menggabungkan keduanya**.

---

# 5️⃣ Selain WMS & WFS
## Standar OGC Lainnya

---

# WMTS — Web Map Tile Service

**Masalah WMS:** server me-render gambar setiap request → lambat, tidak bisa di-cache CDN.

**Solusi WMTS:** server menyiapkan **tile** terpotong dengan skema z/x/y → bisa di-cache.

```
https://server.example.com/wmts/{layer}/{tilematrixset}/{z}/{x}/{y}.png
```

- Mirip XYZ tiles tapi dengan **metadata standar** (CRS, skala, batas)
- Cara modern menyajikan basemap raster
- Didukung penuh OpenLayers (`ol.source.WMTS`)

> Saat kalian pakai OSM atau Esri tile → secara konsep itu adalah WMTS.

---

# WMS-T — WMS dengan Dimensi Waktu

WMS bisa diperluas dengan dimensi **waktu** dan **elevasi**.

```
&TIME=2026-04-27T00:00:00Z
&ELEVATION=500
```

**Sangat relevan untuk Indonesia:**
- 🌧️ **BMKG** — radar cuaca, citra satelit Himawari per jam
- 🛰️ **LAPAN/BRIN** — time series Sentinel/Landsat untuk tutupan lahan
- 🔥 **Hotspot kebakaran** — animasi harian
- 🌊 **Banjir & longsor** — monitoring temporal

GeoServer mendukung WMS-T langsung jika data punya kolom waktu.

---

# Vector Tiles — Tile Vektor

Bukan gambar, tapi **fitur vektor** dipotong per tile (Protobuf, sangat ringan).

**Format dominan: Mapbox Vector Tile (MVT)**
- Adopted as **OGC Community Standard** (2018)
- Diserve oleh GeoServer, tegola, Martin, pg_tileserv
- Klien: MapLibre GL JS, Mapbox GL JS, OpenLayers

**Keunggulan:**
- Ringan (data di-encode protobuf)
- Bisa di-restyle di klien (warna, font, ikon)
- Smooth zoom & rotation (rendering WebGL)

**Format file populer:** **PMTiles** — semua tile dalam 1 file, bisa di-host di S3/GitHub Pages.

---

# OGC API — Generasi Baru

Standar lama (WMS/WFS) berbasis XML & SOAP-style query.
Standar baru: **REST + JSON + OpenAPI**.

| Lama | Baru |
|---|---|
| WFS | **OGC API - Features** |
| WMS / WMTS | **OGC API - Tiles, Maps** |
| WPS | **OGC API - Processes** |
| CSW | **OGC API - Records** |

Contoh URL OGC API - Features:
```
https://demo.pygeoapi.io/master/collections/lakes/items?f=json&limit=10
```

> WFS belum ditinggalkan, tapi proyek baru sebaiknya pakai OGC API Features.

---

# Keluarga Standar OGC (Ringkas)

| Standar | Untuk apa |
|---|---|
| **WMS** | Peta sebagai gambar |
| **WMTS** | Tile raster pre-rendered |
| **WFS** | Fitur vektor |
| **WCS** | Data raster mentah (citra) |
| **CSW** | Catalog metadata |
| **WPS** | Geoprocessing jarak jauh |
| **SensorThings API** | Data IoT/sensor real-time |
| **OGC API - \*** | Penerus modern (REST/JSON) |

> Tidak perlu hafal semua — kenali ada, cari saat butuh.

---

# Server yang Bicara OGC

| Server | Sifat | Cocok untuk |
|---|---|---|
| **GeoServer** ☕ | Java, GUI, paling populer | General purpose, geoportal |
| **MapServer** ⚡ | C, sangat cepat | High performance, batch |
| **QGIS Server** 🦊 | Pakai project QGIS | Workflow desktop → web |
| **pygeoapi** 🐍 | Python, OGC API native | Modern API-first |
| **pg_tileserv / Martin** | Vector tiles dari PostGIS | Vector tile serving |

> Hari ini kita pakai **GeoServer (Docker)** untuk demo.

---

# 6️⃣ Demo Langsung

---

# Demo: OpenLayers + GeoServer

**Stack:**
- OpenLayers 10 (klien)
- GeoServer lokal via Docker (server)
- 1 layer ditampilkan dua cara: **WMS** dan **WFS**

**Yang akan ditunjukkan:**
1. WMS layer → klik untuk `GetFeatureInfo`
2. WFS layer → klik untuk lihat properties (data sudah ada di klien)
3. Toggle WMS/WFS on/off
4. Inspect URL request di Network tab browser

🔗 [`/ogc-services/`](./index.html)

---

# Konfigurasi Demo

Edit konstanta di atas `app.js`:

```javascript
const GEOSERVER_BASE = 'http://localhost:8080/geoserver';
const WORKSPACE = 'YOUR_WORKSPACE';
const LAYER     = 'YOUR_LAYER';
```

Pastikan GeoServer Docker:
- Berjalan di port 8080
- CORS diaktifkan (jika klien beda origin)
- Workspace & layer sudah dibuat

---

# Tips: Debugging WMS/WFS

🔍 **Buka DevTools → Network tab**
- Lihat URL request yang dikirim OpenLayers
- Lihat response (image untuk WMS, JSON untuk WFS)

🔍 **Cek `GetCapabilities` langsung di browser**
- Pastikan layer ada
- Cek nama persis (case-sensitive!)

🔍 **CORS error?**
- GeoServer perlu config CORS untuk akses lintas origin

🔍 **Layer kosong?**
- Cek BBOX & CRS — sering tertukar (1.1.1 vs 1.3.0)

---

# 7️⃣ Wrap-up

---

# Key Takeaways

1. **OGC** = standar agar server & klien bicara bahasa yang sama
2. **WMS** = server mengirim **gambar** → cepat, cocok data besar
3. **WFS** = server mengirim **fitur vektor** → interaktif, fleksibel
4. **`GetCapabilities`** selalu jadi titik mulai eksplorasi server
5. Hati-hati **axis order** WMS 1.3.0 — sumber bug klasik
6. **WMTS** untuk basemap, **WMS-T** untuk data temporal (cuaca, satelit)
7. **Vector Tiles (MVT)** = generasi baru, ringan & restyle-able
8. **OGC API** = penerus modern berbasis REST/JSON

---

# Refleksi

🤔 Kenapa WMS dan WFS perlu standar terbuka, bukan API proprietary?
🤔 Kapan beban styling sebaiknya di server, kapan di klien?
🤔 Data peta administratif Indonesia (BIG) — sebaiknya WMS atau WFS? Kenapa?
🤔 Apa risiko terlalu mengandalkan satu server OGC?

---

# Latihan Mandiri

1. Akses `GetCapabilities` GeoServer publik atau Docker lokal — list 3 layer
2. Susun manual URL `GetMap` untuk satu layer, buka di browser → muncul gambar
3. Susun URL `GetFeature` dengan `OUTPUTFORMAT=application/json` → buka di browser
4. Tambahkan filter `CQL_FILTER` untuk satu atribut
5. Tampilkan keduanya (WMS + WFS dari layer sama) di OpenLayers, bandingkan perilaku klik
6. (Opsional) Bandingkan WMS 1.1.1 vs 1.3.0 untuk layer EPSG:4326 — perhatikan axis order

---

# 📚 Referensi

- [OGC WMS Standard](https://www.ogc.org/standard/wms/)
- [OGC WFS Standard](https://www.ogc.org/standard/wfs/)
- [OGC WMTS Standard](https://www.ogc.org/standard/wmts/)
- [OGC API - Features](https://ogcapi.ogc.org/features/)
- [Mapbox Vector Tile Spec (OGC Community Standard)](https://github.com/mapbox/vector-tile-spec)
- [PMTiles](https://protomaps.com/docs/pmtiles)
- [GeoServer Docs](https://docs.geoserver.org/) · [GeoServer Docker](https://hub.docker.com/r/geoserver/geoserver)
- [pygeoapi](https://pygeoapi.io/) — server OGC API Python
- [OpenLayers WMS Example](https://openlayers.org/en/latest/examples/wms-tiled.html) · [WFS Example](https://openlayers.org/en/latest/examples/vector-wfs.html)
- [CQL Filter Reference (GeoServer)](https://docs.geoserver.org/latest/en/user/filter/ecql_reference.html)
- [This presentation](https://github.com/ismailsunni/web-gis-2026)

> Selamat ber-eksperimen dengan server OGC kalian sendiri!
