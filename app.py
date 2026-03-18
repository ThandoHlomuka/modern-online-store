"""
Modern Online Store - Flask Application
With Authentication, User Profiles, Admin Dashboard, Multi-Currency & Shipping

PostgreSQL Database Required
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
import os
import json
from datetime import datetime

from database import DATABASE_URI, USE_POSTGRES
from models import db, User, Product, Order, OrderItem, Address, Cart, CartItem
from models import ShippingZone, ShippingMethod, CurrencyRate, OrderTracking
from forms import (LoginForm, RegistrationForm, ProfileForm, ChangePasswordForm,
                   AddressForm, ProductForm, OrderStatusForm, ShippingZoneForm)
from currency import (convert_currency, format_currency, get_currency_options,
                      DEFAULT_CURRENCY, CURRENCY_SYMBOLS, EXCHANGE_RATES)
from shipping import (get_shipping_options, calculate_shipping_cost, get_shipping_zone,
                      estimate_order_weight)
from upload import process_avatar_upload, upload_base64_image, get_avatar_url, delete_from_supabase

# Initialize extensions
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'modern-store-secret-key-2024')
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_TIME_LIMIT'] = 3600
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max upload

# Initialize extensions
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Initialize database
db.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Add context processor for currency
@app.context_processor
def inject_currency():
    """Make currency functions available in templates"""
    return {
        'convert_currency': convert_currency,
        'format_currency': format_currency,
        'get_currency_options': get_currency_options,
        'CURRENCY_SYMBOLS': CURRENCY_SYMBOLS,
        'user_currency': session.get('currency', DEFAULT_CURRENCY),
        'get_avatar_url': get_avatar_url
    }


# ==================== PUBLIC ROUTES ====================

@app.route('/')
def index():
    """Home page with featured products"""
    featured_products = Product.query.filter_by(is_featured=True, is_active=True).limit(4).all()
    if not featured_products:
        featured_products = Product.query.filter_by(is_active=True).limit(4).all()
    
    currency = session.get('currency', DEFAULT_CURRENCY)
    
    return render_template('index.html', products=featured_products, categories=CATEGORIES, currency=currency)


@app.route('/shop')
def shop():
    """Shop page with all products"""
    category = request.args.get('category', 'All')
    currency = session.get('currency', DEFAULT_CURRENCY)
    
    if category == 'All':
        products = Product.query.filter_by(is_active=True).all()
    else:
        products = Product.query.filter_by(category=category, is_active=True).all()
    
    return render_template('shop.html', products=products, categories=CATEGORIES, 
                         current_category=category, currency=currency)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Product detail page"""
    product = Product.query.get_or_404(product_id)
    related_products = Product.query.filter_by(category=product.category, is_active=True).filter(
        Product.id != product.id).limit(3).all()
    currency = session.get('currency', DEFAULT_CURRENCY)
    
    return render_template('product.html', product=product, related_products=related_products, currency=currency)


@app.route('/cart')
def cart():
    """Shopping cart page"""
    currency = session.get('currency', DEFAULT_CURRENCY)
    return render_template('cart.html', currency=currency)


@app.route('/api/set-currency', methods=['POST'])
def set_currency():
    """Set user's currency preference"""
    data = request.get_json()
    currency = data.get('currency', DEFAULT_CURRENCY)
    
    if currency in EXCHANGE_RATES:
        session['currency'] = currency
        if current_user.is_authenticated:
            current_user.currency_preference = currency
            db.session.commit()
        return jsonify({'success': True, 'currency': currency})
    
    return jsonify({'success': False, 'error': 'Invalid currency'}), 400


