import streamlit as st
import sqlite3
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random
from datetime import datetime, timedelta
import tempfile
from fpdf import FPDF
import base64
import pywhatkit as kit
import hashlib

# os.makedirs("user_bills", exist_ok=True)

# Set page configuration
st.set_page_config(
    page_title="Bizzence - Shopping & Billing System",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling with animations and hover effects
st.markdown("""
<style>
    /* Make buttons smaller */
    .stButton>button {
        padding: 0.25rem 0.5rem;
        font-size: 0.8rem;
        height: auto;
        width: auto;
    }
    
    /* Make select boxes smaller */
    .stSelectbox>div>div>div>input {
        padding: 0.25rem 0.5rem;
        font-size: 0.8rem;
    }
    
    /* Make date inputs smaller */
    .stDateInput>div>div>input {
        padding: 0.25rem 0.5rem;
        font-size: 0.8rem;
    }
    
    /* Make text inputs smaller */
    .stTextInput>div>div>input {
        padding: 0.25rem 0.5rem;
        font-size: 0.8rem;
    }
    
    /* Make tabs smaller */
    .stTabs [data-baseweb="tab-list"] button {
        padding: 0.25rem 0.5rem;
        font-size: 0.8rem;
    }
    
    /* Make dataframes more compact */
    .stDataFrame {
        font-size: 0.8rem;
    }
    
    /* Reduce padding in containers */
    .stContainer {
        padding: 0.5rem;
    }


    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
        transition: all 0.3s ease;
    }
    
    .main-header {
        font-family: 'Poppins', sans-serif;
        text-align: center;
        color: #4CAF50;
        margin-bottom: 0;
        font-size: 2.5rem;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
        animation: fadeIn 0.8s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .subheader {
        font-size: 1.2rem;
        text-align: center;
        font-style: italic;
        color: #5D6D7E;
        margin-bottom: 1.5rem;
        animation: fadeIn 0.8s ease-in-out 0.2s both;
    }
    
    .datetime-display {
        text-align: right;
        font-size: 0.9rem;
        color: #5D6D7E;
        margin-bottom: 1rem;
        background: rgba(255,255,255,0.8);
        padding: 8px 12px;
        border-radius: 20px;
        display: inline-block;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    .section-header {
        background: linear-gradient(135deg, #4285F4, #34A853);
        color: white;
        padding: 12px 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        font-weight: 600;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border-left: 5px solid #FBBC05;
    }
    
    .section-header:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    div[data-testid="stForm"] {
        border: 1px solid #E5E8E8;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        margin-bottom: 20px;
        background: white;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stForm"]:hover {
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }
    
    div.stButton > button {
        width: 100%;
        font-weight: 600;
        height: 3em;
        background: linear-gradient(135deg, #4CAF50, #2E7D32);
        color: white;
        border: none;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover {
        background: linear-gradient(135deg, #388E3C, #1B5E20);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    .bill-item {
        background-color: #F5F5F5;
        padding: 12px 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        border-left: 4px solid #4CAF50;
        transition: all 0.3s ease;
    }
    
    .bill-item:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        background-color: #E8F5E9;
    }
    
    .bill-total {
        background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
        padding: 15px;
        border-radius: 8px;
        margin-top: 20px;
        border-left: 4px solid #2E7D32;
        font-weight: bold;
        font-size: 1.1rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(46, 125, 50, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(46, 125, 50, 0); }
        100% { box-shadow: 0 0 0 0 rgba(46, 125, 50, 0); }
    }
    
    .success-message {
        padding: 12px;
        background: linear-gradient(135deg, #D4EFDF, #A9DFBF);
        border-left: 5px solid #2ECC71;
        margin: 10px 0;
        border-radius: 5px;
        animation: slideIn 0.5s ease-out;
    }
    
    .error-message {
        padding: 12px;
        background: linear-gradient(135deg, #FADBD8, #F5B7B1);
        border-left: 5px solid #E74C3C;
        margin: 10px 0;
        border-radius: 5px;
        animation: shake 0.5s ease-in-out;
    }
    
    .info-message {
        padding: 12px;
        background: linear-gradient(135deg, #EBF5FB, #D6EAF8);
        border-left: 5px solid #3498DB;
        margin: 10px 0;
        border-radius: 5px;
        animation: fadeIn 0.8s ease-out;
    }
    
    .warning-message {
        padding: 12px;
        background: linear-gradient(135deg, #FCF3CF, #F9E79F);
        border-left: 5px solid #F1C40F;
        margin: 10px 0;
        border-radius: 5px;
        animation: pulse 2s infinite;
    }
    
    @keyframes slideIn {
        from { transform: translateX(20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        20%, 60% { transform: translateX(-5px); }
        40%, 80% { transform: translateX(5px); }
    }
    
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: linear-gradient(135deg, #F8F9F9, #EAEDED);
        color: #5D6D7E;
        text-align: center;
        padding: 12px 0;
        font-size: 0.8rem;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
        z-index: 100;
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    th {
        background: linear-gradient(135deg, #4CAF50, #388E3C);
        color: white;
        text-align: left;
        padding: 12px;
        position: sticky;
        top: 0;
    }
    
    td {
        padding: 12px;
        border-bottom: 1px solid #eee;
    }
    
    tr:hover {
        background-color: rgba(76, 175, 80, 0.1);
        transform: scale(1.01);
    }
    
    .data-table {
        margin-top: 15px;
        margin-bottom: 15px;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .cart-item {
        background: linear-gradient(135deg, #F9FFF9, #E8F5E9);
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #D4EDD4;
        margin-bottom: 10px;
        transition: all 0.3s ease;
    }
    
    .cart-item:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    
    .remove-button {
        background: linear-gradient(135deg, #F44336, #D32F2F);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 6px 12px;
        font-size: 0.8rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .remove-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 20px;
        background: #f0f2f6;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #e0e5ec;
        color: #4CAF50;
    }
    
    .stTabs [aria-selected="true"] {
        background: #4CAF50 !important;
        color: white !important;
    }
    
    /* Input field styling */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        border-radius: 8px !important;
        padding: 10px 12px !important;
        border: 1px solid #ddd !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: #4CAF50 !important;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2) !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    
    /* Floating action button effect */
    .floating-btn {
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* Glow effect for important elements */
    .glow {
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 0 5px rgba(76, 175, 80, 0.5); }
        to { box-shadow: 0 0 15px rgba(76, 175, 80, 0.8); }
    }
</style>
""", unsafe_allow_html=True)

if 'db_filename' not in st.session_state or 'username' not in st.session_state:
    st.error("❌ Please log in to access this page")
    st.page_link("auth2.py", label="Click here to login", icon="🔑")
    st.stop()

def get_db_connection():
    return sqlite3.connect(st.session_state.db_filename)

def get_all_products():
    conn = get_db_connection()
    products = pd.read_sql_query('SELECT * FROM products ORDER BY name', conn)
    conn.close()
    return products


# Initialize SQLite database
def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Create products table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            gst_category INTEGER NOT NULL
        )
    ''')
    
    # Create bills table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_phone TEXT,
            bill_date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            total_gst REAL NOT NULL,
            grand_total REAL NOT NULL,
            payment_method TEXT NOT NULL,
            payment_reference TEXT,
            payment_note TEXT
        )
    
    ''')

    
    # Create bill_items table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS bill_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            gst_rate REAL NOT NULL,
            gst_amount REAL NOT NULL,
            total_amount REAL NOT NULL,
            FOREIGN KEY (bill_id) REFERENCES bills (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    # Insert some sample products if the table is empty
    conn.execute('SELECT COUNT(*) FROM products')
    row=c.fetchone()
    if row and row[0] == 0:
        sample_products = [
            ('Fresh Apples', 'Fruits & Vegetables', 120.00, 0),
            ('Tomatoes', 'Fruits & Vegetables', 60.00, 0),
            ('Onions', 'Fruits & Vegetables', 40.00, 0),
            ('Potatoes', 'Fruits & Vegetables', 30.00, 0),
            ('Milk (1L)', 'Dairy', 60.00, 0),
            ('Yogurt', 'Dairy', 45.00, 0),
            ('Whole Wheat Bread', 'Bakery', 40.00, 5),
            ('Brown Bread', 'Bakery', 35.00, 5),
            ('Organic Honey', 'Grocery', 250.00, 5),
            ('Rice (5kg)', 'Grocery', 350.00, 5),
            ('Wheat Flour (5kg)', 'Grocery', 220.00, 5),
            ('Cooking Oil (1L)', 'Grocery', 180.00, 5),
            ('Toothpaste', 'Personal Care', 80.00, 12),
            ('Soap Bar', 'Personal Care', 40.00, 12),
            ('Shampoo (200ml)', 'Personal Care', 120.00, 12),
            ('Breakfast Cereal', 'Processed Foods', 220.00, 12),
            ('Biscuits', 'Processed Foods', 60.00, 12),
            ('Instant Noodles', 'Processed Foods', 40.00, 12),
            ('Frozen Peas', 'Frozen Foods', 120.00, 18),
            ('Butter (500g)', 'Dairy', 250.00, 18),
            ('Cheese (200g)', 'Dairy', 180.00, 18),
            ('Chocolates', 'Confectionery', 150.00, 28),
            ('Soft Drinks (2L)', 'Beverages', 120.00, 28),
            ('Potato Chips', 'Snacks', 60.00, 28)
        ]
        conn.executemany('INSERT INTO products (name, category, price, gst_category) VALUES (?, ?, ?, ?)', sample_products)
    
    conn.commit()
    conn.close()

# Function to get all products
def get_all_products():
    conn = sqlite3.connect(st.session_state.db_filename)
    products = pd.read_sql_query('SELECT * FROM products ORDER BY name', conn)
    conn.close()
    return products

# Function to add a new product
def add_product(name, category, price, gst_category):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO products (name, category, price, gst_category) VALUES (?, ?, ?, ?)', 
                 (name, category, price, gst_category))
        conn.commit()
        success = True
    except Exception as e:
        success = False
        error = str(e)
    finally:
        conn.close()
    
    if success:
        return True, "Product added successfully!"
    else:
        return False, f"Error adding product: {error}"

