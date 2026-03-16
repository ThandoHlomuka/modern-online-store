# 🚀 Quick Start Guide - Modern Online Store

Get your online store running in 15 minutes!

---

## ⚡ Super Quick Start (Local Testing)

### For First-Time Setup (5 minutes)

1. **Run the setup script:**
   ```bash
   setup.bat
   ```

2. **Edit `.env` file** with these minimum settings:
   ```env
   SECRET_KEY=any-random-32-character-string-here
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key
   SUPABASE_DB_URL=postgresql://postgres:password@db.xxx.supabase.co:5432/postgres
   ```

3. **Start the server:**
   ```bash
   run.bat
   ```

4. **Open browser:** `http://localhost:5000`

**Done!** 🎉

---

## 📋 Complete Setup Guide (15 minutes)

### Step 1: Create Supabase Account (2 min)

1. Go to [supabase.com](https://supabase.com)
2. Click **"Start your project"** or **"New Project"**
3. Fill in:
   - **Project name**: `modern-store` (or your choice)
   - **Database password**: Choose a strong password (save it!)
   - **Region**: Select closest to you (e.g., Africa for SA)
4. Click **"Create new project"**

### Step 2: Set Up Database (3 min)

1. Wait for project to finish creating (~2 minutes)
2. In Supabase Dashboard, click **"SQL Editor"** (left sidebar)
3. Click **"New Query"**
4. Open `supabase-schema.sql` from the project folder
5. Copy ALL content and paste into SQL Editor
6. Click **"Run"** or press `Ctrl+Enter`
7. You should see: "Success. No rows returned"

### Step 3: Create Storage Bucket (2 min)

1. Click **"Storage"** in Supabase Dashboard
2. Click **"New Bucket"**
3. Name: `avatars`
4. Toggle **"Public bucket"** to ON
5. Click **"Create bucket"**

### Step 4: Get Credentials (1 min)

1. Click **"Settings"** (bottom left) > **"API"**
2. Copy these values:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon/public key**: `eyJhbG...` (long string starting with eyJ)
3. Click **"Database"** (left sidebar under Settings)
4. Copy **Connection string** (URI mode)

### Step 5: Configure Local Environment (2 min)

1. Open project folder in File Explorer
2. Find `.env.example` file
3. Copy it and rename to `.env`
4. Open `.env` in a text editor
5. Replace these values:

```env
SECRET_KEY=modern-store-super-secret-key-2024-change-this-for-production

SUPABASE_URL=https://your-actual-project-id.supabase.co
SUPABASE_KEY=your-actual-anon-key-here
SUPABASE_DB_URL=postgresql://postgres:YOUR-PASSWORD@db.your-project-id.supabase.co:5432/postgres
```

6. Save the file

### Step 6: Install and Run (3 min)

1. **Open Command Prompt** in project folder
2. **Run setup:**
   ```bash
   setup.bat
   ```
3. **Wait** for dependencies to install (~2 minutes)
4. **Start server:**
   ```bash
   run.bat
   ```
5. **Open browser:** `http://localhost:5000`

### Step 7: Test the Store (2 min)

1. **Browse products** at home page
2. **Add items to cart**
3. **Create account:** Click any auth link to register
4. **Login** with your new account
5. **Test admin panel:**
   - Go to: `http://localhost:5000/admin`
   - Username: `ThandoHlomuka`
   - Password: `Nozibusiso89`

---

## 🎯 What You Can Do Now

### As a Customer:
- ✅ Browse products by category
- ✅ Add items to cart
- ✅ Create account and login
- ✅ Upload profile picture
- ✅ Manage addresses
- ✅ Checkout with shipping calculation
- ✅ View order history

### As an Admin:
- ✅ View dashboard analytics
- ✅ Add/edit/delete products
- ✅ Manage orders
- ✅ View/manage customers
- ✅ Configure shipping zones
- ✅ Set currency rates

---

## 🔐 Important Security Notes

**BEFORE GOING LIVE:**

1. **Change admin password:**
   - Login as admin
   - Go to profile
   - Change password immediately

2. **Generate strong SECRET_KEY:**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Replace in `.env`

3. **Set DEBUG=False** in `.env` for production

---

## 🌐 Deploy to Vercel (Optional)

See **DEPLOYMENT.md** for complete deployment guide.

### Quick Deploy Steps:

1. **Push to GitHub:**
   ```bash
   setup-git.bat
   # Follow the instructions
   ```

2. **Deploy on Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Import GitHub repository
   - Set environment variables
   - Click Deploy

3. **Done!** Your store is live

---

## 💡 Tips & Tricks

### Adding Products

**Via Admin Dashboard:**
1. Login as admin
2. Go to Products > Add Product
3. Fill in details
4. Upload image URL (use Unsplash or similar)

**Via Database:**
```sql
INSERT INTO products (name, description, price, category, image, stock_quantity, weight_kg)
VALUES ('New Product', 'Description', 999.00, 'Electronics', 'https://image-url.com', 50, 1.0);
```

### Testing Checkout

1. Add products to cart
2. Go to checkout
3. Use test address:
   - Name: Test Customer
   - Address: 123 Test Street
   - City: Johannesburg
   - Province: Gauteng
   - Postal Code: 2000

### Currency Switching

- Primary currency is ZAR (South African Rand)
- Users can view prices in USD, EUR, GBP, etc.
- Exchange rates are configurable in admin

---

## 🛠️ Troubleshooting

### "Module not found" error
**Solution:** Run `setup.bat` again to install dependencies

### "Cannot connect to database" error
**Solution:** 
1. Check `.env` file has correct Supabase credentials
2. Verify database password in connection string
3. Test connection in Supabase dashboard

### "Port 5000 already in use" error
**Solution:** 
- Stop other applications using port 5000
- Or change port in `app.py`: `app.run(port=5001)`

### Avatar upload not working
**Solution:**
1. Verify `avatars` bucket exists in Supabase Storage
2. Check bucket is set to public
3. Verify RLS policies are applied

### Admin login not working
**Solution:**
1. Check database has admin user:
   ```sql
   SELECT * FROM users WHERE username = 'ThandoHlomuka';
   ```
2. Re-run the schema SQL if needed

---

## 📞 Getting Help

### Documentation
- **README.md** - Full feature overview
- **DEPLOYMENT.md** - Detailed deployment guide
- **Supabase Docs** - [supabase.com/docs](https://supabase.com/docs)
- **Flask Docs** - [flask.palletsprojects.com](https://flask.palletsprojects.com)

### Common Issues
Check the Troubleshooting section in DEPLOYMENT.md

---

## ✅ Setup Checklist

- [ ] Supabase account created
- [ ] Project created in Supabase
- [ ] Database schema deployed
- [ ] Storage bucket created
- [ ] `.env` file configured
- [ ] Setup script ran successfully
- [ ] Server starts without errors
- [ ] Can browse products
- [ ] Can add to cart
- [ ] Can create account
- [ ] Admin login works
- [ ] Can view admin dashboard

**All checked?** You're ready to customize and deploy! 🎉

---

**Made with ❤️ in South Africa 🇿🇦**
