# Soal Pilihan Ganda — OGC Services & LBS / Mobile GIS

**Program Sarjana Terapan Teknologi Survei dan Pemetaan Dasar — Sekolah Vokasi UGM**
CPMK-3 · 50 soal pilihan ganda

> Petunjuk: Pilih satu jawaban yang paling tepat. Kunci jawaban ada di bagian akhir.

---

## Bagian A — OGC Services (WMS & WFS) — Soal 1–30

**1. Apa kepanjangan dari OGC?**
A. Open Geographic Community
B. Official Geospatial Committee
C. Open Geospatial Consortium
D. Online GIS Consortium

**2. Apa masalah utama yang ingin diselesaikan oleh standar OGC?**
A. Vendor lock-in, data silos, dan integrasi yang mahal & rapuh
B. Mempercepat rendering peta di klien
C. Mengurangi ukuran file shapefile
D. Menghapus kebutuhan akan basemap

**3. Pada arsitektur Service-Oriented GIS, siapa yang bertugas membaca format data asli (PostGIS, SHP, GeoTIFF)?**
A. Klien (browser)
B. CDN
C. Pengguna akhir
D. Map server

**4. Apa output utama dari WMS?**
A. Fitur vektor GeoJSON
B. Gambar raster (PNG/JPEG/GIF)
C. File XML Schema
D. Tile protobuf

**5. Apa output utama dari WFS?**
A. Fitur vektor (GML/GeoJSON)
B. Gambar raster
C. Tile berskema z/x/y
D. Citra satelit terkompresi

**6. Manakah TIGA operasi utama WMS?**
A. GetCapabilities, DescribeFeatureType, GetFeature
B. GetMap, Transaction, GetTile
C. GetMap, GetFeature, GetLegend
D. GetCapabilities, GetMap, GetFeatureInfo

**7. Operasi WMS manakah yang dipakai untuk melihat "menu" layanan (daftar layer, CRS, format)?**
A. GetMap
B. GetFeatureInfo
C. GetCapabilities
D. DescribeFeatureType

**8. Pada operasi `GetMap`, parameter `BBOX` berisi urutan nilai...**
A. width, height, format, style
B. minX, minY, maxX, maxY
C. lat pusat, lon pusat, zoom
D. CRS, layer, style, format

**9. Pada WMS, parameter sistem koordinat di versi 1.1.1 dan 1.3.0 berturut-turut bernama...**
A. CRS dan SRS
B. EPSG dan PROJ
C. SRID dan CRS
D. SRS dan CRS

**10. Apa perbedaan penting WMS 1.3.0 dibanding 1.1.1 untuk EPSG:4326?**
A. Urutan sumbu menjadi `lat, lon` (bukan `lon, lat`)
B. 1.3.0 hanya mendukung PNG
C. 1.3.0 menghapus parameter BBOX
D. 1.3.0 tidak mendukung transparansi

**11. Operasi WMS `GetFeatureInfo` digunakan untuk...**
A. Meminta gambar peta yang sudah dirender
B. Menanyakan atribut fitur pada koordinat/pixel tertentu
C. Mengetahui skema atribut sebuah layer
D. Mengedit fitur pada server

**12. Pada `GetFeatureInfo`, parameter `I` dan `J` mewakili...**
A. Koordinat geografis lon/lat
B. Lebar dan tinggi gambar
C. Index layer dan style
D. Pixel yang diklik pada gambar

**13. Manakah yang merupakan kelebihan (Pro) WMS?**
A. Klien menerima data atribut langsung
B. Mudah di-restyle di klien
C. Cocok untuk layer besar (jutaan fitur) karena server sudah render
D. Bisa diedit langsung dari web

**14. Manakah yang merupakan kekurangan (Con) WMS?**
A. Hanya gambar — tidak ada data atribut langsung di klien
B. Tidak mendukung CRS
C. Tidak bisa menampilkan basemap besar
D. Selalu mengembalikan GeoJSON yang berat

**15. Operasi WFS `DescribeFeatureType` mengembalikan...**
A. Gambar peta
B. Daftar seluruh server OGC
C. File konfigurasi GeoServer
D. Skema atribut: nama field & tipe data

**16. Untuk mengambil hanya fitur dalam area tertentu pada WFS digunakan filter...**
A. CQL_FILTER
B. BBOX
C. STYLES
D. INFO_FORMAT

**17. Apa kepanjangan CQL pada `CQL_FILTER`?**
A. Cartographic Query Language
B. Coordinate Query Layer
C. Common Query Language
D. Complex Query Logic

**18. Filter `CQL_FILTER=kelas='arteri' AND panjang>500` artinya...**
A. Ambil fitur dengan kelas arteri DAN panjang lebih dari 500
B. Ambil semua fitur tanpa filter
C. Ambil fitur kelas arteri ATAU panjang 500
D. Hapus fitur kelas arteri

