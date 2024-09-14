import re

import mysql.connector
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Database connection function
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",      # XAMPP MySQL host
        user="root",           # Default MySQL user
        password="",           # Default MySQL password (empty)
        database="payment_web_service"    # Your database name
    )
    return connection

# Testing
class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
        self.test = {'test1','test2'}

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'tests': [test for test in self.test],
            'class': {'attr1':'test','attr2':'test','attr3':'test',}

        }

class Payment:
    def __init__(self, paymentID, transactionID, paymentDateTime, paymentMethod):
        self.paymentID = paymentID
        self.transactionID = transactionID
        self.paymentDateTime = paymentDateTime
        self.paymentMethod = paymentMethod


@app.route('/api/validate-payment', methods=['POST'])
def validate_payment():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Log incoming request data
        print("Request JSON:", request.json)

        # Get the payment method and payment details from the request
        payment_method = request.json.get('paymentMethod')
        payment_details = request.json.get('paymentDetails', {})

        # Initialize response data
        response_data = []

        if payment_method == 'cardPayment':
            card_number = payment_details.get('cardNumber')
            cvv = payment_details.get('cvv')
            expiry_date = payment_details.get('expiryDate')

            # Validate card number (simple check for 16 digits)
            if not re.match(r'^\d{16}$', card_number):
                return jsonify([{"error": "Invalid card number"}]), 400

            # Validate CVV (simple check for 3 digits)
            if not re.match(r'^\d{3}$', cvv):
                return jsonify([{"error": "Invalid CVV"}]), 400

            # Validate expiry date (must be in the future)
            try:
                expiry = datetime.strptime(expiry_date, "%Y-%m")
                if expiry < datetime.now():
                    return jsonify([{"error": "Card has expired"}]), 400
            except ValueError:
                return jsonify([{"error": "Invalid expiry date format"}]), 400

        elif payment_method == 'fpx':
            card_holder_name = payment_details.get('cardHolderName')
            password = payment_details.get('fpxpassword')

            # Validate FPX payment details (basic example)
            if not card_holder_name or not password:
                return jsonify([{"error": "Missing FPX payment details"}]), 400

        elif payment_method == 'tng':
            name = payment_details.get('name')
            password = payment_details.get('tngpassword')

            # Validate TNG E-Wallet payment details (basic example)
            if not name or not password:
                return jsonify([{"error": "Missing TNG E-Wallet details"}]), 400

        else:
            return jsonify([{"error": "Invalid payment method"}]), 400

        # Generate new payment ID
        todayDate = datetime.now().strftime('%y%m%d')
        cursor.execute("SELECT MAX(paymentID) FROM payment WHERE paymentID LIKE %s", (f'PYM-TST-{todayDate}-%',))
        result = cursor.fetchone()
        last_payment_id = result[0] if result[0] else ''

        if last_payment_id:
            last_number = int(last_payment_id[-5:])
            new_number = str(last_number + 1).zfill(5)
        else:
            new_number = '00001'

        payment_id = f'PYM-TST-{todayDate}-{new_number}'

        # Insert the new record into the payment table
        payment_data = {
            'paymentID': payment_id,
            'transactionID': request.json.get('transactionId'),
            'paymentDateTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'paymentMethod': payment_method
        }

        insert_query = """
            INSERT INTO payment (paymentID, transactionID, paymentDateTime, paymentMethod)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            payment_data['paymentID'],
            payment_data['transactionID'],
            payment_data['paymentDateTime'],
            payment_data['paymentMethod']
        ))
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()

        # Format response data as a list of dictionaries
        response_data.append({
            'paymentID': payment_data['paymentID'],
            'transactionID': payment_data['transactionID'],
            'paymentDateTime': payment_data['paymentDateTime'],
            'paymentMethod': payment_data['paymentMethod']
        })

        print("Response JSON:", response_data)  # Log the response for debugging

        return jsonify(response_data)
    except Exception as e:
        print("Error:", e)
        return jsonify([{"error": "Internal server error"}]), 500




@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tests")
    users_data = cursor.fetchall()
    cursor.close()
    conn.close()
    print(users_data)
    # Create an array of User objects
    users = []
    for user in users_data:
        # Instantiate a User object with data from the database
        user_obj = User(
            id=user['id'],
            name=user['name'],
            email=user['email']
        )
        users.append(user_obj.to_dict())

    return jsonify(users)

@app.route('/api/user', methods=['POST'])
def add_user():
    conn = get_db_connection()
    cursor = conn.cursor()
    new_user = request.json

    name = new_user['name']
    email = new_user['email']

    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"message": "User added successfully!"}), 201


# Define a route for the service
@app.route('/api', methods=['GET'])
def api():
    # Example data to return
    data = {
        "message": "Hello, World!",
        "status": "success"
    }
    return jsonify(data)

# Define another route with parameters
@app.route('/api/greet/<name>', methods=['GET'])
def greet(name):
    return jsonify({"message": f"Hello, {name}!"})

# Run the service
if __name__ == '__main__':
    app.run(port=5002, debug=True)