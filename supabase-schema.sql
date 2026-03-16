-- Modern Online Store - Supabase Database Schema
-- Run this SQL in your Supabase SQL Editor to create all tables

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ==================== USERS ====================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone VARCHAR(20),
    avatar VARCHAR(500) DEFAULT 'default-avatar.png',
    avatar_path VARCHAR(500),
    currency_preference VARCHAR(3) DEFAULT 'ZAR',
    is_admin BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster lookups
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- ==================== ADDRESSES ====================
CREATE TABLE addresses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    address_type VARCHAR(20) DEFAULT 'shipping',
    street_address VARCHAR(255) NOT NULL,
    address_line2 VARCHAR(100),
    city VARCHAR(100) NOT NULL,
    province VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) DEFAULT 'South Africa',
    phone VARCHAR(20),
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_addresses_user_id ON addresses(user_id);

-- ==================== PRODUCTS ====================
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price FLOAT NOT NULL,
    category VARCHAR(100) NOT NULL,
    image VARCHAR(500),
    images TEXT,
    rating FLOAT DEFAULT 0.0,
    reviews_count INTEGER DEFAULT 0,
    stock_quantity INTEGER DEFAULT 100,
    weight_kg FLOAT DEFAULT 1.0,
    dimensions_cm VARCHAR(50),
    is_featured BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_active ON products(is_active);

-- ==================== ORDERS ====================
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_number VARCHAR(20) UNIQUE NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    total_amount FLOAT NOT NULL,
    subtotal FLOAT DEFAULT 0.0,
    shipping_cost FLOAT DEFAULT 0.0,
    tax_amount FLOAT DEFAULT 0.0,
    discount_amount FLOAT DEFAULT 0.0,
    currency VARCHAR(3) DEFAULT 'ZAR',
    shipping_method VARCHAR(50),
    shipping_method_name VARCHAR(100),
    shipping_zone VARCHAR(100),
    tracking_number VARCHAR(100),
    bobgo_shipment_id VARCHAR(100),
    shipping_name VARCHAR(200),
    shipping_address TEXT,
    shipping_city VARCHAR(100),
    shipping_province VARCHAR(100),
    shipping_postal_code VARCHAR(20),
    shipping_country VARCHAR(100),
    shipping_phone VARCHAR(20),
    payment_method VARCHAR(50),
    payment_status VARCHAR(50) DEFAULT 'pending',
    payment_reference VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_number ON orders(order_number);

-- ==================== ORDER ITEMS ====================
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE NOT NULL,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    product_name VARCHAR(200),
    product_image VARCHAR(500),
    quantity INTEGER NOT NULL,
    price FLOAT NOT NULL,
    subtotal FLOAT NOT NULL
);

CREATE INDEX idx_order_items_order_id ON order_items(order_id);

