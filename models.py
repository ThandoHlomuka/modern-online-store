"""
Database Models for Modern Online Store
Includes: Authentication, Profiles, Products, Orders, Shipping, Currency
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import uuid

db = SQLAlchemy()


def generate_uuid():
    return str(uuid.uuid4())


class User(UserMixin, db.Model):
    """User model for authentication and profiles"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, default=generate_uuid)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    avatar = db.Column(db.String(500), default='default-avatar.png')
    avatar_path = db.Column(db.String(500))  # Supabase storage path
    currency_preference = db.Column(db.String(3), default='ZAR')  # ZAR, USD, EUR, etc.
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    addresses = db.relationship('Address', backref='user', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.username
    
    def is_admin_user(self):
        return self.is_admin


class Address(db.Model):
    """User addresses for shipping"""
    __tablename__ = 'addresses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    address_type = db.Column(db.String(20), default='shipping')
    street_address = db.Column(db.String(255), nullable=False)
    address_line2 = db.Column(db.String(100))
    city = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(100))  # For South Africa
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), default='South Africa')
    phone = db.Column(db.String(20))
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Address {self.street_address}, {self.city}>'
    
    def get_full_address(self):
        parts = [self.street_address]
        if self.address_line2:
            parts.append(self.address_line2)
        region = self.province or self.state
        parts.append(f'{self.city}, {region} {self.postal_code}')
        parts.append(self.country)
        return ', '.join(parts)


class ShippingZone(db.Model):
    """Shipping zones for rate calculation"""
    __tablename__ = 'shipping_zones'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    regions = db.Column(db.Text)  # JSON string of provinces/countries
    base_rate = db.Column(db.Float, default=0.0)
    per_kg_rate = db.Column(db.Float, default=0.0)
    estimated_days = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ShippingZone {self.name}>'


class ShippingMethod(db.Model):
    """Shipping methods (Standard, Express, etc.)"""
    __tablename__ = 'shipping_methods'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    multiplier = db.Column(db.Float, default=1.0)
    bobgo_service_code = db.Column(db.String(50))  # Bobgo API service code
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ShippingMethod {self.name}>'


class Product(db.Model):
    """Product model for store items"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)  # Price in ZAR (base currency)
    category = db.Column(db.String(100), nullable=False, index=True)
    image = db.Column(db.String(500))
    images = db.Column(db.Text)  # JSON array of additional images
    rating = db.Column(db.Float, default=0.0)
    reviews_count = db.Column(db.Integer, default=0)
    stock_quantity = db.Column(db.Integer, default=100)
    weight_kg = db.Column(db.Float, default=1.0)  # For shipping calculation
    dimensions_cm = db.Column(db.String(50))  # Format: "LxWxH"
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def in_stock(self):
        return self.stock_quantity > 0


class Order(db.Model):
    """Order model for customer purchases"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), default='pending')
    total_amount = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, default=0.0)
    shipping_cost = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    discount_amount = db.Column(db.Float, default=0.0)
    currency = db.Column(db.String(3), default='ZAR')
    
    # Shipping details
    shipping_method = db.Column(db.String(50))
    shipping_method_name = db.Column(db.String(100))
    shipping_zone = db.Column(db.String(100))
    tracking_number = db.Column(db.String(100))
    bobgo_shipment_id = db.Column(db.String(100))
    
    # Address snapshot (in case address changes later)
    shipping_name = db.Column(db.String(200))
    shipping_address = db.Column(db.Text)
    shipping_city = db.Column(db.String(100))
    shipping_province = db.Column(db.String(100))
    shipping_postal_code = db.Column(db.String(20))
    shipping_country = db.Column(db.String(100))
    shipping_phone = db.Column(db.String(20))
    
    # Payment
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(50), default='pending')
    payment_reference = db.Column(db.String(100))
    
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.order_number}>'
    
    def generate_order_number(self):
        return f'ORD-{datetime.utcnow().strftime("%Y%m%d")}-{uuid.uuid4().hex[:8].upper()}'


class OrderItem(db.Model):
    """Individual items in an order"""
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_name = db.Column(db.String(200))  # Snapshot in case product changes
    product_image = db.Column(db.String(500))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    
    # Relationships
    product = db.relationship('Product', backref='order_items')
    
    def __repr__(self):
        return f'<OrderItem {self.product_name} x {self.quantity}>'


class Cart(db.Model):
    """Persistent cart storage"""
    __tablename__ = 'carts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('CartItem', backref='cart', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Cart {self.user_id}>'


class CartItem(db.Model):
    """Individual items in a cart"""
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    product = db.relationship('Product', backref='cart_items')
    
    def __repr__(self):
        return f'<CartItem {self.product.name}>'


