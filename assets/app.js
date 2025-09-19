/**
 * Best Muscat client-side application logic.
 * This script powers both the index (listings) page and the detail page.
 * It handles fetching the canonical dataset, applying filters and sort orders,
 * computing open/closed status, and rendering cards and detail views.
 */

/* global window, document */

// In-memory cache of places loaded from data/places.json.
let PLACES_CACHE = null;

/**
 * Fetch the canonical list of places. The result is cached.
 * @returns {Promise<Array>} A promise that resolves to an array of place objects.
 */
async function loadPlaces() {
  if (Array.isArray(PLACES_CACHE)) {
    return PLACES_CACHE;
  }
  const res = await fetch('data/places.json');
  const data = await res.json();
  PLACES_CACHE = data;
  return data;
}
window.loadPlaces = loadPlaces;

/**
 * Parse "HH:MM" into minutes since midnight.
 * @param {string} str
 * @returns {number}
 */
function minutesFromTime(str) {
  const [h, m] = String(str).split(':').map(Number);
  return h * 60 + m;
}

/**
 * Determine whether a place is currently open based on its hours of operation.
 * Supports multiple time windows per day and overnight hours.
 * @param {object} hours An object mapping day abbreviations to arrays of [open, close] strings.
 * @param {Date} [now] Optional date instance; defaults to current time.
 * @returns {boolean}
 */
function isOpenNow(hours, now = new Date()) {
  if (!hours) return false;
  const days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
  const day = days[now.getDay()];
  const windows = hours[day] || [];
  if (!Array.isArray(windows) || windows.length === 0) {
    return false;
  }
  const nowMin = now.getHours() * 60 + now.getMinutes();
  for (const [open, close] of windows) {
    const openMin = minutesFromTime(open);
    const closeMin = minutesFromTime(close);
    if (openMin <= closeMin) {
      if (nowMin >= openMin && nowMin <= closeMin) {
        return true;
      }
    } else {
      // Over midnight
      if (nowMin >= openMin || nowMin <= closeMin) {
        return true;
      }
    }
  }
  return false;
}

/**
 * Convert hours object into a human friendly string for today's hours.
 * Returns "Closed" if there are no hours defined.
 * @param {object} hours
 * @returns {string}
 */
function todayHoursString(hours) {
  if (!hours) return 'Closed';
  const days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
  const day = days[new Date().getDay()];
  const windows = hours[day] || [];
  if (windows.length === 0) return 'Closed';
  return windows.map(([o, c]) => `${o}–${c}`).join(', ');
}

/**
 * Render an individual listing card for a place.
 * @param {object} place
 * @param {boolean} compact If true, renders a compact card.
 * @returns {string} HTML string for the card.
 */
function renderCard(place, compact = false) {
  const open = isOpenNow(place.hours);
  const price = place.price_range?.symbol || '';
  const cuisine = (place.cuisines && place.cuisines.length > 0) ? place.cuisines[0] : '';
  const badgesHtml = (place.badges || []).map(b => `<span class="badge">${b}</span>`).join('');
  const rating = typeof place.rating_overall === 'number' ? place.rating_overall.toFixed(1) : '';
  const subscoresHtml = place.subscores ? Object.entries(place.subscores)
    .map(([k, v]) => `<div class="subscore"><span class="subscore-name">${k}</span> <span class="subscore-value">${parseFloat(v).toFixed(1)}</span></div>`)
    .join('') : '';
  return `
    <a class="card${compact ? ' compact' : ''}" href="tool.html?slug=${encodeURIComponent(place.slug)}">
      <div class="card-header">
        <h3>${place.name}</h3>
        <div class="badges">${badgesHtml}</div>
      </div>
      <div class="card-meta">
        ${rating ? `<span class="rating">${rating}</span>` : ''}
        <span class="status ${open ? 'open' : 'closed'}">${open ? 'Open' : 'Closed'}</span>
        ${price ? `<span class="price">${price}</span>` : ''}
        ${cuisine ? `<span class="cuisine">${cuisine}</span>` : ''}
      </div>
      <div class="subscores">${subscoresHtml}</div>
    </a>
  `;
}

