import os
import sys
import json

# Set environment variable for UTF-8 encoding
os.environ['PYTHONIOENCODING'] = 'utf-8'

import bcrypt
from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from flask_mail import Mail, Message
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import random
import time
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
import random
import time
from datetime import datetime

# Fix for Windows Unicode encoding issues
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'replace')

# Data structures
users = []
login_history = []
login_otp_store = {}
guest_orders = []

# Persistence functions
DATA_FILE = 'app_data.json'

def load_data():
    global users, login_history, guest_orders
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            users = data.get('users', [])
            login_history = data.get('login_history', [])
            guest_orders = data.get('guest_orders', [])

def save_data():
    data = {
        'users': users,
        'login_history': login_history,
        'guest_orders': guest_orders
    }
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Load data on startup
load_data()

# Dummy functions
def load_food_items():
    # Dummy food items data
    return [
        {'id': 1, 'name': 'Burger', 'price': 100, 'image': 'burger.jpg', 'protein': 20, 'carbs': 30, 'fats': 15, 'calories': 400},
        {'id': 2, 'name': 'Fries', 'price': 50, 'image': 'fries.jpg', 'protein': 5, 'carbs': 40, 'fats': 10, 'calories': 300},
        # Add more items as needed
    ]

def get_food_recommendations(item_id):
    # Dummy recommendations based on item_id
    recommendations = [
        {'id': 2, 'name': 'Fries', 'price': 50, 'image': 'fries.jpg'},
        {'id': 3, 'name': 'Drink', 'price': 30, 'image': 'drink.jpg'},
    ]
    return recommendations


app = Flask(__name__)
CORS(app)
app.secret_key = 'your_secret_key_here'  # Change to a secure key in production

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'jakhmolaayush3@gmail.com'
app.config['MAIL_PASSWORD'] = 'yzsfhhqraakovbjj'

mail = Mail(app)

# Flask-Limiter configuration
limiter = Limiter(get_remote_address, app=app)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    mobile = data.get('mobile')

    if not name or not email or not password or not mobile:
        return jsonify({'error': 'Name, email, password, and mobile are required'}), 400

    # Check if user already exists
    existing_user = next((u for u in users if u['email'] == email), None)
    if existing_user:
        return jsonify({'error': 'User already exists'}), 400

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Create new user
    new_user = {
        'id': len(users) + 1,
        'name': name,
        'email': email,
        'password': hashed_password.decode('utf-8'),
        'mobile': mobile,
        'dob': None,
        'gender': None
    }
    users.append(new_user)
    save_data()

    return jsonify({'success': True, 'message': 'User registered successfully', 'userId': new_user['id']})

@app.route('/check-user', methods=['POST'])
def check_user():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    user = next((u for u in users if u['email'] == email), None)

    if user:
        user_data = {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'dob': user['dob'],
            'gender': user['gender']
        }
        return jsonify({'exists': True, 'user': user_data})
    else:
        return jsonify({'exists': False})

@app.route('/update-profile', methods=['POST'])
def update_profile():
    data = request.get_json()
    mobile = data.get('mobile')
    name = data.get('name')
    dob = data.get('dob')
    gender = data.get('gender')

    if not mobile:
        return jsonify({'error': 'Mobile number is required'}), 400

    user = next((u for u in users if u['mobile'] == mobile), None)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Update user fields
    if name:
        user['name'] = name
    if dob:
        user['dob'] = dob
    if gender:
        user['gender'] = gender

    updated_user = {
        'id': user['id'],
        'name': user['name'],
        'mobile': user['mobile'],
        'email': user['email'],
        'dob': user['dob'],
        'gender': user['gender']
    }

    return jsonify({'success': True, 'message': 'Profile updated successfully', 'user': updated_user})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = next((u for u in users if u['email'] == email), None)
    if not user:
        return jsonify({'error': 'User not registered'}), 404

    # Verify password using bcrypt
    if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return jsonify({'error': 'Invalid password'}), 401

    user_id = user['id']

    # Record login history
    new_login_history = {
        'id': len(login_history) + 1,
        'user_id': user_id,
        'login_time': datetime.now().isoformat()
    }
    login_history.append(new_login_history)

    # Store user name in session
    session['user_name'] = user['name']
    session['user_id'] = user_id

    return jsonify({'success': True, 'message': 'Login successful', 'userId': user_id, 'userName': user['name']})

