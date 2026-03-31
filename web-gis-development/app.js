/* =========================
   BASE MAPS
========================= */

const basemaps = {
  osm: new ol.source.OSM(),
  carto: new ol.source.XYZ({
    url: "https://basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png",
    attributions: "© CARTO © OSM",
  }),
  satellite: new ol.source.XYZ({
    url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attributions: "© Esri",
  }),
};

const baseLayer = new ol.layer.Tile({ source: basemaps.osm });

/* =========================
   LANDMARKS DATA
========================= */

const landmarks = [
  {
    name: "Tugu Yogyakarta",
    lon: 110.3672,
    lat: -7.7828,
    desc: "Ikon kota Yogyakarta",
    cat: "landmark",
  },
  {
    name: "Malioboro",
    lon: 110.3655,
    lat: -7.7925,
    desc: "Jalan belanja terkenal",
    cat: "street",
  },
  {
    name: "Kraton Yogyakarta",
    lon: 110.3642,
    lat: -7.8053,
    desc: "Istana Kesultanan",
    cat: "landmark",
  },
  {
    name: "Taman Sari",
    lon: 110.359,
    lat: -7.8098,
    desc: "Taman air kerajaan",
    cat: "landmark",
  },
  {
    name: "UGM",
    lon: 110.378,
    lat: -7.7703,
    desc: "Universitas Gadjah Mada",
    cat: "university",
  },
  {
    name: "Benteng Vredeburg",
    lon: 110.3656,
    lat: -7.7991,
    desc: "Benteng Belanda → museum",
    cat: "museum",
  },
  {
    name: "Pasar Beringharjo",
    lon: 110.3663,
    lat: -7.7994,
    desc: "Pasar tradisional sejak 1758",
    cat: "market",
  },
];

/* =========================
   MARKER LAYER (Vector)
========================= */

const markerSource = new ol.source.Vector();

const COLORS = {
  landmark: "#e63946",
  street: "#f59e0b",
  university: "#2563eb",
  museum: "#8b5cf6",
  market: "#059669",
};

landmarks.forEach((lm) => {
  const feature = new ol.Feature({
    geometry: new ol.geom.Point(ol.proj.fromLonLat([lm.lon, lm.lat])),
    name: lm.name,
    desc: lm.desc,
    cat: lm.cat,
  });
  feature.setStyle(
    new ol.style.Style({
      image: new ol.style.Circle({
        radius: 9,
        fill: new ol.style.Fill({ color: COLORS[lm.cat] || "#e63946" }),
        stroke: new ol.style.Stroke({ color: "#fff", width: 2.5 }),
      }),
    }),
  );
  markerSource.addFeature(feature);
});

const markerLayer = new ol.layer.Vector({ source: markerSource });

/* =========================
   GEOJSON LAYER
========================= */

const geojsonData = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      properties: { nama: "Area Malioboro", ket: "Zona pedestrian & belanja" },
      geometry: {
        type: "Polygon",
        coordinates: [
          [
            [110.364, -7.788],
            [110.367, -7.788],
            [110.367, -7.796],
            [110.364, -7.796],
            [110.364, -7.788],
          ],
        ],
      },
    },
    {
      type: "Feature",
      properties: { nama: "Area Kraton", ket: "Kompleks keraton & alun-alun" },
      geometry: {
        type: "Polygon",
        coordinates: [
          [
            [110.361, -7.798],
            [110.368, -7.798],
            [110.368, -7.812],
            [110.361, -7.812],
            [110.361, -7.798],
          ],
        ],
      },
    },
  ],
};

const geojsonLayer = new ol.layer.Vector({
  source: new ol.source.Vector({
    features: new ol.format.GeoJSON().readFeatures(geojsonData, {
      dataProjection: "EPSG:4326",
      featureProjection: "EPSG:3857",
    }),
  }),
  style: new ol.style.Style({
    stroke: new ol.style.Stroke({ color: "#2563eb", width: 2 }),
    fill: new ol.style.Fill({ color: "rgba(37,99,235,0.12)" }),
  }),
});

/* =========================
   MAP
========================= */