# ==================== AUTHENTICATION ROUTES ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember_me.data)
            session['currency'] = user.currency_preference or DEFAULT_CURRENCY
            flash('Welcome back, ' + user.get_full_name() + '!', 'success')
            next_page = request.args.get('next')
            if user.is_admin:
                return redirect(next_page) if next_page else redirect(url_for('admin_dashboard'))
            return redirect(next_page) if next_page else redirect(url_for('profile'))
        flash('Invalid username or password', 'danger')
    return render_template('auth/login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=password_hash,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            currency_preference=DEFAULT_CURRENCY
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


# ==================== PROFILE ROUTES ====================

@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).limit(5).all()
    return render_template('profile/profile.html', orders=orders)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit profile"""
    form = ProfileForm(obj=current_user)
    form.current_user_id = current_user.id
    
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('profile/edit_profile.html', form=form)


@app.route('/profile/upload-avatar', methods=['POST'])
@login_required
def upload_avatar():
    """Upload profile picture"""
    if 'avatar' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['avatar']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    # Delete old avatar if exists
    if current_user.avatar_path:
        delete_from_supabase(current_user.avatar_path)
    
    # Process and upload new avatar
    result = process_avatar_upload(file, current_user.id)
    
    if result['success']:
        current_user.avatar = result['url']
        current_user.avatar_path = result['path']
        db.session.commit()
        return jsonify({'success': True, 'url': result['url']})
    
    return jsonify({'success': False, 'error': result.get('error', 'Upload failed')}), 400


@app.route('/profile/remove-avatar', methods=['POST'])
@login_required
def remove_avatar():
    """Remove profile picture"""
    if current_user.avatar_path:
        delete_from_supabase(current_user.avatar_path)
        current_user.avatar = 'default-avatar.png'
        current_user.avatar_path = None
        db.session.commit()
    return jsonify({'success': True})


@app.route('/profile/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password"""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password_hash, form.current_password.data):
            current_user.password_hash = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('profile'))
        flash('Current password is incorrect', 'danger')
    return render_template('profile/change_password.html', form=form)


@app.route('/profile/addresses')
@login_required
def addresses():
    """User addresses"""
    addresses = Address.query.filter_by(user_id=current_user.id).all()
    return render_template('profile/addresses.html', addresses=addresses)


@app.route('/profile/addresses/add', methods=['GET', 'POST'])
@login_required
def add_address():
    """Add new address"""
    form = AddressForm()
    if form.validate_on_submit():
        if form.is_default.data:
            Address.query.filter_by(user_id=current_user.id, address_type=form.address_type.data).update({'is_default': False})
        address = Address(
            user_id=current_user.id,
            address_type=form.address_type.data,
            street_address=form.street_address.data,
            address_line2=form.address_line2.data,
            city=form.city.data,
            province=form.province.data,
            state=form.state.data,
            postal_code=form.postal_code.data,
            country=form.country.data,
            phone=form.phone.data,
            is_default=form.is_default.data
        )
        db.session.add(address)
        db.session.commit()
        flash('Address added successfully!', 'success')
        return redirect(url_for('addresses'))
    return render_template('profile/address_form.html', form=form, title='Add Address')


@app.route('/profile/addresses/<int:address_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_address(address_id):
    """Edit address"""
    address = Address.query.get_or_404(address_id)
    if address.user_id != current_user.id:
        abort(403)
    
    form = AddressForm(obj=address)
    if form.validate_on_submit():
        if form.is_default.data:
            Address.query.filter_by(user_id=current_user.id, address_type=form.address_type.data).update({'is_default': False})
        address.address_type = form.address_type.data
        address.street_address = form.street_address.data
        address.address_line2 = form.address_line2.data
        address.city = form.city.data
        address.province = form.province.data
        address.state = form.state.data
        address.postal_code = form.postal_code.data
        address.country = form.country.data
        address.phone = form.phone.data
        address.is_default = form.is_default.data
        db.session.commit()
        flash('Address updated successfully!', 'success')
        return redirect(url_for('addresses'))
    return render_template('profile/address_form.html', form=form, title='Edit Address')


@app.route('/profile/addresses/<int:address_id>/delete', methods=['POST'])
@login_required
def delete_address(address_id):
    """Delete address"""
    address = Address.query.get_or_404(address_id)
    if address.user_id != current_user.id:
        abort(403)
    db.session.delete(address)
    db.session.commit()
    flash('Address deleted successfully!', 'success')
    return redirect(url_for('addresses'))


@app.route('/profile/orders')
@login_required
def orders():
    """User order history"""
    currency = session.get('currency', DEFAULT_CURRENCY)
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('profile/orders.html', orders=orders, currency=currency)


@app.route('/profile/orders/<order_number>')
@login_required
def order_detail(order_number):
    """Order detail page"""
    order = Order.query.filter_by(order_number=order_number, user_id=current_user.id).first_or_404()
    currency = session.get('currency', DEFAULT_CURRENCY)
    return render_template('profile/order_detail.html', order=order, currency=currency)


# ==================== ADMIN ROUTES ====================

@app.route('/admin')
@login_required
def admin_dashboard():
    """Admin dashboard"""
    if not current_user.is_admin:
        abort(403)
    
    total_users = User.query.count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    pending_orders = Order.query.filter_by(status='pending').count()
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    # Revenue calculation (in ZAR)
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).filter(
        Order.payment_status == 'paid').scalar() or 0
    
    return render_template('admin/dashboard.html', 
                         total_users=total_users, 
                         total_products=total_products,
                         total_orders=total_orders,
                         pending_orders=pending_orders,
                         total_revenue=total_revenue,
                         recent_orders=recent_orders)


