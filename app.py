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

from twilio.rest import Client

account_sid = os.environ.get("TWILIO_ACCOUNT_SID", "")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN", "")
try:
    if account_sid and auth_token:
        client = Client(account_sid, auth_token)
    else:
        client = None
except Exception as e:
    client = None
    print(f"Twilio Client Init Error: {e}")

TWILIO_WHATSAPP_NUMBER = os.environ.get("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

def send_payment_success(mobile, name):
    if not client: return
    msg = f"""Hey {name} 👋

Thanks for visiting *Healthy Cafe* 🥗

Your order is confirmed ✅
We hope you enjoyed your meal!

See you again soon 💚"""
    try:
        client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=msg,
            to=f"whatsapp:+91{mobile}"
        )
        print(f"Payment success WhatsApp sent to {mobile}")
    except Exception as e:
        print(f"Twilio error (payment success): {e}")

def send_invoice(mobile, pdf_url):
    if not client: return
    try:
        client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            to=f"whatsapp:+91{mobile}",
            media_url=[pdf_url]
        )
        print(f"Invoice WhatsApp sent to {mobile}")
    except Exception as e:
        print(f"Twilio error (invoice): {e}")

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
    """Load active food items from DB filtered by current meal_mode"""
    cursor.execute("SELECT setting_value FROM system_settings WHERE setting_key='meal_mode'")
    result = cursor.fetchone()
    meal_mode = result['setting_value'] if result else 'all'
    
    query = """
        SELECT * FROM menu_items 
        WHERE is_active = 1 
        AND (category = %s OR %s = 'all' OR category IS NULL)
        ORDER BY id DESC
    """
    cursor.execute(query, (meal_mode, meal_mode))
    items = cursor.fetchall()
    
    # Ensure image_url is full path if static/images
    for item in items:
        if item['image_url'] and '/static/images/' not in item['image_url']:
            item['image_url'] = '/static/images/' + item['image_url'].split('/')[-1]
    
    return items

def get_food_recommendations(item_id):

    recommendations = [
        {'id': 2, 'name': 'Fries', 'price': 50, 'image': 'fries.jpg'},
        {'id': 3, 'name': 'Drink', 'price': 30, 'image': 'drink.jpg'},
    ]
    return recommendations



import mysql.connector
from mysql.connector import pooling
from werkzeug.local import LocalProxy
from flask import g

db_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=10,
    pool_reset_session=True,
    host="localhost",
    user="root",
    password="ayush123",
    database="healthy_cafe_db"
)

# Startup DB info for init_schema block
_startup_db = db_pool.get_connection()
cursor = _startup_db.cursor(dictionary=True, buffered=True)
db = _startup_db

def get_db():
    if 'db' not in g:
        g.db = db_pool.get_connection()
    return g.db

def get_req_cursor():
    if 'cursor' not in g:
        g.cursor = get_db().cursor(dictionary=True, buffered=True)
    return g.cursor

def get_cursor():
    """Return the proxy cursor so existing c = get_cursor() code works transparently"""
    return cursor

# Idempotent schema initialization
def init_schema():
    cursor.execute("SHOW COLUMNS FROM menu_items LIKE 'is_active'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE menu_items ADD COLUMN is_active TINYINT(1) DEFAULT 1")
    
    cursor.execute("SHOW COLUMNS FROM menu_items LIKE 'category'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE menu_items ADD COLUMN category VARCHAR(20) DEFAULT 'all'")
        
    cursor.execute("SHOW COLUMNS FROM users LIKE 'health_coins'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE users ADD COLUMN health_coins INT DEFAULT 0")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_settings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            setting_key VARCHAR(50) UNIQUE,
            setting_value VARCHAR(50),
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS security_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            admin_id INT,
            action VARCHAR(255),
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            login_time DATETIME,
            ip_address VARCHAR(50),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_otp (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            otp_code VARCHAR(6),
            expiry_time DATETIME,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    
    cursor.execute("INSERT IGNORE INTO system_settings (setting_key, setting_value) VALUES ('meal_mode', 'all')")


    try:
        cursor.execute("SHOW COLUMNS FROM orders LIKE 'payment_status'")
        if not cursor.fetchone():
            cursor.execute("""
                ALTER TABLE orders 
                ADD COLUMN payment_status VARCHAR(20) DEFAULT 'UNPAID'
            """)
        db.commit()
    except Exception as e:
        print("Schema update error:", e)


init_schema()

# Cleanup startup connections
try:
    cursor.close()
    db.close()
except Exception:
    pass

# Redefine db and cursor to be Context-Bound (LocalProxy) for all incoming routes
db = LocalProxy(get_db)
cursor = LocalProxy(get_req_cursor)

# In‑memory guest order storage (used for quick profile insights)
guest_orders = []

app = Flask(__name__)
CORS(app)
app.secret_key = 'your_secret_key_here'  # Change to a secure key in production

@app.teardown_appcontext
def teardown_db_connection(exception):
    c = g.pop('cursor', None)
    if c is not None:
        try:
            c.close()
        except Exception:
            pass
    d = g.pop('db', None)
    if d is not None:
        try:
            d.close()
        except Exception:
            pass



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
        "userId":user["id"],
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "mobile": user["mobile"]
        }
    })

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """
    GET  - render admin login page
    POST - authenticate admin and establish session (JSON API)
    """
    if request.method == 'GET':
        # Always show the login page, even if admin is already logged in
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
    
    cursor.execute("INSERT INTO security_logs (admin_id, action) VALUES (%s, %s)",
                   (admin["id"], f"Admin login: {email}"))
    db.commit()

    return jsonify({
        "success": True,
        "message": "Admin login successful"
    })


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

