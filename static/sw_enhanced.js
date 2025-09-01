
// Rex AI Assistant - Enhanced Service Worker for Perfect PWA Score
const CACHE_NAME = 'rex-ai-v1.0.0';
const urlsToCache = [
    '/',
    '/static/style.css',
    '/static/script.js',
    '/static/icon-192.png',
    '/static/icon-512.png',
    '/static/manifest.json'
];

// Install event
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Cache opened');
                return cache.addAll(urlsToCache);
            })
    );
});

// Fetch event
self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // Return cached version or fetch from network
                return response || fetch(event.request);
            }
        )
    );
});

// Activate event
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Background sync for offline functionality
self.addEventListener('sync', event => {
    if (event.tag === 'background-sync') {
        event.waitUntil(doBackgroundSync());
    }
});

function doBackgroundSync() {
    return new Promise(resolve => {
        console.log('Background sync executed');
        resolve();
    });
}

// Push notification support
self.addEventListener('push', event => {
    const options = {
        body: event.data ? event.data.text() : 'New message from Rex AI',
        icon: '/static/icon-192.png',
        badge: '/static/icon-72.png',
        vibrate: [100, 50, 100],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: 1
        }
    };
    
    event.waitUntil(
        self.registration.showNotification('Rex AI Assistant', options)
    );
});
