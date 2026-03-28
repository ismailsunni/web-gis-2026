/* =========================
   BASE MAPS
========================= */

const osmLayer = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
});

const satellite = L.tileLayer(
    'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: 18,
    attribution: '© Esri'
});

const cartoLight = L.tileLayer('https://basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© <a href="https://carto.com/">CARTO</a> © OSM'
});

/* =========================
   MAP INITIALIZATION
========================= */

const map = L.map('map', {
    layers: [osmLayer]
}).setView([-7.7956, 110.3695], 14);

/* =========================
   LANDMARKS DATA
========================= */

const landmarks = [
    { name: "Tugu Yogyakarta",   lat: -7.7828, lng: 110.3672, desc: "Ikon kota Yogyakarta, dibangun oleh Sultan HB I", category: "landmark" },
    { name: "Malioboro",         lat: -7.7925, lng: 110.3655, desc: "Jalan belanja dan wisata paling terkenal", category: "street" },
    { name: "Kraton Yogyakarta", lat: -7.8053, lng: 110.3642, desc: "Istana resmi Kesultanan Ngayogyakarta Hadiningrat", category: "landmark" },
    { name: "Taman Sari",        lat: -7.8098, lng: 110.3590, desc: "Bekas taman kerajaan dengan kolam pemandian", category: "landmark" },
    { name: "UGM",               lat: -7.7703, lng: 110.3780, desc: "Universitas Gadjah Mada — kampus tertua", category: "university" },
    { name: "Benteng Vredeburg", lat: -7.7991, lng: 110.3656, desc: "Benteng peninggalan Belanda, kini museum", category: "museum" },
    { name: "Pasar Beringharjo", lat: -7.7994, lng: 110.3663, desc: "Pasar tradisional sejak 1758", category: "market" },
];

/* =========================
   MARKERS WITH POPUPS
========================= */

const markerGroup = L.layerGroup();

landmarks.forEach(lm => {
    const marker = L.marker([lm.lat, lm.lng])
        .bindPopup(`
            <b>${lm.name}</b><br>
            <em>${lm.category}</em><br>
            ${lm.desc}
        `);
    markerGroup.addLayer(marker);
});

markerGroup.addTo(map);

/* =========================
   GEOJSON DATA
========================= */

const geojsonData = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": { "nama": "Area Malioboro", "keterangan": "Zona pedestrian & belanja" },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[110.3640, -7.7880], [110.3670, -7.7880],
                                 [110.3670, -7.7960], [110.3640, -7.7960],
                                 [110.3640, -7.7880]]]
            }
        },
        {
            "type": "Feature",
            "properties": { "nama": "Area Kraton", "keterangan": "Kompleks keraton & alun-alun" },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[110.3610, -7.7980], [110.3680, -7.7980],
                                 [110.3680, -7.8120], [110.3610, -7.8120],
                                 [110.3610, -7.7980]]]
            }
        }
    ]
};

const geojsonLayer = L.geoJSON(geojsonData, {
    style: {
        color: "#ff7800",
        weight: 2,
        fillOpacity: 0.15
    },
    onEachFeature: (feature, layer) => {
        if (feature.properties) {
            layer.bindPopup(`<b>${feature.properties.nama}</b><br>${feature.properties.keterangan}`);
        }
    }
});

geojsonLayer.addTo(map);

/* =========================
   LAYER CONTROL
========================= */

const baseMaps = {
    "OpenStreetMap": osmLayer,
    "Satelit": satellite,
    "Minimalis": cartoLight
};

const overlayMaps = {
    "Landmarks": markerGroup,
    "Area (GeoJSON)": geojsonLayer
};

L.control.layers(baseMaps, overlayMaps).addTo(map);

/* =========================
   SCALE BAR
========================= */

L.control.scale({ imperial: false }).addTo(map);