@app.route('/get-menu', methods=['GET'])
def get_menu():
    """Return active menu items, optionally filtered by diet_type."""
    diet_type = request.args.get('type', 'all')

    try:
        if diet_type and diet_type != 'all':
            cursor.execute(
                "SELECT * FROM menu_items WHERE is_active = 1 AND diet_type = %s ORDER BY id DESC",
                (diet_type,)
            )
        else:
            cursor.execute("SELECT * FROM menu_items WHERE is_active = 1 ORDER BY id DESC")

        items = cursor.fetchall()

        # Ensure image_url is full path
        for item in items:
            if item.get('image_url') and '/static/images/' not in item['image_url']:
                item['image_url'] = '/static/images/' + item['image_url'].split('/')[-1]

        return jsonify(items)
    except Exception as e:
        print(f"Error in /get-menu: {e}")
        return jsonify([]), 500

@app.route('/menu-items', methods=['GET'])
def get_menu_items():
    cursor.execute("SELECT * FROM menu_items WHERE is_active = 1 ORDER BY id DESC")
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
        # Create Professional PDF
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import Image as RLImage
        from reportlab.lib.units import inch
        from reportlab.lib.utils import ImageReader

        static_folder = os.path.join(app.root_path, 'static')
        os.makedirs(static_folder, exist_ok=True)
        invoice_id = f"{int(time.time() * 1000)}"
        filename = f"invoice_{invoice_id}.pdf"
        filepath = os.path.join(static_folder, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        styles = getSampleStyleSheet()
        story = []
        
        # Adding Image watermark function
        logo_path = os.path.join(app.root_path, 'static', 'images', 'cafelogo.jpeg')
        def add_watermark(canvas, doc):
            canvas.saveState()
            if os.path.exists(logo_path):
                # Try to use PIL to create a transparent version on the fly, otherwise just draw text
                try:
                    from PIL import Image as PILImage, ImageEnhance
                    img = PILImage.open(logo_path).convert('RGBA')
                    alpha = img.split()[3]
                    alpha = ImageEnhance.Brightness(alpha).enhance(0.1)
                    img.putalpha(alpha)
                    temp_wm = os.path.join(app.root_path, 'static', 'images', f'temp_wm_{invoice_id}.png')
                    img.save(temp_wm, 'PNG')
                    
                    canvas.drawImage(temp_wm, (A4[0]-300)/2, (A4[1]-300)/2, width=300, height=300, mask='auto')
                    os.remove(temp_wm)
                except Exception:
                    canvas.setFont('Helvetica-Bold', 60)
                    canvas.setFillColorRGB(0.9, 0.9, 0.9)
                    canvas.drawCentredString(A4[0]/2, A4[1]/2, "HEALTHY CAFE")
            canvas.restoreState()

        # Header Section (Logo + Cafe Details)
        header_data = []
        cafe_info = [
            Paragraph("<b>Healthy Cafe</b>", styles['Heading1']),
            Paragraph("<i>Fresh • Healthy • Delicious</i>", styles['Normal']),
            Paragraph("123 Cafe Street, Food City, FC 12345", styles['Normal']),
            Paragraph("Phone: +91 9876543210 | Email: hello@healthycafe.com", styles['Normal'])
        ]
        
        if os.path.exists(logo_path):
            logo = RLImage(logo_path, width=1.5*inch, height=1.5*inch)
            header_data = [[logo, cafe_info]]
        else:
            header_data = [["", cafe_info]]
            
        header_table = Table(header_data, colWidths=[2*inch, 4.5*inch])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (1,0), (1,0), 'LEFT')
        ]))
        story.append(header_table)
        story.append(Spacer(1, 20))
        
        # Invoice Details
        invoice_number = f"CZ{invoice_id}"
        details_data = [
            [Paragraph("<b>Invoice To:</b>", styles['Normal']), Paragraph(f"<b>Invoice #:</b> {invoice_number}", styles['Normal'])],
            [Paragraph(f"Name: {customer_name or 'Walk-in Customer'}", styles['Normal']), Paragraph(f"Date: {datetime.now().strftime('%d %b %Y')}", styles['Normal'])],
            [Paragraph(f"Mobile: {customer_mobile or 'N/A'}", styles['Normal']), Paragraph(f"Time: {datetime.now().strftime('%I:%M %p')}", styles['Normal'])]
        ]
        details_table = Table(details_data, colWidths=[3.25*inch, 3.25*inch])
        details_table.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'LEFT')]))
        story.append(details_table)
        story.append(Spacer(1, 20))
        
        # Table Section
        table_data = [['Item Name', 'Quantity', 'Price', 'Total']]
        for item in order_items:
            table_data.append([
                item['name'],
                str(item['quantity']),
                f"Rs. {item['price']}",
                f"Rs. {(item['price'] * item['quantity']):.2f}"
            ])
            
        # Green theme
        green_color = colors.HexColor('#28a745')
        light_gray = colors.HexColor('#f8f9fa')
        
        invoice_table = Table(table_data, colWidths=[3.25*inch, 1*inch, 1.125*inch, 1.125*inch])
        invoice_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), green_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),  # Left align item names
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_gray]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BOX', (0, 0), (-1, -1), 1, green_color)
        ]))
        story.append(invoice_table)
        story.append(Spacer(1, 15))
        
        # Pricing Section
        subtotal = float(total_amount) - 50  # Delivery fee
        gst_amount = subtotal * 0.18
        delivery_fee = 50
        
        pricing_data = [
            ["", "Subtotal:", f"Rs. {subtotal:.2f}"],
            ["", "GST (18%):", f"Rs. {gst_amount:.2f}"],
            ["", "Delivery Fee:", f"Rs. {delivery_fee:.2f}"],
            ["", "Final Total:", f"Rs. {total_amount}"]
        ]
        pricing_table = Table(pricing_data, colWidths=[3.5*inch, 1.5*inch, 1.5*inch])
        pricing_table.setStyle(TableStyle([
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('FONTNAME', (1, 3), (2, 3), 'Helvetica-Bold'),
            ('BACKGROUND', (1, 3), (2, 3), colors.HexColor('#e8f5e9')),  # Highlight final total
            ('PADDING', (1, 3), (2, 3), 8)
        ]))
        story.append(pricing_table)
        story.append(Spacer(1, 40))
        
        # Footer Section
        centered_style = ParagraphStyle(name='Centered', parent=styles['Normal'], alignment=1)
        story.append(Paragraph(f"Payment Method: <b>{payment_method}</b>", centered_style))
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("<b>Thank you for visiting Healthy Cafe!</b>", centered_style))
        story.append(Paragraph("<i>Stay healthy, eat fresh</i>", centered_style))
        
        # Build document
        doc.build(story, onFirstPage=add_watermark, onLaterPages=add_watermark)
        
        # Read PDF as base64 for frontend response
        with open(filepath, 'rb') as f:
            pdf_data = f.read()
        import base64
        pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
        
        pdf_url = request.host_url.rstrip('/') + f'/static/{filename}'
        if customer_mobile:
            send_invoice(customer_mobile, pdf_url)

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

    # Order create logic per spec
    payment_method = data.get("paymentMethod")
    payment_status = "UNPAID"

    cursor.execute("""
    INSERT INTO orders (user_id, total_amount, order_status, payment_status, created_at)
    VALUES (%s, %s, %s, %s, NOW())
    """, (user_id, total_amount, "PENDING", payment_status))

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