-- ==================== SHIPPING ZONES ====================
CREATE TABLE shipping_zones (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    regions TEXT,
    base_rate FLOAT DEFAULT 0.0,
    per_kg_rate FLOAT DEFAULT 0.0,
    estimated_days VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==================== SHIPPING METHODS ====================
CREATE TABLE shipping_methods (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(255),
    multiplier FLOAT DEFAULT 1.0,
    bobgo_service_code VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==================== CURRENCY RATES ====================
CREATE TABLE currency_rates (
    id SERIAL PRIMARY KEY,
    base_currency VARCHAR(3) DEFAULT 'ZAR',
    target_currency VARCHAR(3) NOT NULL,
    rate FLOAT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(base_currency, target_currency)
);

-- ==================== ORDER TRACKING ====================
CREATE TABLE order_tracking (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE NOT NULL,
    status VARCHAR(50) NOT NULL,
    message VARCHAR(500),
    location VARCHAR(200),
    bobgo_update BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_order_tracking_order_id ON order_tracking(order_id);

-- ==================== CARTS ====================
CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_carts_user_id ON carts(user_id);

-- ==================== CART ITEMS ====================
CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    cart_id INTEGER REFERENCES carts(id) ON DELETE CASCADE NOT NULL,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE NOT NULL,
    quantity INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cart_items_cart_id ON cart_items(cart_id);

-- ==================== DEFAULT DATA ====================

-- Insert default admin user (password: Nozibusiso89)
-- The password hash is generated using bcrypt
INSERT INTO users (username, email, password_hash, first_name, last_name, is_admin, is_active)
VALUES (
    'ThandoHlomuka',
    'admin@modernstore.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS3MebAJu',
    'Thando',
    'Hlomuka',
    TRUE,
    TRUE
);

-- Insert default shipping zones
INSERT INTO shipping_zones (name, code, regions, base_rate, per_kg_rate, estimated_days) VALUES
('Gauteng', 'gauteng', '["Gauteng", "Johannesburg", "Pretoria", "Soweto"]', 65.00, 15.00, '1-2'),
('Western Cape', 'western_cape', '["Western Cape", "Cape Town", "Stellenbosch"]', 85.00, 18.00, '2-3'),
('KwaZulu-Natal', 'kwazulu_natal', '["KwaZulu-Natal", "Durban", "Pietermaritzburg"]', 80.00, 17.00, '2-3'),
('Other South Africa', 'other_sa', '["Free State", "North West", "Northern Cape", "Mpumalanga", "Limpopo"]', 95.00, 22.00, '3-5'),
('Southern Africa (SADC)', 'southern_africa', '["Namibia", "Botswana", "Lesotho", "Eswatini", "Zimbabwe", "Mozambique"]', 250.00, 45.00, '5-10'),
('International', 'international', '[]', 450.00, 85.00, '7-21');

-- Insert default shipping methods
INSERT INTO shipping_methods (name, code, description, multiplier) VALUES
('Standard Shipping', 'standard', '5-7 business days', 1.0),
('Express Shipping', 'express', '2-3 business days', 1.5),
('Overnight Delivery', 'overnight', 'Next business day', 2.5),
('Bobgo Pudo Pickup', 'bobgo_pudo', 'Collect from Pudo point', 0.7);

-- Insert default currency rates (ZAR base)
INSERT INTO currency_rates (base_currency, target_currency, rate) VALUES
('ZAR', 'USD', 0.053),
('ZAR', 'EUR', 0.049),
('ZAR', 'GBP', 0.042),
('ZAR', 'NGN', 82.5),
('ZAR', 'KES', 8.5),
('ZAR', 'BWP', 0.72);

-- Insert sample products
INSERT INTO products (name, description, price, category, image, rating, reviews_count, stock_quantity, weight_kg, is_featured, is_active) VALUES
('Premium Wireless Headphones', 'High-quality wireless headphones with noise cancellation', 4999.00, 'Electronics', 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400', 4.8, 256, 50, 0.5, TRUE, TRUE),
('Minimalist Watch', 'Elegant minimalist design with premium materials', 3499.00, 'Accessories', 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400', 4.9, 189, 30, 0.2, TRUE, TRUE),
('Smart Home Speaker', 'Voice-controlled speaker with premium sound quality', 2799.00, 'Electronics', 'https://images.unsplash.com/photo-1589492477829-5e65395b66cc?w=400', 4.6, 342, 45, 1.0, FALSE, TRUE),
('Designer Sunglasses', 'UV protection with stylish modern design', 1899.00, 'Accessories', 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400', 4.7, 128, 60, 0.1, FALSE, TRUE),
('Leather Backpack', 'Premium leather backpack with laptop compartment', 2999.00, 'Bags', 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400', 4.8, 215, 25, 1.2, TRUE, TRUE),
('Mechanical Keyboard', 'RGB backlit mechanical keyboard with custom switches', 2499.00, 'Electronics', 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400', 4.9, 445, 40, 1.5, FALSE, TRUE),
('Running Shoes', 'Lightweight running shoes with superior comfort', 1999.00, 'Footwear', 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400', 4.5, 567, 100, 0.8, FALSE, TRUE),
('Portable Charger', '20000mAh fast charging power bank', 899.00, 'Electronics', 'https://images.unsplash.com/photo-1609599006353-e629aaabfeae?w=400', 4.6, 892, 150, 0.4, FALSE, TRUE);

-- ==================== STORAGE BUCKET (Supabase Specific) ====================
-- Run this in Supabase Dashboard > Storage to create the avatars bucket
-- Or use the SQL editor with storage schema:

-- Create the avatars storage bucket
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES ('avatars', 'avatars', true, 5242880, ARRAY['image/png', 'image/jpeg', 'image/gif', 'image/webp'])
ON CONFLICT (id) DO NOTHING;

-- Enable Row Level Security for storage objects
ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY;

-- Create policy for users to upload their own avatars
CREATE POLICY "Users can upload own avatar"
ON storage.objects FOR INSERT
WITH CHECK (
    bucket_id = 'avatars' 
    AND (storage.foldername(name))[1] = 'user_' || auth.uid()::text
);

-- Create policy for users to update their own avatar
CREATE POLICY "Users can update own avatar"
ON storage.objects FOR UPDATE
USING (
    bucket_id = 'avatars' 
    AND (storage.foldername(name))[1] = 'user_' || auth.uid()::text
);

-- Create policy for users to delete their own avatar
CREATE POLICY "Users can delete own avatar"
ON storage.objects FOR DELETE
USING (
    bucket_id = 'avatars' 
    AND (storage.foldername(name))[1] = 'user_' || auth.uid()::text
);

-- Create policy for public to view all avatars
CREATE POLICY "Public can view avatars"
ON storage.objects FOR SELECT
USING (bucket_id = 'avatars');

-- Create policy for authenticated users to list avatars
CREATE POLICY "Authenticated users can list avatars"
ON storage.objects FOR SELECT
TO authenticated
USING (bucket_id = 'avatars');

-- ==================== ADDITIONAL SAMPLE PRODUCTS ====================
-- More products for a fuller store

INSERT INTO products (name, description, price, category, image, rating, reviews_count, stock_quantity, weight_kg, is_featured, is_active) VALUES
('Wireless Earbuds Pro', 'True wireless earbuds with active noise cancellation and 30-hour battery life', 1899.00, 'Electronics', 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400', 4.7, 423, 75, 0.15, TRUE, TRUE),
('Canvas Tote Bag', 'Eco-friendly canvas tote bag perfect for daily use', 399.00, 'Bags', 'https://images.unsplash.com/photo-1544816155-12df9643f363?w=400', 4.4, 156, 200, 0.4, FALSE, TRUE),
('Smart Fitness Tracker', 'Advanced fitness tracker with heart rate monitor and GPS', 2499.00, 'Electronics', 'https://images.unsplash.com/photo-1575311373947-33761188c879?w=400', 4.6, 289, 60, 0.08, FALSE, TRUE),
('Classic Leather Wallet', 'Genuine leather wallet with RFID protection', 799.00, 'Accessories', 'https://images.unsplash.com/photo-1627123424574-18bd08331092?w=400', 4.8, 312, 120, 0.2, FALSE, TRUE),
('Yoga Mat Premium', 'Non-slip yoga mat with alignment lines, 6mm thick', 599.00, 'Other', 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400', 4.5, 178, 90, 1.8, FALSE, TRUE),
('Stainless Steel Water Bottle', 'Insulated water bottle keeps drinks cold for 24h or hot for 12h', 349.00, 'Other', 'https://images.unsplash.com/photo-1602143407151-011141951e7a?w=400', 4.7, 534, 150, 0.35, FALSE, TRUE),
('Bluetooth Portable Speaker', 'Waterproof portable speaker with 360° sound', 1299.00, 'Electronics', 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400', 4.6, 267, 80, 0.6, TRUE, TRUE),
('Denim Jacket Classic', 'Timeless denim jacket with modern fit', 1599.00, 'Clothing', 'https://images.unsplash.com/photo-1576995853123-5a297da4030e?w=400', 4.5, 198, 45, 0.9, FALSE, TRUE),
('Ceramic Coffee Mug Set', 'Set of 4 handcrafted ceramic mugs', 499.00, 'Home', 'https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=400', 4.8, 145, 100, 1.2, FALSE, TRUE),
('USB-C Hub Multi-Port', '7-in-1 USB-C hub with HDMI, USB 3.0, and SD card reader', 899.00, 'Electronics', 'https://images.unsplash.com/photo-1625842268584-8f3296236761?w=400', 4.4, 234, 70, 0.15, FALSE, TRUE),
('Scented Candle Collection', 'Set of 3 natural soy wax candles with essential oils', 449.00, 'Home', 'https://images.unsplash.com/photo-1602166556128-20c5e5f18760?w=400', 4.7, 167, 85, 0.8, FALSE, TRUE),
('Phone Stand Adjustable', 'Aluminum phone stand compatible with all smartphones', 249.00, 'Accessories', 'https://images.unsplash.com/photo-1586953229609-75f347c54710?w=400', 4.3, 89, 200, 0.25, FALSE, TRUE);

-- ==================== INDEXES FOR PERFORMANCE ====================
-- Additional indexes for better query performance

CREATE INDEX IF NOT EXISTS idx_products_featured ON products(is_featured);
CREATE INDEX IF NOT EXISTS idx_products_price ON products(price);
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_orders_payment_status ON orders(payment_status);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_shipping_zones_active ON shipping_zones(is_active);
CREATE INDEX IF NOT EXISTS idx_shipping_methods_active ON shipping_methods(is_active);

-- ==================== HELPER FUNCTIONS ====================

-- Function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at trigger to tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_orders_updated_at BEFORE UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_shipping_zones_updated_at BEFORE UPDATE ON shipping_zones
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
