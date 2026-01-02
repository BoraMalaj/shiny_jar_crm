-- Create database if not exists (PostgreSQL creates it automatically with POSTGRES_DB)
-- But let's make sure

-- Create tables
CREATE TABLE IF NOT EXISTS businesses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    instagram_handle VARCHAR(50),
    currency VARCHAR(3) DEFAULT 'EUR',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    business_id INTEGER REFERENCES businesses(id)
);

CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    amount DECIMAL(10, 2) NOT NULL,
    type VARCHAR(10) CHECK (type IN ('expense', 'income')),
    category VARCHAR(50),
    description TEXT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    business_id INTEGER REFERENCES businesses(id),
    user_id INTEGER REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    instagram_handle VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    first_order_date DATE,
    total_spent DECIMAL(10, 2) DEFAULT 0.00,
    notes TEXT,
    business_id INTEGER REFERENCES businesses(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample business (Shiny Jar)
INSERT INTO businesses (name, instagram_handle, currency) 
VALUES ('Shiny Jar', 'shiny_jar', 'EUR')
ON CONFLICT (name) DO NOTHING;

-- Insert admin user (password: admin123)
INSERT INTO users (username, email, full_name, hashed_password, business_id) 
VALUES (
    'admin', 
    'admin@shinyjar.com', 
    'Admin User', 
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',  -- bcrypt for 'admin123'
    (SELECT id FROM businesses WHERE name = 'Shiny Jar')
) ON CONFLICT (username) DO NOTHING;

-- Sample transactions
INSERT INTO transactions (amount, type, category, description, business_id, user_id) VALUES
(150.00, 'expense', 'Materials', 'Silver chains', 1, 1),
(45.00, 'expense', 'Packaging', 'Jewelry boxes', 1, 1),
(89.00, 'income', 'Sales', 'Necklace sale', 1, 1),
(120.00, 'income', 'Sales', 'Earrings sale', 1, 1)
ON CONFLICT DO NOTHING;

-- Sample customers
INSERT INTO customers (name, instagram_handle, email, total_spent, business_id) VALUES
('Maria Silva', 'maria_silva', 'maria@email.com', 250.00, 1),
('John Doe', 'john_jewelry', 'john@email.com', 180.00, 1),
('Anna Smith', 'anna_sparkle', 'anna@email.com', 320.00, 1)
ON CONFLICT DO NOTHING;