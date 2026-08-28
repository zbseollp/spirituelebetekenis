import index from "../data/index.json";
import categoriesRaw from "../data/categories.json";

export type IndexEntry = {
  slug: string;
  title: string;
  date: string;
  categories: string[];
  excerpt: string;
};

export type Category = { slug: string; name: string };

/** Compacte index van alle berichten, nieuwste eerst. De volledige tekst
 *  staat per bericht in src/content/posts/ en wordt pas op de detailpagina
 *  geladen; zo blijft de build van 6792 pagina's behapbaar. */
export const allPosts = index as IndexEntry[];
export const categories = categoriesRaw as Category[];

export const postsInCategory = (slug: string) =>
  allPosts.filter((p) => p.categories.includes(slug));

export const categoryBySlug = (slug: string) =>
  categories.find((c) => c.slug === slug);

const MONTHS = ["januari","februari","maart","april","mei","juni",
                "juli","augustus","september","oktober","november","december"];

export function formatDate(value: string): string {
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return "";
  return `${d.getDate()} ${MONTHS[d.getMonth()]} ${d.getFullYear()}`;
}

export function isoDate(value: string): string {
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? "" : d.toISOString();
}

export function chunk<T>(items: T[], size: number): T[][] {
  const out: T[][] = [];
  for (let i = 0; i < items.length; i += size) out.push(items.slice(i, i + size));
  return out.length ? out : [[]];
}
