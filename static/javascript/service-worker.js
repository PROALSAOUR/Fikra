let staticCacheName = 'djangopwa-v1.1';

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(staticCacheName).then(function(cache) {
      return cache.addAll([
        '/',  // تأكد من أن المسار صحيح
        '/offline/',
        '/static/css/offline-style.css',
        '/static/css/all.css',
        '/static/css/all.min.css',
        '/static/css/style.css', 
        '/static/javascript/main.js',  
        '/static/images/icons/small-logo.png',  
      ]);
    })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
      caches.match(event.request).then(function(response) {
          return response || fetch(event.request).catch(function() {
              return caches.match('/offline/'); // إعادة الصفحة غير المتصلة إذا فشل التحميل
          });
      })
  );
});
