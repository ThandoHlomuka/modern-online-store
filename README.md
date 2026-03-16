# 🛍️ Modern Online Store

A complete, production-ready online store built with Python and Flask, featuring authentication, admin dashboard, multi-currency support (ZAR primary), and Bobgo shipping integration.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![Database](https://img.shields.io/badge/Database-PostgreSQL/Supabase-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### Customer Features
- 🔐 **User Authentication** - Register, login, password management
- 👤 **Profile System** - Edit profile, upload avatar, manage addresses
- 🛒 **Shopping Cart** - Persistent cart with quantity management
- 💱 **Multi-Currency** - ZAR (primary), USD, EUR, GBP, NGN, KES, BWP
- 📦 **Order Tracking** - View order history and status
- 🚚 **Shipping Calculator** - Real-time shipping quotes via Bobgo

### Admin Features
- 📊 **Dashboard** - Sales analytics, order overview
- 📦 **Product Management** - Add, edit, delete products
- 🛒 **Order Management** - Process orders, update status
- 👥 **User Management** - View and manage customers
- 🚚 **Shipping Zones** - Configure shipping rates and zones
- 💰 **Currency Rates** - Manage exchange rates

### Technical Features
- 🔒 **Secure Authentication** - Bcrypt password hashing
- 🗄️ **Supabase Database** - PostgreSQL with real-time capabilities
- ☁️ **Vercel Deployment** - Serverless hosting ready
- 📸 **Avatar Upload** - Supabase Storage integration
- 🌍 **Bobgo Integration** - South African shipping API
- 📱 **Responsive Design** - Mobile-first UI

## 📁 Project Structure

```
modern-online-store/
├── app.py                      # Main Flask application
├── models.py                   # Database models
├── forms.py                    # WTForms
├── database.py                 # Database configuration
├── currency.py                 # Currency conversion
├── shipping.py                 # Bobgo shipping integration
├── upload.py                   # File upload handling
├── requirements.txt            # Python dependencies
├── vercel.json                 # Vercel configuration
├── supabase-schema.sql         # Database schema
├── .env                        # Environment variables
├── .env.example                # Environment variables template
├── .gitignore
├── README.md
├── DEPLOYMENT.md               # Detailed deployment guide
├── api/
│   └── index.py                # Vercel serverless entry
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
└── templates/
    ├── base.html
    ├── index.html
    ├── shop.html
    ├── product.html
    ├── cart.html
    ├── checkout.html
    ├── 403.html, 404.html, 500.html
    ├── auth/
    │   ├── login.html
    │   └── register.html
    ├── profile/
    │   ├── profile.html
    │   ├── edit_profile.html
    │   ├── addresses.html
    │   ├── orders.html
    │   ├── order_detail.html
    │   ├── change_password.html
    │   └── address_form.html
    └── admin/
        ├── dashboard.html
        ├── products.html
        ├── product_form.html
        ├── orders.html
        ├── order_detail.html
        ├── users.html
        └── shipping.html
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Supabase account (free tier available)
- Vercel account (free tier available)

### Local Development

1. **Clone/navigate to the project:**
   ```bash
   cd Desktop/modern-online-store
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file:**
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env  # macOS/Linux
   ```

5. **Set up Supabase:**
   - Create account at [supabase.com](https://supabase.com)
   - Create new project
   - Run `supabase-schema.sql` in SQL Editor
   - Copy credentials to .env

6. **Run the application:**
   ```bash
   python app.py
   ```

7. **Open browser:**
   ```
   http://localhost:5000
   ```

## 🗄️ Supabase Setup

### Step 1: Create Project
1. Go to [supabase.com](https://supabase.com)
2. Click "New Project"
3. Fill in project details
4. Set database password (save it!)

### Step 2: Run Schema
1. Go to SQL Editor in Supabase dashboard
2. Copy contents of `supabase-schema.sql`
3. Paste and run
4. This creates all tables and default data

### Step 3: Get Credentials
1. Go to Settings > API
2. Copy:
   - Project URL → `SUPABASE_URL`
   - Anon/Public Key → `SUPABASE_KEY`
   - Database connection string → `SUPABASE_DB_URL`

### Step 4: Create Storage Bucket
1. Go to Storage in Supabase dashboard
2. Create new bucket: `avatars`
3. Set to public
4. Add policies from `supabase-schema.sql`

## 🌐 Deploy to Vercel

See **DEPLOYMENT.md** for detailed step-by-step deployment instructions.

### Quick Deploy
1. Push to GitHub
2. Import project in Vercel
3. Set environment variables
4. Deploy!

## 💱 Currency Support

**Primary Currency:** South African Rand (ZAR)

**Supported Currencies:**
| Code | Name | Symbol |
|------|------|--------|
| ZAR | South African Rand | R |
| USD | US Dollar | $ |
| EUR | Euro | € |
| GBP | British Pound | £ |
| NGN | Nigerian Naira | ₦ |
| KES | Kenyan Shilling | KSh |
| BWP | Botswana Pula | P |

## 🚚 Shipping Integration

### Bobgo API
Primary shipping provider for South Africa.

**Setup:**
1. Get API key from [bobgo.co.za](https://bobgo.co.za)
2. Add to .env: `BOBGO_API_KEY=your-key`

### Shipping Zones
- Gauteng (1-2 days) - R65 base
- Western Cape (2-3 days) - R85 base
- KwaZulu-Natal (2-3 days) - R80 base
- Other South Africa (3-5 days) - R95 base
- Southern Africa SADC (5-10 days) - R250 base
- International (7-21 days) - R450 base

### Shipping Methods
- Standard Shipping (5-7 days) - 1.0x multiplier
- Express Shipping (2-3 days) - 1.5x multiplier
- Overnight Delivery (next day) - 2.5x multiplier
- Bobgo Pudo Pickup - 0.7x multiplier

## 👤 Admin Access

**Default Admin Credentials:**
- Username: `ThandoHlomuka`
- Password: `Nozibusiso89`

**⚠️ IMPORTANT:** Change the admin password after first login!

**Access:** `http://localhost:5000/admin`

## 📝 API Endpoints

### Public
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page |
| GET | `/shop` | Product listing |
| GET | `/product/<id>` | Product detail |
| GET | `/cart` | Shopping cart |

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/login` | User login |
| GET/POST | `/register` | User registration |
| GET | `/logout` | User logout |

### Profile (Requires Login)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/profile` | Profile overview |
| GET/POST | `/profile/edit` | Edit profile |
| POST | `/profile/upload-avatar` | Upload avatar |
| GET/POST | `/profile/change-password` | Change password |
| GET | `/profile/addresses` | Manage addresses |
| GET | `/profile/orders` | Order history |

### Checkout (Requires Login)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/checkout` | Checkout page |
| POST | `/api/checkout` | Process order |
| POST | `/api/shipping/calculate` | Calculate shipping |

### Admin (Requires Admin)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin` | Dashboard |
| GET | `/admin/products` | Product management |
| GET/POST | `/admin/products/add` | Add product |
| GET | `/admin/orders` | Order management |
| GET | `/admin/users` | User management |
| GET | `/admin/shipping` | Shipping configuration |

### API
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/cart` | Get cart |
| POST | `/api/cart/add` | Add to cart |
| POST | `/api/cart/update` | Update quantity |
| POST | `/api/cart/remove` | Remove item |
| POST | `/api/set-currency` | Set currency |

## 🔧 Configuration

### Environment Variables
See `.env` or `.env.example` for all available options.

**Required:**
- `SECRET_KEY` - Flask secret key
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_KEY` - Supabase anon key
- `SUPABASE_DB_URL` - PostgreSQL connection string

**Optional:**
- `BOBGO_API_KEY` - Bobgo shipping API
- `EXCHANGE_RATE_API_KEY` - Live exchange rates
- `STRIPE_SECRET_KEY` - Payment processing

## 🎨 Customization

### Change Primary Currency
Edit `currency.py`:
```python
DEFAULT_CURRENCY = 'ZAR'  # Change to your currency
```

### Add Shipping Zone
In Supabase or Admin dashboard, add to `shipping_zones` table.

### Update Exchange Rates
Edit `currency.py` or connect to exchange rate API.

## 📄 License

MIT License - See LICENSE file for details.

## 🤝 Support

For issues or questions:
1. Check DEPLOYMENT.md for deployment help
2. Review Supabase schema
3. Verify environment variables

## 🙏 Credits

- Built with Flask & Supabase
- Shipping by Bobgo
- Deployed on Vercel
- Designed with ❤️ in South Africa

---

**Made for South Africa 🇿🇦 | Powered by Modern Web Technologies**
