import streamlit as st
from views import property_page, vendor_page

# 1. Page Configuration
st.set_page_config(page_title="PropertyHub Premium", layout="wide", initial_sidebar_state="expanded")

# 2. Advanced Premium CSS (No Black, Modern Light Theme)
st.markdown("""
    <style>
    /* Google Font Import */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Premium Sidebar Gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
        border-right: 1px solid #cbd5e1;
    }
    
    /* Styling the Radio Buttons to look like modern tabs */
    div.stRadio > div {
        background-color: transparent;
        gap: 15px;
    }
    div.stRadio > div > label {
        background-color: white;
        padding: 12px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        border: 1px solid #e2e8f0;
        cursor: pointer;
    }
    div.stRadio > div > label:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.1);
        border-color: #3b82f6;
    }

    /* Main Headings */
    .premium-title {
        background: -webkit-linear-gradient(45deg, #1e3a8a, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 5px;
    }
    
    /* Dashboard KPI Cards */
    .kpi-card {
        background: white;
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        text-align: center;
        border-top: 4px solid #3b82f6;
        transition: transform 0.3s;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
    }
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0f172a;
    }
    .kpi-label {
        color: #64748b;
        font-size: 1.1rem;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# --- HOME DASHBOARD ---
def show_home():
    st.markdown('<h1 class="premium-title">प्रॉपर्टी हब इकोसिस्टम</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748b; font-size:1.2rem;">प्रॉपर्टी खोजने से लेकर, घर बनाने और गृह प्रवेश तक का वन-स्टॉप प्रीमियम सॉल्यूशन।</p>', unsafe_allow_html=True)
    
    st.write("---")
    
    # Premium KPI Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="kpi-card"><div class="kpi-value">1,250+</div><div class="kpi-label">प्रीमियम प्रॉपर्टीज़</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="kpi-card"><div style="border-top-color:#10b981;" class="kpi-value">340+</div><div class="kpi-label">वेरिफाइड वेंडर्स</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="kpi-card"><div style="border-top-color:#f59e0b;" class="kpi-value">5,000+</div><div class="kpi-label">हैप्पी कस्टमर्स</div></div>', unsafe_allow_html=True)

# --- MAIN ROUTER ---
def main():
    st.sidebar.markdown("### 🌟 नेविगेशन मेनू")
    
    menu = ["🏠 होम (Dashboard)", "🏢 प्रॉपर्टी लिस्टिंग", "🛠️ वेंडर इकोसिस्टम"]
    choice = st.sidebar.radio("", menu)
    
    st.sidebar.write("---")
    st.sidebar.markdown("<small style='color:#64748b;'>⚡ सिंगल-पेज आर्किटेक्चर (ज़ीरो फ्लिकर)</small>", unsafe_allow_html=True)

    # Seamless Routing
    if choice == "🏠 होम (Dashboard)":
        show_home()
    elif choice == "🏢 प्रॉपर्टी लिस्टिंग":
        property_page.show_advanced_filters()
    elif choice == "🛠️ वेंडर इकोसिस्टम":
        vendor_page.show_vendor_ecosystem()

if __name__ == "__main__":
    main()
