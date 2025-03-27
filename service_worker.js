const CACHE_NAME = "tiksaver-cache-v1";
const urlsToCache = [
    "/",
    "/static/css/styles.css",
    "/static/js/main.js",
    "/static/icons/icon-192x192.png",
    "/static/icons/icon-512x512.png"
];

// Install Service Worker & Cache Files
self.addEventListener("install", event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
            .then(() => self.skipWaiting())
    );
});

// Activate Service Worker & Remove Old Caches
self.addEventListener("activate", event => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(keys.map(key => {
                if (key !== CACHE_NAME) {
                    return caches.delete(key);
                }
            }))
        )
    );
});

// Fetch Requests - Serve Cached Files When Offline
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => response || fetch(event.request))
    );
});
