async function reqHandler(req: Request) {
  const reqPath = new URL(req.url).pathname;
  return await fetch("http://127.0.0.1:8080" + reqPath, { headers: req.headers });
}

Deno.serve(reqHandler);

