/* =========================
   BASE MAPS
========================= */

const basemaps = {
    osm: new ol.source.OSM(),
    carto: new ol.source.XYZ({
        url: 'https://basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png',
        attributions: '© CARTO © OSM'
    }),
    satellite: new ol.source.XYZ({
        url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attributions: '© Esri'
    })
};

const baseLayer = new ol.layer.Tile({ source: basemaps.osm });

/* =========================
   LANDMARKS DATA
========================= */

const landmarks = [
    { name: "Tugu Yogyakarta",   lon: 110.3672, lat: -7.7828, desc: "Ikon kota Yogyakarta", cat: "landmark" },
    { name: "Malioboro",         lon: 110.3655, lat: -7.7925, desc: "Jalan belanja terkenal", cat: "street" },
    { name: "Kraton Yogyakarta", lon: 110.3642, lat: -7.8053, desc: "Istana Kesultanan", cat: "landmark" },
    { name: "Taman Sari",        lon: 110.3590, lat: -7.8098, desc: "Taman air kerajaan", cat: "landmark" },
    { name: "UGM",               lon: 110.3780, lat: -7.7703, desc: "Universitas Gadjah Mada", cat: "university" },
    { name: "Benteng Vredeburg", lon: 110.3656, lat: -7.7991, desc: "Benteng Belanda → museum", cat: "museum" },
    { name: "Pasar Beringharjo", lon: 110.3663, lat: -7.7994, desc: "Pasar tradisional sejak 1758", cat: "market" },
];

/* =========================
   MARKER LAYER (Vector)
========================= */

const markerSource = new ol.source.Vector();

const COLORS = {
    landmark: '#e63946', street: '#f59e0b', university: '#2563eb',
    museum: '#8b5cf6', market: '#059669'
};

landmarks.forEach(lm => {
    const feature = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat([lm.lon, lm.lat])),
        name: lm.name,
        desc: lm.desc,
        cat: lm.cat
    });
    feature.setStyle(new ol.style.Style({
        image: new ol.style.Circle({
            radius: 9,
            fill: new ol.style.Fill({ color: COLORS[lm.cat] || '#e63946' }),
            stroke: new ol.style.Stroke({ color: '#fff', width: 2.5 })
        })
    }));
    markerSource.addFeature(feature);
});

const markerLayer = new ol.layer.Vector({ source: markerSource });

/* =========================
   GEOJSON LAYER
========================= */

const geojsonData = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": { "nama": "Area Malioboro", "ket": "Zona pedestrian & belanja" },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[110.3640,-7.7880],[110.3670,-7.7880],[110.3670,-7.7960],[110.3640,-7.7960],[110.3640,-7.7880]]]
            }
        },
        {
            "type": "Feature",
            "properties": { "nama": "Area Kraton", "ket": "Kompleks keraton & alun-alun" },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[110.3610,-7.7980],[110.3680,-7.7980],[110.3680,-7.8120],[110.3610,-7.8120],[110.3610,-7.7980]]]
            }
        }
    ]
};

const geojsonLayer = new ol.layer.Vector({
    source: new ol.source.Vector({
        features: new ol.format.GeoJSON().readFeatures(geojsonData, {
            dataProjection: 'EPSG:4326',
            featureProjection: 'EPSG:3857'
        })
    }),
    style: new ol.style.Style({
        stroke: new ol.style.Stroke({ color: '#2563eb', width: 2 }),
        fill: new ol.style.Fill({ color: 'rgba(37,99,235,0.12)' })
    })
});

/* =========================
   MAP
========================= */

const map = new ol.Map({
    target: 'map',
    layers: [baseLayer, geojsonLayer, markerLayer],
    view: new ol.View({
        center: ol.proj.fromLonLat([110.3695, -7.7956]),
        zoom: 14,
        maxZoom: 18
    })
});

/* =========================
   POPUP (Overlay)
========================= */

const popupEl = document.createElement('div');
popupEl.className = 'ol-popup';
document.body.appendChild(popupEl);

const overlay = new ol.Overlay({
    element: popupEl,
    positioning: 'bottom-center'
});
map.addOverlay(overlay);

map.on('click', (e) => {
    const feature = map.forEachFeatureAtPixel(e.pixel, f => f);
    if (feature && feature.get('name')) {
        popupEl.innerHTML = `<b>${feature.get('name')}</b><br><em>${feature.get('cat')}</em><br>${feature.get('desc')}`;
        overlay.setPosition(e.coordinate);
    } else if (feature && feature.get('nama')) {
        popupEl.innerHTML = `<b>${feature.get('nama')}</b><br>${feature.get('ket')}`;
        overlay.setPosition(e.coordinate);
    } else {
        overlay.setPosition(undefined);
    }
});

// Cursor change on hover
map.on('pointermove', (e) => {
    const hit = map.hasFeatureAtPixel(e.pixel);
    map.getTargetElement().style.cursor = hit ? 'pointer' : '';
});

/* =========================
   BASEMAP SWITCHER
========================= */

document.querySelectorAll('#basemap-switcher button').forEach(btn => {
    btn.addEventListener('click', () => {
        const key = btn.dataset.basemap;
        if (basemaps[key]) {
            baseLayer.setSource(basemaps[key]);
            document.querySelectorAll('#basemap-switcher button').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        }
    });
});

/* =========================
   SCALE BAR
========================= */

map.addControl(new ol.control.ScaleLine());
