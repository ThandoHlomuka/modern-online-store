/**
 * Modern Online Store - Main JavaScript
 */

// Cart state
let cartCount = 0;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadCartCount();
    initializeEventListeners();
});

// Load cart count from server
async function loadCartCount() {
    try {
        const response = await fetch('/api/cart');
        const data = await response.json();
        cartCount = data.count;
        updateCartBadge();
    } catch (error) {
        console.error('Error loading cart:', error);
    }
}

// Update cart badge display
function updateCartBadge() {
    const badge = document.querySelector('.cart-badge');
    if (badge) {
        if (cartCount > 0) {
            badge.textContent = cartCount;
            badge.style.display = 'flex';
        } else {
            badge.style.display = 'none';
        }
    }
}

// Initialize event listeners
function initializeEventListeners() {
    // Add to cart buttons
    document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const productId = this.dataset.productId;
            addToCart(productId);
        });
    });

    // Cart quantity controls
    document.querySelectorAll('.quantity-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.dataset.action;
            const productId = this.dataset.productId;
            if (action === 'increase') {
                updateQuantity(productId, 1);
            } else {
                updateQuantity(productId, -1);
            }
        });
    });

    // Remove from cart buttons
    document.querySelectorAll('.remove-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const productId = this.dataset.productId;
            removeFromCart(productId);
        });
    });

    // Category filter
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

// Add item to cart
async function addToCart(productId) {
    try {
        const response = await fetch('/api/cart/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ product_id: parseInt(productId) })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            cartCount = data.cart_count;
            updateCartBadge();
            showToast('Added to cart!', 'success');
            
            // Animate button
            const btn = document.querySelector(`[data-product-id="${productId}"].add-to-cart-btn`);
            if (btn) {
                btn.innerHTML = '✓ Added';
                setTimeout(() => {
                    btn.innerHTML = 'Add to Cart';
                }, 2000);
            }
        }
    } catch (error) {
        console.error('Error adding to cart:', error);
        showToast('Failed to add to cart', 'error');
    }
}

// Update item quantity
async function updateQuantity(productId, change) {
    const quantityDisplay = document.querySelector(`[data-product-id="${productId}"].quantity-display`);
    const currentQuantity = parseInt(quantityDisplay.textContent);
    const newQuantity = currentQuantity + change;
    
    if (newQuantity < 1) {
        removeFromCart(productId);
        return;
    }
    
    try {
        const response = await fetch('/api/cart/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                product_id: parseInt(productId),
                quantity: newQuantity
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            quantityDisplay.textContent = newQuantity;
            updateCartSummary(data);
        }
    } catch (error) {
        console.error('Error updating quantity:', error);
    }
}

// Remove item from cart
async function removeFromCart(productId) {
    try {
        const response = await fetch('/api/cart/remove', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ product_id: parseInt(productId) })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            cartCount = data.count;
            updateCartBadge();
            
            // Remove item from DOM
            const cartItem = document.querySelector(`[data-product-id="${productId}"].cart-item`);
            if (cartItem) {
                cartItem.style.opacity = '0';
                cartItem.style.transform = 'translateX(-20px)';
                setTimeout(() => {
                    cartItem.remove();
                    checkEmptyCart();
                }, 300);
            }
            
            updateCartSummary(data);
            showToast('Item removed from cart', 'success');
        }
    } catch (error) {
        console.error('Error removing from cart:', error);
    }
}

// Update cart summary
function updateCartSummary(data) {
    const subtotalEl = document.getElementById('subtotal');
    const shippingEl = document.getElementById('shipping');
    const totalEl = document.getElementById('total');
    
    if (subtotalEl) {
        subtotalEl.textContent = '$' + data.total.toFixed(2);
    }
    
    if (shippingEl) {
        const shipping = data.total > 100 ? 0 : 9.99;
        shippingEl.textContent = shipping === 0 ? 'FREE' : '$' + shipping.toFixed(2);
    }
    
    if (totalEl) {
        const shipping = data.total > 100 ? 0 : 9.99;
        totalEl.textContent = '$' + (data.total + shipping).toFixed(2);
    }
}

// Check if cart is empty
function checkEmptyCart() {
    const cartItems = document.querySelector('.cart-items');
    const items = cartItems?.querySelectorAll('.cart-item');
    
    if (!items || items.length === 0) {
        cartItems.innerHTML = `
            <div class="empty-cart">
                <div class="empty-cart-icon">🛒</div>
                <h2>Your cart is empty</h2>
                <p>Add some products to get started!</p>
                <a href="/shop" class="btn btn-gradient">Continue Shopping</a>
            </div>
        `;
    }
}

// Show toast notification
function showToast(message, type = 'success') {
    // Remove existing toast
    const existingToast = document.querySelector('.toast');
    if (existingToast) {
        existingToast.remove();
    }
    
    // Create new toast
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <span>${type === 'success' ? '✓' : '✕'}</span>
        <span>${message}</span>
    `;
    
    document.body.appendChild(toast);
    
    // Show toast
    setTimeout(() => toast.classList.add('show'), 10);
    
    // Hide and remove toast
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Checkout form handling
const checkoutForm = document.getElementById('checkout-form');
if (checkoutForm) {
    checkoutForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const data = Object.fromEntries(formData);
        
        try {
            const response = await fetch('/api/checkout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                showToast(result.message, 'success');
                setTimeout(() => {
                    window.location.href = '/';
                }, 2000);
            }
        } catch (error) {
            console.error('Error processing checkout:', error);
            showToast('Failed to process order', 'error');
        }
    });
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Lazy loading images
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.add('loaded');
                observer.unobserve(img);
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => imageObserver.observe(img));
}
