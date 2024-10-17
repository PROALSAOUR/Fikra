// self.addEventListener('install', function(event) {
//     event.waitUntil(
//       caches.open('my-cache').then(function(cache) {
//         return cache.addAll([
//           '/',
//           '/static/icons/logo.png',
//           '/static/icons/logo2.png',
//           '/static/css/style.css',
//           '/static/javascript/main.js'
//         ]);
//       })
//     );
//   });
  
//   self.addEventListener('fetch', function(event) {
//     event.respondWith(
//       caches.match(event.request).then(function(response) {
//         return response || fetch(event.request);
//       })
//     );
//   });
  