/**
 * Render the listing of places into the page.
 * Applies search, filter and sort options selected by the user.
 */
async function renderList() {
  const container = document.getElementById('place-list');
  if (!container) return;
  const places = await loadPlaces();
  // Build filter state
  let results = [...places];

  // Search filter
  const searchInput = document.getElementById('search-input');
  const query = searchInput && searchInput.value.trim().toLowerCase();
  if (query) {
    results = results.filter(p =>
      p.name.toLowerCase().includes(query) ||
      (p.cuisines && p.cuisines.some(c => c.toLowerCase().includes(query))) ||
      (p.location?.neighborhood && p.location.neighborhood.toLowerCase().includes(query))
    );
  }

  // Awards filter
  const awardCheckboxes = document.querySelectorAll('#filter-awards input[type="checkbox"]:checked');
  const selectedAwards = Array.from(awardCheckboxes).map(cb => cb.value);
  if (selectedAwards.length > 0) {
    results = results.filter(p => Array.isArray(p.badges) && selectedAwards.every(a => p.badges.includes(a)));
  }

  // Price filter
  const priceCheckboxes = document.querySelectorAll('#filter-price input[type="checkbox"]:checked');
  const selectedPrices = Array.from(priceCheckboxes).map(cb => cb.value);
  if (selectedPrices.length > 0) {
    results = results.filter(p => p.price_range && selectedPrices.includes(p.price_range.symbol));
  }

  // Cuisines filter
  const cuisineCheckboxes = document.querySelectorAll('#filter-cuisines input[type="checkbox"]:checked');
  const selectedCuisines = Array.from(cuisineCheckboxes).map(cb => cb.value);
  if (selectedCuisines.length > 0) {
    results = results.filter(p => Array.isArray(p.cuisines) && p.cuisines.some(c => selectedCuisines.includes(c)));
  }

  // Neighborhood filter
  const neighborhoodCheckboxes = document.querySelectorAll('#filter-neighborhoods input[type="checkbox"]:checked');
  const selectedNeighborhoods = Array.from(neighborhoodCheckboxes).map(cb => cb.value);
  if (selectedNeighborhoods.length > 0) {
    results = results.filter(p => p.location && selectedNeighborhoods.includes(p.location.neighborhood));
  }

  // Sort
  const sortSelect = document.getElementById('sort-select');
  const sort = sortSelect ? sortSelect.value : 'featured';
  if (sort === 'rating') {
    results.sort((a, b) => (b.rating_overall || 0) - (a.rating_overall || 0));
  }

  // Compact view
  const compact = document.getElementById('compact-view')?.checked;

  container.innerHTML = results.map(p => renderCard(p, compact)).join('');
}

/**
 * Populate dynamic filter options (cuisines and neighborhoods).
 */
async function populateFilterOptions() {
  const places = await loadPlaces();
  // Collect unique cuisines and neighborhoods
  const cuisines = new Set();
  const neighborhoods = new Set();
  places.forEach(p => {
    (p.cuisines || []).forEach(c => cuisines.add(c));
    if (p.location?.neighborhood) {
      neighborhoods.add(p.location.neighborhood);
    }
  });

  const cuisinesContainer = document.getElementById('filter-cuisines');
  cuisines.forEach(c => {
    const label = document.createElement('label');
    label.innerHTML = `<input type="checkbox" value="${c}"> ${c}`;
    cuisinesContainer?.appendChild(label);
  });

  const neighborhoodsContainer = document.getElementById('filter-neighborhoods');
  neighborhoods.forEach(n => {
    const label = document.createElement('label');
    label.innerHTML = `<input type="checkbox" value="${n}"> ${n}`;
    neighborhoodsContainer?.appendChild(label);
  });
}

/**
 * Initialise event listeners for the index page.
 */