@app.route('/admin/products')
@login_required
def admin_products():
    """Admin product management"""
    if not current_user.is_admin:
        abort(403)
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('admin/products.html', products=products)


@app.route('/admin/products/add', methods=['GET', 'POST'])
@login_required
def admin_add_product():
    """Add new product"""
    if not current_user.is_admin:
        abort(403)
    
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            category=form.category.data,
            image=form.image.data or 'https://via.placeholder.com/400',
            stock_quantity=form.stock_quantity.data,
            weight_kg=form.weight_kg.data or 1.0,
            is_featured=form.is_featured.data,
            is_active=form.is_active.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin_products'))
    return render_template('admin/product_form.html', form=form, title='Add Product')


@app.route('/admin/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_product(product_id):
    """Edit product"""
    if not current_user.is_admin:
        abort(403)
    
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.category = form.category.data
        product.image = form.image.data or product.image
        product.stock_quantity = form.stock_quantity.data
        product.weight_kg = form.weight_kg.data or product.weight_kg
        product.is_featured = form.is_featured.data
        product.is_active = form.is_active.data
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin_products'))
    return render_template('admin/product_form.html', form=form, title='Edit Product')


@app.route('/admin/products/<int:product_id>/delete', methods=['POST'])
@login_required
def admin_delete_product(product_id):
    """Delete product"""
    if not current_user.is_admin:
        abort(403)
    
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin_products'))


@app.route('/admin/orders')
@login_required
def admin_orders():
    """Admin order management"""
    if not current_user.is_admin:
        abort(403)
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)


@app.route('/admin/orders/<int:order_id>', methods=['GET', 'POST'])
@login_required
def admin_order_detail(order_id):
    """Admin order detail"""
    if not current_user.is_admin:
        abort(403)
    
    order = Order.query.get_or_404(order_id)
    form = OrderStatusForm(obj=order)
    
    if form.validate_on_submit():
        old_status = order.status
        order.status = form.status.data
        order.payment_status = form.payment_status.data
        order.notes = form.notes.data or order.notes
        
        # Add tracking event
        if order.status != old_status:
            tracking = OrderTracking(
                order_id=order.id,
                status=order.status,
                message=f'Order status changed to {order.status}'
            )
            db.session.add(tracking)
        
        db.session.commit()
        flash('Order updated successfully!', 'success')
        return redirect(url_for('admin_orders'))
    
    return render_template('admin/order_detail.html', order=order, form=form)


@app.route('/admin/users')
@login_required
def admin_users():
    """Admin user management"""
    if not current_user.is_admin:
        abort(403)
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)


