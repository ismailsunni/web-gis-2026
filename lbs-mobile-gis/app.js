/* =========================
   LBS DEMO — "Apa yang Ada di Sekitar Saya?"
   Konsep LBS lengkap TANPA backend:
   - HTML Geolocation API (getCurrentPosition / watchPosition)
   - Marker posisi pengguna + lingkaran akurasi
   - Hitung jarak Haversine ke tiap POI → urutkan terdekat
   - Tangani izin ditolak / timeout / tidak tersedia
========================= */

/* =========================
   DATA POI (inline GeoJSON-ish)
   Sekitar UGM / Yogyakarta. Ganti dengan data kalian sendiri.
   Koordinat: EPSG:4326 (lon, lat) derajat desimal.
========================= */

const POIS = [
  { nama: "Tugu Yogyakarta", kategori: "Landmark", lon: 110.3671, lat: -7.7829 },
  { nama: "Malioboro", kategori: "Wisata", lon: 110.3658, lat: -7.7926 },
  { nama: "Kraton Yogyakarta", kategori: "Wisata", lon: 110.3644, lat: -7.8053 },
  { nama: "Kampus UGM", kategori: "Kampus", lon: 110.3789, lat: -7.7713 },
  { nama: "Sekolah Vokasi UGM", kategori: "Kampus", lon: 110.3760, lat: -7.7750 },
  { nama: "Stasiun Tugu", kategori: "Transportasi", lon: 110.3637, lat: -7.7892 },
  { nama: "Pasar Beringharjo", kategori: "Pasar", lon: 110.3669, lat: -7.7975 },
  { nama: "Alun-Alun Kidul", kategori: "Wisata", lon: 110.3639, lat: -7.8121 },
  { nama: "RS Sardjito", kategori: "Kesehatan", lon: 110.3742, lat: -7.7686 },
  { nama: "Lembah UGM", kategori: "Olahraga", lon: 110.3736, lat: -7.7651 },
  { nama: "Galeria Mall", kategori: "Belanja", lon: 110.3815, lat: -7.7836 },
  { nama: "Tugu Pal Putih (titik nol)", kategori: "Landmark", lon: 110.3656, lat: -7.8014 },
];

const INITIAL_CENTER = [110.3695, -7.7956]; // Yogyakarta
const INITIAL_ZOOM = 13;
const MAX_LIST = 5; // berapa POI terdekat ditampilkan

/* =========================
   HAVERSINE — jarak (km) antar dua titik lon/lat di permukaan bumi
========================= */

