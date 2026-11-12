import data from './generated/arts.json';
import categoryData from './generated/categories.json';
import type { Art, Category } from './types';

export const arts = data as unknown as Art[]; // shape is guaranteed by scripts/build-content.mjs

export const categories = categoryData as Category[];

export const getCategory = (id: string | null) => categories.find((c) => c.id === id);

export const getArt = (slug: string) => arts.find((a) => a.slug === slug);

export const artNo = (n: number) => String(n).padStart(3, '0');

// Opens a new claude.ai chat with the question prefilled (claude.ai/new?q=...).
export function claudeBreakdownUrl(art: Art) {
  const q =
    `This prompt was given to an AI agent${art.model ? ` (${art.model})` : ''} to make a piece of art called "${art.title}". ` +
    `Break it down for me: what each part of the prompt is doing, which phrases drive the visual result, ` +
    `and what I could change to get interesting variations.\n\n---\n\n${art.prompt}`;
  return `https://claude.ai/new?q=${encodeURIComponent(q)}`;
}
