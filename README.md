# 🛍️ Modern Online Store

A beautiful, eye-catching modern online store built with Python and Flask.

![Modern Online Store](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- 🎨 **Modern Design** - Beautiful gradient UI with smooth animations
- 📱 **Fully Responsive** - Works on desktop, tablet, and mobile
- 🛒 **Shopping Cart** - Add, remove, and update quantities
- 🔍 **Product Filtering** - Filter products by category
- ⭐ **Product Ratings** - Star ratings and review counts
- 🚀 **Fast Performance** - Optimized loading and smooth interactions
- 🔒 **Secure Checkout** - Complete checkout flow with form validation

## 📁 Project Structure

```
modern-online-store/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   ├── js/
│   │   └── main.js       # JavaScript functionality
│   └── images/           # Product images (loaded from Unsplash)
└── templates/
    ├── base.html         # Base template
    ├── index.html        # Home page
    ├── shop.html         # Shop/Products page
    ├── product.html      # Product detail page
    ├── cart.html         # Shopping cart page
    ├── checkout.html     # Checkout page
    └── 404.html          # Error page
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Navigate to the project folder:**
   ```bash
   cd Desktop\modern-online-store
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Open your browser:**
   ```
   http://localhost:5000
   ```

## 🎯 Pages

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Hero section with featured products |
| Shop | `/shop` | Browse all products with category filter |
| Product | `/product/<id>` | Detailed product view |
| Cart | `/cart` | Shopping cart with quantity controls |
| Checkout | `/checkout` | Complete checkout form |

## 🎨 Design Features

- **Gradient Hero Section** - Eye-catching purple-pink gradient
- **Product Cards** - Hover effects with quick actions
- **Smooth Animations** - Fade-in effects and transitions
- **Toast Notifications** - Feedback for user actions
- **Sticky Header** - Navigation always accessible
- **Cart Badge** - Live cart count indicator

## 🛠️ Customization

### Adding Products

Edit the `PRODUCTS` list in `app.py`:

```python
PRODUCTS = [
    {
        'id': 9,
        'name': 'Your Product',
        'price': 99.99,
        'category': 'Electronics',
        'image': 'https://example.com/image.jpg',
        'description': 'Product description',
        'rating': 4.5,
        'reviews': 100
    },
    # ... more products
]
```

### Changing Colors

Edit CSS variables in `static/css/style.css`:

```css
:root {
    --primary: #6366f1;      /* Main brand color */
    --secondary: #ec4899;    /* Accent color */
    --accent: #14b8a6;       /* Secondary accent */
    /* ... more variables */
}
```

## 📝 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/cart` | Get cart contents |
| POST | `/api/cart/add` | Add item to cart |
| POST | `/api/cart/remove` | Remove item from cart |
| POST | `/api/cart/update` | Update item quantity |
| POST | `/api/cart/clear` | Clear entire cart |
| POST | `/api/checkout` | Process checkout |

## 🖼️ Images

Product images are loaded from Unsplash (free, high-quality stock photos). You can replace them with your own images by:

1. Adding images to `static/images/`
2. Updating the `image` field in the product data

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Support

For questions or issues, please create an issue in the repository.

---

## 🚀 Deploy to Vercel

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Push to GitHub:**
   ```bash
   # Initialize git repository
   git init
   git add .
   git commit -m "Initial commit: Modern Online Store"
   
   # Create a new repository on GitHub, then:
   git remote add origin https://github.com/YOUR_USERNAME/modern-online-store.git
   git branch -M main
   git push -u origin main
   ```

2. **Deploy on Vercel:**
   - Go to [vercel.com](https://vercel.com) and sign in
   - Click **"Add New Project"**
   - Select **"Import Git Repository"**
   - Choose your `modern-online-store` repository
   - Click **"Deploy"**
   - Vercel will automatically detect the Python project and deploy it

3. **Configure Environment Variables (optional):**
   - In your Vercel project dashboard, go to **Settings → Environment Variables**
   - Add `SECRET_KEY` with a secure random value for production

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

4. **Deploy to production:**
   ```bash
   vercel --prod
   ```

### Post-Deployment

After deployment, your store will be live at:
- Development URL: `https://modern-online-store-xxx.vercel.app`
- Production URL: `https://your-domain.com` (after connecting a custom domain)

### Notes for Vercel Deployment

- **Sessions**: The app uses cookie-based sessions which work with Vercel's serverless functions
- **Static Files**: CSS, JS, and images are served from the `/static` folder
- **Environment Variables**: Set `SECRET_KEY` in Vercel for production security
- **Build Time**: First deployment takes ~2-3 minutes

---

**Built with ❤️ using Python & Flask**