const map = new ol.Map({
  target: "map",
  controls: ol.control.defaults.defaults({
    zoom: false,
    attribution: false,
    rotate: false,
  }),
  layers: [baseLayer, geojsonLayer, markerLayer],
  view: new ol.View({
    center: ol.proj.fromLonLat([110.3695, -7.7956]),
    zoom: 14,
    maxZoom: 18,
  }),
});

/* =========================
   POPUP (Overlay)
========================= */

const popupEl = document.createElement("div");
popupEl.className = "ol-popup";
document.body.appendChild(popupEl);

const overlay = new ol.Overlay({
  element: popupEl,
  positioning: "bottom-center",
});
map.addOverlay(overlay);

map.on("click", (e) => {
  const feature = map.forEachFeatureAtPixel(e.pixel, (f) => f);
  if (feature && feature.get("name")) {
    popupEl.innerHTML = `<b>${feature.get("name")}</b><br><em>${feature.get("cat")}</em><br>${feature.get("desc")}`;
    overlay.setPosition(e.coordinate);
  } else if (feature && feature.get("nama")) {
    popupEl.innerHTML = `<b>${feature.get("nama")}</b><br>${feature.get("ket")}`;
    overlay.setPosition(e.coordinate);
  } else {
    overlay.setPosition(undefined);
  }
});

// Cursor change on hover
map.on("pointermove", (e) => {
  const hit = map.hasFeatureAtPixel(e.pixel);
  map.getTargetElement().style.cursor = hit ? "pointer" : "";
});

/* =========================
   BASEMAP SWITCHER
========================= */

document.querySelectorAll("#basemap-switcher button").forEach((btn) => {
  btn.addEventListener("click", () => {
    const key = btn.dataset.basemap;
    if (basemaps[key]) {
      baseLayer.setSource(basemaps[key]);
      document
        .querySelectorAll("#basemap-switcher button")
        .forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      updateAttribution();
    }
  });
});

document.getElementById("zoom-in").addEventListener("click", () => {
  const view = map.getView();
  view.animate({ zoom: view.getZoom() + 1, duration: 200 });
});

document.getElementById("zoom-out").addEventListener("click", () => {
  const view = map.getView();
  view.animate({ zoom: view.getZoom() - 1, duration: 200 });
});

function updateAttribution() {
  const attributionEl = document.getElementById("attribution-display");
  const currentSource = baseLayer.getSource();
  const attributions = currentSource.getAttributions?.() || [];
  const resolved =
    typeof attributions === "function"
      ? attributions(map.getView())
      : attributions;
  const values = Array.isArray(resolved) ? resolved : [resolved];
  attributionEl.innerHTML =
    values.filter(Boolean).join(" · ") || "© OpenStreetMap contributors";
}

function formatScale(lengthMeters) {
  if (lengthMeters >= 1000) {
    return `${(lengthMeters / 1000).toFixed(lengthMeters >= 10000 ? 0 : 1)} km`;
  }
  return `${Math.round(lengthMeters)} m`;
}

function updateScale() {
  const scaleTextEl = document.getElementById("scale-text");
  const scaleBarEl = document.getElementById("scale-bar");
  const view = map.getView();
  const resolution = view.getResolution();
  const center = view.getCenter();

  if (!resolution || !center) {
    return;
  }

  const pointResolution = ol.proj.getPointResolution(
    view.getProjection(),
    resolution,
    center,
    "m",
  );
  const targetPx = 100;
  const nominalLength = pointResolution * targetPx;
  const steps = [1, 2, 5];
  const magnitude = 10 ** Math.floor(Math.log10(nominalLength));

  let displayLength = magnitude;
  for (const step of steps) {
    const candidate = step * magnitude;
    if (candidate >= nominalLength) {
      displayLength = candidate;
      break;
    }
  }

  const pixelWidth = displayLength / pointResolution;
  scaleTextEl.textContent = formatScale(displayLength);
  scaleBarEl.style.width = `${Math.round(pixelWidth)}px`;
}

map.on("moveend", () => {
  updateScale();
  updateAttribution();
});

updateScale();
updateAttribution();