@app.route('/initiate-order', methods=['POST'])
def initiate_order():
    data = request.get_json()
    user_id = data.get("user_id")
    total_amount = data.get("total_amount")
    cart = data.get("cart")

    if not cart:
        return jsonify({"error":"Cart empty"}), 400

    try:
        cursor.execute("""
        INSERT INTO orders (user_id, total_amount, order_status, payment_status, created_at)
        VALUES (%s, %s, %s, %s, NOW())
        """, (user_id, float(total_amount), "PENDING", "UNPAID"))
        db.commit()

        order_id = cursor.lastrowid

        # Insert order items
        for item in cart:
            cursor.execute("""
            INSERT INTO order_items (order_id, menu_item_id, quantity, price)
            VALUES (%s, %s, %s, %s)
            """, (order_id, item["id"], item["quantity"], item["price"]))
        db.commit()

        return jsonify({"success": True, "order_id": order_id})
    except Exception as e:
        print(f"Error initiating order: {e}")
        return jsonify({"error": "Failed to initiate order"}), 500

@app.route('/save-order', methods=['POST'])
def save_order():
    data = request.get_json()
    order_id = data.get('order_id')
    name = data.get('name')
    mobile = data.get('mobile')
    email = data.get('email')
    order_data = data.get('order_data')  # JSON string of cart items
    total_amount = data.get('total_amount')
    payment_method = data.get('payment_method')
    diet_preference = data.get('diet_preference')  # 'diet', 'non-diet', or None
    user_id = data.get('user_id')  # Optional for logged-in users

    if not order_id or not total_amount or not payment_method:
        return jsonify({'error': 'Missing required fields'}), 400

    # Save to guest_orders list (for quick profile analytics)
    new_order = {
        'id': order_id,
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

    # Persist the final status to the DB
    try:
        payment_status = "PAID" if payment_method == "Card Payment" else "UNPAID"
        order_status = "PAID" if payment_method == "Card Payment" else "COD_CONFIRMED"
        
        cursor.execute(
            """
            UPDATE orders
            SET order_status = %s, payment_status = %s
            WHERE id = %s
            """,
            (order_status, payment_status, order_id),
        )
        db.commit()
    except Exception as e:
        print(f"Warning persisting save_order to DB: {e}")

    print(f"Order completed: {name}, {mobile}, {email}, {total_amount}, diet: {diet_preference}, user_id: {user_id}, order_id: {order_id}")
    if mobile:
        send_payment_success(mobile, name or "Customer")

    return jsonify({'success': True, 'message': 'Payment successful', 'order_id': order_id})

@app.route('/upi-payment', methods=['POST'])
def upi_payment():
    data = request.get_json()
    order_id = data.get('order_id')
    name = data.get('name')
    mobile = data.get('mobile')
    email = data.get('email')
    order_data = data.get('order_data')
    total_amount = data.get('total_amount')
    payment_method = data.get('payment_method')
    diet_preference = data.get('diet_preference')
    user_id = data.get('user_id')
    whatsapp_mobile = data.get('whatsapp_mobile')

    if not order_id or not total_amount or not whatsapp_mobile:
        return jsonify({'error': 'Missing required fields for UPI'}), 400

    # 1. Save to guest_orders list
    new_order = {
        'id': order_id,
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

    # 2. Persist to DB
    try:
        cursor.execute(
            """
            UPDATE orders
            SET order_status = %s, payment_status = %s
            WHERE id = %s
            """,
            ("PAID", "PAID", order_id),
        )
        db.commit()
    except Exception as e:
        print(f"Warning persisting upi_payment to DB: {e}")

    # 3. Trigger WhatsApp Payment Success Message
    if whatsapp_mobile:
        send_payment_success(whatsapp_mobile, name or "Customer")

    return jsonify({
        'success': True, 
        'message': 'UPI Payment successful.', 
        'order_id': order_id
    })

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

        cursor.execute("SELECT id, name, mobile, email, dob, gender FROM users WHERE mobile=%s", (mobile,))
        user = cursor.fetchone()

        if user:
            return jsonify({'exists': True, 'user': user})
        else:
            return jsonify({'exists': False})

    return render_template('profile.html')

@app.route('/api/user/profile', methods=['GET'])
def get_user_profile_api():
    mobile = request.args.get('mobile')
    if not mobile:
        return jsonify({'error': 'Mobile number is required'}), 400

    cursor.execute(
        "SELECT id, name, email, mobile, dob, gender, health_coins FROM users WHERE mobile=%s",
        (mobile,),
    )
    user = cursor.fetchone()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'user': user})

