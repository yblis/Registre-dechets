const CACHE_NAME = 'registre-dechets-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/static/css/custom.css',
  '/static/js/forms.js',
  '/static/js/modals.js',
  '/static/js/notifications.js',
  '/static/js/waste_entries.js',
  '/static/manifest.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(ASSETS_TO_CACHE))
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

self.addEventListener('fetch', (event) => {
  // Skip cross-origin requests
  if (!event.request.url.startsWith(self.location.origin)) {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        if (response) {
          return response;
        }

        return fetch(event.request).then((response) => {
          // Don't cache responses that aren't successful
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }

          // Clone the response since it can only be consumed once
          const responseToCache = response.clone();

          caches.open(CACHE_NAME)
            .then((cache) => {
              cache.put(event.request, responseToCache);
            });

          return response;
        });
      })
  );
});

// Handle background sync for offline submissions
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-waste-records') {
    event.waitUntil(
      syncWasteRecords()
    );
  }
});

// Function to sync waste records when back online
async function syncWasteRecords() {
  try {
    const records = await getOfflineRecords();
    for (const record of records) {
      await submitRecord(record);
    }
    await clearOfflineRecords();
  } catch (error) {
    console.error('Sync failed:', error);
  }
}

// Placeholder functions for offline storage
async function getOfflineRecords() {
  // In a real implementation, this would get records from IndexedDB
  return [];
}

async function submitRecord(record) {
  // In a real implementation, this would submit to the server
  return fetch('/record/new', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(record)
  });
}

async function clearOfflineRecords() {
  // In a real implementation, this would clear synced records from IndexedDB
}
