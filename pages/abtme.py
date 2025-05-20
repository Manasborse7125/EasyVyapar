import streamlit as st
import base64
from PIL import Image
import requests
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Manas Borse - Portfolio",
    page_icon="🌟",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stApp {
        background-color: #f7f7f7;
    }
    h1, h2, h3 {
        color: #1E3A8A;
    }
    .highlight {
        background-color: #E5EDFF;
        padding: 0.2rem 0.5rem;
        border-radius: 0.3rem;
        font-weight: 500;
    }
    .card {
        background-color: white;
        border-radius: 0.8rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    .sidebar-content {
        text-align: center;
    }
    .project-card {
        background-color: white;
        border-left: 4px solid #1E3A8A;
        padding: 1rem;
        margin-bottom: 0.8rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .skill-chip {
        background-color: #E5EDFF;
        padding: 0.3rem 0.6rem;
        border-radius: 1rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        display: inline-block;
        font-size: 0.8rem;
        color: #1E3A8A;
    }
    .icons {
        font-size: 1.2rem;
        margin-right: 0.5rem;
    }
    .contact-item {
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Create columns for layout
left_col, right_col = st.columns([1, 2])

# Left column - Photo and contact information
with left_col:
    st.markdown('<div class="card sidebar-content">', unsafe_allow_html=True)
    
    # Placeholder for profile image
    st.image("https://media.licdn.com/dms/image/v2/D5603AQEwXxKBmXCH5w/profile-displayphoto-shrink_800_800/B56ZVbVPHHGQAc-/0/1740994058084?e=1753315200&v=beta&t=DY_et5JaAfbPvGOgZAaQM2NbDBE82YfBaq217nEbYwQ", width=250)
    
    st.markdown("### Contact Information")
    st.markdown('<div class="contact-item">📧<a href="manasborse7@gmail.com">manasborse7@gmail.com</a></div>', unsafe_allow_html=True)
    st.markdown('<div class="contact-item">🔗 GitHub: <a href="http://github.com/Manasborse7125">manasborse7125</a></div>', unsafe_allow_html=True)
    st.markdown('<div class="contact-item">📱 Instagram: <a href="https://www.instagram.com/manasborse_xviii/profilecard/?igsh=YThpbnEwdXphcm1j">manasborse_xviii</div>', unsafe_allow_html=True)
    
    st.markdown("### Education")
    st.markdown("🎓 **B.Tech Computer Science**")
    st.markdown("NMIMS Shirpur")
    st.markdown("3nd Year, 5th Semester")
    
    st.markdown("### Quick Links")
    if st.button("Resume"):
        st.write("Resume download functionality will be implemented")
    if st.button("GitHub Projects"):
        st.write("GitHub profile will be linked")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Right column - Content
with right_col:
    # Header
    st.markdown("# Manas Borse")
    st.markdown("## 🌟 Aspiring Data Scientist | Educator | Entrepreneurial Thinker")
    
    # About me section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 👨‍💼 About Me")
    st.markdown("""
    I'm **Manas Borse**, a curious and driven B.Tech Computer Science student at **NMIMS Shirpur**, 
    currently in my 2nd year, 4th semester. I am passionate about exploring the intersection of 
    **data science, education, and entrepreneurial mindset**. My journey is rooted in both technical 
    skill-building and purpose-driven initiatives that aim to inspire change from the ground up.
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Technical Skills
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 👨‍💻 Tech Skills & Learning Path")
    st.markdown("I've been consistently building a strong foundation in programming and data science:")
    
    skills_col1, skills_col2 = st.columns(2)
    
    with skills_col1:
        st.markdown('<div class="skill-chip">Python</div>', unsafe_allow_html=True)
        st.markdown('<div class="skill-chip">R Programming</div>', unsafe_allow_html=True)
        st.markdown('<div class="skill-chip">Machine Learning</div>', unsafe_allow_html=True)
    
    with skills_col2:
        st.markdown('<div class="skill-chip">Power BI</div>', unsafe_allow_html=True)
        st.markdown('<div class="skill-chip">JavaScript & Java</div>', unsafe_allow_html=True)
        st.markdown('<div class="skill-chip">SQL</div>', unsafe_allow_html=True)
    
    st.markdown("""
    * ✅ **Python (60-day journey)** – mastered recursion, loops, match-case, lists, tuples, and sets
    * ✅ **R Programming** – working with vectors, matrices, data frames, and conditional statements
    * ✅ **Machine Learning** – developed projects like a heart disease prediction model and lab test predictor (MediPredixt)
    * ✅ **Power BI** – created dashboards for **Netflix** and **Adidas**, available on GitHub
    * ✅ **JavaScript & Java** – currently learning OOP, DOM, control structures, and Spring MVC
    * ✅ **SQL** – explored Oracle SQL, with plans to integrate databases into real-world applications
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Projects
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🧠 Projects That Matter")
    st.markdown("I believe learning by doing is the best way to grow:")
    
    # Project Cards
    st.markdown('<div class="project-card">', unsafe_allow_html=True)
    st.markdown("""
    A Streamlit web app for predicting diseases using ML algorithms like Logistic Regression & Decision Trees
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="project-card">', unsafe_allow_html=True)
    st.markdown("#### 🎬 Movie Recommendation System")
    st.markdown("""
    Built in Python, allows users to select genres and get curated lists (GUI coming soon!)
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="project-card">', unsafe_allow_html=True)
    st.markdown("#### 💰 TeenTreasure")
    st.markdown("""
    My latest project: a personal financial recorder for teenage students using Streamlit, 
    designed to manage expenses smartly
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="project-card">', unsafe_allow_html=True)
    st.markdown("#### 🌳 Student Record Management (DSA)")
    st.markdown("""
    A hands-on role-play activity using binary search trees for CRUD operations in data structures
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Community Work
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🌱 Purpose-Driven Community Work")
    st.markdown("""
    My journey isn't just about tech. I strongly believe in **experiential learning and self-awareness**:
    
    * 💡 As part of **Let's Enterprise**, I advocate for embedding entrepreneurial thinking and real-world challenges in education
    * 🏫 Volunteered at **Buddhist International School, Nashik** mentoring minority students, working with Siddharth Ingole and Sarthak
    * 🎨 Member of **Saturday 10 AM Club**, managing social media editing and team collaboration under Riya Ma'am and Yug Shah
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Initiatives and Events
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🚀 Initiatives, Events & Ambassadorships")
    st.markdown("""
    * 🎓 Completed a **C++ Bootcamp** by Let's Upgrade, NSDC, and GDG MAD
    * 📊 Attended a **Data Science Course at IIT Bombay** with mentor Sonali Salunke
    * 💼 Engaged in **Next Upgrade's Student Ambassador Program**
    * 💬 Participated in **National Startup Day @ NMIMS Shirpur**, organized by Bhushan Sir and led by Sangram Sir
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Vision
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 💭 Vision")
    st.markdown("""
    I dream of a world where education is not just academic but **transformational**. I'm on a mission to:
    
    * Promote **entrepreneurial thinking** from an early age
    * Help students understand their **values, strengths, and passions**
    * Build tools and platforms that **bridge the gap between learning and real-life challenges**
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Fun Fact
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📌 Fun Fact")
    st.markdown("""
    While I aspire to be a **data scientist**, I also once dreamed of becoming a **train driver** — 
    and that sense of wonder and exploration still drives me today.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 2rem; padding: 1rem; background-color: #E5EDFF; border-radius: 0.5rem;">
    <p>© 2025 Manas Borse | Last Updated: May 2025</p>
</div>
""", unsafe_allow_html=True)

# Add a feature to upload your own photo
st.sidebar.markdown("## Customize Portfolio")
uploaded_file = st.sidebar.file_uploader("Upload your profile photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Process the uploaded image
    image = Image.open(uploaded_file)
    # Update the image in the left column
    with left_col:
        st.image(image, width=250)