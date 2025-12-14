CREATE TABLE IF NOT EXISTS delivery (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    address TEXT NOT NULL,
    delivery_status TEXT DEFAULT 'pending'
        CHECK (delivery_status IN ('pending', 'shipped','delivered')),
    delivery_date DATETIME,
    
    FOREIGN KEY (order_id) REFERENCES orders(id)
);