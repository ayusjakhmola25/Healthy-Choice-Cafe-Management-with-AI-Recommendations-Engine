
import os
import sys
import json


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
from datetime import datetime, timedelta


if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'replace')

import re

def validate_password(password):
    """
    Validate password meets the following requirements:
    - Length 8-12 characters
    - At least 1 uppercase letter
    - At least 1 number
    - At least 1 special character
    """
    if len(password) < 8 or len(password) > 12:
        return False, 'Password must be 8-12 characters long'
    if not re.search(r'[A-Z]', password):
        return False, 'Password must contain at least 1 uppercase letter'
    if not re.search(r'[0-9]', password):
        return False, 'Password must contain at least 1 number'
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, 'Password must contain at least 1 special character'
    
    return True, 'Password is valid'



# Dummy functions
def load_food_items():

    return [
        {'id': 1, 'name': 'Burger', 'price': 100, 'image': 'burger.jpg', 'protein': 20, 'carbs': 30, 'fats': 15, 'calories': 400},
        {'id': 2, 'name': 'Fries', 'price': 50, 'image': 'fries.jpg', 'protein': 5, 'carbs': 40, 'fats': 10, 'calories': 300},

    ]

def get_food_recommendations(item_id):

    recommendations = [
        {'id': 2, 'name': 'Fries', 'price': 50, 'image': 'fries.jpg'},
        {'id': 3, 'name': 'Drink', 'price': 30, 'image': 'drink.jpg'},
    ]
    return recommendations



import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ayush123", 
    database="healthy_cafe_db"
)

cursor = db.cursor(dictionary=True)

app = Flask(__name__)
CORS(app)
app.secret_key = 'your_secret_key_here'  # Change to a secure key in production





import smtplib  

try:
    # Use SSL on port 465 (more reliable than TLS on port 587)    
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'healthycafe2025@gmail.com'
    app.config['MAIL_PASSWORD'] = 'yrzljphqtcrywzmd'
    app.config['MAIL_DEFAULT_SENDER'] = 'healthycafe2025@gmail.com'
    
    mail = Mail(app)    
except Exception as e:
      print(f"Warning during mail config:{e}")



limiter = Limiter(get_remote_address, app=app)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    mobile = data.get('mobile')

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    query = """
    INSERT INTO users (name,email,mobile,password_hash,role)
    VALUES (%s,%s,%s,%s,%s)
    """

    values = (name,email,mobile,hashed_password.decode('utf-8'),"user")

    cursor.execute(query,values)
    db.commit()

    return jsonify({
        "success":True,
        "message":"User registered successfully"
    })

@app.route('/check-user', methods=['POST'])
def check_user():

    data = request.get_json()

    email = data.get('email')

    cursor.execute(
        "SELECT id,name,email,mobile,dob,gender FROM users WHERE email=%s",
        (email,)
    )

    user = cursor.fetchone()

    if user:
        return jsonify({
            "exists":True,
            "user":user
        })

    return jsonify({"exists":False})

@app.route('/user-profile/<int:user_id>')
def get_user_profile(user_id):

	cursor.execute("""
	SELECT id,name,email,mobile,dob,gender
	FROM users
	WHERE id=%s
	""",(user_id,))

	user = cursor.fetchone()

	return jsonify(user)

@app.route('/update-profile', methods=['POST'])
def update_profile():

    data = request.get_json()

    name = data.get("name")
    mobile = data.get("mobile")
    dob = data.get("dob")
    gender = data.get("gender")

    query = """
    UPDATE users
    SET name=%s,dob=%s,gender=%s
    WHERE mobile=%s
    """

    cursor.execute(query,(name,dob,gender,mobile))
    db.commit()

    return jsonify({"success":True})

@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    user = cursor.fetchone()

    if not user:
        return jsonify({"error":"User not found"}),404

    if not bcrypt.checkpw(password.encode('utf-8'), user["password_hash"].encode('utf-8')):
        return jsonify({"error":"Invalid password"}),401

    session["user_id"] = user["id"]

    
    ip_address = request.remote_addr

    cursor.execute("""
    INSERT INTO login_history (user_id, login_time, ip_address)
    VALUES (%s,%s,%s)
    """,(user["id"], datetime.now(), ip_address))

    db.commit()

    return jsonify({
        "success":True,
        "message":"Login successful",
        "userId":user["id"]
    })

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """
    GET  - render admin login page
    POST - authenticate admin and establish session (JSON API)
    """
    if request.method == 'GET':
        if "admin_id" in session:
            return render_template("admin/dashboard.html")
        return render_template("admin/login.html")

    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    cursor.execute("""
    SELECT * FROM users
    WHERE email=%s AND role='admin'
    """, (email,))

    admin = cursor.fetchone()

    if not admin:
        return jsonify({"error": "Admin not found"}), 404

    if not bcrypt.checkpw(password.encode('utf-8'), admin["password_hash"].encode('utf-8')):
        return jsonify({"error": "Invalid password"}), 401

    session["admin_id"] = admin["id"]

    return jsonify({
        "success": True,
        "message": "Admin login successful"
    })

