import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

export default defineConfig({
  site: "https://spirituelebetekenis.com",
  output: "static",
  trailingSlash: "always",
  build: { format: "directory", concurrency: 2 },
  integrations: [
    sitemap({
      entryLimit: 1000, // zoals de oude site: meerdere post-sitemaps
      filter: (page) => !/\/page\/\d+\//.test(page),
    }),
  ],
});
