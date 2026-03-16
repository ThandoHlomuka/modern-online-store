# 🚀 Vercel Deployment Guide - Modern Online Store

Complete step-by-step guide to deploy your Modern Online Store to Vercel with Supabase backend.

## 📋 Prerequisites

Before deploying, ensure you have:
- ✅ Supabase account and project set up
- ✅ Vercel account (free tier available)
- ✅ GitHub account
- ✅ Bobgo API credentials (optional, for shipping)

---

## 🗄️ Step 1: Set Up Supabase Database

### 1.1 Create Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Click **"New Project"**
3. Fill in:
   - **Project Name**: `modern-online-store` (or your choice)
   - **Database Password**: Save this securely!
   - **Region**: Choose closest to your customers (e.g., Africa for SA)
4. Click **"Create new project"** (takes 2-3 minutes)

### 1.2 Run Database Schema
1. In Supabase Dashboard, go to **SQL Editor** (left sidebar)
2. Click **"New Query"**
3. Copy entire contents of `supabase-schema.sql`
4. Paste and click **"Run"** or press `Ctrl+Enter`
5. Verify tables created: `users`, `products`, `orders`, `addresses`, etc.

### 1.3 Create Storage Bucket for Avatars
1. Go to **Storage** in Supabase Dashboard
2. Click **"New Bucket"**
3. Name: `avatars`
4. Settings:
   - ✅ Public: true
   - File size limit: `5242880` (5MB)
5. Click **"Create bucket"**

### 1.4 Get Supabase Credentials
1. Go to **Settings** > **API**
2. Copy these values:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon/public key**: `eyJhbG...` (long string)
3. Go to **Settings** > **Database**
4. Copy **Connection string** (URI mode):
   - `postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres`
   - Replace `[YOUR-PASSWORD]` with your database password

---

## 💻 Step 2: Prepare Local Environment

### 2.1 Create .env File
Copy `.env.example` to `.env` and fill in:

```env
# Application
SECRET_KEY=your-random-secret-key-min-32-chars

# Supabase
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_DB_URL=postgresql://postgres:your-password@db.your-project-id.supabase.co:5432/postgres
SUPABASE_STORAGE_BUCKET=avatars

# Bobgo Shipping (Optional)
BOBGO_API_URL=https://api.bobgo.co.za/v1
BOBGO_API_KEY=your-bobgo-api-key

# Flask
FLASK_ENV=production
DEBUG=False
```

### 2.2 Generate Secret Key
Run this Python command to generate a secure secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2.3 Test Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Visit `http://localhost:5000` and verify everything works.

**Admin Login:**
- Username: `ThandoHlomuka`
- Password: `Nozibusiso89`

---

## 🌐 Step 3: Deploy to Vercel

### 3.1 Push to GitHub
```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit - Modern Online Store"

# Create GitHub repository and push
git remote add origin https://github.com/yourusername/modern-online-store.git
git branch -M main
git push -u origin main
```

