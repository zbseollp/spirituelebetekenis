import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const categoryRef = z.object({ slug: z.string(), name: z.string() });

const posts = defineCollection({
  loader: glob({ pattern: "*.json", base: "./src/content/posts" }),
  schema: z.object({
    slug: z.string(),
    title: z.string(),
    date: z.string(),
    modified: z.string(),
    categories: z.array(categoryRef),
    content: z.string(),
    seoTitle: z.string(),
    seoDescription: z.string(),
    canonical: z.string(),
    ogImage: z.string(),
  }),
});

const pages = defineCollection({
  loader: glob({ pattern: "*.json", base: "./src/content/pages" }),
  schema: z.object({
    slug: z.string(),
    title: z.string(),
    date: z.string(),
    modified: z.string(),
    content: z.string(),
    seoTitle: z.string(),
    seoDescription: z.string(),
    canonical: z.string(),
    ogImage: z.string(),
  }),
});

export const collections = { posts, pages };
