// Service Worker – Cache-Name enthält die Version, damit jede neue Version sauber übernommen wird.
// Die Zeile CACHE wird von version-erhoehen.sh automatisch angepasst.
const CACHE = "wissen-rd-1.10.0-b23";
const SHELL = [
  "./", "index.html", "css/style.css", "manifest.webmanifest",
  "js/version.js", "js/app.js", "js/text.js", "js/bereiche.js", "js/firebase-config.js",
  "icons/icon.svg", "icons/icon-192.png", "icons/icon-512.png", "icons/apple-touch-icon.png"
];

// Firebase-SDK gleich bei der Installation mitladen – sonst fehlt es nach einem Update,
// wenn die App zum ersten Mal ohne Netz gestartet wird.
const SDK = ["firebase-app.js", "firebase-auth.js", "firebase-firestore.js"]
  .map(f => "https://www.gstatic.com/firebasejs/10.12.4/" + f);

self.addEventListener("install", ev => {
  ev.waitUntil(caches.open(CACHE).then(async c => {
    await c.addAll(SHELL);
    await Promise.all(SDK.map(u => c.add(u).catch(() => {})));
  }));
});

self.addEventListener("activate", ev => {
  ev.waitUntil(caches.keys().then(keys =>
    Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
  ).then(() => self.clients.claim()));
});

self.addEventListener("message", ev => { if (ev.data === "skipWaiting") self.skipWaiting(); });

self.addEventListener("fetch", ev => {
  const url = new URL(ev.request.url);
  if (ev.request.method !== "GET") return;
  // Firestore/Auth-Verbindungen nie cachen (Firestore hat eigenen Offline-Speicher)
  if (url.hostname.includes("googleapis.com") || url.hostname.includes("firebaseapp.com")) return;

  // Firebase-SDK vom CDN: einmal laden, dann aus dem Cache
  if (url.hostname === "www.gstatic.com") {
    ev.respondWith(caches.match(ev.request).then(r => r || fetch(ev.request).then(res => {
      const kopie = res.clone();
      caches.open(CACHE).then(c => c.put(ev.request, kopie));
      return res;
    })));
    return;
  }

  // Changelog immer frisch, sonst Cache
  if (url.pathname.endsWith("CHANGELOG.md")) {
    ev.respondWith(fetch(ev.request).catch(() => caches.match(ev.request)));
    return;
  }

  if (url.origin === location.origin) {
    // App-Dateien: zuerst Cache (schnell & offline), ?q=… ignorieren
    ev.respondWith(caches.match(ev.request, { ignoreSearch: true }).then(r => r || fetch(ev.request)));
  }
});
