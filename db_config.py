"""
MySQL Database Configuration for Healthy Cafe Management System
Uses mysql-connector-python for database connections
"""

import mysql.connector
from mysql.connector import Error
import bcrypt

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_mysql_password',  # Change this to your MySQL password
    'database': 'usertemp'
}

def get_db_connection():
    """
    Create and return a database connection
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def init_db():
    """
    Initialize database connection and return connection object
    """
    return get_db_connection()

# =============================================
# User Operations
# =============================================

def create_user(name, email, password, mobile=None, dob=None, gender=None):
    """
    Create a new user with bcrypt hashed password
    """
    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO users (name, email, password, mobile, dob, gender)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (name, email, hashed_password.decode('utf-8'), mobile, dob, gender)
            cursor.execute(query, values)
            connection.commit()
            user_id = cursor.lastrowid
            cursor.close()
            connection.close()
            return user_id
        except Error as e:
            print(f"Error creating user: {e}")
            connection.close()
            return None
    return None

def get_user_by_email(email):
    """
    Get user by email address
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            return user
        except Error as e:
            print(f"Error getting user: {e}")
            connection.close()
            return None
    return None

def get_user_by_id(user_id):
    """
    Get user by ID
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            return user
        except Error as e:
            print(f"Error getting user: {e}")
            connection.close()
            return None
    return None

def get_user_by_mobile(mobile):
    """
    Get user by mobile number
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE mobile = %s"
            cursor.execute(query, (mobile,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            return user
        except Error as e:
            print(f"Error getting user: {e}")
            connection.close()
            return None
    return None

def verify_password(password, hashed_password):
    """
    Verify password using bcrypt
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def update_user_profile(user_id, name=None, dob=None, gender=None):
    """
    Update user profile
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Build dynamic update query
            updates = []
            values = []
            if name:
                updates.append("name = %s")
                values.append(name)
            if dob:
                updates.append("dob = %s")
                values.append(dob)
            if gender:
                updates.append("gender = %s")
                values.append(gender)
            
            if updates:
                query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
                values.append(user_id)
                cursor.execute(query, values)
                connection.commit()
            
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Error updating user: {e}")
            connection.close()
            return False
    return False

# =============================================
# OTP Operations
# =============================================

def create_otp(user_id, otp_code, expiry_minutes=5):
    """
    Create a new OTP for user
    """
    from datetime import datetime, timedelta
    
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            expiry_time = datetime.now() + timedelta(minutes=expiry_minutes)
            
            query = """
                INSERT INTO otp (user_id, otp_code, expiry_time)
                VALUES (%s, %s, %s)
            """
            values = (user_id, otp_code, expiry_time)
            cursor.execute(query, values)
            connection.commit()
            otp_id = cursor.lastrowid
            cursor.close()
            connection.close()
            return otp_id
        except Error as e:
            print(f"Error creating OTP: {e}")
            connection.close()
            return None
    return None

def get_valid_otp(user_id, otp_code):
    """
    Get valid (not expired, not used) OTP for user
    """
    from datetime import datetime
    
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT * FROM otp 
                WHERE user_id = %s AND otp_code = %s 
                AND expiry_time > %s AND is_used = FALSE
                ORDER BY created_at DESC LIMIT 1
            """
            cursor.execute(query, (user_id, otp_code, datetime.now()))
            otp = cursor.fetchone()
            cursor.close()
            connection.close()
            return otp
        except Error as e:
            print(f"Error getting OTP: {e}")
            connection.close()
            return None
    return None

def mark_otp_used(otp_id):
    """
    Mark OTP as used
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "UPDATE otp SET is_used = TRUE WHERE id = %s"
            cursor.execute(query, (otp_id,))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Error marking OTP as used: {e}")
            connection.close()
            return False
    return False

def increment_otp_attempts(otp_id):
    """
    Increment OTP attempt count
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "UPDATE otp SET attempts = attempts + 1 WHERE id = %s"
            cursor.execute(query, (otp_id,))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Error incrementing OTP attempts: {e}")
            connection.close()
            return False
    return False

def delete_expired_otps():
    """
    Delete expired OTPs
    """
    from datetime import datetime
    
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM otp WHERE expiry_time < %s"
            cursor.execute(query, (datetime.now(),))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Error deleting expired OTPs: {e}")
            connection.close()
            return False
    return False

# =============================================
# Login History Operations
# =============================================

def add_login_history(user_id, ip_address=None, device_info=None):
    """
    Add login history entry
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO login_history (user_id, ip_address, device_info)
                VALUES (%s, %s, %s)
            """
            values = (user_id, ip_address, device_info)
            cursor.execute(query, values)
            connection.commit()
            history_id = cursor.lastrowid
            cursor.close()
            connection.close()
            return history_id
        except Error as e:
            print(f"Error adding login history: {e}")
            connection.close()
            return None
    return None

def get_login_history(user_id, limit=10):
    """
    Get login history for user
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT * FROM login_history 
                WHERE user_id = %s 
                ORDER BY login_time DESC 
                LIMIT %s
            """
            cursor.execute(query, (user_id, limit))
            history = cursor.fetchall()
            cursor.close()
            connection.close()
            return history
        except Error as e:
            print(f"Error getting login history: {e}")
            connection.close()
            return None
    return None

def get_login_count(user_id):
    """
    Get total login count for user
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT COUNT(*) FROM login_history WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            count = cursor.fetchone()[0]
            cursor.close()
            connection.close()
            return count
        except Error as e:
            print(f"Error getting login count: {e}")
            connection.close()
            return 0
    return 0