@app.route('/send-login-otp', methods=['POST'])
def send_login_otp():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    user = next((u for u in users if u['email'] == email), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    otp = str(random.randint(100000, 999999))
    otp_id = f"otp_{int(time.time())}_{random.randint(1000, 9999)}"

    login_otp_store[otp_id] = {
        'otp': otp,
        'email': email,
        'expiry': time.time() + 300,  # 5 minutes
        'attempts': 0
    }

    msg = Message(
        subject="HangOut Cafe Login Verification Code",
        sender=app.config['MAIL_USERNAME'],
        recipients=[email]
    )

    msg.html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body {{
    font-family: Arial, sans-serif;
    background-color: #f4f6f8;
    padding: 20px;
}}

.container {{
    max-width: 500px;
    margin: auto;
    background: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    text-align: center;
}}

.header {{
    font-size: 22px;
    font-weight: bold;
    color: #2c3e50;
}}

.otp-box {{
    margin: 25px 0;
    font-size: 32px;
    letter-spacing: 6px;
    font-weight: bold;
    color: white;
    background: #3498db;
    padding: 15px;
    border-radius: 8px;
    display: inline-block;
}}

.info {{
    font-size: 14px;
    color: #555;
}}

.footer {{
    margin-top: 25px;
    font-size: 12px;
    color: #999;
}}
</style>
</head>

<body>

<div class="container">

<div class="header">
HangOut Cafe Security Verification
</div>

<p>Hello,</p>

<p>Your One Time Password (OTP) for login is:</p>

<div class="otp-box">{otp}</div>

<p class="info">
This OTP is valid for <b>5 minutes</b>.
</p>

<p class="info">
Do not share this code with anyone for security reasons.
</p>

<div class="footer">
HangOut Cafe • Secure Login System
</div>

</div>

</body>
</html>
"""

    try:
        mail.send(msg)
    except Exception as e:
        print(f"Error sending email: {e}")
        return jsonify({'error': 'Failed to send OTP email'}), 500

    return jsonify({'message': 'OTP sent successfully', 'otpId': otp_id})

@app.route('/verify-login-otp', methods=['POST'])
def verify_login_otp():
    data = request.get_json()
    otp_id = data.get('otpId')
    otp = data.get('otp')

    if not otp_id or not otp:
        return jsonify({'error': 'OTP ID and OTP are required'}), 400

    stored_otp = login_otp_store.get(otp_id)

    if not stored_otp:
        return jsonify({'error': 'Invalid OTP ID'}), 400

    if time.time() > stored_otp['expiry']:
        del login_otp_store[otp_id]
        return jsonify({'error': 'OTP expired'}), 400

    if stored_otp['otp'] != otp:
        return jsonify({'error': 'Invalid OTP'}), 400

    user = next((u for u in users if u['email'] == stored_otp['email']), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_id = user['id']

    # Record login history
    new_login_history = {
        'id': len(login_history) + 1,
        'user_id': user_id,
        'login_time': datetime.now().isoformat()
    }
    login_history.append(new_login_history)

    # Store user name in session
    session['user_name'] = user['name']
    session['user_id'] = user_id

    del login_otp_store[otp_id]

    return jsonify({'success': True, 'message': 'Login successful', 'userId': user_id})

@app.route('/login-count', methods=['POST'])
def login_count():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    user = next((u for u in users if u['email'] == email), None)
    if not user:
        return jsonify({'loginCount': 0})

    login_count_value = len([lh for lh in login_history if lh['user_id'] == user['id']])
    return jsonify({'loginCount': login_count_value})

@app.route('/get-login-history', methods=['POST'])
def get_login_history():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    user = next((u for u in users if u['email'] == email), None)
    if not user:
        return jsonify({'loginHistory': []})

    user_login_history = [lh for lh in login_history if lh['user_id'] == user['id']]
    user_login_history.sort(key=lambda x: x['login_time'], reverse=True)
    history_data = [{
        'id': entry['id'],
        'login_time': entry['login_time']
    } for entry in user_login_history]
    return jsonify({'loginHistory': history_data})

@app.route('/food-items', methods=['GET'])
def get_food_items():
    items = load_food_items()
    return jsonify(items)

@app.route('/recommendations/<item_id>', methods=['GET'])
def get_recommendations(item_id):
    try:
        recommendations = get_food_recommendations(item_id)
        return jsonify({'success': True, 'recommendations': recommendations})
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        return jsonify({'success': False, 'error': 'Failed to get recommendations'}), 500

@app.route('/generate-invoice', methods=['POST'])
def generate_invoice():
    data = request.get_json()
    order_items = data.get('orderItems')
    total_amount = data.get('totalAmount')
    payment_method = data.get('paymentMethod')
    customer_name = data.get('customerName')
    customer_mobile = data.get('customerMobile')

    if not order_items or not total_amount or not payment_method:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        # Create PDF
        filename = f"invoice_{int(time.time())}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Header
        title_style = styles['Heading1']
        title_style.alignment = 1  # Center alignment
        title = Paragraph("Cafe Zone", title_style)
        story.append(title)

        subtitle = Paragraph("Invoice", styles['Heading2'])
        story.append(subtitle)
        story.append(Spacer(1, 12))

        # Invoice details
        invoice_info = [
            f"Date: {datetime.now().strftime('%Y-%m-%d')}",
            f"Time: {datetime.now().strftime('%H:%M:%S')}",
            f"Invoice #: CZ{int(time.time() * 1000)}"
        ]

        if customer_name:
            invoice_info.append(f"Customer: {customer_name}")
        if customer_mobile:
            invoice_info.append(f"Mobile: {customer_mobile}")

        for info in invoice_info:
            story.append(Paragraph(info, styles['Normal']))
        story.append(Spacer(1, 12))

        # Order details header
        story.append(Paragraph("Order Details:", styles['Heading3']))
        story.append(Spacer(1, 6))

        # Table data
        table_data = [['Item', 'Qty', 'Price', 'Total']]
        for item in order_items:
            table_data.append([
                item['name'],
                str(item['quantity']),
                f"₹{item['price']}",
                f"₹{(item['price'] * item['quantity']):.2f}"
            ])

        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        story.append(Spacer(1, 12))

        # Calculate amounts
        subtotal = float(total_amount) - 50  # Subtract delivery fee
        gst_amount = subtotal * 0.18
        delivery_fee = 50

        amounts = [
            f"Subtotal: ₹{subtotal:.2f}",
            f"GST (18%): ₹{gst_amount:.2f}",
            f"Delivery Fee: ₹{delivery_fee:.2f}",
            f"Total Amount: ₹{total_amount}"
        ]

        for amount in amounts:
            story.append(Paragraph(amount, styles['Normal']))
        story.append(Spacer(1, 6))

        story.append(Paragraph(f"Payment Method: {payment_method}", styles['Normal']))
        story.append(Spacer(1, 12))

        # Footer
        footer_style = styles['Normal']
        footer_style.fontSize = 8
        footer_style.textColor = colors.gray
        story.append(Paragraph("Thank you for choosing Cafe Zone!", footer_style))
        story.append(Paragraph("For any queries, contact us at support@cafezone.com", footer_style))

        doc.build(story)

        # Read PDF as base64
        with open(filename, 'rb') as f:
            pdf_data = f.read()
        import base64
        pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')

        # Clean up
        os.remove(filename)

        return jsonify({
            'success': True,
            'pdf': pdf_base64,
            'invoiceNumber': f"CZ{int(time.time() * 1000)}"
        })

    except Exception as e:
        print(f"Error generating invoice: {e}")
        return jsonify({'error': 'Failed to generate invoice'}), 500

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    item_id = data.get('item_id')
    quantity = data.get('quantity', 1)

    if not item_id:
        return jsonify({'error': 'Item ID is required'}), 400

    # Get or create cart in session
    cart = session.get('cart', {})
    cart[str(item_id)] = cart.get(str(item_id), 0) + quantity
    session['cart'] = cart

    return jsonify({'success': True, 'message': 'Item added to cart', 'cart': cart})

@app.route('/save-order', methods=['POST'])
def save_order():
    data = request.get_json()
    name = data.get('name')
    mobile = data.get('mobile')
    email = data.get('email')
    order_data = data.get('order_data')  # JSON string of cart items
    total_amount = data.get('total_amount')
    payment_method = data.get('payment_method')
    diet_preference = data.get('diet_preference')  # 'diet', 'non-diet', or None
    user_id = data.get('user_id')  # Optional for logged-in users

    if not name or not mobile or not email or not order_data or not total_amount or not payment_method:
        return jsonify({'error': 'All fields are required'}), 400

    # Save to guest_orders list
    new_order = {
        'id': len(guest_orders) + 1,
        'user_id': user_id,
        'name': name,
        'mobile': mobile,
        'email': email,
        'order_data': order_data,
        'total_amount': total_amount,
        'payment_method': payment_method,
        'diet_preference': diet_preference,
        'order_date': datetime.now().isoformat()
    }
    guest_orders.append(new_order)

    print(f"Guest order saved: {name}, {mobile}, {email}, {total_amount}, diet: {diet_preference}, user_id: {user_id}")

    return jsonify({'success': True, 'message': 'Order saved successfully', 'order_id': new_order['id']})

@app.route('/get-guest-orders', methods=['POST'])
def get_guest_orders():
    data = request.get_json()
    mobile = data.get('mobile')
    email = data.get('email')

    if not mobile and not email:
        return jsonify({'error': 'Mobile or email is required'}), 400

    # Filter orders
    orders = guest_orders
    if mobile:
        orders = [o for o in orders if o['mobile'] == mobile]
    if email:
        orders = [o for o in orders if o['email'] == email]

    # Sort by order_date descending
    orders.sort(key=lambda x: x['order_date'], reverse=True)

    orders_data = [{
        'id': order['id'],
        'name': order['name'],
        'mobile': order['mobile'],
        'email': order['email'],
        'order_data': order['order_data'],
        'total_amount': order['total_amount'],
        'payment_method': order['payment_method'],
        'diet_preference': order['diet_preference'],
        'order_date': order['order_date']
    } for order in orders]

    return jsonify({'success': True, 'orders': orders_data})

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

# Routes for HTML pages
@app.route('/')
def home():   
    return render_template('login.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/cart')
def cart_page():
    return render_template('cart.html')

@app.route('/orders')
def orders_page():
    return render_template('orders.html')

@app.route('/payment')
def payment_page():
    return render_template('payment.html')

@app.route('/payment.html')
def payment_html_page():
    return render_template('payment.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile_page():
    if request.method == 'POST':
        data = request.get_json()
        mobile = data.get('mobile')

        if not mobile:
            return jsonify({'error': 'Mobile number is required'}), 400

        user = next((u for u in users if u['mobile'] == mobile), None)

        if user:
            user_data = {
                'id': user['id'],
                'name': user['name'],
                'mobile': user['mobile'],
                'email': user['email'],
                'dob': user['dob'],
                'gender': user['gender']
            }
            return jsonify({'exists': True, 'user': user_data})
        else:
            return jsonify({'exists': False})

    return render_template('profile.html')

@app.route('/profile-data', methods=['POST'])
def get_profile_data():
    data = request.get_json()
    mobile = data.get('mobile')

    if not mobile:
        return jsonify({'error': 'Mobile number is required'}), 400

    user = next((u for u in users if u['mobile'] == mobile), None)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_data = {
        'id': user['id'],
        'name': user['name'],
        'mobile': user['mobile'],
        'email': user['email'],
        'dob': user['dob'],
        'gender': user['gender']
    }

    # Get login count
    login_count_value = len([lh for lh in login_history if lh['user_id'] == user['id']])

    # Get login history
    user_login_history = [lh for lh in login_history if lh['user_id'] == user['id']]
    user_login_history.sort(key=lambda x: x['login_time'], reverse=True)
    history_data = [{
        'id': entry['id'],
        'login_time': entry['login_time']
    } for entry in user_login_history]

    # Get orders
    orders = [o for o in guest_orders if o['mobile'] == mobile]
    orders.sort(key=lambda x: x['order_date'], reverse=True)
    orders_data = [{
        'id': order['id'],
        'name': order['name'],
        'mobile': order['mobile'],
        'email': order['email'],
        'order_data': order['order_data'],
        'total_amount': order['total_amount'],
        'payment_method': order['payment_method'],
        'diet_preference': order['diet_preference'],
        'order_date': order['order_date']
    } for order in orders]

    # Calculate nutritional insights
    total_orders = len(orders)
    if total_orders > 0:
        total_protein = 0
        total_carbs = 0
        total_fats = 0
        total_calories = 0

        for order in orders:
            try:
                items = eval(order['order_data'])  # Assuming order_data is a string representation of list
                for item in items:
                    total_protein += (item.get('protein', 0) * item.get('quantity', 1))
                    total_carbs += (item.get('carbs', 0) * item.get('quantity', 1))
                    total_fats += (item.get('fats', 0) * item.get('quantity', 1))
                    total_calories += (item.get('calories', 0) * item.get('quantity', 1))
            except:
                pass

        avg_protein = total_protein / total_orders
        avg_carbs = total_carbs / total_orders
        avg_fats = total_fats / total_orders
        avg_calories = total_calories / total_orders
    else:
        avg_protein = avg_carbs = avg_fats = avg_calories = 0

    # Determine preference
    diet_orders = sum(1 for o in orders if o['diet_preference'] == 'diet')
    non_diet_orders = sum(1 for o in orders if o['diet_preference'] == 'non-diet')
    if diet_orders > non_diet_orders:
        preference = 'Diet'
    elif non_diet_orders > diet_orders:
        preference = 'Non-Diet'
    else:
        preference = 'Mixed'

    return jsonify({
        'user': user_data,
        'loginCount': login_count_value,
        'loginHistory': history_data,
        'totalOrders': total_orders,
        'avgProtein': round(avg_protein, 1),
        'avgCarbs': round(avg_carbs, 1),
        'avgFats': round(avg_fats, 1),
        'avgCalories': round(avg_calories),
        'preference': preference
    })

@app.route('/welcome', methods=['GET'])
def welcome():
    return jsonify({'message': 'Welcome to Cafe Zone!'})

@app.route('/cafeteria')
def cafeteria():
    # Fetch all food items from CSV
    items = load_food_items()
    user_name = session.get('user_name', 'Guest')
    return render_template('cafeteria.html', items=items, user_name=user_name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500

@app.errorhandler(Exception)
def handle_exception(e):
    return render_template("500.html"), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