### 3.2 Deploy on Vercel
1. Go to [vercel.com](https://vercel.com)
2. Click **"Add New..."** > **"Project"**
3. Import your GitHub repository
4. Configure project:
   - **Framework Preset**: Other
   - **Root Directory**: `./`
   - **Build Command**: (leave empty)
   - **Output Directory**: `static`
   - **Install Command**: `pip install -r requirements.txt`

5. Click **"Deploy"** (first deploy takes ~5 minutes)

### 3.3 Set Environment Variables in Vercel
1. After deployment, go to **Project Settings** > **Environment Variables**
2. Add each variable:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Your random secret key |
| `SUPABASE_URL` | `https://your-project-id.supabase.co` |
| `SUPABASE_KEY` | Your Supabase anon key |
| `SUPABASE_DB_URL` | Full PostgreSQL connection string |
| `BOBGO_API_KEY` | Your Bobgo API key (optional) |
| `FLASK_ENV` | `production` |
| `DEBUG` | `False` |

3. Click **"Save"**
4. Redeploy: Go to **Deployments** > Click latest > **"Redeploy"**

---

## 🔧 Step 4: Post-Deployment Configuration

### 4.1 Update Supabase Site URL
1. In Supabase Dashboard, go to **Authentication** > **URL Configuration**
2. Add your Vercel URL to **Site URL**: `https://your-project.vercel.app`
3. Add to **Redirect URLs**:
   - `https://your-project.vercel.app/**`

### 4.2 Test Production
1. Visit your Vercel URL
2. Test:
   - ✅ User registration
   - ✅ Login/Logout
   - ✅ Product browsing
   - ✅ Cart functionality
   - ✅ Admin dashboard (`/admin`)
   - ✅ Profile picture upload

---

## 🚚 Bobgo Shipping Integration

### Get Bobgo API Access
1. Contact Bobgo at [bobgo.co.za](https://bobgo.co.za)
2. Request API credentials for e-commerce integration
3. Add credentials to Vercel environment variables

### Shipping Features
Once Bobgo is configured:
- Real-time shipping rates
- Pudo pickup point locator
- Automated tracking updates
- Label generation

---

## 💱 Currency Configuration

### Primary Currency: ZAR (South African Rand)
All prices are stored in ZAR. Users can view prices in:
- USD (US Dollar)
- EUR (Euro)
- GBP (British Pound)
- NGN (Nigerian Naira)
- KES (Kenyan Shilling)
- BWP (Botswana Pula)

### Live Exchange Rates (Optional)
1. Get API key from [exchangerate-api.com](https://www.exchangerate-api.com)
2. Add to Vercel: `EXCHANGE_RATE_API_KEY=your-key`
3. Update `currency.py` to fetch live rates

---

## 🔐 Security Checklist

- ✅ Change default admin password after first login
- ✅ Use strong SECRET_KEY (32+ characters)
- ✅ Enable HTTPS (automatic on Vercel)
- ✅ Set `FLASK_ENV=production`
- ✅ Set `DEBUG=False`
- ✅ Configure Supabase Row Level Security (RLS)
- ✅ Use environment variables (never commit .env)

---

## 📊 Monitoring & Analytics

### Vercel Analytics
1. Go to **Analytics** in Vercel dashboard
2. Enable for your project
3. View traffic, performance, errors

### Supabase Logs
1. Go to **Settings** > **Logs** in Supabase
2. Monitor database queries
3. Set up alerts for errors

---

## 🛠️ Troubleshooting

### Build Fails
**Error**: `ModuleNotFoundError`
- **Fix**: Ensure all dependencies in `requirements.txt`
- Run: `pip freeze > requirements.txt`

### Database Connection Error
**Error**: Cannot connect to Supabase
- **Fix**: Verify `SUPABASE_DB_URL` in Vercel env vars
- Check database password is correct in connection string

### Avatar Upload Fails
**Error**: Storage bucket not found
- **Fix**: Create `avatars` bucket in Supabase Storage
- Verify bucket is public

### 500 Internal Server Error
- Check Vercel **Functions** logs
- Check Supabase **Database** logs
- Enable debug mode temporarily: `DEBUG=True`

---

## 📈 Performance Optimization

### Enable Caching
Add to `app.py`:
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

### Database Indexes
Already included in schema for:
- `users.username`, `users.email`
- `products.category`, `products.is_active`
- `orders.user_id`, `orders.status`

### CDN for Static Files
Vercel automatically serves static files via CDN.

---

## 🎯 Custom Domain

### Add Domain to Vercel
1. Go to **Project Settings** > **Domains**
2. Add your domain: `yourstore.co.za`
3. Follow DNS configuration instructions
4. SSL certificate auto-generated

### Update Supabase URLs
Add custom domain to:
- **Authentication** > **URL Configuration**
- **Site URL**: `https://yourstore.co.za`

---

## 📞 Support

### Documentation
- Flask: [flask.palletsprojects.com](https://flask.palletsprojects.com)
- Supabase: [supabase.com/docs](https://supabase.com/docs)
- Vercel: [vercel.com/docs](https://vercel.com/docs)

### Community
- Supabase Discord: [discord.supabase.com](https://discord.supabase.com)
- Vercel Community: [github.com/vercel/vercel/discussions](https://github.com/vercel/vercel/discussions)

---

## ✅ Deployment Checklist

- [ ] Supabase project created
- [ ] Database schema deployed
- [ ] Storage bucket created
- [ ] .env file configured locally
- [ ] Local testing passed
- [ ] GitHub repository created
- [ ] Vercel project deployed
- [ ] Environment variables set in Vercel
- [ ] Supabase Auth URLs updated
- [ ] Production testing completed
- [ ] Admin password changed
- [ ] Custom domain configured (optional)
- [ ] Bobgo API integrated (optional)

---

**🎉 Congratulations! Your Modern Online Store is live!**

Made with ❤️ in South Africa 🇿🇦