@app.route('/api/user/stats', methods=['GET'])
def get_user_stats_api():
    mobile = request.args.get('mobile')
    if not mobile:
        return jsonify({'error': 'Mobile number is required'}), 400

    cursor.execute("SELECT id FROM users WHERE mobile=%s", (mobile,))
    user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    user_id = user['id']

    cursor.execute("SELECT COUNT(*) as total FROM orders WHERE user_id=%s AND order_status='DELIVERED'", (user_id,))
    total_orders = cursor.fetchone()['total'] or 0

    if total_orders > 0:
        cursor.execute("""
            SELECT 
                SUM(mi.protein * oi.quantity) as tp,
                SUM(mi.carbs * oi.quantity) as tc,
                SUM(mi.fats * oi.quantity) as tf,
                SUM(mi.calories * oi.quantity) as tcal
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            JOIN menu_items mi ON oi.menu_item_id = mi.id
            WHERE o.user_id=%s AND o.order_status='DELIVERED'
        """, (user_id,))
        macros = cursor.fetchone()

        total_protein = float(macros['tp'] or 0)
        total_carbs = float(macros['tc'] or 0)
        total_fats = float(macros['tf'] or 0)
        total_calories = float(macros['tcal'] or 0)

        avg_protein = total_protein / total_orders
        avg_carbs = total_carbs / total_orders
        avg_fats = total_fats / total_orders
        avg_calories = total_calories / total_orders

        cursor.execute("""
            SELECT mi.diet_type, COUNT(*) as c
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            JOIN menu_items mi ON oi.menu_item_id = mi.id
            WHERE o.user_id=%s AND o.order_status='DELIVERED'
            GROUP BY mi.diet_type
            ORDER BY c DESC
            LIMIT 1
        """, (user_id,))
        pref_row = cursor.fetchone()
        preference = pref_row['diet_type'].capitalize() if (pref_row and pref_row['diet_type']) else 'Mixed'
    else:
        avg_protein = avg_carbs = avg_fats = avg_calories = 0
        total_protein = total_carbs = total_fats = total_calories = 0
        preference = 'Mixed'

    return jsonify({
        'totalOrders': total_orders,
        'avgProtein': round(avg_protein, 1),
        'avgCarbs': round(avg_carbs, 1),
        'avgFats': round(avg_fats, 1),
        'avgCalories': round(avg_calories),
        'totalProtein': round(total_protein, 1),
        'totalCarbs': round(total_carbs, 1),
        'totalFats': round(total_fats, 1),
        'totalCalories': round(total_calories),
        'preference': preference
    })