# Function to get product details by ID
def get_product_by_id(product_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE id=?', (product_id,))
    product = c.fetchone()
    conn.close()
    
    if product:
        return {
            'id': product[0],
            'name': product[1],
            'category': product[2],
            'price': product[3],
            'gst_category': product[4]
        }
    return None

# Function to save a bill
def save_bill(customer_name, customer_phone, bill_date, total_amount,total_gst, grand_total,payment_method, payment_reference, payment_note, items):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        # Insert bill header
        c.execute('''
        INSERT INTO bills (
            customer_name,
            customer_phone,
            bill_date,
            total_amount,
            total_gst,
            grand_total,
            payment_method,
            payment_reference,
            payment_note
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        customer_name,
        customer_phone,
        bill_date,
        total_amount,
        total_gst,
        grand_total,
        payment_method,
        payment_reference,
        payment_note
    ))
        
        bill_id = c.lastrowid
        
        # Insert bill items
        for item in items:
            c.execute('''
                INSERT INTO bill_items (bill_id, product_id, product_name, quantity, price, gst_rate, 
                gst_amount, total_amount)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                bill_id, 
                item['product_id'], 
                item['product_name'], 
                item['quantity'], 
                item['price'], 
                item['gst_rate'], 
                item['gst_amount'], 
                item['total_amount']
            ))
        
        conn.commit()
        success = True
        bill_number = bill_id
    except Exception as e:
        conn.rollback()
        success = False
        error = str(e)
        bill_number = None
    finally:
        conn.close()
    
    if success:
        return True, f"Bill #{bill_number} saved successfully!", bill_number
    else:
        return False, f"Error saving bill: {error}", None

# Function to convert GST category to rate
def get_gst_rate(gst_category):
    gst_rates = {
        0: 0,
        5: 5,
        12: 12,
        18: 18,
        28: 28
    }
    return gst_rates.get(gst_category, 0)




def sales_report_section():
    st.markdown("""
                <style>
                    .section-header {
                        font-size: 28px;
                        font-weight: bold;
                        color: #2c3e50;
                        margin-bottom: 20px;
                        padding-bottom: 10px;
                        border-bottom: 2px solid #3498db;
                        animation: fadeIn 1s ease-in;
                    }
                    @keyframes fadeIn {
                        from { opacity: 0; transform: translateY(-20px); }
                        to { opacity: 1; transform: translateY(0); }
                    }
                    .stMetric {
                        border-radius: 10px;
                        padding: 15px;
                        background: white;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                        transition: all 0.3s ease;
                    }
                    .stMetric:hover {
                        transform: translateY(-5px);
                        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
                    }
                    .stDataFrame {
                        border-radius: 10px;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    }
                    .tab-container {
                        margin-top: 20px;
                    }
                    .date-range-container {
                        background: #f8f9fa;
                        padding: 15px;
                        border-radius: 10px;
                        margin-bottom: 20px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                    }
                    .chart-container {
                        background: white;
                        padding: 20px;
                        border-radius: 10px;
                        margin-top: 20px;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                        transition: all 0.3s ease;
                    }
                    .chart-container:hover {
                        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
                    }
                </style>
            """, unsafe_allow_html=True)

            

