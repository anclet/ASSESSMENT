from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///applications.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Email configuration (adjust to your mail provider)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  #for Gmail account
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

# Define the Application model
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    citizenship = db.Column(db.String(50), nullable=False)
    identification_number = db.Column(db.String(50))
    passport_number = db.Column(db.String(50))
    other_names = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    nationality = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(100))
    business_type = db.Column(db.String(50), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    tin_number = db.Column(db.String(20), nullable=False)
    registration_date = db.Column(db.String(20), nullable=False)
    purpose_of_importation = db.Column(db.String(100), nullable=False)
    product_category = db.Column(db.String(100), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    weight_kg = db.Column(db.Float)
    description = db.Column(db.Text, nullable=False)
    unit_of_measurement = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Route for the root URL
@app.route('/')
def index():
    return "Welcome to the RICA Import Permit Application API!"

# Function to send email
def send_email(application_data):
    msg = Message("RICA Import Permit Application Received", recipients=["ukurikiyeyezuanaclet201@gmail.com"])
    msg.body = f"""
    A new application has been submitted:

    Citizenship: {application_data['citizenship']}
    Other Names: {application_data['other_names']}
    Surname: {application_data['surname']}
    Nationality: {application_data['nationality']}
    Phone Number: {application_data['phone_number']}
    Email: {application_data['email']}
    Business Type: {application_data['business_type']}
    Company Name: {application_data['company_name']}
    TIN Number: {application_data['tin_number']}
    Registration Date: {application_data['registration_date']}
    Purpose of Importation: {application_data['purpose_of_importation']}
    Product Category: {application_data['product_category']}
    Product Name: {application_data['product_name']}
    Weight (kg): {application_data['weight_kg']}
    Description: {application_data['description']}
    Unit of Measurement: {application_data['unit_of_measurement']}
    Quantity: {application_data['quantity']}
    """
    try:
        mail.send(msg)
    except Exception as e:
        print(f"Error sending email: {str(e)}")

# Route to handle form submissions
@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        data = request.json

        # Validate required fields
        required_fields = [
            'citizenship', 'other_names', 'surname', 'nationality',
            'business_type', 'company_name', 'tin_number', 'registration_date',
            'purpose_of_importation', 'product_category', 'product_name',
            'description', 'unit_of_measurement', 'quantity'
        ]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"{field} is required"}), 400

        # Create a new application record
        application = Application(
            citizenship=data['citizenship'],
            identification_number=data.get('identification_number'),
            passport_number=data.get('passport_number'),
            other_names=data['other_names'],
            surname=data['surname'],
            nationality=data['nationality'],
            phone_number=data.get('phone_number'),
            email=data.get('email'),
            business_type=data['business_type'],
            company_name=data['company_name'],
            tin_number=data['tin_number'],
            registration_date=data['registration_date'],
            purpose_of_importation=data['purpose_of_importation'],
            product_category=data['product_category'],
            product_name=data['product_name'],
            weight_kg=data.get('weight_kg'),
            description=data['description'],
            unit_of_measurement=data['unit_of_measurement'],
            quantity=data['quantity']
        )

        # Add and commit the record to the database
        db.session.add(application)
        db.session.commit()

        # Send email
        send_email(data)

        return jsonify({"message": "Form submitted successfully!"}), 200

    except Exception as e:
        # Handle any errors
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