class CurrencyRate(db.Model):
    """Currency exchange rates"""
    __tablename__ = 'currency_rates'
    
    id = db.Column(db.Integer, primary_key=True)
    base_currency = db.Column(db.String(3), default='ZAR')
    target_currency = db.Column(db.String(3), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('base_currency', 'target_currency', name='unique_currency_pair'),)
    
    def __repr__(self):
        return f'<CurrencyRate {self.base_currency}/{self.target_currency}>'


class OrderTracking(db.Model):
    """Order tracking events"""
    __tablename__ = 'order_tracking'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500))
    location = db.Column(db.String(200))
    bobgo_update = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    order = db.relationship('Order', backref='tracking_events')
    
    def __repr__(self):
        return f'<OrderTracking {self.order.order_number} - {self.status}>'


def init_db(app):
    """Initialize database with app context"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        create_default_data()


def create_default_data():
    """Create default admin user and shipping data"""
    from flask_bcrypt import Bcrypt
    bcrypt = Bcrypt()
    
    # Create admin user
    admin = User.query.filter_by(username='ThandoHlomuka').first()
    if not admin:
        admin = User(
            username='ThandoHlomuka',
            email='admin@modernstore.com',
            password_hash=bcrypt.generate_password_hash('Nozibusiso89').decode('utf-8'),
            first_name='Thando',
            last_name='Hlomuka',
            is_admin=True,
            is_active=True
        )
        db.session.add(admin)
        print('Admin user created!')
    
    # Create default shipping zones
    default_zones = [
        {'name': 'Gauteng', 'code': 'gauteng', 'regions': '["Gauteng", "Johannesburg", "Pretoria", "Soweto"]', 'base_rate': 65.00, 'per_kg_rate': 15.00, 'estimated_days': '1-2'},
        {'name': 'Western Cape', 'code': 'western_cape', 'regions': '["Western Cape", "Cape Town", "Stellenbosch"]', 'base_rate': 85.00, 'per_kg_rate': 18.00, 'estimated_days': '2-3'},
        {'name': 'KwaZulu-Natal', 'code': 'kwazulu_natal', 'regions': '["KwaZulu-Natal", "Durban", "Pietermaritzburg"]', 'base_rate': 80.00, 'per_kg_rate': 17.00, 'estimated_days': '2-3'},
        {'name': 'Other South Africa', 'code': 'other_sa', 'regions': '["Free State", "North West", "Northern Cape", "Mpumalanga", "Limpopo"]', 'base_rate': 95.00, 'per_kg_rate': 22.00, 'estimated_days': '3-5'},
        {'name': 'Southern Africa (SADC)', 'code': 'southern_africa', 'regions': '["Namibia", "Botswana", "Lesotho", "Eswatini", "Zimbabwe", "Mozambique"]', 'base_rate': 250.00, 'per_kg_rate': 45.00, 'estimated_days': '5-10'},
        {'name': 'International', 'code': 'international', 'regions': '[]', 'base_rate': 450.00, 'per_kg_rate': 85.00, 'estimated_days': '7-21'},
    ]
    
    for zone_data in default_zones:
        existing = ShippingZone.query.filter_by(code=zone_data['code']).first()
        if not existing:
            zone = ShippingZone(**zone_data)
            db.session.add(zone)
    
    # Create default shipping methods
    default_methods = [
        {'name': 'Standard Shipping', 'code': 'standard', 'description': '5-7 business days', 'multiplier': 1.0},
        {'name': 'Express Shipping', 'code': 'express', 'description': '2-3 business days', 'multiplier': 1.5},
        {'name': 'Overnight Delivery', 'code': 'overnight', 'description': 'Next business day', 'multiplier': 2.5},
        {'name': 'Bobgo Pudo Pickup', 'code': 'bobgo_pudo', 'description': 'Collect from Pudo point', 'multiplier': 0.7},
    ]
    
    for method_data in default_methods:
        existing = ShippingMethod.query.filter_by(code=method_data['code']).first()
        if not existing:
            method = ShippingMethod(**method_data)
            db.session.add(method)
    
    # Create default currency rates (ZAR base)
    default_rates = [
        {'base_currency': 'ZAR', 'target_currency': 'USD', 'rate': 0.053},
        {'base_currency': 'ZAR', 'target_currency': 'EUR', 'rate': 0.049},
        {'base_currency': 'ZAR', 'target_currency': 'GBP', 'rate': 0.042},
        {'base_currency': 'ZAR', 'target_currency': 'NGN', 'rate': 82.5},
        {'base_currency': 'ZAR', 'target_currency': 'KES', 'rate': 8.5},
        {'base_currency': 'ZAR', 'target_currency': 'BWP', 'rate': 0.72},
    ]
    
    for rate_data in default_rates:
        existing = CurrencyRate.query.filter_by(
            base_currency=rate_data['base_currency'],
            target_currency=rate_data['target_currency']
        ).first()
        if not existing:
            rate = CurrencyRate(**rate_data)
            db.session.add(rate)
    
    db.session.commit()
    print('Default data created!')