def generate_pdf_bill(bill_data):
    class PDF(FPDF):
        def header(self):
            # Logo - if you have one
            # self.image("assets/me.png", 10, 8, 33)
            
            # Shop Name
            self.set_font('Arial', 'B', 16)
            self.cell(0, 10, 'MANAS SUPER MART', 0, 1, 'C')
            
            # Address and contact info
            self.set_font('Arial', '', 10)
            self.cell(0, 6, '123 Main Market, Nashik, Maharasthra - 421001', 0, 1, 'C')
            self.cell(0, 6, 'Phone: +91 9000000001 | Email: contact@bizzence.com', 0, 1, 'C')
            self.cell(0, 6, 'GSTIN: 29ABCDE1234F1Z5', 0, 1, 'C')
            
            # Line break
            self.line(10, self.get_y()+3, 200, self.get_y()+3)
            self.ln(10)

    pdf = PDF()
    pdf.add_page()
    
    # Document title
    pdf.set_font('Arial', 'B', 15)
    pdf.cell(0, 10, 'TAX INVOICE', 0, 1, 'C')
    pdf.ln(5)

    # Bill Header - Left side
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(95, 6, 'Customer Details:', 0, 0)
    
    # Bill Header - Right side
    pdf.cell(95, 6, 'Invoice Details:', 0, 1)
    
    # Customer info - Left column
    pdf.set_font('Arial', '', 10)
    pdf.cell(95, 5, f"Name: {bill_data['customer_name']}", 0, 0)
    
    # Invoice info - Right column
    pdf.cell(95, 5, f"Invoice #: {bill_data['bill_number']}", 0, 1)
    
    # Customer phone - Left column
    if bill_data.get('customer_phone'):
        pdf.cell(95, 5, f"Phone: {bill_data['customer_phone']}", 0, 0)
    else:
        pdf.cell(95, 5, "", 0, 0)
    
    # Date - Right column
    pdf.cell(95, 5, f"Date: {bill_data['bill_date']}", 0, 1)
    
    # Payment method - Right column
    pdf.cell(95, 5, "", 0, 0)
    pdf.cell(95, 5, f"Payment: {bill_data.get('payment_method')}", 0, 1)
    
    # Add payment reference if available
    if bill_data.get('payment_reference'):
        pdf.cell(95, 5, "", 0, 0)
        pdf.cell(95, 5, f"Ref: {bill_data['payment_reference']}", 0, 1)
    
    pdf.ln(5)

    # Bill Items Table
    pdf.set_font('Arial', 'B', 9)
    col_widths = [8, 65, 22, 18, 20, 20, 25, 25]
    headers = ['#', 'Item', 'Price', 'Qty', 'GST%', 'GST Amt', 'Total']

    # Header Background
    pdf.set_fill_color(30, 136, 229)  # Blue
    pdf.set_text_color(255, 255, 255)  # White text
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 8, header, 1, 0, 'C', True)
    pdf.ln()

    # Table Content
    pdf.set_text_color(0, 0, 0)  # Black text
    pdf.set_font('Arial', '', 8)
    for i, item in enumerate(bill_data['items']):
        pdf.cell(col_widths[0], 7, str(i + 1), 1)
        pdf.cell(col_widths[1], 7, item['product_name'], 1)
        pdf.cell(col_widths[2], 7, f"Rs.{item['price']:.2f}", 1)
        pdf.cell(col_widths[3], 7, str(item['quantity']), 1)
        pdf.cell(col_widths[4], 7, f"{item['gst_rate']}%", 1)
        pdf.cell(col_widths[5], 7, f"Rs.{item['gst_amount']:.2f}", 1)
        pdf.cell(col_widths[7], 7, f"Rs.{item['total_amount']:.2f}", 1)
        pdf.ln()

    # Bill Summary
    pdf.ln(5)
    summary_x = 120  # X position to start summary    
    
    # Draw box around summary - start
    summary_start_y = pdf.get_y()
    
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(summary_x - 10)  # Move to position
    pdf.cell(30, 7, "Subtotal:", 'LT')
    pdf.cell(40, 7, f"Rs.{bill_data['total_amount']:.2f}", 'TR', 1, 'R')
    
    # Show Total GST
    pdf.cell(summary_x - 10)
    pdf.cell(30, 7, "Total GST:", 'L')
    pdf.cell(40, 7, f"Rs.{bill_data['total_gst']:.2f}", 'R', 1, 'R')

    # Grand Total
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(summary_x - 10)
    pdf.cell(30, 8, "Grand Total:", 'LB')
    pdf.cell(40, 8, f"Rs.{bill_data['grand_total']:.2f}", 'RB', 1, 'R')
    
    # Net Amount in bold
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(summary_x - 10)

    # Terms and conditions
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(0, 5, "Terms & Conditions:", 0, 1)
    pdf.set_font('Arial', '', 8)
    pdf.multi_cell(0, 4, "1. All items sold are non-returnable and non-refundable.\n2. Warranty as per manufacturer's terms where applicable.\n3. This is a computer-generated invoice and doesn't require a signature.")
    
    # Footer
    pdf.ln(5)
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 10, "Thank you for shopping with MANAS SUPER MART ! Please visit again.", 0, 1, 'C')

    # Save PDF to a file path
    pdf_filename = r"C:\Users\Admin\OneDrive - Shri Vile Parle Kelavani Mandal\Desktop\TeenTeasure\bill.pdf"
    pdf.output(pdf_filename, 'F')  # Adding 'F' to specify file output

    return pdf_filename

