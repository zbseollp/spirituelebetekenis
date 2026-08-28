/**
 * Drie dingen die de statische assets zelf niet kunnen:
 *
 * 1. De XML-sitemap bevat absolute URL's met het productiedomein. Op een
 *    *.workers.dev-preview wijst die naar een host die daar niets serveert.
 *    Deze Worker herschrijft het domein naar de host waarop hij wordt
 *    opgevraagd; op het echte domein is dat een no-op.
 * 2. WordPress serveerde de RSS-feed op /feed/; Astro bouwt hem als /feed.xml.
 * 3. De gemaskeerde affiliate-links (/bol, /intuitie, ...) waren op WordPress
 *    301-redirects. Vul het doel in src/data/affiliate-redirects.json in en ze
 *    werken weer; blijft een doel leeg, dan valt het pad door naar de 404 —
 *    precies wat de oude site er nu ook mee doet.
 *
 * De ETag van het bronbestand hoort NIET ongewijzigd terug bij een herschreven
 * body: anders levert een revalidatie een 304 op en blijft er een oude versie
 * in de browsercache hangen.
 */
import affiliate from "../src/data/affiliate-redirects.json";

const CANONICAL = 'https://spirituelebetekenis.com';
const SITEMAP = /^\/sitemap[\w.-]*\.xml$/;
const ALIAS = {
  '/sitemap.xml': '/sitemap-index.xml',
  '/sitemap_index.xml': '/sitemap-index.xml',
  '/feed/': '/feed.xml',
  '/feed': '/feed.xml',
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname.replace(/\/$/, '') || '/';

    const target = affiliate[path];
    if (target) {
      return Response.redirect(target, 301);
    }

    const alias = ALIAS[url.pathname];
    if (!SITEMAP.test(url.pathname) && !alias) return env.ASSETS.fetch(request);

    // Zonder conditionele headers opvragen, zodat we altijd een volledige body
    // krijgen om te herschrijven (nooit een kaal 304'tje).
    const assetRequest = new Request(new URL(alias || url.pathname, url).toString(), {
      method: 'GET',
      headers: {},
    });
    const response = await env.ASSETS.fetch(assetRequest);
    if (!response.ok) return response;

    const body = (await response.text()).split(CANONICAL).join(url.origin);

    const headers = new Headers(response.headers);
    headers.delete('content-length');
    headers.delete('last-modified');
    headers.delete('etag');
    headers.set('content-type', 'application/xml; charset=utf-8');
    headers.set('cache-control', 'no-store, must-revalidate');

    return new Response(body, { status: 200, headers });
  },
};
