<div align="center">

<img src="static/images/cafelogo.jpeg" alt="Healthy Cafe Zone" width="100"/>

# 🥗 Healthy Choice Cafe Management System
### *with AI Recommendations Engine*

*AI-powered cafeteria management with smart food recommendations, OTP verification, real-time order tracking, and automated invoice generation.*

<br/>

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3.3-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![scikit--learn](https://img.shields.io/badge/scikit--learn-1.3.0-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![ReportLab](https://img.shields.io/badge/ReportLab-4.0.4-CC0000?style=for-the-badge&logoColor=white)
![bcrypt](https://img.shields.io/badge/bcrypt-4.0.1-003366?style=for-the-badge&logoColor=white)

<br/>

[![GitHub stars](https://img.shields.io/github/stars/yourusername/healthy-cafe-management?style=social)](https://github.com/yourusername/healthy-cafe-management)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/healthy-cafe-management?style=social)](https://github.com/yourusername/healthy-cafe-management)

</div>

---

## 📸 Screenshots

<div align="center">

| Cafeteria Menu | Admin Dashboard | Invoice |
|:-:|:-:|:-:|
| ![Menu](static/images/dashboard.jpeg) | ![Dashboard](static/images/dashboard1.jpeg) | ![Invoice](static/images/invoice.jpeg) |

</div>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [🗄️ Database Schema](#️-database-schema)
- [💳 Payment Flow](#-payment-flow)
- [🚀 Getting Started](#-getting-started)
- [📁 Project Structure](#-project-structure)
- [🤖 AI Features](#-ai-features)
- [📦 Tech Stack](#-tech-stack)
- [🔒 Security](#-security)
- [🤝 Contributing](#-contributing)

---

## ✨ Features

### 👤 Customer Side

| Feature | Description | Tech Used |
|---------|-------------|-----------|
| 🤖 **AI Food Chatbot** | Asks age + weight → calculates BMI → recommends best menu items free of cost | Rule engine + scikit-learn |
| 🔐 **OTP Verification** | Mobile → 6-digit OTP → verify → download invoice (5 min expiry, single use) | bcrypt + Flask session |
| 📄 **PDF Invoice** | Professional invoice with logo watermark, GST, loyalty discount, PAID badge | ReportLab 4.0.4 |
| 🧬 **Nutrition Tracking** | Every item has calories, protein, carbs, fats — profile shows cumulative history | Chart.js |
| 🪙 **Health Coins** | Earn 10 coins per healthy item — gamified loyalty system | MySQL |
| 📦 **Order Tracking** | Real-time: Pending → Preparing → Ready → Delivered | Flask REST API |

### 🛠️ Admin Side

| Feature | Description |
|---------|-------------|
| 📊 **Dashboard** | Revenue charts, order distribution, best-selling items, live orders |
| 🍽️ **Menu Management** | Add, edit, delete, toggle items with image upload |
| 📦 **Order Management** | Update order status, filter by date/status |
| 🏪 **Inventory Tracking** | Ingredient levels with low-stock threshold alerts |
| 👥 **User Management** | View all registered users and their order history |
| 🛡️ **Security Logs** | All login attempts with IP address and timestamp |
| ⚙️ **Settings** | Configure GST rate, delivery fee, cafe name |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USERS                                │
│         Customer                        Admin               │
│   (Browse · Order · Pay)         (Manage · Monitor)         │
└──────────────┬───────────────────────────┬──────────────────┘
               │                           │
               ▼                           ▼
┌─────────────────────────────────────────────────────────────┐
│               FRONTEND  (HTML / CSS / JavaScript)           │
│                                                             │
│  cafeteria.html   cart.html   payment.html   profile.html   │
│  orders.html                                                │
│                                                             │
│  admin/dashboard  admin/menu  admin/orders  admin/inventory │
└──────────────────────────┬──────────────────────────────────┘
                           │  HTTP / REST API
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              FLASK BACKEND  (app.py)                        │
│                                                             │
│  /register /login /send-otp /verify-otp                     │
│  /food-items /menu-items /recommendations                   │
│  /create-order /save-order /generate-invoice                │
│  /api/user/profile /api/user/stats                          │
│  /admin/dashboard /admin/orders /admin/inventory            │
│                                                             │
│  Middleware: Flask-Limiter · bcrypt · Flask-CORS · Session  │
└────┬──────────────┬─────────────┬───────────────┬───────────┘
     │              │             │               │
     ▼              ▼             ▼               ▼
┌─────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐
│  MySQL  │  │ReportLab │  │scikit-   │  │ OTP / SMS  │
│   DB    │  │PDF Engine│  │learn AI  │  │ Fast2SMS   │
│ 8 tables│  │ Invoices │  │ Recos    │  │ Flask-Mail │
└─────────┘  └──────────┘  └──────────┘  └────────────┘
```

---

## 🗄️ Database Schema

```sql
-- User accounts with health gamification
users (id, name, email, mobile, password_hash, role, dob, gender, health_coins, created_at)

-- Food items with full nutritional data
menu_items (id, name, price, image_url, protein, carbs, fats, calories, category, diet_type, is_active)

-- Order lifecycle management
orders (id, user_id, total_amount, order_status, payment_status, created_at)

-- Individual items within each order
order_items (id, order_id, menu_item_id, quantity, price)

-- Kitchen ingredient stock with alerts
inventory (id, ingredient_name, quantity, threshold)

-- OTP storage with expiry
login_otp (id, user_id, otp_code, expiry_time)

-- Security audit trail
login_history (id, user_id, login_time, ip_address)

-- Dynamic cafe configuration
system_settings (setting_key, setting_value)
```

---

## 💳 Payment Flow

```
User selects UPI / Google Pay
            │
            ▼
    ┌───────────────┐
    │ Enter 10-digit │
    │ mobile number  │
    └───────┬───────┘
            │
            ▼
    ┌───────────────┐
    │  Send OTP     │──► 6-digit OTP stored server-side
    │  (click btn)  │    with 5-minute expiry
    └───────┬───────┘
            │
            ▼
    ┌───────────────┐
    │ Enter 6-digit │    OTP shown on screen
    │    OTP code   │    (or SMS via Fast2SMS)
    └───────┬───────┘
            │
            ▼
    ┌───────────────┐
    │ Server verify │──► Wrong OTP → Error
    │               │──► Expired  → Resend
    └───────┬───────┘──► Correct  → Proceed ✅
            │
            ▼
    ┌───────────────┐
    │  PDF Invoice  │    ReportLab generates:
    │  generated &  │    • Cafe logo watermark
    │  downloaded   │    • Itemised bill + GST
    └───────────────┘    • PAID badge + Transaction ID
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- MySQL 8.0+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/healthy-cafe-management.git
cd healthy-cafe-management

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Set up MySQL database
mysql -u root -p
CREATE DATABASE healthy_cafe;
USE healthy_cafe;

# 5. Configure environment variables
cp .env.example .env

# 6. Run the application
python app.py
```

### Environment Variables

Create a `.env` file in the root directory:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=healthy_cafe

SECRET_KEY=your_secret_key_here

MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
```

### Access the App

| URL | Description |
|-----|-------------|
| `http://localhost:5000` | Customer login page |
| `http://localhost:5000/cafeteria` | Main menu |
| `http://localhost:5000/admin` | Admin panel |

---

## 📁 Project Structure

```
healthy-cafe/
│
├── app.py                      # Main Flask app — all routes + logic
├── requirements.txt            # Python dependencies
├── schema.txt                  # Database schema reference
├── .env                        # Environment variables (not in git)
│
├── templates/                  # Jinja2 HTML templates
│   ├── login.html
│   ├── register.html
│   ├── cafeteria.html          # Menu + AI food chatbot
│   ├── cart.html
│   ├── payment.html            # OTP flow + invoice download
│   ├── orders.html
│   ├── profile.html            # Nutrition dashboard + AI reco
│   └── admin/
│       ├── dashboard.html      # Revenue charts + KPIs
│       ├── menu.html           # CRUD menu items
│       ├── orders.html         # Order management
│       ├── inventory.html      # Stock management
│       ├── users.html          # User management
│       ├── security_logs.html  # Login audit logs
│       └── settings.html       # Cafe configuration
│
└── static/
    ├── style.css               # Main stylesheet
    ├── script.js               # Frontend JavaScript
    ├── admin.css
    ├── admin.js
    └── images/                 # Food images + cafe logo
```

---

## 🤖 AI Features

### 1. Menu Chatbot — Age & Weight Based Recommendations

The floating chatbot on the cafeteria page collects user health data and recommends the best menu items. **Completely free — no external AI API needed.**

| Age Group | BMI Category | Recommendation Logic |
|-----------|--------------|----------------------|
| 5–12 yrs | Any | Light, veg, low calorie, easy to digest |
| 13–17 yrs | Any | High protein + energy foods for growth |
| 18+ | Underweight (BMI < 18.5) | High calorie + high protein items |
| 18+ | Normal (BMI 18.5–24.9) | Balanced macro items |
| 18+ | Overweight (BMI 25–29.9) | Low calorie + low fat items |
| 18+ | Obese (BMI 30+) | Very low calorie + diet type items |
| 50+ | Any | Light, easy to digest, low fat |

### 2. Profile AI Recommendations

The profile page uses **scikit-learn** to analyze past order history and suggest new menu items the user is likely to enjoy based on collaborative filtering.

---

## 📦 Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Language | Python | 3.12 |
| Web Framework | Flask | 2.3.3 |
| Database | MySQL + mysql-connector | 8.0 |
| Machine Learning | scikit-learn | 1.3.0 |
| Data Processing | pandas | 2.0.3 |
| PDF Generation | ReportLab | 4.0.4 |
| Password Security | bcrypt | 4.0.1 |
| Rate Limiting | Flask-Limiter | 3.5.0 |
| Email | Flask-Mail | 0.9.1 |
| CORS | Flask-CORS | 4.0.0 |
| Frontend Charts | Chart.js | Latest |
| Frontend Icons | Font Awesome | 6.0.0 |

---

## 🔒 Security

| Feature | Implementation |
|---------|----------------|
| 🔑 **Password Hashing** | bcrypt with salt — never stored in plain text |
| ⏱️ **OTP Expiry** | 6-digit OTPs expire in 5 minutes, single-use enforced |
| 🚦 **Rate Limiting** | Flask-Limiter blocks brute force on login & OTP endpoints |
| 🗂️ **Audit Logging** | All login attempts logged with IP address and timestamp |
| 🔒 **Session Auth** | Admin and user sessions fully separated with secret key |
| 🛂 **Password Policy** | 8–12 chars, uppercase, number, special character required |
| 🌐 **CORS Protection** | Flask-CORS configured for allowed origins only |

---

## 🤝 Contributing

Contributions are welcome!

```bash
# 1. Fork the repository
# 2. Create your feature branch
git checkout -b feature/AmazingFeature

# 3. Commit your changes
git commit -m 'Add some AmazingFeature'

# 4. Push to the branch
git push origin feature/AmazingFeature

# 5. Open a Pull Request
```

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ for healthy eating and smart cafe management**

⭐ **Star this repo if you found it helpful!** ⭐

<br/>

*Healthy Cafe Zone — Taste the Difference*

</div>
