CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    status TEXT DEFAULT 'new'
    CHECK (status IN ('new', 'pending', 'paid',
        'shipped', 'delivered', 'cancelled')),
    total_sum REAL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);