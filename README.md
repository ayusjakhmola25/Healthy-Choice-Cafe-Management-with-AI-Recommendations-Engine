<div align="center">
  <img src="static/images/cafelogo.jpeg" alt="Healthy Cafe Zone Logo" width="150" style="border-radius:50%"/>
  <h1>🌿 Healthy Cafe Zone</h1>
  <p><strong>A Next-Generation, AI-Ready Smart Cafeteria Management System</strong></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Flask-2.3.3-black.svg?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
    <img src="https://img.shields.io/badge/MySQL-8.0+-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL" />
    <img src="https://img.shields.io/badge/Security-OTP_Auth-orange.svg?style=for-the-badge&logo=security&logoColor=white" alt="Security" />
    <img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="License" />
  </p>
  
  <p>
    <em>Bringing health, efficiency, and seamless user experiences to everyday dining.</em>
  </p>
</div>

---

## ✨ Why Healthy Cafe Zone?

Healthy Cafe Zone is not just another e-commerce platform; it's a **secure, highly scalable, full-stack cafeteria management ecosystem** engineered to promote healthy eating habits. With a sleek UI, robust real-time admin analytics, and bulletproof security, this application sets a new standard for food ordering systems.

Whether you're a food enthusiast looking for a balanced meal or an administrator tracking revenue flows, **Healthy Cafe Zone** provides an intuitive, world-class experience.

## 🚀 Top Tier Features

### 🛡️ Enterprise-Grade Security
* **Passwordless-like Experience:** OTP-based email authentication powered by Gmail SMTP.
* **Fortified Passwords:** `bcrypt` hashing with strict complexity requirements.
* **DDoS Protection:** Endpoint rate-limiting with `Flask-Limiter`.
* **Audit Trails:** Comprehensive IP tracking and security logs for every login.

### 🍱 Next-Gen Ordering & E-Commerce
* **Smart Filtering:** Dynamically sort meals by `Breakfast`, `Lunch`, `Dinner`, or `Category`.
* **Frictionless Cart:** Seamless state management for both guests and logged-in users.
* **Automated Invoicing:** Auto-generates branded PDF invoices with GST and delivery fee calculation using `ReportLab`.

### 📊 Powerful Admin Operations
* **Command Center:** Real-time dashboards monitoring users, orders, revenue, and inventory alerts.
* **Dynamic Menu Management:** Full CRUD capabilities for menu items with quick active/inactive toggling.
* **Order Tracking:** One-click confirmation and cancellation of client orders.
* **System Settings:** Control global application states (e.g., active meal mode).

---

## 🏗️ Architecture & Tech Stack

This project is built using an extremely decoupled and robust architecture.

| Layer | Technologies Used | Description |
| :--- | :--- | :--- |
| **Frontend** | Jinja2, HTML5, Vanilla JS, CSS3 | A highly responsive, aesthetically pleasing user interface. |
| **Backend** | Python, Flask, Flask-CORS | API-driven architectural backbone handling business logic. |
| **Database** | MySQL (Connection Pooling) | Highly optimized querying with automated schema migrations. |
| **PDF Generation** | ReportLab | Programmatic drawing of pixel-perfect invoice manifests. |
| **Auth/Security** | bcrypt, Flask-Limiter, SMTP | Military-grade hashing and multi-factor capabilities. |
| **AI Preparedness**| Pandas, Scikit-learn | Built-in stubs ready for predictive food recommendations. |

---

## 📸 Sneak Peek

<div align="center">
  <table>
    <tr>
      <td align="center"><b>🍔 Dynamic Cafeteria</b></td>
      <td align="center"><b>🛒 Intuitive Cart</b></td>
      <td align="center"><b>📈 Analytics Profile</b></td>
    </tr>
    <tr>
      <td><img src="static/images/healthy.jpg" alt="Menu" width="250"/></td>
      <td><img src="static/images/ragi_dosa_with_sambar_25da86d7.jpg" alt="Cart" width="250"/></td>
      <td><img src="static/images/profile.jpg" alt="Profile" width="250"/></td>
    </tr>
  </table>
  
  <br/>
  
  <table>
    <tr>
      <td align="center"><b>⚡ Command Dashboard</b></td>
      <td align="center"><b>🧾 Branded PDF Invoices</b></td>
    </tr>
    <tr>
       <td><img src="static/images/dashboard1.jpg" alt="Dashboard" width="375"/></td>
       <td><img src="static/images/invoice.jpg" alt="Invoice" width="375"/></td>
    </tr>
  </table>
</div>
<p align="center"><i>Images are representative of the actual stunning UI/UX available in the app.</i></p>

---

## 🛠️ Quick Installation Guide

Get up and running in literal minutes!

### 1. Prerequisites
Ensure you have the following installed:
- **Python 3.8+**
- **MySQL Server 8.0+**

### 2. Clone the Repository
```bash
git clone https://github.com/ayusjakhmola25/Healthy-Choice-Caf-management-with-AI-Recommendations-Engine.git
cd Healthy-Choice-Caf-management-with-AI-Recommendations-Engine
```

### 3. Setup Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Database Configuration
The app takes care of creating tables automatically! Just ensure your credentials match in `app.py`:
```python
db_pool = pooling.MySQLConnectionPool(
    host="localhost",
    user="root",        # default
    password="your_password",
    database="healthy_cafe_db"
)
```
*(Create the empty database `healthy_cafe_db` in MySQL beforehand.)*

### 6. Ignition 🚀
```bash
python app.py
```
Open **[http://127.0.0.1:3000](http://127.0.0.1:3000)** in your browser and prepare to be amazed!

---

## 📡 Essential REST APIs

A completely scalable interface for headless integrations.

| Endpoint | HTTP Method | Access | Purpose |
| :--- | :---: | :---: | :--- |
| `/register` | `POST` | Public | Create a new user profile. |
| `/send-login-otp` | `POST` | Public | Dispatches SMTP verification code. |
| `/verify-login-otp` | `POST` | Public | Authorizes and initiates session. |
| `/food-items` | `GET` | User | Fetches context-aware, active menu items. |
| `/add-to-cart` | `POST` | Public | Handles shopping cart item persistence. |
| `/generate-invoice` | `POST` | User | Returns high-res base64 encoded PDF invoice. |
| `/admin/menu-items` | `POST` | Admin | Perform restricted CRUD on food items. |

---

## 📂 Project Structure

A meticulously organized file structure ensuring effortless maintainability.

```text
Healthy-Cafe/
├── app.py                  # Entry point, Routes, Controllers, & DB Operations
├── requirements.txt        # Python dependency manifest
├── README.md               # 📖 You are here
├── static/                 # Production-ready CSS, JS, and optimized Images
│   ├── css/
│   ├── js/
│   └── images/
└── templates/              # Server-rendered Jinja2 views
    ├── admin/              # Secured Admin Command Center pages
    └── user/               # Public and Client-side pages (Cafeteria, Cart, Payment)
```

---

## 🤝 Contributing

We welcome absolute excellence! To contribute to Healthy Cafe Zone:

1. **Fork** the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Added some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a **Pull Request**.

Ensure your code adheres to standard PEP-8 style guidelines and comes with appropriate tests.

---

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

<div align="center">
  <b>Built with passion for clean code and healthy living ❤️</b><br/>
  <sup>If you like this project, please consider leaving a ⭐ on the repository!</sup>
</div>
