DROP TABLE IF EXISTS sequences;

CREATE TABLE sequences (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  sequence TEXT NOT NULL,
  results TEXT
);
