import re

import mysql.connector
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)


# Database connection function
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",  # XAMPP MySQL host
        user="root",  # Default MySQL user
        password="",  # Default MySQL password (empty)
        database="payment_web_service"  # Your database name
    )
    return connection


class Payment:
    def __init__(self, paymentID, transactionID, paymentDateTime, paymentMethod, paymentAmount):
        self.paymentID = paymentID
        self.transactionID = transactionID
        self.paymentDateTime = paymentDateTime
        self.paymentMethod = paymentMethod
        self.paymentAmount = paymentAmount

    def to_dict(self):
        return {
            'paymentID': self.paymentID,
            'transactionID': self.transactionID,
            'paymentDateTime': self.paymentDateTime,
            'paymentMethod': self.paymentMethod,
            'paymentAmount': self.paymentAmount,
        }


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

        if payment_method == 'Card Payment':
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

        elif payment_method == 'FPX':
            card_holder_name = payment_details.get('cardHolderName')
            password = payment_details.get('fpxpassword')

            # Validate FPX payment details (basic example)
            if not card_holder_name or not password:
                return jsonify([{"error": "Missing FPX payment details"}]), 400

        elif payment_method == 'TNG E-Wallet':
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
            'paymentMethod': payment_method,
            'paymentAmount': request.json.get('totalPayment')
        }

        insert_query = """
            INSERT INTO payment (paymentID, transactionID, paymentDateTime, paymentMethod, paymentAmount)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            payment_data['paymentID'],
            payment_data['transactionID'],
            payment_data['paymentDateTime'],
            payment_data['paymentMethod'],
            payment_data['paymentAmount']
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
            'paymentMethod': payment_data['paymentMethod'],
            'paymentAmount': payment_data['paymentAmount']
        })

        print("Response JSON:", response_data)  # Log the response for debugging

        return jsonify(response_data)
    except Exception as e:
        print("Error:", e)
        return jsonify([{"error": "Internal server error"}]), 500


@app.route('/api/get-payments', methods=['GET'])
def get_payments():
    # Retrieve optional query parameters with defaults
    transactionID = request.args.get('transactionID', default=None)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if (transactionID == None):
        cursor.execute("SELECT * FROM payment")
    if (transactionID != None):
        cursor.execute("SELECT * FROM payment WHERE transactionID = %s", (transactionID,))

    payments_data = cursor.fetchall()
    cursor.close()
    conn.close()
    print(payments_data)
    # Create an array of Payment objects
    payments = []
    for payment in payments_data:
        # Instantiate a Payment object with data from the database
        payment_obj = Payment(
            paymentID=payment['paymentID'],
            transactionID=payment['transactionID'],
            paymentDateTime=payment['paymentDateTime'],
            paymentMethod=payment['paymentMethod'],
            paymentAmount=payment['paymentAmount'],
        )
        payments.append(payment_obj.to_dict())

    return jsonify(payments)


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