**19. Operasi tambahan WFS untuk insert/update/delete fitur (advanced) disebut...**
A. GetFeatureInfo
B. DescribeFeatureType
C. GetMap
D. Transaction (WFS-T)

**20. Pada OpenLayers, strategi `ol.loadingstrategy.bbox` untuk WFS berarti...**
A. Memuat seluruh fitur sekaligus saat awal
B. Server hanya mengirim fitur sesuai viewport, berubah saat pan/zoom
C. Menonaktifkan loading fitur
D. Mengubah WFS menjadi WMS

**21. Manakah kelebihan (Pro) WFS dibanding WMS?**
A. Klien mendapat data asli — bisa restyle, query, dan analisis
B. Selalu lebih ringan untuk jutaan fitur
C. Styling ditentukan sepenuhnya di server
D. Tidak memerlukan koneksi internet

**22. Apa masalah WMS biasa yang diselesaikan oleh WMTS?**
A. WMS tidak mendukung vektor
B. WMS tidak punya GetCapabilities
C. WMS me-render gambar tiap request → lambat & sulit di-cache CDN
D. WMS tidak mendukung HTTPS

**23. Ekstensi WMS dengan dimensi waktu (mis. `&TIME=...`) disebut WMS-T dan sangat relevan untuk...**
A. Data administratif statis
B. Layer jalan raya
C. Editing fitur dari web
D. Data temporal seperti radar cuaca BMKG & citra satelit per jam

**24. Format dominan untuk Vector Tiles yang menjadi OGC Community Standard (2018) adalah...**
A. GeoTIFF
B. Mapbox Vector Tile (MVT)
C. Shapefile
D. KML

**25. Format file populer yang menyimpan semua tile dalam satu file dan bisa di-host di S3/GitHub Pages adalah...**
A. GeoPackage
B. GML
C. PMTiles
D. WKT

**26. Generasi baru standar OGC berbasis REST + JSON + OpenAPI. Penerus WFS adalah...**
A. OGC API - Features
B. OGC API - Tiles
C. OGC API - Processes
D. OGC API - Records

**27. Manakah pasangan standar OGC dan fungsinya yang BENAR?**
A. WCS — geoprocessing jarak jauh
B. WPS — data raster mentah
C. WFS — peta sebagai gambar
D. WCS — data raster mentah

**28. Server OGC manakah yang berbasis Java, ber-GUI, dan paling populer untuk general purpose/geoportal?**
A. MapServer
B. GeoServer
C. pg_tileserv
D. pygeoapi

**29. Mengapa `GetCapabilities` disebut sebagai titik mulai eksplorasi server baru?**
A. Karena memuat daftar layer, CRS, format, dan style yang ditawarkan
B. Karena langsung menampilkan peta
C. Karena satu-satunya operasi yang gratis
D. Karena mengembalikan GeoJSON

**30. Penyebab paling umum "peta saya kosong / di tempat aneh" pada WMS adalah...**
A. Format PNG tidak didukung
B. Tidak memakai HTTPS
C. Tertukarnya axis order/BBOX antara versi 1.1.1 dan 1.3.0
D. Lupa memanggil clearWatch()

---

## Bagian B — LBS & Mobile GIS — Soal 31–50

**31. Definisi LBS (Location-Based Services) yang paling tepat adalah...**
A. Layanan yang hanya berjalan di perangkat mobile
B. Layanan peta tanpa internet
C. Standar pertukaran data OGC
D. Layanan yang memanfaatkan posisi geografis pengguna untuk memberi informasi/fungsi relevan

**32. "Cari ATM terdekat" termasuk mode LBS...**
A. Proactive (push)
B. Reactive (pull)
C. Geofencing
D. Hybrid

**33. Notifikasi promo otomatis saat pengguna lewat mall termasuk mode...**
A. Proactive (push) / geofencing
B. Reactive (pull)
C. A-GPS
D. Manual input

**34. Geofencing adalah...**
A. Mengukur jarak antar dua titik
B. Menggabungkan beberapa sumber lokasi
C. Memicu aksi saat pengguna masuk/keluar batas area virtual
D. Mengubah CRS koordinat

**35. Manakah BUKAN salah satu dari lima komponen klasik LBS?**
A. Perangkat (HP, browser)
B. Penyedia posisi (GPS, WiFi)
C. Penyedia konten/data (peta, POI)
D. Kompiler bahasa pemrograman

**36. Sumber lokasi manakah yang paling akurat (5–10 m) tetapi boros baterai dan butuh langit terbuka?**
A. WiFi
B. GPS / GNSS
C. Cell tower
D. IP Address