function haversine([lon1, lat1], [lon2, lat2]) {
  const R = 6371; // radius bumi (km)
  const toRad = (d) => (d * Math.PI) / 180;
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

function formatJarak(km) {
  return km < 1 ? `${Math.round(km * 1000)} m` : `${km.toFixed(2)} km`;
}

/* =========================
   BASEMAP & MAP
========================= */

const baseLayer = new ol.layer.Tile({ source: new ol.source.OSM() });

/* POI layer — vektor dari data inline */
const poiSource = new ol.source.Vector();
POIS.forEach((p) => {
  const feature = new ol.Feature({
    geometry: new ol.geom.Point(ol.proj.fromLonLat([p.lon, p.lat])),
    data: p,
  });
  poiSource.addFeature(feature);
});

const poiLayer = new ol.layer.Vector({
  source: poiSource,
  style: new ol.style.Style({
    image: new ol.style.Circle({
      radius: 6,
      fill: new ol.style.Fill({ color: "#db2777" }),
      stroke: new ol.style.Stroke({ color: "#fff", width: 2 }),
    }),
  }),
});

/* Layer untuk posisi pengguna + lingkaran akurasi */
const meSource = new ol.source.Vector();
const meLayer = new ol.layer.Vector({
  source: meSource,
  style: (feature) => {
    if (feature.get("type") === "accuracy") {
      return new ol.style.Style({
        fill: new ol.style.Fill({ color: "rgba(37, 99, 235, 0.12)" }),
        stroke: new ol.style.Stroke({ color: "rgba(37, 99, 235, 0.4)", width: 1 }),
      });
    }
    return new ol.style.Style({
      image: new ol.style.Circle({
        radius: 8,
        fill: new ol.style.Fill({ color: "#2563eb" }),
        stroke: new ol.style.Stroke({ color: "#fff", width: 3 }),
      }),
    });
  },
});

const map = new ol.Map({
  target: "map",
  layers: [baseLayer, poiLayer, meLayer],
  controls: [], // no default OL controls; pan/zoom via mouse, scroll, pinch
  view: new ol.View({
    center: ol.proj.fromLonLat(INITIAL_CENTER),
    zoom: INITIAL_ZOOM,
  }),
});

/* =========================
   POPUP
========================= */

const popupEl = document.createElement("div");
popupEl.className = "ol-popup";
popupEl.style.display = "none";
document.body.appendChild(popupEl);

const overlay = new ol.Overlay({
  element: popupEl,
  positioning: "bottom-center",
  stopEvent: false,
});
map.addOverlay(overlay);

map.on("click", (e) => {
  const feature = map.forEachFeatureAtPixel(e.pixel, (f) => f, {
    layerFilter: (l) => l === poiLayer,
  });
  if (feature) {
    const p = feature.get("data");
    popupEl.innerHTML = `<b>${p.nama}</b><br><span class="cat">${p.kategori}</span>`;
    popupEl.style.display = "block";
    overlay.setPosition(feature.getGeometry().getCoordinates());
  } else {
    popupEl.style.display = "none";
    overlay.setPosition(undefined);
  }
});

map.on("pointermove", (e) => {
  if (e.dragging) return;
  const hit = map.hasFeatureAtPixel(e.pixel, { layerFilter: (l) => l === poiLayer });
  map.getTargetElement().style.cursor = hit ? "pointer" : "";
});

/* =========================
   STATUS PANEL
========================= */

const statusEl = document.getElementById("status");

function setStatus(kind, html) {
  const label = { ok: "OK", warn: "Perhatian", err: "Error", info: "Info" }[kind];
  statusEl.innerHTML = `<span class="tag ${kind}">${label}</span><br>${html}`;
}

/* =========================
   RENDER POSISI PENGGUNA
========================= */

function updateMe(lon, lat, accuracy) {
  meSource.clear();

  const center = ol.proj.fromLonLat([lon, lat]);
  const point = new ol.Feature({ geometry: new ol.geom.Point(center) });
  point.set("type", "me");

  // Lingkaran akurasi: radius dalam meter, dikonversi ke satuan proyeksi peta
  const resolutionFactor = ol.proj
    .getPointResolution("EPSG:3857", 1, center);
  const radius = accuracy / resolutionFactor;
  const circle = new ol.Feature({
    geometry: new ol.geom.Circle(center, radius),
  });
  circle.set("type", "accuracy");

  meSource.addFeatures([circle, point]);
}

/* =========================
   POI TERDEKAT
========================= */

function renderTerdekat(lon, lat) {
  const withDist = POIS.map((p) => ({
    ...p,
    jarak: haversine([lon, lat], [p.lon, p.lat]),
  })).sort((a, b) => a.jarak - b.jarak);

  const listEl = document.getElementById("poi-list");
  const emptyEl = document.getElementById("poi-empty");
  emptyEl.style.display = "none";

  listEl.innerHTML = withDist
    .slice(0, MAX_LIST)
    .map(
      (p) => `
      <div class="poi-item">
        <div>
          <div class="name">${p.nama}</div>
          <div class="cat">${p.kategori}</div>
        </div>
        <div class="dist">${formatJarak(p.jarak)}</div>
      </div>`,
    )
    .join("");

  return withDist[0];
}

/* =========================
   GEOLOCATION — getCurrentPosition
========================= */

const btnLocate = document.getElementById("btn-locate");
const btnWatch = document.getElementById("btn-watch");
const toggleAccuracy = document.getElementById("toggle-accuracy");

function geoOptions() {
  return {
    enableHighAccuracy: toggleAccuracy.checked,
    timeout: 10000,
    maximumAge: 0,
  };
}

function onPosition(position, { recenter } = {}) {
  const { latitude: lat, longitude: lon, accuracy } = position.coords;

  updateMe(lon, lat, accuracy);
  const terdekat = renderTerdekat(lon, lat);

  if (recenter) {
    map.getView().animate({
      center: ol.proj.fromLonLat([lon, lat]),
      zoom: Math.max(map.getView().getZoom(), 14),
      duration: 500,
    });
  }

  setStatus(
    "ok",
    `Posisi: <code>${lat.toFixed(5)}, ${lon.toFixed(5)}</code><br>
     Akurasi: ±${Math.round(accuracy)} m<br>
     Terdekat: <b>${terdekat.nama}</b> (${formatJarak(terdekat.jarak)})`,
  );
}

function onError(error) {
  let msg;
  switch (error.code) {
    case error.PERMISSION_DENIED:
      msg = `Akses lokasi <b>ditolak</b>. Aktifkan izin lokasi di browser,
             atau gunakan lokasi default (peta tetap menampilkan POI).`;
      break;
    case error.POSITION_UNAVAILABLE:
      msg = "Informasi lokasi tidak tersedia. Coba lagi di area dengan sinyal lebih baik.";
      break;
    case error.TIMEOUT:
      msg = `Permintaan lokasi <b>timeout</b>. Coba matikan "Akurasi tinggi" lalu ulangi.`;
      break;
    default:
      msg = error.message;
  }
  setStatus("err", msg);
}

if (!("geolocation" in navigator)) {
  setStatus("err", "Browser ini tidak mendukung Geolocation API.");
  btnLocate.disabled = true;
  btnWatch.disabled = true;
}

btnLocate.addEventListener("click", () => {
  setStatus("info", "Meminta izin & mengambil lokasi…");
  navigator.geolocation.getCurrentPosition(
    (pos) => onPosition(pos, { recenter: true }),
    onError,
    geoOptions(),
  );
});

/* =========================
   GEOLOCATION — watchPosition
   Pantau terus; ingat clearWatch() untuk hemat baterai.
========================= */

let watchId = null;
let firstWatchFix = true;

btnWatch.addEventListener("click", () => {
  if (watchId === null) {
    firstWatchFix = true;
    setStatus("info", "Memantau pergerakan… (watchPosition aktif)");
    watchId = navigator.geolocation.watchPosition(
      (pos) => {
        onPosition(pos, { recenter: firstWatchFix });
        firstWatchFix = false;
      },
      onError,
      geoOptions(),
    );
    btnWatch.textContent = "■ Hentikan (clearWatch)";
    btnWatch.classList.add("active");
  } else {
    navigator.geolocation.clearWatch(watchId);
    watchId = null;
    btnWatch.textContent = "▶ Ikuti pergerakan (watch)";
    btnWatch.classList.remove("active");
    setStatus("warn", "Pemantauan dihentikan. Sensor lokasi dimatikan (hemat baterai).");
  }
});
