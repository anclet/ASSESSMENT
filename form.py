import streamlit as st
import requests

# Function to display the form
def main():
    st.title("RICA - Import Permit Application")
    
    # Business Owner Details Section
    st.header("Business Owner Details")
    col1, col2 = st.columns(2)
    
    with col1:
        citizenship = st.selectbox("Applicant Citizenship *", ["Rwandan", "Foreigner"], index=0)
    
    with col2:
        # Conditional fields for ID/Passport based on citizenship
        if citizenship == "Rwandan":
            nid = st.text_input("Identification Document Number *", help="Must be 16 digits")
            passport = None
        else:
            passport = st.text_input("Passport Number *")
            nid = None
    
    # General details in columns
    with col1:
        other_names = st.text_input("Other Names *")
        surname = st.text_input("Surname *")
        nationality = st.text_input("Nationality *")
        phone = st.text_input("Phone Number")
    
    with col2:
        email = st.text_input("Email Address")
        business_owner_address = st.text_input("Business Owner Address *")

    # Business Details Section
    st.header("Business Details")
    col1, col2 = st.columns(2)
    
    with col1:
        business_type = st.selectbox("Business Type *", ["Retailer", "Wholesale", "Manufacturer"], index=0)
        company_name = st.text_input("Company Name *")
        tin_number = st.text_input("TIN Number *", help="Must be 9 digits")
    
    with col2:
        registration_date = st.date_input("Registration Date *")
        business_address = st.text_input("Business Address *")
    
    # Product Information Section
    st.header("Product Information")
    col1, col2 = st.columns(2)
    
    with col1:
        purpose_of_importation = st.selectbox("Purpose of Importation *", ["Direct sale", "Personal use", "Trial use", "Other"], index=0)
    
    with col2:
        # Additional input for "Other" in purpose of importation
        specify_purpose = ""
        if purpose_of_importation == "Other":
            specify_purpose = st.text_input("Specify Purpose of Importation *")
    
    col1, col2 = st.columns(2)
    
    with col1:
        product_category = st.selectbox("Product Category *", ["General purpose", "Construction materials", "Chemicals"], index=0)
        product_name = st.text_input("Product Name *")
        weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
    
    with col2:
        unit_of_measurement = st.selectbox("Unit of Measurement *", ["Kgs", "Tonnes"], index=0)
        quantity = st.number_input("Quantity of Product(s) *", min_value=1, step=1)
        description = st.text_area("Description of Products *")

    # Prepare the required fields dictionary with all form inputs
    required_fields = {
        "citizenship": citizenship,
        "nid or passport": nid if citizenship == "Rwandan" else passport,
        "other_names": other_names,
        "surname": surname,
        "nationality": nationality,
        "business_owner_address": business_owner_address,
        "business_type": business_type,
        "company_name": company_name,
        "tin_number": tin_number,
        "registration_date": registration_date,
        "business_address": business_address,
        "purpose_of_importation": purpose_of_importation,
        "specify_purpose": specify_purpose if purpose_of_importation == "Other" else None,  # Set to None if not required
        "product_category": product_category,
        "product_name": product_name,
        "unit_of_measurement": unit_of_measurement,
        "quantity": quantity,
        "description": description,

    }
    
    # Check if all required fields are filled
    form_valid = all(value is not None and value != "" for field, value in required_fields.items() if field != "specify_purpose" or purpose_of_importation == "Other")
    
    # Form Submission Button
    if st.button("Submit Application"):
        if form_valid:
            # Prepare the data for submission
            data = {
                "citizenship": citizenship,
                "identification_number": nid if citizenship == "Rwandan" else None,
                "passport_number": passport if citizenship != "Rwandan" else None,
                "other_names": other_names,
                "surname": surname,
                "nationality": nationality,
                "phone_number": phone,
                "email": email,
                "business_type": business_type,
                "company_name": company_name,
                "tin_number": tin_number,
                "registration_date": str(registration_date),
                "purpose_of_importation": purpose_of_importation,
                "product_category": product_category,
                "product_name": product_name,
                "weight_kg": weight,
                "unit_of_measurement": unit_of_measurement,
                "quantity": quantity,
                "description": description 
            }

            try:
                # Send the data to the Flask backend using a POST request
                response = requests.post('http://127.0.0.1:5000/submit', json=data)

                if response.status_code == 200:
                    st.success("Your application has been submitted successfully!")
                    st.balloons()  # Add a celebratory animation
                else:
                    st.error(f"Error: {response.json().get('error', 'An unknown error occurred')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the server: {e}")
        else:
            st.error("Please fill in all required fields marked with an asterisk (*) before submitting.")
            st.write("Failed fields:")
            for field, value in required_fields.items():
                if not value and (field != "specify_purpose" or purpose_of_importation == "Other"):
                    st.write(f"Missing: {field}")

if __name__ == "__main__":
    main()
