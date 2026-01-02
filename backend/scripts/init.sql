-- Complete Shiny Jar Database Schema
DROP TABLE IF EXISTS transaction_items CASCADE;
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS inventory CASCADE;
DROP TABLE IF EXISTS suppliers CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS businesses CASCADE;

-- Core tables
CREATE TABLE businesses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    instagram_handle VARCHAR(50),
    currency VARCHAR(3) DEFAULT 'EUR',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    role VARCHAR(20) DEFAULT 'user',
    business_id INTEGER REFERENCES businesses(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    type VARCHAR(10) CHECK (type IN ('expense', 'income', 'both')),
    color VARCHAR(7) DEFAULT '#3B82F6',
    business_id INTEGER REFERENCES businesses(id),
    UNIQUE(name, business_id)
);

CREATE TABLE suppliers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    website VARCHAR(200),
    address TEXT,
    notes TEXT,
    business_id INTEGER REFERENCES businesses(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    instagram_handle VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    customer_since DATE DEFAULT CURRENT_DATE,
    total_spent DECIMAL(10,2) DEFAULT 0.00,
    last_purchase DATE,
    notes TEXT,
    business_id INTEGER REFERENCES businesses(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    unit_cost DECIMAL(10,2) NOT NULL,
    quantity INTEGER DEFAULT 0,
    reorder_level INTEGER DEFAULT 10,
    supplier_id INTEGER REFERENCES suppliers(id),
    business_id INTEGER REFERENCES businesses(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Main transactions table with proper foreign keys
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    transaction_date DATE NOT NULL DEFAULT CURRENT_DATE,
    amount DECIMAL(10,2) NOT NULL,
    type VARCHAR(10) NOT NULL CHECK (type IN ('expense', 'income')),
    category_id INTEGER REFERENCES categories(id),
    description TEXT,
    customer_id INTEGER REFERENCES customers(id),
    supplier_id INTEGER REFERENCES suppliers(id),
    user_id INTEGER REFERENCES users(id),
    business_id INTEGER REFERENCES businesses(id),
    payment_method VARCHAR(20),
    reference_number VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transaction items for detailed line items
CREATE TABLE transaction_items (
    id SERIAL PRIMARY KEY,
    transaction_id INTEGER REFERENCES transactions(id) ON DELETE CASCADE,
    inventory_id INTEGER REFERENCES inventory(id),
    description VARCHAR(200),
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) GENERATED ALWAYS AS (quantity * unit_price) STORED
);

-- Budgets table for university requirement
CREATE TABLE budgets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category_id INTEGER REFERENCES categories(id),
    amount DECIMAL(10,2) NOT NULL,
    period VARCHAR(20) CHECK (period IN ('daily', 'weekly', 'monthly', 'quarterly', 'yearly')),
    start_date DATE NOT NULL,
    end_date DATE,
    business_id INTEGER REFERENCES businesses(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(category_id, period, business_id)
);

-- Insert Shiny Jar business
INSERT INTO businesses (name, instagram_handle, currency) 
VALUES ('Shiny Jar', 'shiny_jar', 'EUR');

-- Insert admin user (password: admin123)
INSERT INTO users (username, email, full_name, hashed_password, business_id, role) 
VALUES (
    'admin', 
    'admin@shinyjar.com', 
    'Admin User', 
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
    1,
    'admin'
);

-- Insert categories
INSERT INTO categories (name, type, color, business_id) VALUES
-- Expense categories
('Materials', 'expense', '#EF4444', 1),
('Packaging', 'expense', '#3B82F6', 1),
('Shipping', 'expense', '#8B5CF6', 1),
('Marketing', 'expense', '#10B981', 1),
('Tools & Equipment', 'expense', '#F59E0B', 1),
('Office Supplies', 'expense', '#6366F1', 1),
('Website & Hosting', 'expense', '#EC4899', 1),
('Professional Services', 'expense', '#14B8A6', 1),
-- Income categories
('Necklaces', 'income', '#10B981', 1),
('Earrings', 'income', '#3B82F6', 1),
('Bracelets', 'income', '#8B5CF6', 1),
('Rings', 'income', '#F59E0B', 1),
('Custom Orders', 'income', '#EC4899', 1),
('Repairs', 'income', '#14B8A6', 1),
('Workshops', 'income', '#84CC16', 1);

-- Insert sample suppliers (20 suppliers)
INSERT INTO suppliers (name, contact_person, email, phone, website, business_id) VALUES
('Silver World Inc.', 'John Smith', 'john@silverworld.com', '+1234567890', 'silverworld.com', 1),
('Golden Beads Co.', 'Maria Garcia', 'maria@goldenbeads.com', '+0987654321', 'goldenbeads.com', 1),
('Crystal Palace', 'David Chen', 'david@crystalpalace.com', '+1122334455', 'crystalpalace.com', 1),
('Leather Crafts Ltd', 'Emma Wilson', 'emma@leathercrafts.com', '+5566778899', 'leathercrafts.com', 1),
('Pearl Paradise', 'Sophie Martin', 'sophie@pearlparadise.com', '+6677889900', 'pearlparadise.com', 1),
('Gemstone Wholesale', 'Michael Brown', 'michael@gemstone.com', '+7788990011', 'gemstone.com', 1),
('Metal Findings Corp', 'Lisa Taylor', 'lisa@metalfindings.com', '+8899001122', 'metalfindings.com', 1),
('Packaging Solutions', 'Robert Lee', 'robert@packaging.com', '+9900112233', 'packagingsolutions.com', 1),
('Tool Masters', 'Jennifer Wang', 'jennifer@toolmasters.com', '+0011223344', 'toolmasters.com', 1),
('Shipping Express', 'Thomas Anderson', 'thomas@shippingexpress.com', '+2233445566', 'shippingexpress.com', 1),
('Marketing Pros', 'Sarah Johnson', 'sarah@marketingpros.com', '+3344556677', 'marketingpros.com', 1),
('Web Services Inc', 'Kevin Davis', 'kevin@webservices.com', '+4455667788', 'webservices.com', 1),
('Accounting Plus', 'Amanda Clark', 'amanda@accountingplus.com', '+5566778899', 'accountingplus.com', 1),
('Legal Eagles', 'Daniel White', 'daniel@legaleagles.com', '+6677889900', 'legaleagles.com', 1),
('Insurance Partners', 'Jessica Hall', 'jessica@insurancepartners.com', '+7788990011', 'insurancepartners.com', 1),
('Cleaning Services', 'Brian King', 'brian@cleaning.com', '+8899001122', 'cleaningservices.com', 1),
('Utilities Co', 'Michelle Scott', 'michelle@utilities.com', '+9900112233', 'utilitiesco.com', 1),
('Rent Space Ltd', 'Christopher Young', 'chris@rentspace.com', '+0011223344', 'rentspace.com', 1),
('Software Solutions', 'Laura Allen', 'laura@softwaresolutions.com', '+1122334455', 'softwaresolutions.com', 1),
('Consulting Group', 'James Hernandez', 'james@consulting.com', '+2233445566', 'consultinggroup.com', 1);

-- Insert sample customers (100 customers with realistic data)
INSERT INTO customers (name, instagram_handle, email, phone, customer_since, total_spent, last_purchase, business_id) VALUES
('Emma Johnson', 'emma_jewels', 'emma.johnson@email.com', '+1112223333', '2023-01-15', 1250.75, '2024-12-10', 1),
('Luca Rossi', 'luca_designs', 'luca.rossi@email.com', '+2223334444', '2023-02-20', 890.50, '2024-12-05', 1),
('Sophie Chen', 'sophie_style', 'sophie.chen@email.com', '+3334445555', '2023-03-10', 2100.00, '2024-12-01', 1),
('Marcus Lee', 'marcus_creates', 'marcus.lee@email.com', '+4445556666', '2023-04-05', 750.25, '2024-11-28', 1),
('Isabella Garcia', 'bella_jewelry', 'isabella.garcia@email.com', '+5556667777', '2023-05-12', 1850.00, '2024-11-25', 1),
('Oliver Smith', 'oliver_smith', 'oliver.smith@email.com', '+6667778888', '2023-06-18', 620.80, '2024-11-20', 1),
('Chloe Williams', 'chloe_designs', 'chloe.williams@email.com', '+7778889999', '2023-07-22', 1450.30, '2024-11-15', 1),
('Noah Brown', 'noah_brown', 'noah.brown@email.com', '+8889990000', '2023-08-30', 980.45, '2024-11-10', 1),
('Mia Taylor', 'mia_taylor', 'mia.taylor@email.com', '+9990001111', '2023-09-05', 1120.60, '2024-11-05', 1),
('Liam Miller', 'liam_miller', 'liam.miller@email.com', '+0001112222', '2023-10-10', 830.25, '2024-10-30', 1),
-- Add 90 more customers with realistic variations...
('Ava Davis', 'ava_davis', 'ava.davis@email.com', '+1112223334', '2023-11-15', 1560.90, '2024-10-25', 1),
('Ethan Wilson', 'ethan_wilson', 'ethan.wilson@email.com', '+2223334445', '2023-12-20', 720.35, '2024-10-20', 1),
('Charlotte Moore', 'charlotte_moore', 'charlotte.moore@email.com', '+3334445556', '2024-01-25', 1950.40, '2024-10-15', 1),
('Benjamin Anderson', 'ben_anderson', 'benjamin.anderson@email.com', '+4445556667', '2024-02-28', 540.75, '2024-10-10', 1),
('Amelia Thomas', 'amelia_thomas', 'amelia.thomas@email.com', '+5556667778', '2024-03-15', 1780.20, '2024-10-05', 1),
('James Jackson', 'james_jackson', 'james.jackson@email.com', '+6667778889', '2024-04-20', 910.65, '2024-09-30', 1),
('Harper White', 'harper_white', 'harper.white@email.com', '+7778889990', '2024-05-25', 1320.80, '2024-09-25', 1),
('Lucas Harris', 'lucas_harris', 'lucas.harris@email.com', '+8889990001', '2024-06-30', 670.95, '2024-09-20', 1),
('Evelyn Martin', 'evelyn_martin', 'evelyn.martin@email.com', '+9990001112', '2024-07-05', 1480.10, '2024-09-15', 1),
('Alexander Thompson', 'alex_thompson', 'alexander.thompson@email.com', '+0001112223', '2024-08-10', 850.45, '2024-09-10', 1);

-- Insert inventory items
INSERT INTO inventory (name, description, category, unit_cost, quantity, reorder_level, supplier_id, business_id) VALUES
('Sterling Silver Chain', '1mm sterling silver chain per meter', 'Materials', 25.50, 100, 20, 1, 1),
('Gold-plated Earring Hooks', 'Gold-plated fishhook earrings', 'Materials', 0.75, 500, 100, 2, 1),
('Swarovski Crystals', 'Assorted Swarovski crystals pack', 'Materials', 45.00, 50, 10, 3, 1),
('Leather Cord', '2mm black leather cord per meter', 'Materials', 3.20, 200, 40, 4, 1),
('Freshwater Pearls', 'Assorted freshwater pearls', 'Materials', 85.00, 30, 5, 5, 1),
('Amethyst Beads', '6mm amethyst beads strand', 'Materials', 32.00, 40, 8, 6, 1),
('Silver Clasps', 'Sterling silver lobster clasps', 'Materials', 2.50, 300, 50, 7, 1),
('Jewelry Boxes', 'Small velvet jewelry boxes', 'Packaging', 1.80, 200, 40, 8, 1),
('Pliers Set', 'Professional jewelry pliers set', 'Tools', 45.00, 10, 2, 9, 1),
('Shipping Boxes', 'Small shipping boxes 10x10x5cm', 'Shipping', 0.60, 500, 100, 10, 1);

-- Insert sample transactions (linked to customers and suppliers)
INSERT INTO transactions (transaction_date, amount, type, category_id, description, customer_id, supplier_id, user_id, business_id, payment_method) VALUES
-- Sales to customers (income)
('2024-12-01', 89.99, 'income', 9, 'Silver necklace with crystal', 1, NULL, 1, 1, 'card'),
('2024-12-02', 45.50, 'income', 10, 'Gold-plated earrings', 2, NULL, 1, 1, 'paypal'),
('2024-12-03', 120.00, 'income', 11, 'Leather bracelet set', 3, NULL, 1, 1, 'cash'),
('2024-12-04', 75.25, 'income', 12, 'Custom engraved ring', 4, NULL, 1, 1, 'card'),
('2024-12-05', 200.00, 'income', 13, 'Custom wedding necklace', 5, NULL, 1, 1, 'bank_transfer'),
-- Expenses from suppliers
('2024-12-01', 255.00, 'expense', 1, 'Silver chains purchase', NULL, 1, 1, 1, 'card'),
('2024-12-02', 37.50, 'expense', 1, 'Earring hooks', NULL, 2, 1, 1, 'paypal'),
('2024-12-03', 225.00, 'expense', 1, 'Swarovski crystals', NULL, 3, 1, 1, 'bank_transfer'),
('2024-12-04', 64.00, 'expense', 1, 'Leather cord', NULL, 4, 1, 1, 'card'),
('2024-12-05', 170.00, 'expense', 1, 'Freshwater pearls', NULL, 5, 1, 1, 'card'),
('2024-12-06', 96.00, 'expense', 2, 'Jewelry boxes', NULL, 8, 1, 1, 'paypal'),
('2024-12-07', 45.00, 'expense', 5, 'New pliers set', NULL, 9, 1, 1, 'card'),
('2024-12-08', 30.00, 'expense', 3, 'Shipping supplies', NULL, 10, 1, 1, 'cash'),
('2024-12-09', 150.00, 'expense', 4, 'Instagram ads', NULL, 11, 1, 1, 'card'),
('2024-12-10', 99.99, 'expense', 6, 'Website hosting', NULL, 12, 1, 1, 'card');

-- Insert budgets for university requirement
INSERT INTO budgets (name, category_id, amount, period, start_date, end_date, business_id) VALUES
('Monthly Materials Budget', 1, 1000.00, 'monthly', '2024-12-01', '2024-12-31', 1),
('Monthly Marketing Budget', 4, 500.00, 'monthly', '2024-12-01', '2024-12-31', 1),
('Monthly Packaging Budget', 2, 200.00, 'monthly', '2024-12-01', '2024-12-31', 1),
('Quarterly Tools Budget', 5, 300.00, 'quarterly', '2024-10-01', '2024-12-31', 1),
('Yearly Website Budget', 6, 1200.00, 'yearly', '2024-01-01', '2024-12-31', 1);

-- Create indexes for performance
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_transactions_customer ON transactions(customer_id);
CREATE INDEX idx_transactions_supplier ON transactions(supplier_id);
CREATE INDEX idx_transactions_type ON transactions(type);
CREATE INDEX idx_customers_instagram ON customers(instagram_handle);
CREATE INDEX idx_customers_email ON customers(email);

SELECT '✅ Database initialized with complete business schema!' as status;



-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
-- -- -- -- -- INITIAL VERSION OF DB -- -- -- -- -- 
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

-- -- Shiny Jar Database Initialization
-- -- Version: Simple - No Foreign Keys for now

-- -- Drop tables if they exist (clean start)
-- DROP TABLE IF EXISTS transactions CASCADE;
-- DROP TABLE IF EXISTS customers CASCADE;
-- DROP TABLE IF EXISTS users CASCADE;
-- DROP TABLE IF EXISTS businesses CASCADE;

-- -- Create businesses table FIRST
-- CREATE TABLE businesses (
--     id SERIAL PRIMARY KEY,
--     name VARCHAR(100) NOT NULL UNIQUE,
--     instagram_handle VARCHAR(50),
--     currency VARCHAR(3) DEFAULT 'EUR',
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- -- Create users table
-- CREATE TABLE users (
--     id SERIAL PRIMARY KEY,
--     username VARCHAR(50) UNIQUE NOT NULL,
--     email VARCHAR(100) UNIQUE NOT NULL,
--     full_name VARCHAR(100),
--     hashed_password VARCHAR(255) NOT NULL,
--     is_active BOOLEAN DEFAULT true,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     business_id INTEGER REFERENCES businesses(id)
-- );

-- -- Create transactions table
-- CREATE TABLE transactions (
--     id SERIAL PRIMARY KEY,
--     amount DECIMAL(10, 2) NOT NULL,
--     type VARCHAR(10) CHECK (type IN ('expense', 'income')),
--     category VARCHAR(50),
--     description TEXT,
--     date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     business_id INTEGER REFERENCES businesses(id),
--     user_id INTEGER REFERENCES users(id)
-- );

-- -- Create customers table
-- CREATE TABLE customers (
--     id SERIAL PRIMARY KEY,
--     name VARCHAR(100) NOT NULL,
--     instagram_handle VARCHAR(50),
--     email VARCHAR(100),
--     phone VARCHAR(20),
--     first_order_date DATE,
--     total_spent DECIMAL(10, 2) DEFAULT 0.00,
--     notes TEXT,
--     business_id INTEGER REFERENCES businesses(id),
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- -- Insert sample business (Shiny Jar) - MUST BE FIRST!
-- INSERT INTO businesses (name, instagram_handle, currency) 
-- VALUES ('Shiny Jar', 'shiny_jar', 'EUR');

-- -- Insert admin user (password: admin123)
-- INSERT INTO users (username, email, full_name, hashed_password, business_id) 
-- VALUES (
--     'admin', 
--     'admin@shinyjar.com', 
--     'Admin User', 
--     '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
--     1  -- Business ID 1 (Shiny Jar)
-- );

-- -- Sample transactions
-- INSERT INTO transactions (amount, type, category, description, business_id, user_id) VALUES
-- (150.00, 'expense', 'Materials', 'Silver chains', 1, 1),
-- (45.00, 'expense', 'Packaging', 'Jewelry boxes', 1, 1),
-- (89.00, 'income', 'Sales', 'Necklace sale', 1, 1),
-- (120.00, 'income', 'Sales', 'Earrings sale', 1, 1);

-- -- Sample customers
-- INSERT INTO customers (name, instagram_handle, email, total_spent, business_id) VALUES
-- ('Maria Silva', 'maria_silva', 'maria@email.com', 250.00, 1),
-- ('John Doe', 'john_jewelry', 'john@email.com', 180.00, 1),
-- ('Anna Smith', 'anna_sparkle', 'anna@email.com', 320.00, 1);

-- -- Success message
-- SELECT '✅ Database initialized successfully!' as message;