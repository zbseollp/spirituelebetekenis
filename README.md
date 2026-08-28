# Spirituele Betekenissen

Astro 5 statische site voor **spirituelebetekenis.com**, 1-op-1 overgezet vanaf
WordPress en uitgeserveerd via Cloudflare Workers.

## Commando's

```bash
npm install
npm run content   # bouwt src/content/ opnieuw uit migration/source/
npm run dev
npm run build     # bouwt 7141 pagina's naar ./dist
npm run deploy    # build + wrangler deploy
```

## URL-structuur

Elke URL is gelijk aan die van de oude WordPress-site:

| Pad | Inhoud |
| --- | --- |
| `/` | voorpagina |
| `/{slug}/` | de 6792 berichten, plus `over`, `trainingen`, `privacybeleid` |
| `/contact/` | contactpagina met formulier |
| `/blog/`, `/blog/page/{n}/` | alle berichten, 40 per pagina (170 pagina's) |
| `/info/{categorie}/`, `/info/{categorie}/page/{n}/` | categoriearchief, 40 per pagina |
| `/sitemap/` | de HTML-sitemap die de oude site ook had |
| `/sitemap-index.xml`, `/sitemap.xml`, `/sitemap_index.xml` | XML-sitemap |
| `/feed/` | RSS-feed (Worker-alias voor `/feed.xml`) |

Let op: de categorieën staan onder `/info/`, niet onder `/category/`. Dat is
wat WordPress deed en dus wat er in Google staat.

## Nog in te vullen

Twee dingen kunnen pas werken met gegevens die niet uit de oude site te halen
zijn:

1. **`src/data/affiliate-redirects.json`** — de gemaskeerde affiliate-links
   (`/bol`, `/intuitie`, `/tekenszijnoveral`, …) waren op WordPress
   301-redirects. Die redirects zijn daar inmiddels stuk: op de live site geven
   ze allemaal een 404. Zet hier de echte affiliate-URL achter een pad en de
   Worker stuurt bezoekers weer door.
2. **`contact.web3formsKey` in `src/data/site.ts`** — zolang die leeg is toont
   `/contact/` het mailadres in plaats van een formulier.

## Waar de inhoud vandaan komt

| Script | Doel |
| --- | --- |
| `migration/scripts_fetch_rest.py` | haalt berichten, pagina's, categorieën en media op via de WP REST API |
| `migration/scripts_fetch_meta.py` | scrapet de `<title>` en meta-description uit de live HTML — RankMath zet die niet in de REST API |
| `migration/scripts_build_content.py` | zet dat om naar `src/content/` plus een compacte `src/data/index.json` |
| `migration/scripts_clean_elementor.py` | haalt de semantische inhoud uit de Elementor-markup van de pagina's |
| `migration/scripts_download_images.py` | haalt de afbeeldingen op naar `public/wp-content/uploads/` |

De berichten staan als losse JSON-bestanden in `src/content/posts/`. Samen is
dat ~160 MB HTML; in één import zou dat de build onnodig zwaar maken, en de
archieven hebben alleen `src/data/index.json` nodig.

De ruwe REST-dumps (`migration/source/posts.json`, `meta.json`) en de
HTML-spiegel staan in `.gitignore`: bronmateriaal, geen sitecode.