function initIndexPage() {
  const searchInput = document.getElementById('search-input');
  const filterToggle = document.getElementById('filter-toggle');
  const applyFiltersButton = document.getElementById('apply-filters');
  const sortSelect = document.getElementById('sort-select');
  const compactView = document.getElementById('compact-view');

  if (searchInput) {
    searchInput.addEventListener('input', () => renderList());
  }
  if (filterToggle) {
    filterToggle.addEventListener('click', () => {
      const drawer = document.getElementById('filter-drawer');
      drawer?.classList.toggle('open');
    });
  }
  if (applyFiltersButton) {
    applyFiltersButton.addEventListener('click', () => {
      const drawer = document.getElementById('filter-drawer');
      drawer?.classList.remove('open');
      renderList();
    });
  }
  if (sortSelect) {
    sortSelect.addEventListener('change', () => renderList());
  }
  if (compactView) {
    compactView.addEventListener('change', () => renderList());
  }

  populateFilterOptions().then(() => {
    renderList();
  });
}

/**
 * Render a detail page for a single place.
 * Populates all the sections and inserts JSON-LD into the head.
 * @param {object} place
 */
function renderPlaceDetail(place) {
  // Basic fields
  const nameEl = document.getElementById('place-name');
  if (nameEl) nameEl.textContent = place.name;
  const badgeContainer = document.getElementById('place-badges');
  if (badgeContainer) {
    badgeContainer.innerHTML = (place.badges || []).map(b => `<span class="badge">${b}</span>`).join('');
  }
  const ratingEl = document.getElementById('place-rating');
  if (ratingEl) ratingEl.textContent = typeof place.rating_overall === 'number' ? `Rating ${place.rating_overall.toFixed(1)}` : '';
  const statusEl = document.getElementById('place-status');
  if (statusEl) statusEl.textContent = isOpenNow(place.hours) ? 'Open now' : 'Closed';

  // About and verified note
  const aboutTextEl = document.getElementById('about-text');
  if (aboutTextEl) aboutTextEl.textContent = place.about || '';
  const verifiedNote = document.getElementById('verified-note');
  if (verifiedNote) {
    if (place.verified) {
      verifiedNote.textContent = place.methodology_note || 'Verified listing';
    } else {
      verifiedNote.textContent = '';
    }
  }

  // Best times
  const bestTimesDiv = document.getElementById('best-times-list');
  if (bestTimesDiv) {
    bestTimesDiv.innerHTML = (place.best_times || []).map(bt =>
      `<div class="best-time"><strong>${bt.label}:</strong> ${bt.window}</div>`
    ).join('');
  }

  // Public sentiment
  const psDiv = document.getElementById('public-sentiment-content');
  if (psDiv) {
    if (place.public_sentiment) {
      psDiv.innerHTML = `
      <p>${place.public_sentiment.summary || ''}</p>
      <p><em>Based on ${place.public_sentiment.count || 0} reviews (${place.public_sentiment.last_updated || ''})</em></p>
    `;
    } else {
      psDiv.innerHTML = '';
    }
  }

  // Dishes
  const dishesList = document.getElementById('dishes-list');
  if (dishesList) {
    dishesList.innerHTML = (place.dishes || []).map(d => `<li>${d}</li>`).join('');
  }

  // Amenities
  const amenitiesList = document.getElementById('amenities-list');
  if (amenitiesList) {
    amenitiesList.innerHTML = (place.amenities || []).map(a => `<li>${a}</li>`).join('');
  }

  // Hours
  const hoursTable = document.getElementById('hours-table');
  if (hoursTable) {
    const rows = [];
    const days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
    days.forEach(d => {
      const windows = place.hours?.[d] || [];
      const hoursString = windows.length > 0 ? windows.map(([o, c]) => `${o}–${c}`).join(', ') : 'Closed';
      rows.push(`<tr><th>${d}</th><td>${hoursString}</td></tr>`);
    });
    hoursTable.innerHTML = rows.join('');
  }

  // Gallery
  const galleryDiv = document.getElementById('gallery-list');
  if (galleryDiv) {
    galleryDiv.innerHTML = (place.gallery || []).map(src => `<img src="${src}" alt="">`).join('');
  }

  // FAQs
  const faqsDiv = document.getElementById('faqs-list');
  if (faqsDiv) {
    faqsDiv.innerHTML = (place.faqs || []).map(f => `<div class="faq"><strong>${f.q}</strong><p>${f.a}</p></div>`).join('');
  }

  // Location
  const addressLine = document.getElementById('address-line');
  if (addressLine) addressLine.textContent = place.location?.address || '';
  const mapsLink = document.getElementById('maps-link');
  if (mapsLink) {
    mapsLink.href = place.actions?.maps_url || '#';
  }

  // Inject JSON‑LD
  injectJsonLd(place);
}
window.renderPlaceDetail = renderPlaceDetail;