# Function to create a download link for a file
def get_download_link(file_path, filename):
    with open(file_path, "rb") as f:
        bytes_data = f.read()
    b64 = base64.b64encode(bytes_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download Bill as PDF</a>'
    return href
# Main function
def main():
    # Initialize database
    init_db()
    
    # Initialize session state variables
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    if 'bill_saved' not in st.session_state:
        st.session_state.bill_saved = False
    if 'pdf_path' not in st.session_state:
        st.session_state.pdf_path = None
    if 'bill_number' not in st.session_state:
        st.session_state.bill_number = None
    if 'products_df' not in st.session_state:
        st.session_state.products_df = get_all_products()
    
    # Display current date and time
    current_datetime = datetime.now().strftime("%B %d, %Y %I:%M %p")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"<div class='datetime-display'>{current_datetime}</div>", unsafe_allow_html=True)
    with col2:
        if st.button("Logout", key="logout_btn"):
        # Clear session state
            del st.session_state.username
            del st.session_state.db_filename
            if 'shop_name' in st.session_state:
                del st.session_state.shop_name
            st.success("Logged out successfully!")
            st.switch_page("auth2.py")

    # App Header
    st.markdown("<h1 class='main-header'>🛒 Bizzence</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subheader'>“Redefining the Way India Does Business.”</p>", unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2, tab3 , tab4 = st.tabs(["📝 Billing", "🏷️ Product Management", "📊 Reports","📜 History"])
    
    # Tab 1: Billing
    with tab1:
        # Customer information form - top section
        st.markdown("<div class='section-header'>Customer Information</div>", unsafe_allow_html=True)
        
        customer_col1, customer_col2 = st.columns(2)
        with customer_col1:
            customer_name = st.text_input("Customer Name*", placeholder="Enter customer name")
        with customer_col2:
            customer_phone = st.text_input("Phone Number", placeholder="Enter phone number (optional)")
        
        if st.button("Save Customer Info"):
            if not customer_name:
                st.error("Please enter customer name")
            else:
                st.session_state.customer_name = customer_name
                st.session_state.customer_phone = customer_phone
                st.success("Customer information saved!")
        
        
        # Calculate totals
        subtotal = sum(item['price'] * item['quantity'] for item in st.session_state.cart)
        total_gst = sum(item['gst_amount'] for item in st.session_state.cart)

        
        # Item selection section - horizontal layout
        st.markdown("<div class='section-header'>Add Items to Bill</div>", unsafe_allow_html=True)
        
        # Refresh product list
        st.session_state.products_df = get_all_products()
        
        # Get product names and IDs
        product_options = st.session_state.products_df[['id', 'name', 'category', 'price']].values.tolist()
        product_dict = {f"{p[1]} - {p[2]} (₹{p[3]:.2f})": p[0] for p in product_options}
        
        # Item selection in a horizontal layout
        item_col1, item_col2, item_col3 = st.columns([3, 1, 1])
        
        with item_col1:
            selected_product_label = st.selectbox(
                "Select Product*", 
                options=list(product_dict.keys()),
                format_func=lambda x: x
            )
        
        with item_col2:
            quantity = st.number_input("Quantity*", min_value=1, value=1)
        
        with item_col3:
            add_button = st.button("Add to Bill")
            
        if add_button:
            selected_product_id = product_dict[selected_product_label] if selected_product_label else None
            if not selected_product_id:
                st.error("Please select a product")
            else:
                product = get_product_by_id(selected_product_id)
                if product:
                    # Calculate GST
                    price = product['price']
                    gst_rate = get_gst_rate(product['gst_category'])
                    gst_amount = (price * quantity * gst_rate) / 100
                    total_amount = (price * quantity) + gst_amount
                    
                    # Add to cart
                    st.session_state.cart.append({
                        'product_id': selected_product_id,
                        'product_name': product['name'],
                        'category': product['category'],
                        'price': price,
                        'quantity': quantity,
                        'gst_rate': gst_rate,
                        'gst_amount': gst_amount,
                        'total_amount': total_amount
                    })
                    st.success(f"Added {quantity} x {product['name']} to the bill")
                    st.rerun()
        
        # Clear cart button
        if st.session_state.cart and st.button("Clear Cart"):
            st.session_state.cart = []
            st.warning("Cart has been cleared!")
            st.rerun()
        
        # Current Bill Section - Below the add items section
        st.markdown("<div class='section-header'>Current Bill</div>", unsafe_allow_html=True)
        
        if not st.session_state.cart:
            st.info("No items added to the bill yet.")
        else:
            # Create a table to display cart items
            bill_data = []
            for item in st.session_state.cart:
                bill_data.append([
                    item['product_name'],
                    item['category'],
                    f"₹{item['price']:.2f}",
                    str(item['quantity']),
                    f"{item['gst_rate']}%",
                    f"₹{item['gst_amount']:.2f}",
                    f"₹{item['total_amount']:.2f}"
                ])
            
            bill_df = pd.DataFrame(
                bill_data,
                columns=["Product", "Category", "Price", "Quantity", "GST Rate", "GST Amount", "Total"]
            )
            
            st.dataframe(bill_df, use_container_width=True)
            
            # Add remove buttons section
            st.markdown("<p>Select items to remove:</p>", unsafe_allow_html=True)
            remove_cols = st.columns(min(4, len(st.session_state.cart)))
            for i in range(len(st.session_state.cart)):
                with remove_cols[i % 4]:
                    item_name = st.session_state.cart[i]['product_name']
                    if st.button(f"Remove {item_name}", key=f"remove_{i}"):
                        st.session_state.cart.pop(i)
                        st.rerun()
            
            # Calculate totals
            subtotal = sum(item['price'] * item['quantity'] for item in st.session_state.cart)
            total_gst = sum(item['gst_amount'] for item in st.session_state.cart)
            grand_total = sum(item['total_amount'] for item in st.session_state.cart)
            st.markdown(f"<div class='bill-total'>"
                        f"Subtotal: ₹{subtotal:.2f}<br>"
                        f"Total GST: ₹{total_gst:.2f}<br>"
                        f"<strong>Grand Total: ₹{grand_total:.2f}</strong>"
                        f"</div>", 
                        unsafe_allow_html=True)
            
        st.markdown("<div class='section-header'>Payment Information</div>", unsafe_allow_html=True)
        payment_method = st.selectbox("Payment Method*", ["Cash", "Credit Card", "Debit Card", "UPI", "Mobile Wallet", "Net Banking", "Sodexo/Meal Card", "Other"])
        payment_col1, payment_col2 = st.columns(2)
        with payment_col1:
            payment_reference = st.text_input("Payment Reference", 
                                            placeholder="Transaction ID/Reference number (if applicable)")
        with payment_col2:
            payment_note = st.text_input("Payment Note", 
                                        placeholder="Additional payment details (optional)")
    
            # Generate bill button
        if 'customer_name' in st.session_state and st.session_state.customer_name:
            if st.button("Generate & Save Bill"):
                bill_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Save to database
                success, message, bill_number = save_bill(
                    st.session_state.customer_name,
                    st.session_state.customer_phone,
                    bill_date,
                    subtotal,
                    total_gst,
                    grand_total,
                    payment_method,
                    payment_reference,
                    payment_note,
                    st.session_state.cart
                )
                
                if success:
                    # Generate PDF
                    bill_data = {
                        'bill_number': bill_number,
                        'customer_name': st.session_state.customer_name,
                        'customer_phone': st.session_state.customer_phone,
                        'bill_date': bill_date,
                        'items': st.session_state.cart,
                        'total_amount': subtotal,
                        'total_gst': total_gst,
                        'grand_total': grand_total,
                        'payment_method': payment_method,
                        'payment_reference': payment_reference,
                        'payment_note': payment_note
                    
                    }
                    
                    pdf_path = generate_pdf_bill(bill_data)
                    st.session_state.pdf_path = pdf_path
                    st.session_state.bill_saved = True
                    st.session_state.bill_number = bill_number
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        else:
            st.warning("Please enter customer information before generating the bill")
        
        # Display download link if bill is saved
        if st.session_state.bill_saved and st.session_state.pdf_path:
            st.markdown("<div class='success-message'>Bill saved successfully!</div>", unsafe_allow_html=True)
            filename = f"Bill_{st.session_state.bill_number}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
            st.markdown(get_download_link(st.session_state.pdf_path, filename), unsafe_allow_html=True)
            
            if st.button("Start New Bill"):
                # Clear all session data for a new bill
                st.session_state.cart = []
                st.session_state.bill_saved = False
                st.session_state.pdf_path = None
                st.session_state.bill_number = None
                if 'customer_name' in st.session_state:
                    del st.session_state.customer_name
                if 'customer_phone' in st.session_state:
                    del st.session_state.customer_phone
                st.rerun()
    
    # Tab 2: Product Management
    with tab2:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("<div class='section-header'>Add New Product</div>", unsafe_allow_html=True)
            
            # Add product form
            with st.form(key='add_product_form'):
                product_name = st.text_input("Product Name*", placeholder="Enter product name")
                
                # Categories
                categories = [
                    "Fruits & Vegetables", "Dairy", "Bakery", "Grocery", 
                    "Personal Care", "Electronics", "Household", "Appliances",
                    "Confectionery", "Beverages", "Snacks", "Frozen Foods",
                    "Meat & Seafood", "Stationery", "Toys", "Others"
                ]
                product_category = st.selectbox("Category*", options=categories)
                
                product_price = st.number_input("Price (₹)*", min_value=0.01, value=100.00, format="%.2f")
                
                # GST Categories with descriptions
                gst_categories = {
                    "0% (Essential items)": 0,
                    "5% (Basic needs)": 5,
                    "12% (Processed foods & basic items)": 12,
                    "18% (Most services & electronics)": 18,
                    "28% (Luxury goods)": 28
                }
                product_gst = st.selectbox("GST Category*", options=list(gst_categories.keys()))
                gst_value = gst_categories[product_gst]
                
                add_product_submit = st.form_submit_button("Add Product")
                
                if add_product_submit:
                    if not product_name or not product_category:
                        st.error("Please fill in all required fields")
                    else:
                        success, message = add_product(product_name, product_category, product_price, gst_value)
                        if success:
                            st.success(message)
                            # Refresh product list
                            st.session_state.products_df = get_all_products()
                        else:
                            st.error(message)
        
        with col2:
            st.markdown("<div class='section-header'>Product Catalog</div>", unsafe_allow_html=True)
            
            # Filter options
            filter_col1, filter_col2 = st.columns(2)
            with filter_col1:
                search_term = st.text_input("Search Products", placeholder="Enter product name")
            with filter_col2:
                category_filter = st.selectbox("Filter by Category", 
                                            options=["All"] + list(st.session_state.products_df['category'].unique()))
            
            # Apply filters
            filtered_df = st.session_state.products_df.copy()
            if search_term:
                filtered_df = filtered_df[filtered_df['name'].str.contains(search_term, case=False)]
            if category_filter != "All":
                filtered_df = filtered_df[filtered_df['category'] == category_filter]
            
            # Display products table
            if not filtered_df.empty:
                # Convert GST category to display string
                filtered_df['gst_display'] = filtered_df['gst_category'].apply(lambda x: f"{x}%")
                
                # Format price column
                filtered_df['price_display'] = filtered_df['price'].apply(lambda x: f"₹{x:.2f}")
                
                # Display table with formatted columns
                st.dataframe(
                    filtered_df[['name', 'category', 'price_display', 'gst_display']].rename(
                        columns={
                            'name': 'Product Name',
                            'category': 'Category',
                            'price_display': 'Price',
                            'gst_display': 'GST Rate'
                        }
                    ),
                    use_container_width=True,
                    height=400
                )
            else:
                st.info("No products found matching your filters")
    
    # Tab 3: Reports
    with tab3:
        st.markdown("<div class='section-header'>Sales Analytics & Reports</div>", unsafe_allow_html=True)
            
            # Date range selector at the top (consistent across all tabs)
        with st.container():
            st.markdown("<div class='date-range-container'>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Report Start Date", 
                                        value=datetime.now() - timedelta(days=30),
                                        key="report_start_date")
            with col2:
                end_date = st.date_input("Report End Date", 
                                    value=datetime.now(),
                                    key="report_end_date")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Convert to string for SQL queries
        date_range = (start_date.strftime('%Y-%m-%d'), 
                    (end_date + timedelta(days=1)).strftime('%Y-%m-%d'))
        
        report_tab1, report_tab2, report_tab3, report_tab4 = st.tabs([
            "📊 Sales Overview", 
            "📈 Trends Analysis", 
            "🧑‍💼 Customer Analytics", 
            "📦 Product Performance"
        ])
        
        # Tab 1: Sales Overview
        with report_tab1:
            st.subheader("Sales Performance Summary")
            
            try:
                conn = get_db_connection()
                if conn:
                    # Get summary metrics
                    summary = pd.read_sql_query('''
                        SELECT 
                            COUNT(*) as total_bills,
                            SUM(grand_total) as total_sales,
                            AVG(grand_total) as avg_bill_value,
                            SUM(total_gst) as total_tax_collected
                        FROM bills 
                        WHERE bill_date BETWEEN ? AND ?
                    ''', conn, params=date_range)
                    
                    # Get daily sales
                    daily_sales = pd.read_sql_query('''
                        SELECT 
                            DATE(bill_date) as sale_date,
                            COUNT(*) as bill_count,
                            SUM(grand_total) as daily_sales,
                            SUM(total_gst) as daily_tax
                        FROM bills
                        WHERE bill_date BETWEEN ? AND ?
                        GROUP BY DATE(bill_date)
                        ORDER BY sale_date
                    ''', conn, params=date_range)
                    
                    conn.close()
                    
                    if not summary.empty:
                        # Display KPI cards with animation
                        st.markdown("""
                            <style>
                                .kpi-card {
                                    background: white;
                                    border-radius: 10px;
                                    padding: 15px;
                                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                                    transition: all 0.3s ease;
                                    animation: fadeIn 0.5s ease-in;
                                }
                                .kpi-card:hover {
                                    transform: translateY(-5px);
                                    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
                                }
                                .kpi-value {
                                    font-size: 24px;
                                    font-weight: bold;
                                    color: #2c3e50;
                                }
                                .kpi-label {
                                    font-size: 14px;
                                    color: #7f8c8d;
                                }
                            </style>
                        """, unsafe_allow_html=True)
                        
                        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
                        with kpi1:
                            st.markdown(f"""
                                <div class='kpi-card'>
                                    <div class='kpi-value'>{summary['total_bills'].values[0]}</div>
                                    <div class='kpi-label'>Total Bills</div>
                                </div>
                            """, unsafe_allow_html=True)
                        with kpi2:
                            st.markdown(f"""
                                <div class='kpi-card'>
                                    <div class='kpi-value'>₹{summary['total_sales'].values[0]:,.2f}</div>
                                    <div class='kpi-label'>Total Sales</div>
                                </div>
                            """, unsafe_allow_html=True)
                        with kpi3:
                            st.markdown(f"""
                                <div class='kpi-card'>
                                    <div class='kpi-value'>₹{summary['avg_bill_value'].values[0]:,.2f}</div>
                                    <div class='kpi-label'>Avg. Bill Value</div>
                                </div>
                            """, unsafe_allow_html=True)
                        with kpi4:
                            st.markdown(f"""
                                <div class='kpi-card'>
                                    <div class='kpi-value'>₹{summary['total_tax_collected'].values[0]:,.2f}</div>
                                    <div class='kpi-label'>Total Tax Collected</div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        # Sales trend chart
                        if not daily_sales.empty:
                            with st.container():
                                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                                fig = px.line(daily_sales, x='sale_date', y='daily_sales',
                                            title='Daily Sales Trend',
                                            labels={'sale_date': 'Date', 'daily_sales': 'Sales Amount (₹)'})
                                fig.update_layout(
                                    hovermode="x unified",
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)'
                                )
                                st.plotly_chart(fig, use_container_width=True)
                                st.markdown("</div>", unsafe_allow_html=True)
                                
                            with st.container():
                                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                                # Bar chart comparing bills count and sales
                                fig = go.Figure()
                                fig.add_trace(go.Bar(
                                    x=daily_sales['sale_date'],
                                    y=daily_sales['bill_count'],
                                    name='Number of Bills',
                                    yaxis='y',
                                    marker_color='#e74c3c',
                                    hovertemplate="%{x|%b %d}: %{y} bills<extra></extra>"
                                ))
                                fig.add_trace(go.Scatter(
                                    x=daily_sales['sale_date'],
                                    y=daily_sales['daily_sales'],
                                    name='Sales Amount',
                                    yaxis='y2',
                                    mode='lines+markers',
                                    line=dict(color='#3498db'),
                                    hovertemplate="%{x|%b %d}: ₹%{y:,.2f}<extra></extra>"
                                ))
                                fig.update_layout(
                                    title='Bills Count vs Sales Amount',
                                    yaxis=dict(title='Number of Bills'),
                                    yaxis2=dict(title='Sales Amount (₹)', overlaying='y', side='right'),
                                    xaxis=dict(title='Date'),
                                    legend=dict(x=0.02, y=0.98),
                                    hovermode="x unified",
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)'
                                )
                                st.plotly_chart(fig, use_container_width=True)
                                st.markdown("</div>", unsafe_allow_html=True)
                        else:
                            st.info("No sales data available for the selected date range")
                    else:
                        st.info("No sales data available for the selected date range")
                else:
                    st.error("Could not connect to database")
            except Exception as e:
                st.error(f"Error generating sales overview: {str(e)}")
        
        # Tab 2: Trends Analysis
        with report_tab2:
            st.subheader("Sales Trends & Patterns")
            
            try:
                conn = get_db_connection()
                if conn:
                    # Hourly sales pattern
                    hourly_sales = pd.read_sql_query('''
                        SELECT 
                            strftime('%H', bill_date) as hour_of_day,
                            COUNT(*) as bill_count,
                            SUM(grand_total) as total_sales
                        FROM bills
                        WHERE bill_date BETWEEN ? AND ?
                        GROUP BY strftime('%H', bill_date)
                        ORDER BY hour_of_day
                    ''', conn, params=date_range)
                    
                    # Weekly pattern
                    weekly_sales = pd.read_sql_query('''
                        SELECT 
                            strftime('%w', bill_date) as day_of_week,
                            strftime('%A', bill_date) as day_name,
                            COUNT(*) as bill_count,
                            SUM(grand_total) as total_sales
                        FROM bills
                        WHERE bill_date BETWEEN ? AND ?
                        GROUP BY strftime('%w', bill_date), strftime('%A', bill_date)
                        ORDER BY day_of_week
                    ''', conn, params=date_range)
                    
                    # Monthly trend (if date range spans multiple months)
                    monthly_sales = pd.read_sql_query('''
                        SELECT 
                            strftime('%Y-%m', bill_date) as month,
                            COUNT(*) as bill_count,
                            SUM(grand_total) as total_sales
                        FROM bills
                        WHERE bill_date BETWEEN ? AND ?
                        GROUP BY strftime('%Y-%m', bill_date)
                        ORDER BY month
                    ''', conn, params=date_range)
                    
                    conn.close()
                    
                    if not hourly_sales.empty:
                        # Hourly sales heatmap
                        with st.container():
                            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                            st.markdown("#### Hourly Sales Pattern")
                            fig = px.bar(hourly_sales, x='hour_of_day', y='total_sales',
                                        title='Sales by Hour of Day',
                                        labels={'hour_of_day': 'Hour', 'total_sales': 'Sales Amount (₹)'},
                                        color='total_sales',
                                        color_continuous_scale='Blues')
                            fig.update_layout(
                                hovermode="x unified",
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)'
                            )
                            fig.update_traces(
                                hovertemplate="Hour %{x}: ₹%{y:,.2f}<extra></extra>"
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Weekly pattern
                        with st.container():
                            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                            st.markdown("#### Weekly Sales Pattern")
                            fig = px.bar(weekly_sales, x='day_name', y='total_sales',
                                        title='Sales by Day of Week',
                                        labels={'day_name': 'Day', 'total_sales': 'Sales Amount (₹)'},
                                        color='total_sales',
                                        color_continuous_scale='Greens')
                            fig.update_layout(
                                hovermode="x unified",
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                xaxis={'categoryorder': 'array', 'categoryarray': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']}
                            )
                            fig.update_traces(
                                hovertemplate="%{x}: ₹%{y:,.2f}<extra></extra>"
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Monthly trend
                        if len(monthly_sales) > 1:
                            with st.container():
                                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                                st.markdown("#### Monthly Sales Trend")
                                fig = px.line(monthly_sales, x='month', y='total_sales',
                                            title='Monthly Sales Trend',
                                            labels={'month': 'Month', 'total_sales': 'Sales Amount (₹)'},
                                            markers=True)
                                fig.update_layout(
                                    hovermode="x unified",
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)'
                                )
                                fig.update_traces(
                                    hovertemplate="%{x}: ₹%{y:,.2f}<extra></extra>",
                                    line=dict(color='#9b59b6', width=3)
                                )
                                st.plotly_chart(fig, use_container_width=True)
                                st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.info("No trend data available for the selected date range")
                else:
                    st.error("Could not connect to database")
            except Exception as e:
                st.error(f"Error analyzing sales trends: {str(e)}")
        
        # Tab 3: Customer Analytics
        with report_tab3:
            st.subheader("Customer Behavior Analysis")
    
            try:
                conn = get_db_connection()
                if conn:
                    # Customer segmentation by spending
                    customer_segments = pd.read_sql_query('''
                        SELECT 
                            customer_phone,
                            customer_name,
                            COUNT(*) as visit_count,
                            SUM(grand_total) as total_spent,
                            AVG(grand_total) as avg_spent_per_visit
                        FROM bills
                        WHERE bill_date BETWEEN ? AND ?
                        GROUP BY customer_phone
                        HAVING customer_phone IS NOT NULL AND customer_phone != ''
                        ORDER BY total_spent DESC
                    ''', conn, params=date_range)
                    
                    # New vs returning customers
                    customer_analysis = pd.read_sql_query('''
                        WITH first_purchases AS (
                            SELECT customer_phone, MIN(DATE(bill_date)) as first_purchase_date
                            FROM bills
                            GROUP BY customer_phone
                        )
                        SELECT 
                            CASE 
                                WHEN DATE(b.bill_date) = fp.first_purchase_date THEN 'New'
                                ELSE 'Returning'
                            END as customer_type,
                            COUNT(*) as bill_count,
                            SUM(b.grand_total) as total_sales
                        FROM bills b
                        JOIN first_purchases fp ON b.customer_phone = fp.customer_phone
                        WHERE b.bill_date BETWEEN ? AND ?
                        GROUP BY customer_type
                    ''', conn, params=(date_range[0], date_range[1]))
                    
                    conn.close()
                    
                    if not customer_segments.empty:
                        # Top customers
                        with st.container():
                            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                            st.markdown("#### Top Customers by Spending")
                            top_customers = customer_segments.head(10).copy()
                            top_customers['total_spent'] = top_customers['total_spent'].apply(lambda x: f"₹{x:,.2f}")
                            st.dataframe(
                                top_customers[['customer_name', 'customer_phone', 'visit_count', 'total_spent']]
                                .rename(columns={
                                    'customer_name': 'Name',
                                    'customer_phone': 'Phone',
                                    'visit_count': 'Visits',
                                    'total_spent': 'Total Spent'
                                }),
                                use_container_width=True,
                                height=400
                            )
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Customer segmentation
                        with st.container():
                            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                            st.markdown("#### Customer Spending Segments")
                            bins = [0, 500, 2000, 5000, float('inf')]
                            labels = ['< ₹500', '₹500-₹2000', '₹2000-₹5000', '> ₹5000']
                            customer_segments['segment'] = pd.cut(customer_segments['total_spent'], bins=bins, labels=labels)
                            segment_counts = customer_segments['segment'].value_counts().reset_index()
                            segment_counts.columns = ['Spending Range', 'Customer Count']
                            
                            fig = px.pie(segment_counts, values='Customer Count', names='Spending Range',
                                        title='Customer Distribution by Spending Range',
                                        color_discrete_sequence=px.colors.sequential.RdBu)
                            fig.update_traces(
                                textposition='inside',
                                textinfo='percent+label',
                                hovertemplate="<b>%{label}</b><br>%{value} customers (%{percent})<extra></extra>"
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        # New vs returning customers
                        if not customer_analysis.empty:
                            with st.container():
                                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                                st.markdown("#### New vs Returning Customers")
                                col1, col2 = st.columns(2)
                                with col1:
                                    fig = px.pie(customer_analysis, values='total_sales', names='customer_type',
                                                title='Sales Distribution',
                                                color_discrete_map={'New':'#e74c3c','Returning':'#2ecc71'})
                                    fig.update_traces(
                                        textposition='inside',
                                        textinfo='percent+label',
                                        hovertemplate="<b>%{label}</b><br>₹%{value:,.2f} (%{percent})<extra></extra>"
                                    )
                                    st.plotly_chart(fig, use_container_width=True)
                                
                                with col2:
                                    fig = px.pie(customer_analysis, values='bill_count', names='customer_type',
                                                title='Visit Distribution',
                                                color_discrete_map={'New':'#e74c3c','Returning':'#2ecc71'})
                                    fig.update_traces(
                                        textposition='inside',
                                        textinfo='percent+label',
                                        hovertemplate="<b>%{label}</b><br>%{value} visits (%{percent})<extra></extra>"
                                    )
                                    st.plotly_chart(fig, use_container_width=True)
                                st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.info("No customer data available for the selected date range")
                else:
                    st.error("Could not connect to database")
            except Exception as e:
                st.error(f"Error analyzing customer data: {str(e)}")
        
        # Tab 4: Product Performance
        with report_tab4:
            st.subheader("Product Sales Analysis")
            
            try:
                conn = get_db_connection()
                if conn:
                    # Top selling products
                    product_sales = pd.read_sql_query('''
                        SELECT 
                            p.name AS product_name,               
                            p.category AS product_category,      
                            SUM(bi.quantity) as total_quantity,
                            SUM(bi.total_price) as total_revenue
                        FROM bill_items bi
                        JOIN products p ON bi.product_id = p.product_id
                        JOIN bills b ON bi.bill_id = b.bill_id
                        WHERE b.bill_date BETWEEN ? AND ?
                        GROUP BY p.product_id
                        ORDER BY total_revenue DESC
                    ''', conn, params=date_range)

                    # Category performance (updated column name)
                    category_sales = pd.read_sql_query('''
                        SELECT 
                            p.category AS product_category,       
                            SUM(bi.quantity) as total_quantity,
                            SUM(bi.total_price) as total_revenue,
                            COUNT(DISTINCT b.bill_id) as bills_appeared_in
                        FROM bill_items bi
                        JOIN products p ON bi.product_id = p.product_id
                        JOIN bills b ON bi.bill_id = b.bill_id
                        WHERE b.bill_date BETWEEN ? AND ?
                        GROUP BY p.category                       
                        ORDER BY total_revenue DESC
                    ''', conn, params=date_range)
                    
                    conn.close()
                    
                    if not product_sales.empty:
                        # Top products
                        with st.container():
                            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                            st.markdown("#### Top Selling Products")
                            top_products = product_sales.head(10).copy()
                            top_products['total_revenue'] = top_products['total_revenue'].apply(lambda x: f"₹{x:,.2f}")
                            st.dataframe(
                                top_products[['product_name', 'product_category', 'total_quantity', 'total_revenue']]
                                .rename(columns={
                                    'product_name': 'Product',
                                    'product_category': 'Category',
                                    'total_quantity': 'Quantity Sold',
                                    'total_revenue': 'Total Revenue'
                                }),
                                use_container_width=True,
                                height=400
                            )
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Category performance
                        with st.container():
                            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                            st.markdown("#### Category Performance")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                fig = px.bar(category_sales, x='product_category', y='total_revenue',
                                            title='Revenue by Category',
                                            labels={'product_category': 'Category', 'total_revenue': 'Revenue (₹)'},
                                            color='total_revenue',
                                            color_continuous_scale='Viridis')
                                fig.update_layout(
                                    hovermode="x unified",
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    xaxis_tickangle=-45
                                )
                                fig.update_traces(
                                    hovertemplate="<b>%{x}</b><br>₹%{y:,.2f}<extra></extra>"
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            
                            with col2:
                                fig = px.pie(category_sales, values='total_revenue', names='product_category',
                                            title='Revenue Share by Category',
                                            hole=0.4)
                                fig.update_traces(
                                    textposition='inside',
                                    textinfo='percent+label',
                                    hovertemplate="<b>%{label}</b><br>₹%{value:,.2f} (%{percent})<extra></extra>"
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.info("No product data available for the selected date range")
                else:
                    st.error("Could not connect to database")
            except Exception as e:
                st.error(f"Error analyzing product performance: {str(e)}")
    
    # Tab 4: History & Customer Search
    with tab4:
        st.markdown("<div class='section-header'>Customer History & Search</div>", unsafe_allow_html=True)
        
        # Create two sub-tabs for different history views
        history_tab1, history_tab2 = st.tabs(["📜 All Bills History", "🔍 Customer Search"])
        
        # Tab 1: All Bills History
        with history_tab1:
            st.subheader("Recent Bills")
        
        try:
            # Get bills from database
            conn = get_db_connection()
            if conn:
                bills_df = pd.read_sql_query('''
                    SELECT id, customer_name, customer_phone, bill_date, grand_total
                    FROM bills 
                    ORDER BY bill_date DESC
                    LIMIT 100
                ''', conn)
                conn.close()
            else:
                st.error("Could not connect to database")
                bills_df = pd.DataFrame()
                
            if not bills_df.empty:
                # Format the dataframe for display
                bills_df['bill_date'] = pd.to_datetime(bills_df['bill_date']).dt.strftime('%Y-%m-%d %H:%M')
                bills_df['grand_total'] = bills_df['grand_total'].apply(lambda x: f"₹{x:.2f}")
                bills_df.columns = ['Bill #', 'Customer Name', 'Phone', 'Date & Time', 'Amount']
                
                # Display bills with a filter for date range
                date_col1, date_col2 = st.columns(2)
                with date_col1:
                    start_date = st.date_input("From Date", value=datetime.now() - pd.Timedelta(days=30))
                with date_col2:
                    end_date = st.date_input("To Date", value=datetime.now())
                
                # Apply date filter
                bills_df['Date Only'] = pd.to_datetime(bills_df['Date & Time']).dt.date
                filtered_bills = bills_df[
                    (bills_df['Date Only'] >= start_date) & 
                    (bills_df['Date Only'] <= end_date)
                ]
                filtered_bills = filtered_bills.drop('Date Only', axis=1)
                
                if not filtered_bills.empty:
                    st.dataframe(filtered_bills, use_container_width=True)
                    
                    # Add bill details view
                    selected_bill = st.selectbox(
                        "Select a bill to view details:",
                        options=filtered_bills['Bill #'].tolist(),
                        format_func=lambda x: f"Bill #{x} - {filtered_bills[filtered_bills['Bill #']==x]['Customer Name'].values[0]}"
                    )
                    
                    if st.button("View Bill Details"):
                        conn = get_db_connection()
                        if conn:
                            try:
                                bill_header = pd.read_sql_query(
                                    "SELECT id, customer_name, customer_phone, bill_date, total_amount, total_gst, grand_total FROM bills WHERE id = ?", 
                                    conn, params=(selected_bill,))
                                
                                bill_items = pd.read_sql_query(
                                    "SELECT product_name, quantity, price, gst_rate, gst_amount, total_amount FROM bill_items WHERE bill_id = ?",
                                    conn, params=(selected_bill,))
                                
                                # Display bill details...
                                # (Rest of your bill details display code here)
                                
                            except sqlite3.Error as e:
                                st.error(f"Database error: {str(e)}")
                            finally:
                                conn.close()
                        else:
                            st.error("Could not connect to database")
                else:
                    st.info(f"No bills found between {start_date} and {end_date}")
            else:
                st.info("No billing history found")
        except Exception as e:
            st.error(f"Error retrieving bill data: {str(e)}")
            st.info("Please check the database structure and ensure the required tables and columns exist.")
    
    # Tab 2: Customer Search
    with history_tab2:
        st.subheader("Search Customer by Phone Number")
        
        search_phone = st.text_input("Enter Phone Number", placeholder="10-digit phone number")
        
        if search_phone:
            try:
                conn = get_db_connection()
                if conn:
                    customer_bills = pd.read_sql_query(
                        "SELECT id, customer_name, customer_phone, bill_date, grand_total FROM bills WHERE customer_phone LIKE ? ORDER BY bill_date DESC",
                        conn, params=(f"%{search_phone}%",))
                    conn.close()
                else:
                    st.error("Could not connect to database")
                    customer_bills = pd.DataFrame()
                
                if not customer_bills.empty:
                    # Customer summary and details display...
                    # (Rest of your customer search code here)
                    pass
                else:
                    st.warning(f"No customer found with phone number containing '{search_phone}'")
            except Exception as e:
                st.error(f"Error searching for customer: {str(e)}")
        
        # Top Customers section
        st.markdown("<div class='section-header'>Top Customers</div>", unsafe_allow_html=True)
        
        try:
            conn = get_db_connection()
            if conn:
                top_customers = pd.read_sql_query('''
                    SELECT customer_name, customer_phone, COUNT(*) as visit_count, 
                        SUM(grand_total) as total_spent
                    FROM bills
                    WHERE customer_phone IS NOT NULL AND customer_phone != ''
                    GROUP BY customer_phone
                    ORDER BY total_spent DESC
                    LIMIT 10
                ''', conn)
                conn.close()
                
                if not top_customers.empty:
                    top_customers['total_spent'] = top_customers['total_spent'].apply(lambda x: f"₹{x:.2f}")
                    top_customers.columns = ['Customer Name', 'Phone', 'Total Visits', 'Total Spent']
                    st.dataframe(top_customers, use_container_width=True)
                else:
                    st.info("No customer data available yet")
            else:
                st.error("Could not connect to database")
        except Exception as e:
            st.error(f"Error loading top customers: {str(e)}")
    st.markdown("""
    <div class='footer'>
        <p>© 2025 Bizzence - Shopping & Billing System | Innovated & Engineered by Manas Borse 💡</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
    