@app.route('/admin/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
def admin_toggle_user_status(user_id):
    """Toggle user active status"""
    if not current_user.is_admin:
        abort(403)
    
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Cannot deactivate your own account', 'danger')
    else:
        user.is_active = not user.is_active
        db.session.commit()
        flash(f'User {"activated" if user.is_active else "deactivated"} successfully!', 'success')
    return redirect(url_for('admin_users'))


@app.route('/admin/shipping')
@login_required
def admin_shipping():
    """Admin shipping management"""
    if not current_user.is_admin:
        abort(403)
    
    zones = ShippingZone.query.all()
    methods = ShippingMethod.query.all()
    return render_template('admin/shipping.html', zones=zones, methods=methods)


@app.route('/admin/shipping/zones/add', methods=['POST'])
@login_required
def admin_add_shipping_zone():
    """Add shipping zone"""
    if not current_user.is_admin:
        abort(403)
    
    data = request.get_json()
    zone = ShippingZone(
        name=data.get('name'),
        code=data.get('code'),
        regions=json.dumps(data.get('regions', [])),
        base_rate=float(data.get('base_rate', 0)),
        per_kg_rate=float(data.get('per_kg_rate', 0)),
        estimated_days=data.get('estimated_days', '3-5')
    )
    db.session.add(zone)
    db.session.commit()
    return jsonify({'success': True})


@app.route('/admin/shipping/zones/<int:zone_id>/update', methods=['POST'])
@login_required
def admin_update_shipping_zone(zone_id):
    """Update shipping zone"""
    if not current_user.is_admin:
        abort(403)
    
    zone = ShippingZone.query.get_or_404(zone_id)
    data = request.get_json()
    
    zone.name = data.get('name', zone.name)
    zone.base_rate = float(data.get('base_rate', zone.base_rate))
    zone.per_kg_rate = float(data.get('per_kg_rate', zone.per_kg_rate))
    zone.estimated_days = data.get('estimated_days', zone.estimated_days)
    
    db.session.commit()
    return jsonify({'success': True})


# ==================== CHECKOUT & SHIPPING ====================

@app.route('/checkout')
@login_required
def checkout():
    """Checkout page"""
    currency = session.get('currency', DEFAULT_CURRENCY)
    return render_template('checkout.html', currency=currency)


@app.route('/api/shipping/calculate', methods=['POST'])
@login_required
def calculate_shipping():
    """Calculate shipping cost for checkout"""
    data = request.get_json()
    province = data.get('province', '')
    country = data.get('country', 'South Africa')
    method = data.get('method', 'standard')
    
    # Get cart items and estimate weight
    cart = session.get('cart', [])
    weight = estimate_order_weight(cart)
    
    # Get shipping options
    options = get_shipping_options(province, country, weight)
    
    # Find selected method
    selected = next((o for o in options if o['key'] == method), None)
    
    if selected:
        return jsonify({
            'success': True,
            'cost': selected['cost'],
            'method': selected['name'],
            'estimated_days': selected['estimated_days']
        })
    
    return jsonify({'success': False, 'error': 'Invalid shipping method'}), 400


@app.route('/api/checkout', methods=['POST'])
@login_required
def process_checkout():
    """Process checkout"""
    cart = session.get('cart', [])
    if not cart:
        return jsonify({'error': 'Cart is empty'}), 400
    
    data = request.get_json()
    
    # Calculate totals
    subtotal = sum(item['price'] * item['quantity'] for item in cart)
    weight = estimate_order_weight(cart)
    
    # Get shipping cost
    shipping_cost = data.get('shipping_cost', 0)
    
    # Calculate tax (15% VAT for South Africa)
    tax_rate = 0.15 if data.get('country') == 'South Africa' else 0
    tax_amount = subtotal * tax_rate
    
    total = subtotal + shipping_cost + tax_amount
    
    # Create order
    order = Order(
        user_id=current_user.id,
        order_number=f'ORD-{datetime.utcnow().strftime("%Y%m%d")}-{os.urandom(4).hex().upper()[:8]}',
        status='pending',
        payment_status='pending',
        currency=session.get('currency', DEFAULT_CURRENCY),
        subtotal=subtotal,
        shipping_cost=shipping_cost,
        tax_amount=tax_amount,
        total_amount=total,
        shipping_method=data.get('shipping_method', 'standard'),
        shipping_method_name=data.get('shipping_method_name', 'Standard Shipping'),
        shipping_zone=data.get('shipping_zone', ''),
        shipping_name=data.get('full_name', current_user.get_full_name()),
        shipping_address=data.get('address', ''),
        shipping_city=data.get('city', ''),
        shipping_province=data.get('province', ''),
        shipping_postal_code=data.get('postal_code', ''),
        shipping_country=data.get('country', 'South Africa'),
        shipping_phone=data.get('phone', current_user.phone or ''),
        payment_method=data.get('payment_method', 'card')
    )
    db.session.add(order)
    db.session.flush()
    
    # Create order items
    for item in cart:
        product = Product.query.get(item['id'])
        order_item = OrderItem(
            order_id=order.id,
            product_id=item['id'],
            product_name=item['name'],
            product_image=item.get('image', ''),
            quantity=item['quantity'],
            price=item['price'],
            subtotal=item['price'] * item['quantity']
        )
        db.session.add(order_item)
        
        # Update stock
        if product:
            product.stock_quantity -= item['quantity']
    
    # Add tracking event
    tracking = OrderTracking(
        order_id=order.id,
        status='pending',
        message='Order placed successfully'
    )
    db.session.add(tracking)
    
    db.session.commit()
    session['cart'] = []
    session.modified = True
    
    return jsonify({
        'success': True,
        'message': 'Order placed successfully!',
        'order_id': order.id,
        'order_number': order.order_number
    })


# ==================== API ROUTES ====================

@app.route('/api/cart', methods=['GET'])
def get_cart():
    """Get cart items from session"""
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    currency = session.get('currency', DEFAULT_CURRENCY)
    
    # Convert to user's currency
    if currency != DEFAULT_CURRENCY:
        total = convert_currency(total, DEFAULT_CURRENCY, currency)
    
    return jsonify({
        'items': cart,
        'total': round(total, 2),
        'count': len(cart),
        'currency': currency
    })


@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    data = request.get_json()
    product_id = data.get('product_id')
    
    if product_id is None:
        return jsonify({'error': 'Product ID required'}), 400
    
    product = Product.query.get(int(product_id))
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    cart = session.get('cart', [])
    
    for item in cart:
        if item['id'] == int(product_id):
            item['quantity'] += 1
            session['cart'] = cart
            session.modified = True
            return jsonify({'message': 'Quantity updated', 'cart_count': len(cart)})
    
    cart.append({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'image': product.image,
        'category': product.category,
        'quantity': 1
    })
    session['cart'] = cart
    session.modified = True
    return jsonify({'message': 'Added to cart', 'cart_count': len(cart)})


@app.route('/api/cart/remove', methods=['POST'])
def remove_from_cart():
    """Remove item from cart"""
    data = request.get_json()
    product_id = data.get('product_id')
    
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    session.modified = True
    
    total = sum(item['price'] * item['quantity'] for item in cart)
    return jsonify({'items': cart, 'total': round(total, 2), 'count': len(cart)})


@app.route('/api/cart/update', methods=['POST'])
def update_cart():
    """Update item quantity in cart"""
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] = max(1, quantity)
            break
    
    session['cart'] = cart
    session.modified = True
    total = sum(item['price'] * item['quantity'] for item in cart)
    return jsonify({'items': cart, 'total': round(total, 2), 'count': len(cart)})


