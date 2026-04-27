/* =========================
   CONFIG — edit these to point at your GeoServer
========================= */

const GEOSERVER_BASE = "http://localhost:8080/geoserver";
const WORKSPACE = "topp";        // contoh bawaan GeoServer
const LAYER = "states";          // layer di workspace tersebut
const INITIAL_CENTER = [-98.5, 39.5]; // [lon, lat] — disesuaikan layer
const INITIAL_ZOOM = 4;

const QUALIFIED_LAYER = `${WORKSPACE}:${LAYER}`;
const WMS_URL = `${GEOSERVER_BASE}/wms`;
const WFS_URL = `${GEOSERVER_BASE}/wfs`;

/* =========================
   BASEMAP
========================= */

const baseLayer = new ol.layer.Tile({ source: new ol.source.OSM() });

/* =========================
   WMS LAYER
========================= */

const wmsSource = new ol.source.TileWMS({
  url: WMS_URL,
  params: {
    LAYERS: QUALIFIED_LAYER,
    TILED: true,
  },
  serverType: "geoserver",
  crossOrigin: "anonymous",
});

const wmsLayer = new ol.layer.Tile({
  source: wmsSource,
  opacity: 0.85,
});

wmsSource.on("tileloadstart", (e) => {
  logRequest("wms", e.tile.src_ || "(WMS GetMap tile)");
});

/* =========================
   WFS LAYER
========================= */

const wfsSource = new ol.source.Vector({
  format: new ol.format.GeoJSON(),
  url: (extent) => {
    const url =
      `${WFS_URL}?service=WFS&version=2.0.0&request=GetFeature` +
      `&typename=${encodeURIComponent(QUALIFIED_LAYER)}` +
      `&outputFormat=application/json` +
      `&srsname=EPSG:3857` +
      `&bbox=${extent.join(",")},EPSG:3857`;
    logRequest("wfs", url);
    return url;
  },
  strategy: ol.loadingstrategy.bbox,
});

const wfsLayer = new ol.layer.Vector({
  source: wfsSource,
  style: new ol.style.Style({
    stroke: new ol.style.Stroke({ color: "#059669", width: 2 }),
    fill: new ol.style.Fill({ color: "rgba(5, 150, 105, 0.08)" }),
    image: new ol.style.Circle({
      radius: 6,
      fill: new ol.style.Fill({ color: "#059669" }),
      stroke: new ol.style.Stroke({ color: "#fff", width: 2 }),
    }),
  }),
});

/* =========================
   MAP
========================= */

const map = new ol.Map({
  target: "map",
  layers: [baseLayer, wmsLayer, wfsLayer],
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

function showPopup(coord, html) {
  popupEl.innerHTML = html;
  popupEl.style.display = "block";
  overlay.setPosition(coord);
}

function hidePopup() {
  popupEl.style.display = "none";
  overlay.setPosition(undefined);
}

function propsTable(props, skipKeys = ["geometry"]) {
  const rows = Object.entries(props)
    .filter(([k]) => !skipKeys.includes(k))
    .slice(0, 10)
    .map(([k, v]) => `<tr><td>${k}</td><td>${v}</td></tr>`)
    .join("");
  return `<table>${rows}</table>`;
}

/* =========================
   CLICK HANDLER:
   - WFS: data sudah di klien → langsung baca properties
   - WMS: tidak ada fitur di klien → kirim GetFeatureInfo
========================= */

map.on("click", (e) => {
  hidePopup();

  // 1. Cek WFS feature dulu (vektor di klien)
  if (wfsLayer.getVisible()) {
    const feature = map.forEachFeatureAtPixel(
      e.pixel,
      (f) => f,
      { layerFilter: (l) => l === wfsLayer },
    );
    if (feature) {
      const props = feature.getProperties();
      showPopup(
        e.coordinate,
        `<span class="src-tag wfs">WFS</span>
         <b>Feature dari WFS</b>
         ${propsTable(props)}`,
      );
      return;
    }
  }

  // 2. Fallback: WMS GetFeatureInfo
  if (wmsLayer.getVisible()) {
    const viewResolution = map.getView().getResolution();
    const url = wmsSource.getFeatureInfoUrl(
      e.coordinate,
      viewResolution,
      "EPSG:3857",
      {
        INFO_FORMAT: "application/json",
        FEATURE_COUNT: 5,
      },
    );
    if (!url) return;
    logRequest("gfi", url);
    fetch(url)
      .then((r) => (r.ok ? r.json() : null))
      .then((data) => {
        if (!data || !data.features || data.features.length === 0) {
          showPopup(
            e.coordinate,
            `<span class="src-tag wms">WMS</span>
             <b>GetFeatureInfo</b><br>
             <em>Tidak ada fitur di koordinat ini.</em>`,
          );
          return;
        }
        const f = data.features[0];
        showPopup(
          e.coordinate,
          `<span class="src-tag wms">WMS</span>
           <b>GetFeatureInfo</b>
           ${propsTable(f.properties || {})}`,
        );
      })
      .catch((err) => {
        showPopup(
          e.coordinate,
          `<span class="src-tag wms">WMS</span>
           <b>GetFeatureInfo gagal</b><br>
           <em>${err.message}</em><br>
           Cek CORS &amp; URL GeoServer.`,
        );
      });
  }
});

map.on("pointermove", (e) => {
  if (e.dragging) return;
  const hit = map.hasFeatureAtPixel(e.pixel, {
    layerFilter: (l) => l === wfsLayer,
  });
  map.getTargetElement().style.cursor = hit ? "pointer" : "";
});

/* =========================
   LAYER TOGGLES
========================= */

document.getElementById("toggle-wms").addEventListener("change", (e) => {
  wmsLayer.setVisible(e.target.checked);
});

document.getElementById("toggle-wfs").addEventListener("change", (e) => {
  wfsLayer.setVisible(e.target.checked);
});

/* =========================
   REQUEST LOG (didactic)
========================= */

const logEntriesEl = document.getElementById("request-log-entries");
const MAX_LOG_ENTRIES = 8;

function logRequest(kind, url) {
  const entry = document.createElement("div");
  entry.className = "entry";
  const label = kind === "gfi" ? "GFI" : kind.toUpperCase();
  entry.innerHTML = `<span class="label ${kind}">${label}</span>${shortenUrl(url)}`;
  logEntriesEl.prepend(entry);
  while (logEntriesEl.children.length > MAX_LOG_ENTRIES) {
    logEntriesEl.removeChild(logEntriesEl.lastChild);
  }
}

function shortenUrl(url) {
  if (url.length <= 240) return url;
  return url.slice(0, 220) + "…" + url.slice(-16);
}
