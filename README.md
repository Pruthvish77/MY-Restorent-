<div align="center">
  <img src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80" alt="LuxeBite Banner" width="100%" style="border-radius: 15px;"/>

  <h1>🍔 LuxeBite</h1>
  <p><strong>A Premium Food Delivery & Restaurant Management Platform</strong></p>
  
  [![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)](https://www.djangoproject.com/)
  [![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
  [![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com/)
  [![Razorpay](https://img.shields.io/badge/Razorpay-02042B?style=for-the-badge&logo=razorpay&logoColor=3395FF)](https://razorpay.com/)
</div>

<br/>

## 📖 Overview

**LuxeBite** (formerly FinalMealmate) is a state-of-the-art food delivery and restaurant management system built with Django. It features a modern, interactive, and premium user interface utilizing glassmorphism and dynamic animations to provide the best possible experience for both food enthusiasts and restaurant owners.

---

## ✨ Key Features

### 🛍️ For Customers
- **Interactive UI**: Stunning glassmorphism design with dynamic hover effects and welcome animations.
- **Restaurant Discovery**: Search for your favorite restaurants, browse cuisines, and view menus.
- **Cart Management**: Add multiple items, adjust quantities, and see real-time pricing.
- **Seamless Checkout**: Integrated securely with **Razorpay** for smooth payment processing.
- **Order Tracking**: Keep track of current and past orders effortlessly.

### 🏪 For Restaurants & Admins
- **Restaurant Partner Portal**: Apply to become a restaurant partner on the platform.
- **Admin Dashboard**: Approve or reject pending restaurant applications.
- **Menu Management**: Add, update, and manage restaurant menus seamlessly.
- **Analytics & Users**: Track users and overall sales distribution.

---

## 🛠️ Tech Stack

- **Backend**: Python, Django
- **Frontend**: HTML5, Vanilla CSS (Glassmorphism), JavaScript
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Payment Gateway**: Razorpay API
- **Deployment**: Vercel ready (Configured with WhiteNoise for static files)

---

## 🚀 Running Locally

Follow these steps to set up LuxeBite on your local machine:

### 1. Clone the repository & setup Virtual Environment
```bash
# Clone the project (if applicable)
git clone https://github.com/your-username/LuxeBite.git
cd LuxeBite

# Create and activate a virtual environment
python -m venv myenv
source myenv/bin/activate  # On Windows use: myenv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Start the Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000` in your browser.

---

## ☁️ Deploying to Vercel

This repository is optimized for **Vercel Deployment**.

1. Connect your GitHub repository to Vercel.
2. In Vercel Project Settings, add a new Environment Variable for your Postgres Database:
   - **Key**: `DATABASE_URL`
   - **Value**: `postgres://username:password@hostname/dbname` *(Get this from Supabase, Neon, or Render)*
3. **Razorpay Secrets (Optional but recommended for Checkout)**:
   - `RAZORPAY_KEY_ID`: Your Razorpay public key
   - `RAZORPAY_KEY_SECRET`: Your Razorpay secret key
4. Deploy! Vercel will automatically run `build_files.sh` to collect static files and host the Django WSGI application.

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

<div align="center">
  <p>Made with ❤️ for food lovers.</p>
</div>
