import data from './generated/arts.json';
import categoryData from './generated/categories.json';
import type { Art, Category } from './types';

export const arts = data as unknown as Art[]; // shape is guaranteed by scripts/build-content.mjs

export const categories = categoryData as Category[];

export const getCategory = (id: string | null) => categories.find((c) => c.id === id);

export const getArt = (slug: string) => arts.find((a) => a.slug === slug);

export const artNo = (n: number) => String(n).padStart(3, '0');
