// Cities web map: Leaflet frontend for the Week 3 Cities API.
// Data source: GET /api/cities/geojson/  (GeoJSON FeatureCollection, paginated)

const DUBLIN = [53.3498, -6.2603];
const API_URL = '/api/cities/geojson/?page_size=100';   // 100 is the API's max page size

const map = L.map('map').setView(DUBLIN, 5);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 19,
    minZoom: 2
}).addTo(map);

let citiesData = [];   // flat list of city objects (see featureToCity)
let markers = {};      // city id -> Leaflet marker
const markerLayer = L.layerGroup().addTo(map);

// ---------------------------------------------------------------- data

// GeoJSON Feature -> flat city object. GeoJSON order is [lng, lat].
function featureToCity(feature) {
    const [lng, lat] = feature.geometry.coordinates;
    return {
        id: feature.id ?? feature.properties.id,
        ...feature.properties,
        latitude: lat,
        longitude: lng
    };
}

// The API returns 20..100 features per page; follow `next` until the end.
async function fetchAllCities() {
    const cities = [];
    let url = API_URL;
    while (url) {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status} (${url})`);
        }
        const data = await response.json();
        cities.push(...data.features.map(featureToCity));
        // `next` is an absolute URL; keep only path + query so it works from any host
        url = data.next ? new URL(data.next).pathname + new URL(data.next).search : null;
    }
    return cities;
}

async function initMap() {
    showLoading(true);
    try {
        citiesData = await fetchAllCities();
        document.getElementById('cityTotal').textContent = citiesData.length;
        addMarkersToMap(citiesData);
        fitToCities(citiesData);
    } catch (error) {
        console.error('Error fetching cities:', error);
        alert('Failed to load cities data. Check the browser console and `docker compose logs web`.');
    } finally {
        showLoading(false);
    }
}

// ------------------------------------------------------------- markers

function addMarkersToMap(cities) {
    markerLayer.clearLayers();
    markers = {};

    cities.forEach(city => {
        const lat = Number(city.latitude);
        const lng = Number(city.longitude);
        if (!Number.isFinite(lat) || !Number.isFinite(lng)) {
            console.warn(`Invalid coordinates for ${city.name}`);
            return;
        }

        // Radius grows with population; capitals are orange
        const radius = Math.min(14, Math.max(5, Math.sqrt(city.population) / 400));
        const marker = L.circleMarker([lat, lng], {
            radius,
            fillColor: city.is_capital ? '#fd7e14' : '#007bff',
            color: city.is_capital ? '#c2590a' : '#0056b3',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.8
        });
        marker.bindPopup(createPopupContent(city));
        marker.addTo(markerLayer);
        markers[city.id] = marker;
    });

    document.getElementById('cityCount').textContent = Object.keys(markers).length;
}

function fitToCities(cities) {
    const points = cities.map(c => [c.latitude, c.longitude]);
    if (points.length === 1) {
        map.setView(points[0], 9);
    } else if (points.length > 1) {
        map.fitBounds(points, { padding: [40, 40] });
    }
}

// City names etc. come from the database, so escape before using innerHTML
function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g, ch => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[ch]));
}

function formatNumber(num) {
    return Number(num).toLocaleString('en-IE');
}

function createPopupContent(city) {
    return `
        <div class="city-popup">
            <h3>${escapeHtml(city.name)}${city.is_capital ? ' ★' : ''}</h3>
            <p><strong>Country:</strong> ${escapeHtml(city.country)}</p>
            ${city.region ? `<p><strong>Region:</strong> ${escapeHtml(city.region)}</p>` : ''}
            <p><strong>Population:</strong> ${formatNumber(city.population)}
               (${escapeHtml(city.population_category)})</p>
            <p><strong>Coordinates:</strong> ${Number(city.latitude).toFixed(4)}, ${Number(city.longitude).toFixed(4)}</p>
            ${city.elevation_m !== null && city.elevation_m !== undefined
                ? `<p><strong>Elevation:</strong> ${city.elevation_m} m</p>` : ''}
            ${city.founded_year !== null && city.founded_year !== undefined
                ? `<p><strong>Founded:</strong> ${Math.abs(city.founded_year)}${city.founded_year < 0 ? ' BC' : ''}</p>` : ''}
            ${city.timezone ? `<p><strong>Timezone:</strong> ${escapeHtml(city.timezone)}</p>` : ''}
        </div>
    `;
}

// -------------------------------------------------------------- search

const searchInput = document.getElementById('searchInput');
const resultsDiv = document.getElementById('results');

searchInput.addEventListener('input', function (e) {
    const query = e.target.value.trim().toLowerCase();

    if (query.length === 0) {
        resultsDiv.innerHTML = '';
        addMarkersToMap(citiesData);
        return;
    }

    const filtered = citiesData.filter(city =>
        city.name.toLowerCase().includes(query) ||
        city.country.toLowerCase().includes(query)
    );

    addMarkersToMap(filtered);

    if (filtered.length === 0) {
        resultsDiv.innerHTML = '<p class="no-results">No cities found</p>';
        return;
    }

    resultsDiv.innerHTML = filtered.map(city => `
        <div class="result-item" data-city-id="${city.id}">
            <strong>${escapeHtml(city.name)}</strong>, ${escapeHtml(city.country)}
        </div>
    `).join('');
    fitToCities(filtered);
});

// One delegated click handler instead of inline onclick attributes
resultsDiv.addEventListener('click', function (e) {
    const item = e.target.closest('.result-item');
    if (item) goToCity(Number(item.dataset.cityId));
});

function goToCity(cityId) {
    const city = citiesData.find(c => c.id === cityId);
    if (!city) return;
    map.setView([city.latitude, city.longitude], 10);
    if (markers[cityId]) markers[cityId].openPopup();
}

document.getElementById('resetBtn').addEventListener('click', function () {
    searchInput.value = '';
    resultsDiv.innerHTML = '';
    addMarkersToMap(citiesData);
    fitToCities(citiesData);
});

// ------------------------------------------------------------- helpers

function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
}

document.addEventListener('DOMContentLoaded', initMap);
