CREATE TABLE users (
  id         TEXT PRIMARY KEY,              -- Google account id ("sub")
  email      TEXT NOT NULL,
  name       TEXT,
  picture    TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE waitlist (
  user_id    TEXT PRIMARY KEY REFERENCES users(id),
  art_url    TEXT NOT NULL,                 -- the link where their art can be seen
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
