// Way2Sec is paused: this worker clears the old offline copy of the app and removes itself.
self.addEventListener('install', function(){ self.skipWaiting(); });
self.addEventListener('activate', function(e){
  e.waitUntil(caches.keys().then(function(ks){ return Promise.all(ks.map(function(k){ return caches.delete(k); })); })
    .then(function(){ return self.registration.unregister(); })
    .then(function(){ return self.clients.matchAll(); })
    .then(function(cs){ cs.forEach(function(c){ c.navigate(c.url); }); }));
});
