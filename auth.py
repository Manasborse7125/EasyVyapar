import streamlit as st
import sqlite3
import hashlib
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="EasyVyapar",
    page_icon="🛒",
    layout="wide",  # Changed to wide for better space utilization
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-family: 'Trebuchet MS', sans-serif;
        text-align: right;
        color: #2E86C1;
        margin-top: 0;
        padding-top: 0;
        margin-bottom: 0;
    }
    .subheader {
        font-size: 1.2rem;
        text-align: right;
        font-style: italic;
        color: #5D6D7E;
        margin-bottom: 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #F8F9F9;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        padding-left: 20px;
        padding-right: 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2E86C1;
        color: white;
    }
    div[data-testid="stForm"] {
        border: 1px solid #E5E8E8;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    div.stButton > button {
        width: 100%;
        font-weight: bold;
        height: 3em;
        background-color: #2E86C1;
        color: white;
    }
    div.stButton > button:hover {
        background-color: #1A5276;
        color: white;
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
    .info-card {
        background-color: #EBF5FB;
        border-left: 5px solid #3498DB;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
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
        background-color: #EBF5FB;
        border-radius: 10px;
        margin-right: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .form-container {
        overflow-y: auto;
        max-height: calc(100vh - 150px);
        padding-right: 10px;
    }
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Function to hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Initialize the SQLite database
def init_db():
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
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

# Add new user to database
def add_user(username, phone, city, state, email, password):
    conn = sqlite3.connect("easy_users.db")
    cursor = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (username, phone, city, state, email, hash_password(password), created_at))
    conn.commit()
    conn.close()

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
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    data = cursor.fetchone()
    conn.close()
    return data

# Main App
def main():
    init_db()
    # App header
    st.markdown("<h1 class='main-header'>💰 EasyVyapar</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subheader'>Apka Dukaan Ka Digital Saathi.</p>", unsafe_allow_html=True)
    
    # Create two columns: one for image, one for login/signup
    left_col, right_col = st.columns([3, 5])
    
    # Image column
    with left_col:
        st.markdown("""
        <div class="image-container">
            <img src="https://pplx-res.cloudinary.com/image/upload/v1747653492/gpt4o_images/vol0mmhllxbbk1maqwll.png" alt="TeenTreasure" style="max-width: 100%; max-height: 500%; object-fit: contain; border-radius: 10px;">
        </div>
        """, unsafe_allow_html=True)
        st.write("") 
        st.write("")
        st.write("")
        st.write("")
        
        st.markdown("""
        <div class="image-container">
            <img src="https://quickbooks.intuit.com/oidam/intuit/sbseg/en_us/Blog/Graphic/what-is-billing-system-header-image-us-en.png" alt="TeenTreasure" style="max-width: 100%; max-height: 500%; object-fit: contain; border-radius: 10px;">
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        st.write("") 
        st.write("") 
        st.write("") 
        # st.write("") 
        # st.write("")
        # st.write("")
        
        st.markdown("""
        <div class="image-container">
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
        
        # Create tabs for Login and Sign Up
        tab1, tab2 = st.tabs(["📝 Login", "✨ Sign Up"])
        
        # Login Tab
        with tab1:
            with st.form("login_form"):
                st.subheader("Welcome Back! 👋")
                
                username = st.text_input("Username", key="login_username")
                password = st.text_input("Password", type='password', key="login_password")
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    remember_me = st.checkbox("Remember Me")
                with col2:
                    st.markdown("<div style='text-align: right;'><a href='#'>Forgot Password?</a></div>", unsafe_allow_html=True)
                
                submit_button = st.form_submit_button("Login")
                
                if submit_button:
                    if not username or not password:
                        st.session_state.login_status = "empty"
                    else:
                        result = login_user(username, password)
                        if result:
                            st.session_state.login_status = "success"
                            st.session_state.current_user = username
                        else:
                            st.session_state.login_status = "error"
            
            # Display login status message outside the form
            if st.session_state.login_status == "success":
                st.switch_page("pages/app.py")
                st.markdown(f"""
                <div class='success-message'>
                    <h3>🎉 Login Successful!</h3>
                    <p>Welcome back, {st.session_state.current_user}! You're now signed in to your TeenTreasure account.</p>
                </div>
                """, unsafe_allow_html=True)
                
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
                
            # Additional information
            st.markdown("""
            <div class='info-card'>
                <h4>📱 Download the EasyVyapar App (Available Shortly)</h4>
                <p>Access your finances on the go with our mobile app available for iOS and Android.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Sign Up Tab
        with tab2:
            with st.form("signup_form"):
                st.subheader("Create Your Account 🚀")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    username = st.text_input("Username", key="signup_username", 
                                            placeholder="Choose a unique username")
                    city = st.text_input("City", key="signup_city",
                                        placeholder="Your city")
                    email = st.text_input("Email", key="signup_email",
                                         placeholder="your.email@example.com")
                
                with col2:
                    phone = st.text_input("Phone Number", key="signup_phone",
                                         placeholder="(123) 456-7890")
                    state = st.text_input("State", key="signup_state",
                                         placeholder="Your state")
                    
                password = st.text_input("Create Password", type='password', key="signup_password",
                                        placeholder="Minimum 8 characters")
                confirm_password = st.text_input("Confirm Password", type='password', key="signup_confirm",
                                               placeholder="Re-enter your password")
                
                terms = st.checkbox("I agree to the Terms and Conditions.")
                
                signup_button = st.form_submit_button("Create Account")
                
                if signup_button:
                    if not (username and phone and city and state and email and password and confirm_password):
                        st.session_state.signup_status = "empty"
                    elif password != confirm_password:
                        st.session_state.signup_status = "password_mismatch"
                    elif not terms:
                        st.session_state.signup_status = "terms_not_accepted"
                    elif username_exists(username):
                        st.session_state.signup_status = "username_exists"
                    else:
                        try:
                            add_user(username, phone, city, state, email, password)
                            st.session_state.signup_status = "success"
                        except Exception as e:
                            st.session_state.signup_status = "error"
                            st.session_state.error_message = str(e)
                        
            # Display signup status message outside the form
            if st.session_state.signup_status == "success":
                st.markdown("""
                <div class='success-message'>
                    <h3>✅ Account Created Successfully!</h3>
                    <p>Congratulations! Your TeenTreasure account has been created. You can now login using your credentials.</p>
                </div>
                """, unsafe_allow_html=True)
            elif st.session_state.signup_status == "empty":
                st.markdown("""
                <div class='error-message'>
                    <h3>⚠️ Missing Information</h3>
                    <p>Please fill in all required fields to create your account.</p>
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
                st.switch_page("pages/main.py")
                
            # Show signup benefits
            st.markdown("""
            <div class='info-card'>
                <h4>✨ Benefits of EasyVyapar Account</h4>
                <ul>
                    <li>Track your savings and spending habits</li>
                    <li>Set financial goals and watch your progress</li>
                    <li>Learn money management skills through interactive tutorials</li>
                    <li>Earn rewards for meeting saving targets</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
                  
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
    <div class='info-card'>
        <h4>👨‍💻 About Manas Borse</h4>
        <ul>
            <li>📚 BTech CS student at NMIMS Shirpur</li>
            <li>🐍 Proficient in <strong>Python, SQL, R,</strong> and exploring Java & JavaScript</li>
            <li>📊 Skilled in <strong>data analysis, Power BI, and machine learning</strong></li>
            <li>💡 Founder of <strong>EasyVyapar</strong> – a personal Smart Biling System</li>
            <li>🧠 Passionate about promoting entrepreneurial mindset & self-awareness</li>
            <li>🎓 Completed a Data Science course at IIT Bombay and multiple bootcamps</li>
            <li>🚀 Created hands-on projects like MediPredixt (health ML app) and Netflix dashboard</li>
            <li>🤝 Collaborates with student clubs, leads teams, and engages in real-world problem-solving</li>
            <li>📬 Contact for Collaboration: <a href='mailto:manasborse7@gmail.com'>manasborse7@gmail.com</a></li>
            <li>🌐 Check out <strong>MediPredixt</strong>: <a href='https://medipredict-manas.up.railway.app' target='_blank'>medipredict-manas.up.railway.app</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class='footer'>
        <p>© 2025 TeenTreasure | Privacy Policy | <a href='mailto:manasborse7@gmail.com'>Contact Us</a> </p>
        Innovated & Engineered by Manas Borse 💡
    </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()