@app.route('/api/user/recommendations', methods=['GET'])
def get_user_recommendations_api():
    mobile = request.args.get('mobile')
    
    # Just return some active healthy items for now as AI reco
    cursor.execute("""
        SELECT id, name, price, image_url 
        FROM menu_items 
        WHERE is_active = 1 AND category = 'healthy'
        LIMIT 3
    """)
    items = cursor.fetchall()
    
    # Format image paths if needed
    for item in items:
        if item['image_url'] and '/static/images/' not in item['image_url']:
            item['image_url'] = '/static/images/' + item['image_url'].split('/')[-1]
            
    return jsonify({"recommendations": items})

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
    try:
        c = get_cursor()

        # Safe defaults
        total_users = 0
        total_orders = 0
        total_revenue = 0.0
        revenue_list = []
        low_stock_count = 0

        # USERS
        c.execute("SELECT COUNT(*) as total FROM users WHERE role='user'")
        result = c.fetchone()
        total_users = result["total"] if result else 0

        # ORDERS
        c.execute("SELECT COUNT(*) as total FROM orders")
        result = c.fetchone()
        total_orders = result["total"] if result else 0

        # REVENUE - only DELIVERED orders
        c.execute("SELECT SUM(total_amount) as total_revenue FROM orders WHERE order_status='DELIVERED'")
        result = c.fetchone()
        total_revenue = result["total_revenue"] or 0

        # LOW STOCK - safe handling
        try:
            c.execute("SELECT COUNT(*) as total FROM inventory WHERE quantity < 10")
            result = c.fetchone()
            low_stock_count = result["total"] if result else 0
        except Exception as e:
            print(f"Inventory query failed (table/column missing): {e}")
            low_stock_count = 0

        # WEEKLY REVENUE - last 7 days DELIVERED only
        seven_days_ago = datetime.now().date() - timedelta(days=7)
        c.execute("""
            SELECT DATE(created_at) as date, SUM(total_amount) as revenue
            FROM orders
            WHERE order_status='DELIVERED' AND DATE(created_at) >= %s
            GROUP BY DATE(created_at)
            ORDER BY DATE(created_at)
        """, (seven_days_ago,))
        revenue_data = c.fetchall()
        
        # Fill 7 days with data or 0
        date_map = {row['date'].strftime('%Y-%m-%d'): float(row['revenue'] or 0) for row in revenue_data}
        for i in range(7):
            target_date = (datetime.now().date() - timedelta(days=i)).strftime('%Y-%m-%d')
            revenue_list.append({
                'day': target_date,
                'revenue': date_map.get(target_date, 0)
            })
        revenue_list.reverse()
        
        for row in revenue_data:
            row["date"] = str(row["date"])

        # Recent orders (top 5)
        c.execute("""
            SELECT o.id, u.name as customer_name, o.total_amount, o.order_status, o.created_at
            FROM orders o
            JOIN users u ON o.user_id = u.id
            ORDER BY o.created_at DESC
            LIMIT 5
        """)
        recent_orders = c.fetchall()

        # Category sales data
        try:
            c.execute("""
                SELECT mi.category, COUNT(*) as order_count
                FROM order_items oi
                JOIN menu_items mi ON oi.menu_item_id = mi.id
                GROUP BY mi.category
                ORDER BY order_count DESC
            """)
            category_raw = c.fetchall()
            category_data = [{'label': row['category'] or 'Uncategorized', 'value': row['order_count'] or 0} for row in category_raw]
        except Exception as e:
            print("Categories error:", e)
            category_data = []

        # Order status distribution
        c.execute("""
            SELECT order_status, COUNT(*) as count
            FROM orders
            GROUP BY order_status
        """)
        status_raw = c.fetchall()
        total_orders_all = total_orders or 1
        order_status_data = [
            {'label': row['order_status'], 'value': row['count'], 'percentage': round((row['count']/total_orders_all)*100, 1)}
            for row in status_raw
        ]

        c.close()

        return render_template(
            "admin/dashboard.html",
            total_users=total_users,
            total_orders=total_orders,
            total_revenue=total_revenue,
            low_stock_items=low_stock_count,
            recent_orders=recent_orders,
            revenue=revenue_list,
            category_data=category_data,
            order_status_data=order_status_data
        )
    except Exception as e:
        print(f"ERROR in admin_dashboard: {e}")
        try:
            return render_template("500.html"), 500
        except Exception:
            return "<h1>500 - Server Error</h1><p>Something went wrong.</p><a href='/'>Go Home</a>", 500

@app.route("/admin/users")
@admin_required
def admin_users():
    cursor.execute("""
        SELECT id, name, email, role, created_at 
        FROM users 
        WHERE role = 'user'
        ORDER BY id DESC
    """)
    users = cursor.fetchall()

    return render_template('admin/users.html', users=users)

@app.route("/admin/menu")
@admin_required
def admin_menu():
    return render_template("admin/menu.html")


