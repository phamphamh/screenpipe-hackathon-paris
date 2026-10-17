const PORT = 4300;
const MIME = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".json": "application/json" };

Bun.serve({
  port: PORT,
  fetch(req) {
    let path = new URL(req.url).pathname;
    if (path === "/") path = "/index.html";
    const file = Bun.file("." + path);
    const ext = path.slice(path.lastIndexOf("."));
    return file.exists().then((ok) =>
      ok
        ? new Response(file, { headers: { "Content-Type": MIME[ext] || "application/octet-stream" } })
        : new Response("Not found", { status: 404 })
    );
  },
});

console.log(`Dashboard client — Étude & Pilotage : http://localhost:${PORT}`);
