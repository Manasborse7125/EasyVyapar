import streamlit as st
import sqlite3
import hashlib
import os
from datetime import datetime
from streamlit.components.v1 import html

# Set page configuration
st.set_page_config(
    page_title="Bizzence",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling with animations
st.markdown("""
<style>

    
    
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
        transition: all 0.3s ease;
    }
    
    .main-header {
        font-family: 'Poppins', sans-serif;
        text-align: right;
        color: #2E86C1;
        margin-top: 0;
        padding-top: 0;
        margin-bottom: 0;
        font-weight: 700;
        font-size: 2.5rem;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }
    
    .subheader {
        font-size: 1.2rem;
        text-align: right;
        color: #5D6D7E;
        margin-bottom: 1rem;
        font-weight: 400;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #F8F9F9;
        border-radius: 8px;
        gap: 1px;
        padding: 10px 20px;
        font-weight: 500;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border: 1px solid #E5E8E8;
        margin: 0 5px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2E86C1;
        color: white;
        box-shadow: 0 4px 8px rgba(46,134,193,0.3);
    }
    
    div[data-testid="stForm"] {
        border: 1px solid #E5E8E8;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
        background: white;
    }
    
    div.stButton > button {
        width: 100%;
        font-weight: 600;
        height: 3em;
        background-color: #2E86C1;
        color: white;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(46,134,193,0.3);
        border: none;
    }
    
    div.stButton > button:hover {
        background-color: #1A5276;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(26,82,118,0.3);
    }
    
    .footer {
        position: below;
        left: 0;
        bottom: 0;
        width: 100%;
        background: linear-gradient(90deg, #2E86C1 0%, #1A5276 100%);
        color: white;
        text-align: center;
        padding: 12px 0;
        font-size: 0.8rem;
        z-index: 100;
    }
    
    .footer a {
        color: white !important;
        text-decoration: none;
    }
    
    .footer a:hover {
        text-decoration: underline;
    }
    
    .success-message {
        padding: 15px;
        background-color: #D4EFDF;
        border-left: 5px solid #2ECC71;
        margin: 15px 0;
        border-radius: 8px;
        animation: fadeIn 0.5s ease-in-out;
    }
    
    .error-message {
        padding: 15px;
        background-color: #FADBD8;
        border-left: 5px solid #E74C3C;
        margin: 15px 0;
        border-radius: 8px;
        animation: shake 0.5s ease-in-out;
    }
    
    .info-card {
        background-color: #EBF5FB;
        border-left: 5px solid #3498DB;
        padding: 20px;
        margin: 15px 0;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    
    .info-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    
    .main-container {
        display: flex;
        flex-direction: row;
        height: calc(100vh - 120px);
    }
    
    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        background: linear-gradient(135deg, #EBF5FB 0%, #D4E6F1 100%);
        border-radius: 15px;
        margin-right: 15px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        position: relative;
    }
    
    .image-container img {
        transition: transform 0.5s ease;
    }
    
    .image-container:hover img {
        transform: scale(1.03);
    }
    
    .form-container {
        overflow-y: auto;
        max-height: calc(100vh - 150px);
        padding-right: 15px;
    }
    
    /* Input field styling */
    .stTextInput input, .stTextInput textarea {
        border-radius: 8px !important;
        border: 1px solid #E5E8E8 !important;
        padding: 10px 15px !important;
    }
    
    .stTextInput input:focus, .stTextInput textarea:focus {
        border-color: #2E86C1 !important;
        box-shadow: 0 0 0 2px rgba(46,134,193,0.2) !important;
    }
    
    /* Checkbox styling */
    .stCheckbox span {
        font-weight: 400;
    }
    
    /* Animation keyframes */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        20%, 60% { transform: translateX(-5px); }
        40%, 80% { transform: translateX(5px); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Pulse animation for important elements */
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Floating animation */
    .floating {
        animation: floating 3s ease-in-out infinite;
    }
    
    @keyframes floating {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #2E86C1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #1A5276;
    }
    
    /* Glow effect for active elements */
    .glow-on-hover:hover {
        box-shadow: 0 0 15px rgba(46,134,193,0.5);
    }
    
    /* Gradient text */
    .gradient-text {
        background: linear-gradient(90deg, #2E86C1 0%, #1ABC9C 100%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# Add some JavaScript for additional interactivity
st.markdown("""
<script>
// Add hover class to elements when mouse enters
document.addEventListener('mouseover', function(e) {
    if (e.target.closest('.stButton > button')) {
        e.target.closest('.stButton > button').classList.add('glow-on-hover');
    }
    if (e.target.closest('.info-card')) {
        e.target.closest('.info-card').classList.add('glow-on-hover');
    }
});

// Remove hover class when mouse leaves
document.addEventListener('mouseout', function(e) {
    if (e.target.closest('.stButton > button')) {
        e.target.closest('.stButton > button').classList.remove('glow-on-hover');
    }
    if (e.target.closest('.info-card')) {
        e.target.closest('.info-card').classList.remove('glow-on-hover');
    }
});
</script>
""", unsafe_allow_html=True)

# Function to hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Initialize the SQLite database for user authentication
def init_auth_db():
    conn = sqlite3.connect("easy_users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            phone TEXT,
            city TEXT,
            state TEXT,
            email TEXT,
            password TEXT,
            created_at TEXT,
            shop_name TEXT,
            shop_address TEXT,
            gst_number TEXT
        )
    """)
    conn.commit()
    conn.close()

# Initialize shopkeeper's database
def init_shopkeeper_db(username):
    user_db = f"minimart_{username}.db"
    conn = sqlite3.connect(user_db)
    c = conn.cursor()
    
    # Create products table
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            gst_category INTEGER NOT NULL
        )
    ''')
    
    # Create bills table
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
    
    # Create bill_items table
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
    
    # Insert sample products if table is empty
    c.execute('SELECT COUNT(*) FROM products')
    if c.fetchone()[0] == 0:
        sample_products = [
            ('Fresh Apples', 'Fruits & Vegetables', 120.00, 0),
            ('Tomatoes', 'Fruits & Vegetables', 60.00, 0),
            # Add more sample products as needed
        ]
        c.executemany('INSERT INTO products (name, category, price, gst_category) VALUES (?, ?, ?, ?)', sample_products)
    
    conn.commit()
    conn.close()

# Add new user to database
def add_user(username, phone, city, state, email, password, shop_name, shop_address, gst_number):
    conn = sqlite3.connect("easy_users.db")
    cursor = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (username, phone, city, state, email, hash_password(password), created_at, 
                    shop_name, shop_address, gst_number))
    conn.commit()
    conn.close()
    
    # Initialize shopkeeper's database
    init_shopkeeper_db(username)

# Check if username exists
def username_exists(username):
    conn = sqlite3.connect("easy_users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    data = cursor.fetchone()
    conn.close()
    return data is not None

# Verify login credentials
def login_user(username, password):
    conn = sqlite3.connect("easy_users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                   (username, hash_password(password)))
    data = cursor.fetchone()
    conn.close()
    return data

# Main App
def main():
    init_auth_db()
    
    # App header with gradient text
    st.markdown("<h1 class='main-header gradient-text'>💰 Bizzence</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subheader'>Redefining the Way India Does Business.</p>", unsafe_allow_html=True)
    
    # Create two columns: one for image, one for login/signup
    left_col, right_col = st.columns([3, 5])
    
    # Image column with floating animation
    with left_col:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.markdown("""
        <div class="image-container floating">
            <img src="https://pplx-res.cloudinary.com/image/upload/v1747653492/gpt4o_images/vol0mmhllxbbk1maqwll.png" 
                 alt="Bizzence" style="max-width: 100%; max-height: 500%; object-fit: contain; border-radius: 10px;">
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.write("") 
        st.write("") 
        st.write("")
        st.write("")
        st.write("") 
        
        st.markdown("""
        <div class="image-container floating" style="animation-delay: 0.5s;">
            <img src="https://5.imimg.com/data5/SELLER/Default/2023/10/353218567/FP/VJ/GT/154906243/retail-shop-billing-software.png" 
                 alt="Billing System" style="max-width: 100%; max-height: 500%; object-fit: contain; border-radius: 10px;">
        </div>
        """, unsafe_allow_html=True)
         
        
        st.write("")
        st.write("") 
        st.write("")
        st.write("") 
        st.write("") 
        st.markdown("""
        <div class="image-container floating" style="animation-delay: 1s;">
            <img src="https://media.licdn.com/dms/image/v2/D5603AQEwXxKBmXCH5w/profile-displayphoto-shrink_800_800/B56ZVbVPHHGQAc-/0/1740994058084?e=1753315200&v=beta&t=DY_et5JaAfbPvGOgZAaQM2NbDBE82YfBaq217nEbYwQ" alt="Manas Borse" style="max-width: 100%; max-height: 500%; object-fit: contain; border-radius: 10px;">
        </div>
        """, unsafe_allow_html=True)

    # Login/Signup column
    with right_col:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        # Session state for messages
        if 'login_status' not in st.session_state:
            st.session_state.login_status = None
        if 'signup_status' not in st.session_state:
            st.session_state.signup_status = None
        
        # Create tabs for Login and Sign Up with pulse animation
        tab1, tab2 = st.tabs(["📝 Login", "✨ Sign Up"])
        
        # Login Tab
        with tab1:
            with st.form("login_form"):
                st.subheader("Welcome Back! 👋")
                
                username = st.text_input("Username", key="login_username", placeholder="Enter your username")
                password = st.text_input("Password", type='password', key="login_password", placeholder="Enter your password")
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    remember_me = st.checkbox("Remember Me")
                with col2:
                    st.markdown("<div style='text-align: right;'><a href='#' style='color: #2E86C1;'>Forgot Password?</a></div>", 
                               unsafe_allow_html=True)
                
                submit_button = st.form_submit_button("Login", type="primary")
                
                if submit_button:
                    if not username or not password:
                        st.session_state.login_status = "empty"
                    else:
                        result = login_user(username, password)
                        if result:
                            st.session_state.login_status = "success"
                            st.session_state.username = username
                            st.session_state.db_filename = f"minimart_{username}.db"
                            st.session_state.shop_name = result[7]
                            st.rerun()
                        else:
                            st.session_state.login_status = "error"
            
            if "login_status" not in st.session_state:
                st.session_state.login_status = None

            if "current_user" not in st.session_state:
                st.session_state.current_user = None

            # Display login status message outside the form
            if st.session_state.login_status == "success":
                st.markdown(f"""
                <div class='success-message pulse'>
                    <h3>🎉 Login Successful!</h3>
                    <p>Welcome back, {st.session_state.current_user}! Redirecting to your dashboard...</p>
                </div>
                """, unsafe_allow_html=True)
                st.switch_page("pages/abc.py")
                
            elif st.session_state.login_status == "error":
                st.markdown("""
                <div class='error-message'>
                    <h3>❌ Login Failed</h3>
                    <p>The username or password you entered is incorrect. Please try again.</p>
                </div>
                """, unsafe_allow_html=True)
            elif st.session_state.login_status == "empty":
                st.markdown("""
                <div class='error-message'>
                    <h3>⚠️ Missing Information</h3>
                    <p>Please fill in both username and password fields.</p>
                </div>
                """, unsafe_allow_html=True)
                
            # Additional information with hover effect
            st.markdown("""
            <div class='info-card glow-on-hover'>
                <h4>📱 Download the Bizzence App (Coming Soon!!)</h4>
                <p>Access your shop management on the go with our mobile app.</p>
                <div style="text-align: center; margin-top: 15px;">
                    <img src="https://cdn-icons-png.flaticon.com/512/888/888857.png" style="height: 40px; margin: 0 5px;" class="hover-grow">
                    <img src="https://cdn-icons-png.flaticon.com/512/888/888841.png" style="height: 40px; margin: 0 5px;" class="hover-grow">
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Sign Up Tab
        with tab2:
            with st.form("signup_form"):
                st.subheader("Create Your Shop Account 🚀")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    username = st.text_input("Username*", key="signup_username", 
                                            placeholder="Choose a unique username")
                    city = st.text_input("City*", key="signup_city",
                                        placeholder="Your city")
                    email = st.text_input("Email*", key="signup_email",
                                         placeholder="your.email@example.com")
                    shop_name = st.text_input("Shop Name*", key="signup_shop_name",
                                            placeholder="Your shop/business name")
                
                with col2:
                    phone = st.text_input("Phone Number*", key="signup_phone",
                                         placeholder="10 digit mobile number")
                    state = st.text_input("State*", key="signup_state",
                                         placeholder="Your state")
                    password = st.text_input("Create Password*", type='password', key="signup_password",
                                            placeholder="Minimum 8 characters")
                    shop_address = st.text_input("Shop Address*", key="signup_address",
                                               placeholder="Your shop address")
                
                gst_number = st.text_input("GST Number (Optional)", key="signup_gst",
                                         placeholder="22AAAAA0000A1Z5")
                
                confirm_password = st.text_input("Confirm Password*", type='password', key="signup_confirm",
                                               placeholder="Re-enter your password")
                
                terms = st.checkbox("I agree to the Terms and Conditions*")
                
                signup_button = st.form_submit_button("Create Account", type="primary")
                
                if signup_button:
                    required_fields = [
                        username, phone, city, state, email, 
                        password, confirm_password, shop_name, shop_address
                    ]
                    
                    if not all(required_fields):
                        st.session_state.signup_status = "empty"
                    elif password != confirm_password:
                        st.session_state.signup_status = "password_mismatch"
                    elif not terms:
                        st.session_state.signup_status = "terms_not_accepted"
                    elif username_exists(username):
                        st.session_state.signup_status = "username_exists"
                    else:
                        try:
                            add_user(
                                username, phone, city, state, email, password,
                                shop_name, shop_address, gst_number
                            )
                            st.session_state.signup_status = "success"
                        except Exception as e:
                            st.session_state.signup_status = "error"
                            st.session_state.error_message = str(e)
                        
            # Display signup status message outside the form
            if st.session_state.signup_status == "success":
                st.markdown("""
                <div class='success-message pulse'>
                    <h3>✅ Account Created Successfully!</h3>
                    <p>Your Bizzence account has been created. You can now login using your credentials.</p>
                </div>
                """, unsafe_allow_html=True)
                st.switch_page("pages/abc.py")
            elif st.session_state.signup_status == "empty":
                st.markdown("""
                <div class='error-message'>
                    <h3>⚠️ Missing Information</h3>
                    <p>Please fill in all required fields (*) to create your account.</p>
                </div>
                """, unsafe_allow_html=True)
            elif st.session_state.signup_status == "password_mismatch":
                st.markdown("""
                <div class='error-message'>
                    <h3>❌ Password Mismatch</h3>
                    <p>The passwords you entered do not match. Please try again.</p>
                </div>
                """, unsafe_allow_html=True)
            elif st.session_state.signup_status == "terms_not_accepted":
                st.markdown("""
                <div class='error-message'>
                    <h3>⚠️ Terms Not Accepted</h3>
                    <p>You must agree to the Terms and Conditions to create an account.</p>
                </div>
                """, unsafe_allow_html=True)
            elif st.session_state.signup_status == "username_exists":
                st.markdown("""
                <div class='error-message'>
                    <h3>🚫 Username Already Exists</h3>
                    <p>This username is already taken. Please choose another one.</p>
                </div>
                """, unsafe_allow_html=True)
            elif st.session_state.signup_status == "error":
                st.markdown(f"""
                <div class='error-message'>
                    <h3>❌ Error Creating Account</h3>
                    <p>An error occurred: {st.session_state.get('error_message', 'Unknown error')}</p>
                </div>
                """, unsafe_allow_html=True)
                
            # Show signup benefits with hover effect
            st.markdown("""
            <div class='info-card glow-on-hover'>
                <h4>✨ Benefits of Bizzence</h4>
                <ul style="padding-left: 20px;">
                    <li style="margin-bottom: 8px;">✅ Complete shop management solution</li>
                    <li style="margin-bottom: 8px;">📈 Track sales and inventory in real-time</li>
                    <li style="margin-bottom: 8px;">🧾 Generate professional bills and invoices</li>
                    <li style="margin-bottom: 8px;">👥 Customer management system</li>
                    <li style="margin-bottom: 8px;">🏛️ GST compliant reporting</li>
                    <li style="margin-bottom: 8px;">📱 Mobile-friendly interface</li>
                    <li style="margin-bottom: 8px;">🔒 Secure cloud backups</li>
                </ul>
                <div style="text-align: center; margin-top: 15px;">
                    <img src="https://cdn-icons-png.flaticon.com/512/2933/2933245.png" style="height: 60px; margin: 0 5px;" class="hover-grow">
                    <img src="https://cdn-icons-png.flaticon.com/512/3143/3143471.png" style="height: 60px; margin: 0 5px;" class="hover-grow">
                    <img src="https://cdn-icons-png.flaticon.com/512/2936/2936886.png" style="height: 60px; margin: 0 5px;" class="hover-grow">
                </div>
            </div>
            """, unsafe_allow_html=True)
                  
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
    <div class='info-card glow-on-hover'>
        <h4 class="gradient-text">👨‍💻 About <strong>Manas Borse</strong></h4>
        <ul style="padding-left: 20px;">
            <li style="margin-bottom: 5px;">🎓 <strong>BTech CS student</strong> at NMIMS Shirpur</li>
            <li style="margin-bottom: 5px;">💻 Proficient in <strong>Python, SQL, R,</strong> and exploring Java & JavaScript</li>
            <li style="margin-bottom: 5px;">📊 Skilled in <strong>data analysis, Power BI, and machine learning</strong></li>
            <li style="margin-bottom: 5px;">🚀 <strong>Founder of Bizzence</strong> – a personal Smart Biling System</li>
            <li style="margin-bottom: 5px;">🧠 Passionate about promoting entrepreneurial mindset & self-awareness</li>
            <li style="margin-bottom: 5px;">🏆 Completed a <strong>Data Science course at IIT Bombay</strong> and multiple bootcamps</li>
            <li style="margin-bottom: 5px;">🩺 Created <strong>MediPredixt</strong> (health ML app) and Netflix dashboard</li>
            <li style="margin-bottom: 5px;">🤝 Collaborates with student clubs and leads teams</li>
            <li style="margin-bottom: 5px;">📬 <strong>Contact for Collaboration:</strong> <a href='mailto:manasborse7@gmail.com' style='color: #2E86C1;'>manasborse7@gmail.com</a></li>
            <li style="margin-bottom: 5px;">🌐 <strong>Check out MediPredixt:</strong> <a href='https://medipredict-manas.up.railway.app' target='_blank' style='color: #2E86C1;'>medipredict-manas.up.railway.app</a></li>
        </ul>
        <div style="text-align: center; margin-top: 15px;">
            <a href="https://www.linkedin.com/in/manas-borse-485028257/" target="_blank"><img src="https://cdn-icons-png.flaticon.com/512/3536/3536505.png" style="height: 30px; margin: 0 5px;" class="hover-grow"></a>
            <a href="https://github.com/manasborse7125" target="_blank"><img src="https://cdn-icons-png.flaticon.com/512/733/733553.png" style="height: 30px; margin: 0 5px;" class="hover-grow"></a>
            <a href="https://twitter.com/manasborse7" target="_blank"><img src="https://cdn-icons-png.flaticon.com/512/733/733579.png" style="height: 30px; margin: 0 5px;" class="hover-grow"></a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Footer with gradient
    st.markdown("""
    <div class='footer'>
        <p>© 2025 EasyVyapar | <a href='#'>Privacy Policy</a> | <a href='mailto:manasborse7@gmail.com'>Contact Us</a> | <a href='#'>Terms of Service</a></p>
        <p style="margin-top: 5px; font-weight: 500;">Innovated & Engineered by <strong>Manas Borse</strong> 💡</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