@app.route("/admin/menu-items", methods=["GET", "POST"])
@admin_required
def admin_menu_items():
    """
    Admin-facing API for listing and creating menu items.
    Uses the same underlying `menu_items` table as the user menu.
    """
    if request.method == "GET":
        # Admin sees all items (including inactive)
        cursor.execute("SELECT * FROM menu_items ORDER BY id DESC")
        items = cursor.fetchall()
        return jsonify(items)

    # POST – create a new item
    data = request.get_json() or {}
    name = data.get("name")
    price = data.get("price")
    image_url = data.get("image_url", "")
    category = data.get("category", "all")
    is_active = data.get("is_active", 1)

    if not name or price is None:
        return jsonify({"error": "Name and price are required"}), 400

    try:
        cursor.execute(
            """
            INSERT INTO menu_items (name, price, image_url, category, is_active)
            VALUES (%s,%s,%s,%s,%s)
            """,
            (name, float(price), image_url, category, int(is_active)),
        )
        db.commit()
        new_id = cursor.lastrowid
        
        admin_id = session.get("admin_id", 0)
        cursor.execute("INSERT INTO security_logs (admin_id, action) VALUES (%s, %s)",
                       (admin_id, f"Added menu item: {name} (ID: {new_id})"))
        db.commit()
        
        cursor.execute("SELECT * FROM menu_items WHERE id=%s", (new_id,))
        item = cursor.fetchone()
        return jsonify({"success": True, "item": item})
    except Exception as e:
        print(f"Error creating menu item: {e}")
        db.rollback()
        return jsonify({"error": "Failed to create menu item"}), 500


@app.route("/admin/menu-items/<int:item_id>", methods=["PUT", "DELETE"])
@admin_required
def admin_update_menu_item(item_id):
    """
    Update or delete a menu item.
    """
    if request.method == "DELETE":
        try:
            cursor.execute("DELETE FROM menu_items WHERE id=%s", (item_id,))
            db.commit()
            
            admin_id = session.get("admin_id", 0)
            cursor.execute("INSERT INTO security_logs (admin_id, action) VALUES (%s, %s)",
                           (admin_id, f"Deleted menu item ID: {item_id}"))
            db.commit()
            
            return jsonify({"success": True})
        except Exception as e:
            print(f"Error deleting menu item {item_id}: {e}")
            db.rollback()
            return jsonify({"error": "Failed to delete menu item"}), 500

    # PUT – update fields
    data = request.get_json() or {}
    name = data.get("name")
    price = data.get("price")
    image_url = data.get("image_url")
    category = data.get("category")
    is_active = data.get("is_active")

    fields = []
    values = []
    if name is not None:
        fields.append("name=%s")
        values.append(name)
    if price is not None:
        fields.append("price=%s")
        values.append(float(price))
    if image_url is not None:
        fields.append("image_url=%s")
        values.append(image_url)
    if category is not None:
        fields.append("category=%s")
        values.append(category)
    if is_active is not None:
        fields.append("is_active=%s")
        values.append(int(is_active))

    if not fields:
        return jsonify({"error": "No fields to update"}), 400

    values.append(item_id)

    try:
        cursor.execute(
            f"UPDATE menu_items SET {', '.join(fields)} WHERE id=%s",
            tuple(values),
        )
        db.commit()
        
        admin_id = session.get("admin_id", 0)
        cursor.execute("INSERT INTO security_logs (admin_id, action) VALUES (%s, %s)",
                       (admin_id, f"Updated menu item ID: {item_id}"))
        db.commit()
        
        cursor.execute("SELECT * FROM menu_items WHERE id=%s", (item_id,))
        item = cursor.fetchone()
        return jsonify({"success": True, "item": item})
    except Exception as e:
        print(f"Error updating menu item {item_id}: {e}")
        db.rollback()
        return jsonify({"error": "Failed to update menu item"}), 500