**37. Sumber lokasi yang paling kasar (akurasi kota/wilayah), biasa dipakai web tanpa GPS, adalah...**
A. IP Address
B. GPS
C. Bluetooth / Beacon
D. WiFi

**38. Apa fungsi A-GPS (Assisted GPS)?**
A. Mengganti GPS dengan WiFi sepenuhnya
B. Menghemat baterai dengan mematikan GPS
C. Mengubah koordinat ke EPSG:3857
D. Memakai data jaringan seluler untuk mempercepat fix GPS

**39. Sebagai developer pada hybrid positioning, kita...**
A. Memilih sumber lokasi secara manual (GPS/WiFi/Cell)
B. Wajib menulis driver GPS sendiri
C. Tidak memilih sumbernya — OS/browser yang menentukan; kita hanya minta tingkat akurasi
D. Harus mematikan WiFi agar akurat

**40. HTML Geolocation API hanya berjalan di context aman, yaitu...**
A. `http://` apa saja
B. `https://` atau `http://localhost`
C. Hanya di aplikasi native
D. Hanya di jaringan LAN

**41. Method manakah yang mengambil posisi pengguna SEKALI saja?**
A. `watchPosition`
B. `clearWatch`
C. `query`
D. `getCurrentPosition`

**42. Method `watchPosition` cocok digunakan untuk...**
A. Navigasi/tracking — dipanggil setiap posisi berubah
B. Mengambil lokasi satu kali saat load
C. Mengecek status izin
D. Menghapus marker

**43. Mengapa penting memanggil `clearWatch()`?**
A. Agar peta berputar
B. Agar GPS tidak terus menyala (hemat baterai)
C. Agar izin otomatis diberikan
D. Agar koordinat menjadi EPSG:4326

**44. Properti `coords.accuracy` menyatakan...**
A. Kecepatan dalam m/s
B. Ketinggian dalam meter
C. Akurasi horizontal dalam meter
D. Arah hadap dalam derajat

**45. Koordinat yang dikembalikan Geolocation API selalu dalam sistem...**
A. EPSG:3857 (Web Mercator)
B. UTM zona 49S
C. EPSG:23837
D. EPSG:4326 / WGS 84 — lon/lat derajat desimal

**46. Pada penanganan error, `error.code` bernilai `PERMISSION_DENIED` artinya...**
A. Pengguna menolak akses lokasi
B. Informasi lokasi tidak tersedia
C. Permintaan timeout
D. Browser tidak mendukung Geolocation

**47. Pada arsitektur LBS, query "cari data dalam jarak/area" (mis. `ST_DWithin`, `ST_Distance`) dikerjakan oleh lapisan...**
A. Client
B. Database spasial
C. Map server
D. CDN

**48. Untuk menghitung jarak antar dua titik lat/lon di permukaan bumi pada demo client-only digunakan fungsi...**
A. ST_DWithin
B. fromLonLat
C. Haversine
D. GetFeatureInfo

**49. Manakah yang BUKAN prinsip privasi LBS yang dianjurkan?**
A. Minta izin secukupnya, saat dibutuhkan saja
B. Kirim lewat HTTPS
C. Simpan lokasi mentah selama mungkin untuk analisis
D. Patuhi regulasi seperti UU PDP

**50. Saat membuka halaman LBS dari HP melalui IP LAN (`http://192.168.x.x`), apa yang terjadi pada Geolocation?**
A. Diblokir karena bukan context aman (HTTP biasa)
B. Berjalan normal
C. Lebih akurat
D. Otomatis memakai mock location

---

## Kunci Jawaban

| No | Jwb | No | Jwb | No | Jwb | No | Jwb | No | Jwb |
|----|-----|----|-----|----|-----|----|-----|----|-----|
| 1  | C   | 11 | B   | 21 | A   | 31 | D   | 41 | D   |
| 2  | A   | 12 | D   | 22 | C   | 32 | B   | 42 | A   |
| 3  | D   | 13 | C   | 23 | D   | 33 | A   | 43 | B   |
| 4  | B   | 14 | A   | 24 | B   | 34 | C   | 44 | C   |
| 5  | A   | 15 | D   | 25 | C   | 35 | D   | 45 | D   |
| 6  | D   | 16 | B   | 26 | A   | 36 | B   | 46 | A   |
| 7  | C   | 17 | C   | 27 | D   | 37 | A   | 47 | B   |
| 8  | B   | 18 | A   | 28 | B   | 38 | D   | 48 | C   |
| 9  | D   | 19 | D   | 29 | A   | 39 | C   | 49 | C   |
| 10 | A   | 20 | B   | 30 | C   | 40 | B   | 50 | A   |

Distribusi kunci: **A = 13, B = 12, C = 12, D = 13**
