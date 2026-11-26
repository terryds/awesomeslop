export type Bindings = {
  DB: D1Database;
  SESSION_SECRET: string;
  GOOGLE_CLIENT_ID?: string;
  GOOGLE_CLIENT_SECRET?: string;
  ADMIN_EMAILS?: string;
  DEV_LOGIN?: string;
};

// `admin` is worked out on every request from ADMIN_EMAILS; it is never stored in the session cookie.
export type User = { id: string; email: string; name: string | null; picture: string | null; admin?: boolean };

export type AppEnv = { Bindings: Bindings; Variables: { user: User | null } };

export type Art = {
  slug: string;
  no: number;
  title: string;
  category: string | null;
  date: string | null;
  summary: string;
  model: string | null;
  agent: string | null;
  medium: string;
  tags: string[];
  specs: Record<string, string>;
  featured: boolean;
  kind: 'live' | 'image' | 'video';
  src: string;
  cover: string | null;
  prompt: string;
  readmeHtml: string;
};

export type Category = { id: string; title: string; blurb: string };