/**
 * Generate and insert schema.org JSON-LD for a place.
 * Uses the LocalBusiness subtype based on the category and adds FAQPage when applicable.
 * @param {object} place
 */
function injectJsonLd(place) {
  const category = Array.isArray(place.categories) ? place.categories[0] : 'LocalBusiness';
  let type = 'LocalBusiness';
  switch (category) {
    case 'Restaurants': type = 'Restaurant'; break;
    case 'Hotels': type = 'Hotel'; break;
    case 'Schools': type = 'School'; break;
    case 'Malls': type = 'ShoppingMall'; break;
    case 'Spas': type = 'HealthAndBeautyBusiness'; break;
    case 'Clinics': type = 'MedicalClinic'; break;
    // default: LocalBusiness
  }
  const json = {
    '@context': 'https://schema.org',
    '@type': type,
    'name': place.name,
    'image': place.gallery && place.gallery.length > 0 ? place.gallery[0] : undefined,
    'url': window.location.href,
    'telephone': place.actions?.phone,
    'priceRange': place.price_range?.symbol,
    'servesCuisine': place.cuisines,
    'address': place.location?.address ? {
      '@type': 'PostalAddress',
      'streetAddress': place.location.address,
      'addressLocality': place.location.neighborhood || '',
      'addressRegion': 'Muscat',
      'addressCountry': 'OM'
    } : undefined,
    'geo': (place.location?.lat && place.location?.lng) ? {
      '@type': 'GeoCoordinates',
      'latitude': place.location.lat,
      'longitude': place.location.lng
    } : undefined,
    'openingHoursSpecification': (place.hours) ? Object.entries(place.hours).map(([day, windows]) => windows.map(([o, c]) => ({
      '@type': 'OpeningHoursSpecification',
      'dayOfWeek': day,
      'opens': o,
      'closes': c
    }))).flat() : undefined,
    'aggregateRating': (typeof place.rating_overall === 'number' && place.public_sentiment) ? {
      '@type': 'AggregateRating',
      'ratingValue': place.rating_overall.toFixed(1),
      'reviewCount': place.public_sentiment.count
    } : undefined
  };
  // Remove undefined values
  Object.keys(json).forEach(key => json[key] === undefined && delete json[key]);
  const scripts = document.querySelectorAll('script[type="application/ld+json"]');
  scripts.forEach(s => s.remove());
  const scriptEl = document.createElement('script');
  scriptEl.type = 'application/ld+json';
  scriptEl.textContent = JSON.stringify(json, null, 2);
  document.head.appendChild(scriptEl);

  // FAQPage JSON-LD if faqs exist
  if (place.faqs && place.faqs.length > 0) {
    const faqJson = {
      '@context': 'https://schema.org',
      '@type': 'FAQPage',
      'mainEntity': place.faqs.map(f => ({
        '@type': 'Question',
        'name': f.q,
        'acceptedAnswer': {
          '@type': 'Answer',
          'text': f.a
        }
      }))
    };
    const faqScript = document.createElement('script');
    faqScript.type = 'application/ld+json';
    faqScript.textContent = JSON.stringify(faqJson, null, 2);
    document.head.appendChild(faqScript);
  }
}

// Initialise the index page when DOM content is ready
document.addEventListener('DOMContentLoaded', () => {
  // Determine if we are on the index page or not
  if (document.getElementById('place-list')) {
    initIndexPage();
  }
});