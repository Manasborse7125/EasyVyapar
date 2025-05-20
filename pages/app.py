import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import datetime
import random
import tempfile
from fpdf import FPDF
import base64

# Set page configuration
st.set_page_config(
    page_title="EasyVyapar - Shopping & Billing System",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-family: 'Trebuchet MS', sans-serif;
        text-align: center;
        color: #4CAF50;
        margin-bottom: 0;
        font-size: 2.5rem;
    }
    .subheader {
        font-size: 1.2rem;
        text-align: center;
        font-style: italic;
        color: #5D6D7E;
        margin-bottom: 1.5rem;
    }
    .datetime-display {
        text-align: right;
        font-size: 0.9rem;
        color: #5D6D7E;
        margin-bottom: 1rem;
    }
    .section-header {
        background-color: #4285F4;
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 15px;
        font-weight: bold;
    }
    div[data-testid="stForm"] {
        border: 1px solid #E5E8E8;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    div.stButton > button {
        width: 100%;
        font-weight: bold;
        height: 3em;
        background-color: #4CAF50;
        color: white;
    }
    div.stButton > button:hover {
        background-color: #388E3C;
        color: white;
    }
    .bill-item {
        background-color: #F5F5F5;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        border-left: 4px solid #4CAF50;
    }
    .bill-total {
        background-color: #E8F5E9;
        padding: 15px;
        border-radius: 5px;
        margin-top: 20px;
        border-left: 4px solid #4CAF50;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .success-message {
        padding: 10px;
        background-color: #D4EFDF;
        border-left: 5px solid #2ECC71;
        margin: 10px 0;
    }
    .error-message {
        padding: 10px;
        background-color: #FADBD8;
        border-left: 5px solid #E74C3C;
        margin: 10px 0;
    }
    .info-message {
        padding: 10px;
        background-color: #EBF5FB;
        border-left: 5px solid #3498DB;
        margin: 10px 0;
    }
    .warning-message {
        padding: 10px;
        background-color: #FCF3CF;
        border-left: 5px solid #F1C40F;
        margin: 10px 0;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #F8F9F9;
        color: #5D6D7E;
        text-align: center;
        padding: 10px 0;
        font-size: 0.8rem;
    }
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th {
        background-color: #4CAF50;
        color: white;
        text-align: left;
        padding: 12px;
    }
    td {
        padding: 12px;
        border-bottom: 1px solid #ddd;
    }
    tr:hover {
        background-color: #f5f5f5;
    }
    .data-table {
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .cart-item {
        background-color: #F9FFF9;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #D4EDD4;
        margin-bottom: 10px;
    }
    .remove-button {
        background-color: #F44336;
        color: white;
        border: none;
        border-radius: 3px;
        padding: 5px 10px;
        font-size: 0.8rem;
        cursor: pointer;
    }
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('minimart.db')
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
    c.execute('SELECT COUNT(*) FROM products')
    if c.fetchone()[0] == 0:
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
        c.executemany('INSERT INTO products (name, category, price, gst_category) VALUES (?, ?, ?, ?)', sample_products)
    
    conn.commit()
    conn.close()

# Function to get all products
def get_all_products():
    conn = sqlite3.connect('minimart.db')
    products = pd.read_sql_query('SELECT * FROM products ORDER BY name', conn)
    conn.close()
    return products

# Function to add a new product
def add_product(name, category, price, gst_category):
    conn = sqlite3.connect('minimart.db')
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
    conn = sqlite3.connect('minimart.db')
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
    conn = sqlite3.connect('minimart.db',check_same_thread=False)
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
            self.cell(0, 6, 'Phone: +91 9000000001 | Email: contact@easyvyapar.com', 0, 1, 'C')
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
    st.markdown(f"<div class='datetime-display'>{current_datetime}</div>", unsafe_allow_html=True)
    
    # App Header
    st.markdown("<h1 class='main-header'>🛒 EasyVyapar</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subheader'>Apka Dukaan Ka Digital Saathi.</p>", unsafe_allow_html=True)
    
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
        st.markdown("<div class='section-header'>Sales Reports</div>", unsafe_allow_html=True)
        st.info("This section is under development. Future updates will include detailed sales reports, GST summaries, and inventory management.")
    
    # Tab 4: History & Customer Search
    # Tab 4: History & Customer Search
    with tab4:
        st.markdown("<div class='section-header'>Customer History & Search</div>", unsafe_allow_html=True)
        
        # Create two sub-tabs for different history views
        history_tab1, history_tab2 = st.tabs(["📜 All Bills History", "🔍 Customer Search"])
        
        # Tab 1: All Bills History
        with history_tab1:
            st.subheader("Recent Bills")
            
            try:
                # Get bills from database - explicitly listing columns to avoid the missing column
                conn = sqlite3.connect('minimart.db')
                bills_df = pd.read_sql_query('''
                    SELECT id, customer_name, customer_phone, bill_date, grand_total
                    FROM bills 
                    ORDER BY bill_date DESC
                    LIMIT 100
                ''', conn)
                conn.close()
                
                if not bills_df.empty:
                    # Format the dataframe for display
                    bills_df['bill_date'] = pd.to_datetime(bills_df['bill_date']).dt.strftime('%Y-%m-%d %H:%M')
                    bills_df['grand_total'] = bills_df['grand_total'].apply(lambda x: f"₹{x:.2f}")
                    # Rename columns for display
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
                            # Get bill details from database
                            conn = sqlite3.connect('minimart.db')
                            bill_header = pd.read_sql_query(f"SELECT id, customer_name, customer_phone, bill_date, total_amount, total_gst, grand_total FROM bills WHERE id = {selected_bill}", conn)
                            bill_items = pd.read_sql_query(f'''
                                SELECT product_name, quantity, price, gst_rate, gst_amount, total_amount 
                                FROM bill_items 
                                WHERE bill_id = {selected_bill}
                            ''', conn)
                            conn.close()
                            
                            # Display bill header information
                            st.markdown("<div class='section-header'>Bill Details</div>", unsafe_allow_html=True)
                            detail_col1, detail_col2, detail_col3 = st.columns(3)
                            
                            with detail_col1:
                                st.markdown(f"**Bill #:** {selected_bill}")
                                st.markdown(f"**Date:** {bill_header['bill_date'].values[0]}")
                                
                            with detail_col2:
                                st.markdown(f"**Customer:** {bill_header['customer_name'].values[0]}")
                                st.markdown(f"**Phone:** {bill_header['customer_phone'].values[0] if bill_header['customer_phone'].values[0] else 'N/A'}")
                                
                            with detail_col3:
                                st.markdown(f"**Payment:** Cash")  # Default since column doesn't exist
                                st.markdown(f"**Grand Total:** ₹{bill_header['grand_total'].values[0]:.2f}")
                            
                            # Display bill items
                            st.markdown("<div class='section-header'>Items Purchased</div>", unsafe_allow_html=True)
                            
                            # Format the dataframe for display
                            bill_items['price'] = bill_items['price'].apply(lambda x: f"₹{x:.2f}")
                            bill_items['gst_amount'] = bill_items['gst_amount'].apply(lambda x: f"₹{x:.2f}")
                            bill_items['total_amount'] = bill_items['total_amount'].apply(lambda x: f"₹{x:.2f}")
                            bill_items['gst_rate'] = bill_items['gst_rate'].apply(lambda x: f"{x}%")
                            bill_items.columns = ['Product', 'Quantity', 'Price', 'GST Rate', 'GST Amount', 'Total']
                            
                            st.dataframe(bill_items, use_container_width=True)
                            
                            # Generate PDF button
                            if st.button("Generate PDF Bill"):
                                # Get all necessary data for PDF generation
                                bill_data = {
                                    'bill_number': selected_bill,
                                    'customer_name': bill_header['customer_name'].values[0],
                                    'customer_phone': bill_header['customer_phone'].values[0],
                                    'bill_date': bill_header['bill_date'].values[0],
                                    'payment_method': "Cash",  # Default value
                                    'payment_reference': "",  # Default value
                                    'total_amount': bill_header['total_amount'].values[0],
                                    'total_gst': bill_header['total_gst'].values[0],
                                    'grand_total': bill_header['grand_total'].values[0],
                                    'items': []
                                }
                                
                                # Get original bill items data in the required format
                                conn = sqlite3.connect('minimart.db')
                                items_data = pd.read_sql_query(f'''
                                    SELECT product_id, product_name, quantity, price, gst_rate, gst_amount, total_amount 
                                    FROM bill_items 
                                    WHERE bill_id = {selected_bill}
                                ''', conn)
                                conn.close()
                                
                                for _, item in items_data.iterrows():
                                    bill_data['items'].append({
                                        'product_id': item['product_id'],
                                        'product_name': item['product_name'],
                                        'quantity': item['quantity'],
                                        'price': item['price'],
                                        'gst_rate': item['gst_rate'],
                                        'gst_amount': item['gst_amount'],
                                        'total_amount': item['total_amount']
                                    })
                                
                                pdf_path = generate_pdf_bill(bill_data)
                                filename = f"Bill_{selected_bill}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
                                st.markdown(get_download_link(pdf_path, filename), unsafe_allow_html=True)
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
                    # Search for customer in database - explicitly listing columns to avoid missing column
                    conn = sqlite3.connect('minimart.db')
                    customer_bills = pd.read_sql_query(f'''
                        SELECT id, customer_name, customer_phone, bill_date, grand_total
                        FROM bills 
                        WHERE customer_phone LIKE '%{search_phone}%'
                        ORDER BY bill_date DESC
                    ''', conn)
                    conn.close()
                    
                    if not customer_bills.empty:
                        # Customer summary
                        st.markdown("<div class='section-header'>Customer Information</div>", unsafe_allow_html=True)
                        
                        # Get customer name from first result
                        customer_name = customer_bills['customer_name'].iloc[0]
                        total_visits = len(customer_bills)
                        total_spent = customer_bills['grand_total'].sum()
                        
                        customer_col1, customer_col2, customer_col3 = st.columns(3)
                        with customer_col1:
                            st.markdown(f"**Customer Name:** {customer_name}")
                            st.markdown(f"**Phone Number:** {search_phone}")
                        
                        with customer_col2:
                            st.markdown(f"**Total Visits:** {total_visits}")
                            st.markdown(f"**First Purchase:** {customer_bills['bill_date'].iloc[-1]}")
                        
                        with customer_col3:
                            st.markdown(f"**Total Spent:** ₹{total_spent:.2f}")
                            st.markdown(f"**Last Purchase:** {customer_bills['bill_date'].iloc[0]}")
                        
                        # Display customer purchase history
                        st.markdown("<div class='section-header'>Purchase History</div>", unsafe_allow_html=True)
                        
                        # Format the dataframe for display
                        customer_bills['bill_date'] = pd.to_datetime(customer_bills['bill_date']).dt.strftime('%Y-%m-%d %H:%M')
                        customer_bills['grand_total'] = customer_bills['grand_total'].apply(lambda x: f"₹{x:.2f}")
                        customer_bills.columns = ['Bill #', 'Customer Name', 'Phone', 'Date & Time', 'Amount']
                        
                        st.dataframe(customer_bills[['Bill #', 'Date & Time', 'Amount']], use_container_width=True)
                        
                        # Allow viewing individual bills
                        selected_bill = st.selectbox(
                            "Select a bill to view details:",
                            options=customer_bills['Bill #'].tolist(),
                            format_func=lambda x: f"Bill #{x} - {customer_bills[customer_bills['Bill #']==x]['Date & Time'].values[0]}"
                        )
                        
                        if st.button("View Customer Bill Details"):
                            # Get bill details from database
                            conn = sqlite3.connect('minimart.db')
                            bill_header = pd.read_sql_query(f"SELECT id, customer_name, customer_phone, bill_date, total_amount, total_gst, grand_total FROM bills WHERE id = {selected_bill}", conn)
                            bill_items = pd.read_sql_query(f'''
                                SELECT product_name, quantity, price, gst_rate, gst_amount, total_amount 
                                FROM bill_items 
                                WHERE bill_id = {selected_bill}
                            ''', conn)
                            conn.close()
                            
                            # Display bill header information
                            st.markdown("<div class='section-header'>Bill Details</div>", unsafe_allow_html=True)
                            detail_col1, detail_col2, detail_col3 = st.columns(3)
                            
                            with detail_col1:
                                st.markdown(f"**Bill #:** {selected_bill}")
                                st.markdown(f"**Date:** {bill_header['bill_date'].values[0]}")
                                
                            with detail_col2:
                                st.markdown(f"**Customer:** {bill_header['customer_name'].values[0]}")
                                st.markdown(f"**Phone:** {bill_header['customer_phone'].values[0]}")
                                
                            with detail_col3:
                                st.markdown(f"**Payment:** Cash")  # Default since column doesn't exist
                                st.markdown(f"**Grand Total:** ₹{bill_header['grand_total'].values[0]:.2f}")
                            
                            # Display bill items
                            st.markdown("<div class='section-header'>Items Purchased</div>", unsafe_allow_html=True)
                            
                            # Format the dataframe for display
                            bill_items['price'] = bill_items['price'].apply(lambda x: f"₹{x:.2f}")
                            bill_items['gst_amount'] = bill_items['gst_amount'].apply(lambda x: f"₹{x:.2f}")
                            bill_items['total_amount'] = bill_items['total_amount'].apply(lambda x: f"₹{x:.2f}")
                            bill_items['gst_rate'] = bill_items['gst_rate'].apply(lambda x: f"{x}%")
                            bill_items.columns = ['Product', 'Quantity', 'Price', 'GST Rate', 'GST Amount', 'Total']
                            
                            st.dataframe(bill_items, use_container_width=True)
                            
                            # Generate PDF button
                            if st.button("Generate PDF for Customer Bill"):
                                # Get all necessary data for PDF generation
                                bill_data = {
                                    'bill_number': selected_bill,
                                    'customer_name': bill_header['customer_name'].values[0],
                                    'customer_phone': bill_header['customer_phone'].values[0],
                                    'bill_date': bill_header['bill_date'].values[0],
                                    'payment_method': "Cash",  # Default value
                                    'payment_reference': "",  # Default value
                                    'total_amount': bill_header['total_amount'].values[0],
                                    'total_gst': bill_header['total_gst'].values[0],
                                    'grand_total': bill_header['grand_total'].values[0],
                                    'items': []
                                }
                                
                                # Get original bill items data in the required format
                                conn = sqlite3.connect('minimart.db')
                                items_data = pd.read_sql_query(f'''
                                    SELECT product_id, product_name, quantity, price, gst_rate, gst_amount, total_amount 
                                    FROM bill_items 
                                    WHERE bill_id = {selected_bill}
                                ''', conn)
                                conn.close()
                                
                                for _, item in items_data.iterrows():
                                    bill_data['items'].append({
                                        'product_id': item['product_id'],
                                        'product_name': item['product_name'],
                                        'quantity': item['quantity'],
                                        'price': item['price'],
                                        'gst_rate': item['gst_rate'],
                                        'gst_amount': item['gst_amount'],
                                        'total_amount': item['total_amount']
                                    })
                                
                                pdf_path = generate_pdf_bill(bill_data)
                                filename = f"Bill_{selected_bill}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
                                st.markdown(get_download_link(pdf_path, filename), unsafe_allow_html=True)
                        
                        # Purchase patterns section
                        st.markdown("<div class='section-header'>Customer Purchase Patterns</div>", unsafe_allow_html=True)
                        
                        # Fetch most purchased items by this customer
                        try:
                            conn = sqlite3.connect('minimart.db')
                            popular_items = pd.read_sql_query(f'''
                                SELECT bill_items.product_name, SUM(bill_items.quantity) as total_quantity,
                                    COUNT(DISTINCT bill_items.bill_id) as purchase_frequency
                                FROM bill_items
                                JOIN bills ON bill_items.bill_id = bills.id
                                WHERE bills.customer_phone LIKE '%{search_phone}%'
                                GROUP BY bill_items.product_name
                                ORDER BY total_quantity DESC
                                LIMIT 10
                            ''', conn)
                            conn.close()
                            
                            if not popular_items.empty:
                                popular_items.columns = ['Product', 'Total Quantity', 'Purchase Frequency']
                                st.write("Most Frequently Purchased Items:")
                                st.dataframe(popular_items, use_container_width=True)
                                
                                # Create a simple visualization of purchase history
                                st.write("Purchase Timeline:")
                                
                                # Format the amount column - extract numeric values from the Amount column
                                purchase_amounts = customer_bills['Amount'].apply(lambda x: float(x.replace('₹', '')))
                                
                                # Create a visualization dataset
                                timeline_data = pd.DataFrame({
                                    'Date': pd.to_datetime(customer_bills['Date & Time']),
                                    'Bill': customer_bills['Bill #'],
                                    'Amount': purchase_amounts
                                })
                                
                                # Plot timeline
                                import plotly.express as px
                                fig = px.line(timeline_data, x='Date', y='Amount', markers=True,
                                            title=f"Purchase History for {customer_name}")
                                st.plotly_chart(fig, use_container_width=True)
                                
                                # Recommendations based on purchase history
                                if len(popular_items) >= 2:
                                    st.markdown("<div class='info-message'>🛒 Recommendation: Based on purchase history, "
                                            f"this customer frequently buys {popular_items['Product'].iloc[0]} and " 
                                            f"{popular_items['Product'].iloc[1]}. Consider offering complementary products.</div>", 
                                            unsafe_allow_html=True)
                                elif len(popular_items) == 1:
                                    st.markdown("<div class='info-message'>🛒 Recommendation: Based on purchase history, "
                                            f"this customer frequently buys {popular_items['Product'].iloc[0]}. "
                                            f"Consider offering complementary products.</div>", 
                                            unsafe_allow_html=True)
                            else:
                                st.info("Not enough purchase data to show patterns")
                        except Exception as e:
                            st.error(f"Error retrieving purchase patterns: {str(e)}")
                        
                    else:
                        st.warning(f"No customer found with phone number containing '{search_phone}'")
                        st.markdown("<div class='info-message'>Try searching with a partial phone number to widen results.</div>", 
                                unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error searching for customer: {str(e)}")
                    st.info("Please check the database structure and ensure the required tables and columns exist.")
            else:
                st.info("Enter a phone number to search for customer history")
                
                # Quick search for top customers
                st.markdown("<div class='section-header'>Top Customers</div>", unsafe_allow_html=True)
                
                try:
                    conn = sqlite3.connect('minimart.db')
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
                except Exception as e:
                    st.error(f"Error loading top customers: {str(e)}")
    # with tab4:
    #     st.markdown("<div class='section-header'>Customer History & Search</div>", unsafe_allow_html=True)
        
    #     # Create two sub-tabs for different history views
    #     history_tab1, history_tab2 = st.tabs(["📜 All Bills History", "🔍 Customer Search"])
        
    #     # Tab 1: All Bills History
    #     with history_tab1:
    #         st.subheader("Recent Bills")
            
    #         # Get bills from database
    #         conn = sqlite3.connect('minimart.db')
    #         bills_df = pd.read_sql_query('''
    #             SELECT id, customer_name, customer_phone, bill_date, 
    #                 grand_total, payment_method
    #             FROM bills 
    #             ORDER BY bill_date DESC
    #             LIMIT 100
    #         ''', conn)
    #         conn.close()
            
    #         if not bills_df.empty:
    #             # Format the dataframe for display
    #             bills_df['bill_date'] = pd.to_datetime(bills_df['bill_date']).dt.strftime('%Y-%m-%d %H:%M')
    #             bills_df['grand_total'] = bills_df['grand_total'].apply(lambda x: f"₹{x:.2f}")
    #             bills_df.columns = ['Bill #', 'Customer Name', 'Phone', 'Date & Time', 'Amount', 'Payment Method']
                
    #             # Display bills with a filter for date range
    #             date_col1, date_col2 = st.columns(2)
    #             with date_col1:
    #                 start_date = st.date_input("From Date", value=datetime.now() - pd.Timedelta(days=30))
    #             with date_col2:
    #                 end_date = st.date_input("To Date", value=datetime.now())
                
    #             # Apply date filter
    #             bills_df['Date Only'] = pd.to_datetime(bills_df['Date & Time']).dt.date
    #             filtered_bills = bills_df[
    #                 (bills_df['Date Only'] >= start_date) & 
    #                 (bills_df['Date Only'] <= end_date)
    #             ]
    #             filtered_bills = filtered_bills.drop('Date Only', axis=1)
                
    #             if not filtered_bills.empty:
    #                 st.dataframe(filtered_bills, use_container_width=True)
                    
    #                 # Add bill details view
    #                 selected_bill = st.selectbox(
    #                     "Select a bill to view details:",
    #                     options=filtered_bills['Bill #'].tolist(),
    #                     format_func=lambda x: f"Bill #{x} - {filtered_bills[filtered_bills['Bill #']==x]['Customer Name'].values[0]}"
    #                 )
                    
    #                 if st.button("View Bill Details"):
    #                     # Get bill details from database
    #                     conn = sqlite3.connect('minimart.db')
    #                     bill_header = pd.read_sql_query(f"SELECT * FROM bills WHERE id = {selected_bill}", conn)
    #                     bill_items = pd.read_sql_query(f'''
    #                         SELECT product_name, quantity, price, gst_rate, gst_amount, total_amount 
    #                         FROM bill_items 
    #                         WHERE bill_id = {selected_bill}
    #                     ''', conn)
    #                     conn.close()
                        
    #                     # Display bill header information
    #                     st.markdown("<div class='section-header'>Bill Details</div>", unsafe_allow_html=True)
    #                     detail_col1, detail_col2, detail_col3 = st.columns(3)
                        
    #                     with detail_col1:
    #                         st.markdown(f"**Bill #:** {selected_bill}")
    #                         st.markdown(f"**Date:** {bill_header['bill_date'].values[0]}")
                            
    #                     with detail_col2:
    #                         st.markdown(f"**Customer:** {bill_header['customer_name'].values[0]}")
    #                         st.markdown(f"**Phone:** {bill_header['customer_phone'].values[0] if bill_header['customer_phone'].values[0] else 'N/A'}")
                            
    #                     with detail_col3:
    #                         st.markdown(f"**Payment:** {bill_header['payment_method'].values[0]}")
    #                         st.markdown(f"**Grand Total:** ₹{bill_header['grand_total'].values[0]:.2f}")
                        
    #                     # Display bill items
    #                     st.markdown("<div class='section-header'>Items Purchased</div>", unsafe_allow_html=True)
                        
    #                     # Format the dataframe for display
    #                     bill_items['price'] = bill_items['price'].apply(lambda x: f"₹{x:.2f}")
    #                     bill_items['gst_amount'] = bill_items['gst_amount'].apply(lambda x: f"₹{x:.2f}")
    #                     bill_items['total_amount'] = bill_items['total_amount'].apply(lambda x: f"₹{x:.2f}")
    #                     bill_items['gst_rate'] = bill_items['gst_rate'].apply(lambda x: f"{x}%")
    #                     bill_items.columns = ['Product', 'Quantity', 'Price', 'GST Rate', 'GST Amount', 'Total']
                        
    #                     st.dataframe(bill_items, use_container_width=True)
                        
    #                     # Generate PDF button
    #                     if st.button("Generate PDF Bill"):
    #                         # Get all necessary data for PDF generation
    #                         bill_data = {
    #                             'bill_number': selected_bill,
    #                             'customer_name': bill_header['customer_name'].values[0],
    #                             'customer_phone': bill_header['customer_phone'].values[0],
    #                             'bill_date': bill_header['bill_date'].values[0],
    #                             'payment_method': bill_header['payment_method'].values[0],
    #                             'payment_reference': bill_header['payment_reference'].values[0],
    #                             'total_amount': bill_header['total_amount'].values[0],
    #                             'total_gst': bill_header['total_gst'].values[0],
    #                             'discount_percentage': bill_header['discount_percentage'].values[0],
    #                             'discount_amount': bill_header['discount_amount'].values[0],
    #                             'grand_total': bill_header['grand_total'].values[0],
    #                             'items': []
    #                         }
                            
    #                         # Get original bill items data in the required format
    #                         conn = sqlite3.connect('minimart.db')
    #                         items_data = pd.read_sql_query(f'''
    #                             SELECT product_id, product_name, quantity, price, gst_rate, gst_amount, total_amount 
    #                             FROM bill_items 
    #                             WHERE bill_id = {selected_bill}
    #                         ''', conn)
    #                         conn.close()
                            
    #                         for _, item in items_data.iterrows():
    #                             bill_data['items'].append({
    #                                 'product_id': item['product_id'],
    #                                 'product_name': item['product_name'],
    #                                 'quantity': item['quantity'],
    #                                 'price': item['price'],
    #                                 'gst_rate': item['gst_rate'],
    #                                 'gst_amount': item['gst_amount'],
    #                                 'total_amount': item['total_amount']
    #                             })
                            
    #                         pdf_path = generate_pdf_bill(bill_data)
    #                         filename = f"Bill_{selected_bill}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    #                         st.markdown(get_download_link(pdf_path, filename), unsafe_allow_html=True)
    #             else:
    #                 st.info(f"No bills found between {start_date} and {end_date}")
    #         else:
    #             st.info("No billing history found")
        
    #     # Tab 2: Customer Search
    #     with history_tab2:
    #         st.subheader("Search Customer by Phone Number")
            
    #         search_phone = st.text_input("Enter Phone Number", placeholder="10-digit phone number")
            
    #         if search_phone:
    #             # Search for customer in database
    #             conn = sqlite3.connect('minimart.db')
    #             customer_bills = pd.read_sql_query(f'''
    #                 SELECT id, customer_name, customer_phone, bill_date, 
    #                     grand_total, payment_method
    #                 FROM bills 
    #                 WHERE customer_phone LIKE '%{search_phone}%'
    #                 ORDER BY bill_date DESC
    #             ''', conn)
    #             conn.close()
                
    #             if not customer_bills.empty:
    #                 # Customer summary
    #                 st.markdown("<div class='section-header'>Customer Information</div>", unsafe_allow_html=True)
                    
    #                 # Get customer name from first result
    #                 customer_name = customer_bills['customer_name'].iloc[0]
    #                 total_visits = len(customer_bills)
    #                 total_spent = customer_bills['grand_total'].sum()
                    
    #                 customer_col1, customer_col2, customer_col3 = st.columns(3)
    #                 with customer_col1:
    #                     st.markdown(f"**Customer Name:** {customer_name}")
    #                     st.markdown(f"**Phone Number:** {search_phone}")
                    
    #                 with customer_col2:
    #                     st.markdown(f"**Total Visits:** {total_visits}")
    #                     st.markdown(f"**First Purchase:** {customer_bills['bill_date'].iloc[-1]}")
                    
    #                 with customer_col3:
    #                     st.markdown(f"**Total Spent:** ₹{total_spent:.2f}")
    #                     st.markdown(f"**Last Purchase:** {customer_bills['bill_date'].iloc[0]}")
                    
    #                 # Display customer purchase history
    #                 st.markdown("<div class='section-header'>Purchase History</div>", unsafe_allow_html=True)
                    
    #                 # Format the dataframe for display
    #                 customer_bills['bill_date'] = pd.to_datetime(customer_bills['bill_date']).dt.strftime('%Y-%m-%d %H:%M')
    #                 customer_bills['grand_total'] = customer_bills['grand_total'].apply(lambda x: f"₹{x:.2f}")
    #                 customer_bills.columns = ['Bill #', 'Customer Name', 'Phone', 'Date & Time', 'Amount', 'Payment Method']
                    
    #                 st.dataframe(customer_bills[['Bill #', 'Date & Time', 'Amount', 'Payment Method']], 
    #                             use_container_width=True)
                    
    #                 # Allow viewing individual bills
    #                 selected_bill = st.selectbox(
    #                     "Select a bill to view details:",
    #                     options=customer_bills['Bill #'].tolist(),
    #                     format_func=lambda x: f"Bill #{x} - {customer_bills[customer_bills['Bill #']==x]['Date & Time'].values[0]}"
    #                 )
                    
    #                 if st.button("View Customer Bill Details"):
    #                     # Get bill details from database
    #                     conn = sqlite3.connect('minimart.db')
    #                     bill_header = pd.read_sql_query(f"SELECT * FROM bills WHERE id = {selected_bill}", conn)
    #                     bill_items = pd.read_sql_query(f'''
    #                         SELECT product_name, quantity, price, gst_rate, gst_amount, total_amount 
    #                         FROM bill_items 
    #                         WHERE bill_id = {selected_bill}
    #                     ''', conn)
    #                     conn.close()
                        
    #                     # Display bill header information
    #                     st.markdown("<div class='section-header'>Bill Details</div>", unsafe_allow_html=True)
    #                     detail_col1, detail_col2, detail_col3 = st.columns(3)
                        
    #                     with detail_col1:
    #                         st.markdown(f"**Bill #:** {selected_bill}")
    #                         st.markdown(f"**Date:** {bill_header['bill_date'].values[0]}")
                            
    #                     with detail_col2:
    #                         st.markdown(f"**Customer:** {bill_header['customer_name'].values[0]}")
    #                         st.markdown(f"**Phone:** {bill_header['customer_phone'].values[0]}")
                            
    #                     with detail_col3:
    #                         st.markdown(f"**Payment:** {bill_header['payment_method'].values[0]}")
    #                         st.markdown(f"**Grand Total:** ₹{bill_header['grand_total'].values[0]:.2f}")
                        
    #                     # Display bill items
    #                     st.markdown("<div class='section-header'>Items Purchased</div>", unsafe_allow_html=True)
                        
    #                     # Format the dataframe for display
    #                     bill_items['price'] = bill_items['price'].apply(lambda x: f"₹{x:.2f}")
    #                     bill_items['gst_amount'] = bill_items['gst_amount'].apply(lambda x: f"₹{x:.2f}")
    #                     bill_items['total_amount'] = bill_items['total_amount'].apply(lambda x: f"₹{x:.2f}")
    #                     bill_items['gst_rate'] = bill_items['gst_rate'].apply(lambda x: f"{x}%")
    #                     bill_items.columns = ['Product', 'Quantity', 'Price', 'GST Rate', 'GST Amount', 'Total']
                        
    #                     st.dataframe(bill_items, use_container_width=True)
                        
    #                     # Generate PDF button
    #                     if st.button("Generate PDF for Customer Bill"):
    #                         # Get all necessary data for PDF generation
    #                         bill_data = {
    #                             'bill_number': selected_bill,
    #                             'customer_name': bill_header['customer_name'].values[0],
    #                             'customer_phone': bill_header['customer_phone'].values[0],
    #                             'bill_date': bill_header['bill_date'].values[0],
    #                             'payment_method': bill_header['payment_method'].values[0],
    #                             'payment_reference': bill_header['payment_reference'].values[0],
    #                             'total_amount': bill_header['total_amount'].values[0],
    #                             'total_gst': bill_header['total_gst'].values[0],
    #                             'discount_percentage': bill_header['discount_percentage'].values[0],
    #                             'discount_amount': bill_header['discount_amount'].values[0],
    #                             'grand_total': bill_header['grand_total'].values[0],
    #                             'items': []
    #                         }
                            
    #                         # Get original bill items data in the required format
    #                         conn = sqlite3.connect('minimart.db')
    #                         items_data = pd.read_sql_query(f'''
    #                             SELECT product_id, product_name, quantity, price, gst_rate, gst_amount, total_amount 
    #                             FROM bill_items 
    #                             WHERE bill_id = {selected_bill}
    #                         ''', conn)
    #                         conn.close()
                            
    #                         for _, item in items_data.iterrows():
    #                             bill_data['items'].append({
    #                                 'product_id': item['product_id'],
    #                                 'product_name': item['product_name'],
    #                                 'quantity': item['quantity'],
    #                                 'price': item['price'],
    #                                 'gst_rate': item['gst_rate'],
    #                                 'gst_amount': item['gst_amount'],
    #                                 'total_amount': item['total_amount']
    #                             })
                            
    #                         pdf_path = generate_pdf_bill(bill_data)
    #                         filename = f"Bill_{selected_bill}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    #                         st.markdown(get_download_link(pdf_path, filename), unsafe_allow_html=True)
                    
    #                 # Purchase patterns section
    #                 st.markdown("<div class='section-header'>Customer Purchase Patterns</div>", unsafe_allow_html=True)
                    
    #                 # Fetch most purchased items by this customer
    #                 conn = sqlite3.connect('minimart.db')
    #                 popular_items = pd.read_sql_query(f'''
    #                     SELECT bill_items.product_name, SUM(bill_items.quantity) as total_quantity,
    #                         COUNT(DISTINCT bill_items.bill_id) as purchase_frequency
    #                     FROM bill_items
    #                     JOIN bills ON bill_items.bill_id = bills.id
    #                     WHERE bills.customer_phone LIKE '%{search_phone}%'
    #                     GROUP BY bill_items.product_name
    #                     ORDER BY total_quantity DESC
    #                     LIMIT 10
    #                 ''', conn)
    #                 conn.close()
                    
    #                 if not popular_items.empty:
    #                     popular_items.columns = ['Product', 'Total Quantity', 'Purchase Frequency']
    #                     st.write("Most Frequently Purchased Items:")
    #                     st.dataframe(popular_items, use_container_width=True)
                        
    #                     # Create a simple visualization of purchase history
    #                     st.write("Purchase Timeline:")
    #                     purchase_dates = pd.to_datetime(customer_bills['Date & Time'])
                        
    #                     # Create a visualization dataset
    #                     timeline_data = pd.DataFrame({
    #                         'Date': purchase_dates,
    #                         'Bill': customer_bills['Bill #'],
    #                         'Amount': customer_bills['Amount'].apply(lambda x: float(x.replace('₹', '')))
    #                     })
                        
    #                     # Plot timeline
    #                     import plotly.express as px
    #                     fig = px.line(timeline_data, x='Date', y='Amount', markers=True,
    #                                 title=f"Purchase History for {customer_name}")
    #                     st.plotly_chart(fig, use_container_width=True)
                        
    #                     # Recommendations based on purchase history
    #                     st.markdown("<div class='info-message'>🛒 Recommendation: Based on purchase history, "
    #                             f"this customer frequently buys {popular_items['Product'].iloc[0]} and " 
    #                             f"{popular_items['Product'].iloc[1]}. Consider offering complementary products.</div>", 
    #                             unsafe_allow_html=True)
    #                 else:
    #                     st.info("Not enough purchase data to show patterns")
                    
    #             else:
    #                 st.warning(f"No customer found with phone number containing '{search_phone}'")
    #                 st.markdown("<div class='info-message'>Try searching with a partial phone number to widen results.</div>", 
    #                         unsafe_allow_html=True)
    #         else:
    #             st.info("Enter a phone number to search for customer history")
                
    #             # Quick search for top customers
    #             st.markdown("<div class='section-header'>Top Customers</div>", unsafe_allow_html=True)
                
    #             conn = sqlite3.connect('minimart.db')
    #             top_customers = pd.read_sql_query('''
    #                 SELECT customer_name, customer_phone, COUNT(*) as visit_count, 
    #                     SUM(grand_total) as total_spent
    #                 FROM bills
    #                 WHERE customer_phone IS NOT NULL AND customer_phone != ''
    #                 GROUP BY customer_phone
    #                 ORDER BY total_spent DESC
    #                 LIMIT 10
    #             ''', conn)
    #             conn.close()
                
    #             if not top_customers.empty:
    #                 top_customers['total_spent'] = top_customers['total_spent'].apply(lambda x: f"₹{x:.2f}")
    #                 top_customers.columns = ['Customer Name', 'Phone', 'Total Visits', 'Total Spent']
    #                 st.dataframe(top_customers, use_container_width=True)


    # Footer
    st.markdown("""
    <div class='footer'>
        <p>© 2025 EasyVyapar - Shopping & Billing System | Innovated & Engineered by Manas Borse 💡</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()