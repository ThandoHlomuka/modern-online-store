"""
Modern Online Store - Flask Application
A beautiful, eye-catching online store built with Python and Flask

Vercel Serverless Deployment Ready
"""

from flask import Flask, render_template, request, jsonify, session
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'modern-store-secret-key-2024')
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Product database
PRODUCTS = [
    {
        'id': 1,
        'name': 'Premium Wireless Headphones',
        'price': 299.99,
        'category': 'Electronics',
        'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400',
        'description': 'High-quality wireless headphones with noise cancellation',
        'rating': 4.8,
        'reviews': 256
    },
    {
        'id': 2,
        'name': 'Minimalist Watch',
        'price': 189.99,
        'category': 'Accessories',
        'image': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400',
        'description': 'Elegant minimalist design with premium materials',
        'rating': 4.9,
        'reviews': 189
    },
    {
        'id': 3,
        'name': 'Smart Home Speaker',
        'price': 149.99,
        'category': 'Electronics',
        'image': 'https://images.unsplash.com/photo-1589492477829-5e65395b66cc?w=400',
        'description': 'Voice-controlled speaker with premium sound quality',
        'rating': 4.6,
        'reviews': 342
    },
    {
        'id': 4,
        'name': 'Designer Sunglasses',
        'price': 249.99,
        'category': 'Accessories',
        'image': 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400',
        'description': 'UV protection with stylish modern design',
        'rating': 4.7,
        'reviews': 128
    },
    {
        'id': 5,
        'name': 'Leather Backpack',
        'price': 179.99,
        'category': 'Bags',
        'image': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400',
        'description': 'Premium leather backpack with laptop compartment',
        'rating': 4.8,
        'reviews': 215
    },
    {
        'id': 6,
        'name': 'Mechanical Keyboard',
        'price': 159.99,
        'category': 'Electronics',
        'image': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400',
        'description': 'RGB backlit mechanical keyboard with custom switches',
        'rating': 4.9,
        'reviews': 445
    },
    {
        'id': 7,
        'name': 'Running Shoes',
        'price': 129.99,
        'category': 'Footwear',
        'image': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400',
        'description': 'Lightweight running shoes with superior comfort',
        'rating': 4.5,
        'reviews': 567
    },
    {
        'id': 8,
        'name': 'Portable Charger',
        'price': 79.99,
        'category': 'Electronics',
        'image': 'https://images.unsplash.com/photo-1609599006353-e629aaabfeae?w=400',
        'description': '20000mAh fast charging power bank',
        'rating': 4.6,
        'reviews': 892
    }
]

# Categories
CATEGORIES = ['All', 'Electronics', 'Accessories', 'Bags', 'Footwear']


@app.route('/')
def index():
    """Home page with featured products"""
    featured_products = PRODUCTS[:4]
    return render_template('index.html', products=featured_products, categories=CATEGORIES)


@app.route('/shop')
def shop():
    """Shop page with all products"""
    category = request.args.get('category', 'All')
    if category == 'All':
        filtered_products = PRODUCTS
    else:
        filtered_products = [p for p in PRODUCTS if p['category'] == category]
    return render_template('shop.html', products=filtered_products, categories=CATEGORIES, current_category=category)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Product detail page"""
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product:
        related_products = [p for p in PRODUCTS if p['category'] == product['category'] and p['id'] != product_id][:3]
        return render_template('product.html', product=product, related_products=related_products)
    return render_template('404.html'), 404


@app.route('/cart')
def cart():
    """Shopping cart page"""
    return render_template('cart.html')


@app.route('/api/cart', methods=['GET'])
def get_cart():
    """Get cart items from session"""
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    return jsonify({'items': cart, 'total': round(total, 2), 'count': len(cart)})


@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    data = request.get_json()
    product_id = data.get('product_id') if data else None

    if product_id is None:
        return jsonify({'error': 'Product ID required'}), 400

    product = next((p for p in PRODUCTS if p['id'] == int(product_id)), None)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    cart = session.get('cart', [])

    # Check if product already in cart
    for item in cart:
        if item['id'] == int(product_id):
            item['quantity'] += 1
            session['cart'] = cart
            session.modified = True
            return jsonify({'message': 'Quantity updated', 'cart_count': len(cart)})

    # Add new item
    cart.append({
        'id': product['id'],
        'name': product['name'],
        'price': product['price'],
        'image': product['image'],
        'quantity': 1
    })
    session['cart'] = cart
    session.modified = True
    return jsonify({'message': 'Added to cart', 'cart_count': len(cart)})


@app.route('/api/cart/remove', methods=['POST'])
def remove_from_cart():
    """Remove item from cart"""
    data = request.get_json()
    product_id = data.get('product_id') if data else None

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
    product_id = data.get('product_id') if data else None
    quantity = data.get('quantity', 1) if data else 1

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


@app.route('/checkout')
def checkout():
    """Checkout page"""
    return render_template('checkout.html')


@app.route('/api/checkout', methods=['POST'])
def process_checkout():
    """Process checkout"""
    session['cart'] = []
    session.modified = True
    return jsonify({'message': 'Order placed successfully!', 'order_id': 'ORD-' + str(os.urandom(4).hex()).upper()})


@app.errorhandler(404)
def not_found(e):
    """404 error page"""
    return render_template('404.html'), 404


# Vercel serverless handler
def handler(request, context):
    """Vercel serverless entry point using WSGI adapter"""
    from wsgiref.handlers import SimpleHandler
    from io import BytesIO
    
    # Create WSGI environ from request
    environ = {
        'REQUEST_METHOD': request.method,
        'PATH_INFO': request.path,
        'QUERY_STRING': request.query or '',
        'CONTENT_TYPE': request.headers.get('content-type', ''),
        'CONTENT_LENGTH': request.headers.get('content-length', '0'),
        'SERVER_NAME': request.headers.get('host', 'localhost'),
        'SERVER_PORT': '443',
        'wsgi.url_scheme': 'https',
        'wsgi.input': BytesIO(request.body or b''),
        'wsgi.errors': BytesIO(),
        'HTTP_COOKIE': request.headers.get('cookie', ''),
    }
    
    # Add all headers
    for key, value in request.headers.items():
        header_key = 'HTTP_' + key.upper().replace('-', '_')
        environ[header_key] = value
    
    # Response handling
    response_data = {'statusCode': 200, 'headers': {}, 'body': ''}
    
    def start_response(status, response_headers):
        response_data['statusCode'] = int(status.split()[0])
        for key, value in response_headers:
            response_data['headers'][key] = value
    
    # Run the Flask app
    result = app(environ, start_response)
    response_data['body'] = b''.join(result).decode('utf-8')
    
    return response_data


# Local development
if __name__ == '__main__':
    print("\n" + "="*60)
    print("  🛍️  MODERN ONLINE STORE")
    print("  Starting server...")
    print("="*60)
    print("\n  Open your browser and navigate to:")
    print("  👉 http://localhost:5000")
    print("\n  Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    app.run(debug=True, port=5000, host='0.0.0.0')
