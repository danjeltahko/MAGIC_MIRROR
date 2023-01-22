self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open('v1').then(function(cache) {
            return cache.addAll([
                '/user/',
                '/static/css/style.css',
                '/static/js/user.js',
                '/static/img/icon.png'
            ]);
        })
    );
});

self.addEventListener('fetch', function(event) {
    var request = event.request;
    var url = new URL(request.url);
    if (url.origin === location.origin) {
        if (url.pathname === '/traffic/' || url.pathname === '/todo-list/' || url.pathname === '/todo-list/change-list/') {
            event.respondWith(
                caches.match('/user/').then(function(response) {
                    return response || fetch('/user/');
                })
            );
        } else {
            event.respondWith(
                caches.match(request).then(function(response) {
                    return response || fetch(request);
                })
            );
        }
    }
});