@app.route('/send-login-otp', methods=['POST'])
def send_login_otp():

    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email required"}), 400

    # Find user
    cursor.execute("SELECT id, name FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"error": "User not found"}), 404

    user_id = user["id"]
    user_name = user.get("name", "User")

    # Delete any existing expired OTPs
    cursor.execute("DELETE FROM login_otp WHERE user_id=%s AND expiry_time < NOW()", (user_id,))
    db.commit()

    # Generate OTP
    otp = random.randint(100000, 999999)

    expiry_time = datetime.now() + timedelta(minutes=5)

    query = """
    INSERT INTO login_otp (user_id, otp_code, expiry_time)
    VALUES (%s,%s,%s)
    """

    cursor.execute(query, (user_id, otp, expiry_time))
    db.commit()

    
    msg = Message(
        subject="Healthy Cafe Login Verification Code",
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
Healthy Cafe Security Verification
</div>

<p>Hello {user_name},</p>

<p>Your One Time Password (OTP) for login is:</p>

<div class="otp-box">{otp}</div>

<p class="info">
This OTP is valid for <b>5 minutes</b>.
</p>

<p class="info">
Do not share this code with anyone for security reasons.
</p>

<div class="footer">
Healthy Cafe • Secure Login System
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

    print("OTP:", otp)

    return jsonify({
        "success": True,
        "otpId": user_id
    })

@app.route('/verify-login-otp', methods=['POST'])
def verify_login_otp():
    data = request.get_json()
    user_id = data.get('otpId')
    otp = data.get('otp')

    if not user_id or not otp:
        return jsonify({'error': 'User ID and OTP are required'}), 400

    # Get OTP from database
    cursor.execute(
        "SELECT * FROM login_otp WHERE user_id=%s AND otp_code=%s AND expiry_time > NOW()",
        (user_id, otp)
    )
    stored_otp = cursor.fetchone()

    if not stored_otp:
        return jsonify({'error': 'Invalid or expired OTP'}), 400

    # Get user from database
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Delete the OTP after successful verification
    cursor.execute("DELETE FROM login_otp WHERE user_id=%s", (user_id,))
    db.commit()

    # Insert login history
    ip_address = request.remote_addr
    query = """
    INSERT INTO login_history (user_id, login_time, ip_address)
    VALUES (%s,%s,%s)
    """
    cursor.execute(query, (user["id"], datetime.now(), ip_address))
    db.commit()

    # Store user info in session
    session['user_id'] = user['id']
    session['user_name'] = user['name']

    return jsonify({'success': True, 'message': 'Login successful', 'userId': user['id']})

@app.route('/login-count', methods=['POST'])
def login_count():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    # Get user by email first
    cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    
    if not user:
        return jsonify({'loginCount': 0})

    # Get login count from database
    cursor.execute("""
        SELECT COUNT(*) as total
        FROM login_history
        WHERE user_id=%s
    """, (user['id'],))
    
    result = cursor.fetchone()
    return jsonify({'loginCount': result['total']})

@app.route('/get-login-history', methods=['POST'])
def get_login_history():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    # Look up user in the database
    cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({'loginHistory': []})

    # Fetch login history from database
    cursor.execute(
        """
        SELECT id, login_time, ip_address
        FROM login_history
        WHERE user_id=%s
        ORDER BY login_time DESC
        """,
        (user["id"],),
    )
    rows = cursor.fetchall()

    history_data = [
        {
            "id": row["id"],
            "login_time": row["login_time"].isoformat() if row["login_time"] else None,
            "ip_address": row.get("ip_address"),
        }
        for row in rows
    ]

    return jsonify({"loginHistory": history_data})

@app.route('/food-items', methods=['GET'])
def get_food_items():
    items = load_food_items()
    return jsonify(items)

@app.route('/menu-items', methods=['GET'])
def get_menu_items():
    cursor.execute("SELECT * FROM menu_items")
    items = cursor.fetchall()
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

@app.route('/create-order', methods=['POST'])
def create_order():
    data = request.get_json()

    user_id = data.get("user_id")
    cart = data.get("cart")

    if not cart:
        return jsonify({"error":"Cart empty"}),400

    total_amount = sum(item["price"] * item["quantity"] for item in cart)

    # create order
    cursor.execute("""
    INSERT INTO orders (user_id,total_amount,order_status,created_at)
    VALUES (%s,%s,%s,NOW())
    """,(user_id,total_amount,"pending"))

    db.commit()

    order_id = cursor.lastrowid

    # insert order items
    for item in cart:
        cursor.execute("""
        INSERT INTO order_items (order_id,menu_item_id,quantity,price)
        VALUES (%s,%s,%s,%s)
        """,(order_id,item["id"],item["quantity"],item["price"]))

    db.commit()

    return jsonify({
        "success":True,
        "order_id":order_id
    })

@app.route('/user-orders/<int:user_id>')
def get_user_orders(user_id):

    cursor.execute("""
    SELECT * FROM orders
    WHERE user_id=%s
    ORDER BY created_at DESC
    """,(user_id,))

    orders = cursor.fetchall()

    return jsonify(orders)

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

    # Fetch user from database
    cursor.execute(
        """
        SELECT id, name, email, mobile, dob, gender
        FROM users
        WHERE mobile=%s
        """,
        (mobile,),
    )
    user = cursor.fetchone()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_data = {
        'id': user['id'],
        'name': user['name'],
        'mobile': user['mobile'],
        'email': user['email'],
        'dob': user.get('dob'),
        'gender': user.get('gender'),
    }

    # Login statistics from database
    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM login_history
        WHERE user_id=%s
        """,
        (user['id'],),
    )
    login_count_row = cursor.fetchone()
    login_count_value = login_count_row['total'] if login_count_row else 0

    cursor.execute(
        """
        SELECT id, login_time, ip_address
        FROM login_history
        WHERE user_id=%s
        ORDER BY login_time DESC
        """,
        (user['id'],),
    )
    login_rows = cursor.fetchall()
    history_data = [
        {
            'id': row['id'],
            'login_time': row['login_time'].isoformat() if row['login_time'] else None,
            'ip_address': row.get('ip_address'),
        }
        for row in login_rows
    ]

    # Orders and nutritional insights
    # NOTE: nutrition is still derived from in-memory guest_orders for now
    orders = [o for o in guest_orders if o['mobile'] == mobile]
    orders.sort(key=lambda x: x['order_date'], reverse=True)

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

def admin_required(f):
    """Decorator to check if admin is logged in"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin_id" not in session:
            return render_template("admin/login.html")
        return f(*args, **kwargs)
    return decorated_function

# Admin Routes
@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    # Aggregate basic metrics for dashboard cards
    cursor.execute("SELECT COUNT(*) AS total_users FROM users")
    users_row = cursor.fetchone() or {"total_users": 0}

    cursor.execute("SELECT COUNT(*) AS total_orders, COALESCE(SUM(total_amount), 0) AS total_revenue FROM orders")
    orders_row = cursor.fetchone() or {"total_orders": 0, "total_revenue": 0}

    # Inventory low stock (assumes inventory table with quantity & threshold columns)
    low_stock_items = []
    low_stock_count = 0
    try:
        cursor.execute(
            """
            SELECT id, ingredient_name, quantity, threshold
            FROM inventory
            WHERE quantity < threshold
            """
        )
        low_stock_items = cursor.fetchall()
        low_stock_count = len(low_stock_items)
    except Exception as e:
        print(f"Warning reading inventory for dashboard: {e}")

    return render_template(
        "admin/dashboard.html",
        total_users=users_row["total_users"],
        total_orders=orders_row["total_orders"],
        total_revenue=orders_row["total_revenue"],
        low_stock_items=low_stock_items,
        low_stock_items_count=low_stock_count,
    )

@app.route("/admin/users")
@admin_required
def admin_users():
    cursor.execute(
        """
        SELECT id, name, email, role, created_at
        FROM users
        ORDER BY created_at DESC
        """
    )
    users_list = cursor.fetchall()
    return render_template("admin/users.html", users=users_list)

@app.route("/admin/menu")
@admin_required
def admin_menu():
    return render_template("admin/menu.html")

@app.route("/admin/inventory")
@admin_required
def admin_inventory():
    items = []
    try:
        cursor.execute(
            """
            SELECT id, ingredient_name, quantity, threshold
            FROM inventory
            ORDER BY ingredient_name
            """
        )
        items = cursor.fetchall()
    except Exception as e:
        print(f"Warning loading inventory: {e}")

    return render_template("admin/inventory.html", inventory_items=items)

@app.route("/admin/orders")
@admin_required
def admin_orders():
    cursor.execute("""
    SELECT orders.*,users.name
    FROM orders
    JOIN users ON users.id=orders.user_id
    """)

    orders = cursor.fetchall()
    return render_template("admin/orders.html", orders=orders)

@app.route("/admin/security-logs")
@admin_required
def admin_logs():
    # Fetch recent login events for audit
    cursor.execute(
        """
        SELECT lh.id,
               lh.login_time,
               lh.ip_address,
               u.email AS user_email
        FROM login_history lh
        JOIN users u ON u.id = lh.user_id
        ORDER BY lh.login_time DESC
        LIMIT 200
        """
    )
    logs = cursor.fetchall()
    return render_template("admin/security_logs.html", logs=logs)

@app.route("/admin/settings")
@admin_required
def admin_settings():
    return render_template("admin/settings.html")

@app.route("/admin")
def admin_index():
    if "admin_id" in session:
        return render_template("admin/dashboard.html")
    return render_template("admin/login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_id", None)
    return render_template("admin/login.html")

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
