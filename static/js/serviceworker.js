const CATALOGUE_ASSETS = "catalogue-assets-v1";
const assets = [
  "/",
  "/index.html",
  "/favourites.html",
  "/login.html",
  "/signup.html",
  "/about.html",
  "/home.html",
  "/vtuber.html",
  "/static/css/style.css",
  "/static/js/app.js",
  "/static/images/background.jpg",
  "/static/images/Hololive-Logo-2016.png",
  "/static/images/Hololive-super-expo-2023.jpg",
  "/static/images/logo.png",
  "/static/images/favicon.png",
  "/static/icons/icon-128x128.png",
  "/static/icons/icon-192x192.png",
  "/static/icons/icon-384x384.png",
  "/static/icons/icon-512x512.png",
];

self.addEventListener("install", (installEvt) => {
  installEvt.waitUntil(
    caches
      .open(CATALOGUE_ASSETS)
      .then((cache) => {
        console.log(cache);
        cache.addAll(assets);
      })
      .then(() => self.skipWaiting())
      .catch((e) => {
        console.log(e);
      }),
  );
});

self.addEventListener("activate", function (evt) {
  evt.waitUntil(
    caches
      .keys()
      .then((keyList) => {
        return Promise.all(
          keyList.map((key) => {
            if (key !== CATALOGUE_ASSETS) {
              console.log("Removed old cache from", key);
              return caches.delete(key);
            }
          }),
        );
      })
      .then(() => self.clients.claim()),
  );
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  event.respondWith(
    caches
      .match(event.request)
      .then((cachedResponse) => {
        return (
          cachedResponse ||
          fetch(event.request).then((response) => {
            return caches.open(CATALOGUE_ASSETS).then((cache) => {
              cache.put(event.request, response.clone());
              return response;
            });
          })
        );
      })
      .catch(() => caches.match("/")),
  );
});
