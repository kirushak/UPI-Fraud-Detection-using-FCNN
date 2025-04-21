import streamlit as st
import tensorflow as tf
import numpy as np
import hashlib
from PIL import Image

# Load the trained model
model = tf.keras.models.load_model('E:/S5 Mini Project 1/Application/upi_fraud_fcnn.keras')

# Function to hash UPI IDs
def hash_upi(upi_id):
    return int(hashlib.sha256(upi_id.encode('utf-8')).hexdigest(), 16) % 10**8

# Define a function to use the model for predictions
def predict_fraud(sender_upi, receiver_upi, transaction_type, amount):
    # Hash the UPI IDs to get numerical values
    sender_upi_hashed = hash_upi(sender_upi)
    receiver_upi_hashed = hash_upi(receiver_upi)
    
    # Convert transaction type to numerical value
    transaction_type = 1 if transaction_type == "Debit" else 0
    
    # Placeholder for additional features
    # Assuming the model expects `transaction_time` and `transaction_location`
    transaction_time = 120  # Example: 120 seconds from the start of the day
    transaction_location = 1  # Example: 1 as an encoded location (e.g., in the same country)

    # Create a sample input in the expected format for your model (with 6 features)
    input_data = np.array([[sender_upi_hashed, receiver_upi_hashed, transaction_type, amount, transaction_time, transaction_location]])
    
    # Make prediction
    prediction = model.predict(input_data)
    
    # Return the prediction result
    return "Fraud" if prediction >= 0.5 else "Not Fraud"

# Apply custom CSS for background and UI enhancement
def apply_custom_css():
    st.markdown("""
        <style>
            body {
                background: lightskyblue;
                background-size: 400% 400%;
                animation: gradient 15s ease infinite;
                font-family: 'Arial', sans-serif;
            }
            @keyframes gradient {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            .main {
                background-color: burlywood;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                transition: transform 0.2s;
            }
            .main:hover {
                transform: scale(1.02);
            }
            h1, h2, h3, h4, h5, h6 {
                color: #333;
                text-align: center;
            }
            .stButton>button {
                background-color: #ff5a5f;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 18px;
                border-radius: 20px;
                cursor: pointer;
                transition: background-color 0.3s, transform 0.2s;
            }
            .stButton>button:hover {
                background-color: #ff7e82;
                transform: translateY(-2px);
            }
            .stTextInput>div>input {
                border-radius: 10px;
                border: 1px solid #ccc;
                padding: 10px;
                font-size: 16px;
                transition: border-color 0.3s;
            }
            .stTextInput>div>input:focus {
                border-color: #ff5a5f;
                box-shadow: 0 0 5px rgba(255, 90, 95, 0.5);
            }
            .stSelectbox>div>select {
                border-radius: 10px;
                border: 1px solid #ccc;
                padding: 10px;
                font-size: 16px;
            }
            .stNumberInput>div>input {
                border-radius: 10px;
                border: 1px solid #ccc;
                padding: 10px;
                font-size: 16px;
            }
            .stNumberInput>div>input:focus {
                border-color: #ff5a5f;
                box-shadow: 0 0 5px rgba(255, 90, 95, 0.5);
            }
            .stForm {
                margin-top: 20px;
            }
            .stError {
                background-color: #ffdddd;
                color: #d8000c;
                border: 1px solid #d8000c;
                padding: 10px;
                border-radius: 10px;
            }
            .stSuccess {
                background-color: #ddffdd;
                color: #4caf50;
                border: 1px solid #4caf50;
                padding: 10px;
                border-radius: 10px;
            }
        </style>
        """, unsafe_allow_html=True)

# Load and display a banner image for the app
banner_image = Image.open("upi_fraud_banner.png")

# Streamlit App UI
apply_custom_css()
st.image(banner_image, use_column_width=True)

st.title("💳 UPI Fraud Detection System")
st.subheader("🔍 Detect potential fraudulent transactions in real-time")

# Section for entering transaction details
st.write("Please enter the transaction details below to detect fraud.")

with st.form(key="fraud_detection_form"):
    sender_upi = st.text_input("Sender UPI ID", placeholder="Enter Sender UPI ID (e.g., sender@bank)")
    receiver_upi = st.text_input("Receiver UPI ID", placeholder="Enter Receiver UPI ID (e.g., receiver@bank)")
    transaction_type = st.selectbox("Transaction Type", ["Debit", "Credit"])
    amount = st.number_input("Transaction Amount", min_value=0.01, step=0.01, format="%.2f")
    
    # Submit button to trigger prediction
    submit_button = st.form_submit_button(label="🔍 Detect Fraud")

# Perform the fraud detection when the form is submitted
if submit_button:
    # Validate inputs
    if not sender_upi or not receiver_upi:
        st.error("Please enter both Sender and Receiver UPI IDs.")
    else:
        # Call the predict function
        result = predict_fraud(sender_upi, receiver_upi, transaction_type, amount)
        
        # Display the result with appropriate styling
        if result == "Fraud":
            st.error(f"🚨 Warning: This transaction is flagged as **{result}**!")
        else:
            st.success(f"✅ This transaction is **{result}**.")
