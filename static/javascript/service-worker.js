let staticCacheName = 'djangopwa-v1.1';

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(staticCacheName).then(function(cache) {
      return cache.addAll([
        '/',  // تأكد من أن المسار صحيح
        '/static/css/styles.css',  // مثال لملف CSS
        '/static/javascript/main.js',  // مثال لملف JS
        '/static/images/icons/small-logo.png',  // مثال لأيقونة
      ]);
    })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request).then(function(response) {
      return response || fetch(event.request);
    })
  );
});