@app.route('/api/cart/clear', methods=['POST'])
def clear_cart():
    """Clear the cart"""
    session['cart'] = []
    session.modified = True
    return jsonify({'message': 'Cart cleared', 'items': [], 'total': 0, 'count': 0})


@app.errorhandler(404)
def not_found(e):
    """404 error page"""
    return render_template('404.html'), 404


@app.errorhandler(403)
def forbidden(e):
    """403 error page"""
    return render_template('403.html'), 403


@app.errorhandler(500)
def internal_error(e):
    """500 error page"""
    db.session.rollback()
    return render_template('500.html'), 500


# Categories
CATEGORIES = ['All', 'Electronics', 'Accessories', 'Bags', 'Footwear', 'Clothing', 'Home']


# Local development
if __name__ == '__main__':
    print("\n" + "="*70)
    print("  🛍️  MODERN ONLINE STORE")
    print("  With Authentication, Admin Dashboard, Multi-Currency & Shipping")
    print("="*70)
    print("\n  Open your browser and navigate to:")
    print("  👉 http://localhost:5000")
    print("\n  Admin Dashboard: http://localhost:5000/admin")
    print("  Admin Login: ThandoHlomuka / Nozibusiso89")
    print("\n  Press Ctrl+C to stop the server")
    print("="*70 + "\n")
    app.run(debug=True, port=5000, host='0.0.0.0')