@app.route("/admin/menu-items/<int:item_id>/toggle", methods=["PATCH"])
@admin_required
def admin_toggle_menu_item(item_id):
    """Toggle is_active status"""
    cursor.execute("SELECT is_active FROM menu_items WHERE id=%s", (item_id,))
    item = cursor.fetchone()
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    new_status = 0 if item['is_active'] else 1
    
    cursor.execute(
        "UPDATE menu_items SET is_active=%s WHERE id=%s",
        (new_status, item_id)
    )
    db.commit()
    
    cursor.execute("SELECT * FROM menu_items WHERE id=%s", (item_id,))
    updated_item = cursor.fetchone()
    
    return jsonify({
        "success": True, 
        "item": updated_item,
        "message": f"Item {'deactivated' if new_status == 0 else 'activated'}"
    })

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
    SELECT o.id, u.name, o.total_amount, o.order_status, o.created_at
    FROM orders o
    JOIN users u ON o.user_id = u.id
    ORDER BY o.id DESC
    """)

    orders = cursor.fetchall()
    return render_template("admin/orders.html", orders=orders)




@app.route("/admin/orders/<int:order_id>/action", methods=["POST"])
@admin_required
def admin_order_action(order_id):
    action = request.form.get("action")
    admin_id = session.get("admin_id", 0)

    if action == "delivered":
        new_status = "DELIVERED"
        
        cursor.execute("SELECT order_status, user_id FROM orders WHERE id=%s", (order_id,))
        order_info = cursor.fetchone()
        
        if order_info and order_info['order_status'] != 'DELIVERED':
            cursor.execute(
                "UPDATE orders SET order_status=%s, payment_status='PAID' WHERE id=%s",
                (new_status, order_id),
            )
            
            # Health Coins Logic
            user_id = order_info['user_id']
            if user_id:
                cursor.execute("""
                    SELECT SUM(oi.quantity) as healthy_items
                    FROM order_items oi
                    JOIN menu_items mi ON oi.menu_item_id = mi.id
                    WHERE oi.order_id = %s AND mi.category = 'healthy'
                """, (order_id,))
                res = cursor.fetchone()
                if res and res['healthy_items']:
                    coins_to_add = int(res['healthy_items']) * 10
                    if coins_to_add > 0:
                        cursor.execute("UPDATE users SET health_coins = health_coins + %s WHERE id = %s", (coins_to_add, user_id))
            
            cursor.execute("INSERT INTO security_logs (admin_id, action) VALUES (%s, %s)",
                           (admin_id, f"Updated order {order_id} status to {new_status} via form"))
            db.commit()
    else:
        return jsonify({"error": "Invalid action"}), 400

    return render_template("admin/orders.html")

@app.route('/admin/update-order-status', methods=['POST'])
def update_order_status():
    data = request.get_json()

    order_id = data.get('order_id')
    status = data.get('status')

    if not order_id or not status:
        return jsonify({"error": "order_id and status required"}), 400

    admin_id = session.get("admin_id", 0)

    if status.upper() == 'DELIVERED':
        cursor.execute("SELECT order_status, user_id FROM orders WHERE id=%s", (order_id,))
        order_info = cursor.fetchone()
        
        if order_info and order_info['order_status'] != 'DELIVERED':
            cursor.execute("""
                UPDATE orders 
                SET payment_status='PAID', order_status='DELIVERED'
                WHERE id=%s
            """, (order_id,))
            
            # Health Coins Logic
            user_id = order_info['user_id']
            if user_id:
                cursor.execute("""
                    SELECT SUM(oi.quantity) as healthy_items
                    FROM order_items oi
                    JOIN menu_items mi ON oi.menu_item_id = mi.id
                    WHERE oi.order_id = %s AND mi.category = 'healthy'
                """, (order_id,))
                res = cursor.fetchone()
                if res and res['healthy_items']:
                    coins_to_add = int(res['healthy_items']) * 10
                    if coins_to_add > 0:
                        cursor.execute("UPDATE users SET health_coins = health_coins + %s WHERE id = %s", (coins_to_add, user_id))
            
            cursor.execute("INSERT INTO security_logs (admin_id, action) VALUES (%s, %s)",
                           (admin_id, f"Updated order {order_id} status to DELIVERED"))
    else:
        return jsonify({"error": "Invalid status. Use 'delivered'"}), 400

    db.commit()

    return jsonify({"success": True})


@app.route("/admin/security-logs")
@admin_required
def admin_logs():
    # Fetch recent security events
    cursor.execute(
        """
        SELECT sl.id,
               sl.timestamp as login_time,
               sl.action,
               u.email AS user_email
        FROM security_logs sl
        LEFT JOIN users u ON u.id = sl.admin_id
        ORDER BY sl.timestamp DESC
        LIMIT 200
        """
    )
    logs = cursor.fetchall()
    return render_template("admin/security_logs.html", logs=logs)

@app.route("/admin/settings", methods=["GET", "POST"])
@admin_required
def admin_settings():
    if request.method == "GET":
        cursor.execute("SELECT setting_value FROM system_settings WHERE setting_key='meal_mode'")
        result = cursor.fetchone()
        meal_mode = result['setting_value'] if result else 'all'
        
        # Serve JSON if requested via API (like fetch), else serve the page
        if 'application/json' in request.headers.get('Accept', '') or request.headers.get('Content-Type') == 'application/json':
            return jsonify({"meal_mode": meal_mode})
            
        return render_template("admin/settings.html", meal_mode=meal_mode)
    
    if request.method == "POST":
        data = request.get_json() or {}
        meal_mode = data.get("meal_mode")
        if not meal_mode or meal_mode not in ['all', 'breakfast', 'lunch', 'dinner']:
            return jsonify({"error": "Valid meal_mode required"}), 400
        
        cursor.execute("""
            INSERT INTO system_settings (setting_key, setting_value) 
            VALUES ('meal_mode', %s) 
            ON DUPLICATE KEY UPDATE setting_value=%s
        """, (meal_mode, meal_mode))
        db.commit()
        
        admin_id = session.get("admin_id", 0)
        cursor.execute("INSERT INTO security_logs (admin_id, action) VALUES (%s, %s)",
                       (admin_id, f"Changed meal mode to: {meal_mode}"))
        db.commit()
        
        return jsonify({"success": True, "meal_mode": meal_mode})

@app.route("/admin")
def admin_index():
    if "admin_id" in session:
        from flask import redirect
        return redirect("/admin/dashboard")
    return render_template("admin/login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_id", None)
    return render_template("admin/login.html")

@app.route('/admin/category-data')
def admin_category_data():
    """API endpoint for Best Selling Categories chart"""
    try:
        c = get_cursor()
        c.execute("""
            SELECT mi.category, COUNT(*) as order_count
            FROM order_items oi
            JOIN menu_items mi ON oi.menu_item_id = mi.id
            GROUP BY mi.category
            ORDER BY order_count DESC
        """)
        rows = c.fetchall()
        c.close()
        data = [{"category": row["category"] or "Uncategorized", "count": row["order_count"]} for row in rows]
        return jsonify(data)
    except Exception as e:
        print(f"Category data error: {e}")
        return jsonify([]), 500

@app.route('/admin/recent-orders')
def recent_orders():
    try:
        c = get_cursor()
        c.execute("""
            SELECT o.id, u.name AS customer, o.total_amount AS total, o.order_status AS status
            FROM orders o
            JOIN users u ON o.user_id = u.id
            ORDER BY o.created_at DESC
            LIMIT 5
        """)
        orders = c.fetchall()
        c.close()
        return jsonify(orders)
    except Exception as e:
        print(f"Recent orders error: {e}")
        return jsonify([]), 500

@app.route('/admin/order-distribution')
def order_distribution():
    try:
        c = get_cursor()
        c.execute("""
            SELECT order_status as status, COUNT(*) as count
            FROM orders
            GROUP BY order_status
        """)
        data = c.fetchall()
        c.close()
        return jsonify(data)
    except Exception as e:
        print(f"Order distribution error: {e}")
        return jsonify([]), 500

@app.route('/admin/revenue-data')
def admin_revenue_data():
    """API endpoint for dashboard revenue chart - last 7 days with 0-filled dates"""
    try:
        c = get_cursor()
        seven_days_ago = datetime.now().date() - timedelta(days=7)
        c.execute("""
            SELECT DATE(created_at) as date, SUM(total_amount) as revenue
            FROM orders
            WHERE order_status='DELIVERED' AND DATE(created_at) >= %s
            GROUP BY DATE(created_at)
            ORDER BY DATE(created_at)
        """, (seven_days_ago,))
        revenue_data = c.fetchall()
        c.close()
        
        # Fill missing dates with 0
        date_map = {row['date'].strftime('%Y-%m-%d'): float(row['revenue'] or 0) for row in revenue_data}
        result = []
        today = datetime.now().date()
        for i in range(6, -1, -1):  # Last 7 days
            d = today - timedelta(days=i)
            key = d.strftime('%Y-%m-%d')
            result.append({
                'date': key,
                'revenue': date_map.get(key, 0)
            })
        return jsonify(result)
    except Exception as e:
        print(f"Revenue data error: {e}")
        return jsonify([]), 500

@app.route('/admin/settings', methods=['GET', 'POST'])
def admin_settings_page():
    c = get_cursor()
    if request.method == 'GET':
        if request.headers.get('Accept') == 'application/json' or request.is_json or request.content_type == 'application/json':
            c.execute("SELECT setting_value FROM system_settings WHERE setting_key='meal_mode'")
            result = c.fetchone()
            meal_mode = result['setting_value'] if result else 'all'
            c.close()
            return jsonify({'success': True, 'meal_mode': meal_mode})
        c.close()
        return render_template('admin/settings.html')
        
    if request.method == 'POST':
        data = request.get_json()
        meal_mode = data.get('meal_mode', 'all')
        
        c.execute("""
            INSERT INTO system_settings (setting_key, setting_value) 
            VALUES ('meal_mode', %s) 
            ON DUPLICATE KEY UPDATE setting_value=%s
        """, (meal_mode, meal_mode))
        db.commit()
        c.close()
        return jsonify({'success': True, 'meal_mode': meal_mode})

@app.route('/admin/inventory', methods=['GET'])
def admin_inventory_page():
    return render_template('admin/inventory.html')

@app.route('/admin/inventory-data', methods=['GET'])
def fetch_admin_inventory_data():
    try:
        c = get_cursor()
        c.execute("SELECT * FROM inventory ORDER BY id DESC")
        items = c.fetchall()
        c.close()
        return jsonify(items)
    except Exception as e:
        print(f"Inventory data error: {e}")
        return jsonify([]), 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(e):
    try:
        return render_template("500.html"), 500
    except Exception:
        return "<h1>500 - Server Error</h1><p>Something went wrong.</p><a href='/'>Go Home</a>", 500

@app.errorhandler(Exception)
def handle_exception(e):
    print(f"Unhandled exception: {e}")
    try:
        return render_template("500.html"), 500
    except Exception:
        return "<h1>500 - Server Error</h1><p>Something went wrong.</p><a href='/'>Go Home</a>", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)