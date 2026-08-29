import streamlit as st
# Import the new advanced_features module
from views import property_page, vendor_page, advanced_features

st.set_page_config(page_title="PropertyHub Premium", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%); border-right: 1px solid #e2e8f0; }
    div.stRadio > div { background-color: transparent; gap: 12px; }
    div.stRadio > div > label { background-color: #ffffff; padding: 12px 20px; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); transition: all 0.3s ease; border: 1px solid #e2e8f0; cursor: pointer; }
    div.stRadio > div > label:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.08); border-color: #3b82f6; }
    .premium-title { background: linear-gradient(45deg, #1e3a8a, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 2.8rem; margin-bottom: 5px; letter-spacing: -0.5px; }
    .kpi-card { background: #ffffff; padding: 24px; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); text-align: center; border-top: 4px solid #3b82f6; transition: transform 0.3s ease; }
    .kpi-card:hover { transform: translateY(-5px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
    .kpi-value { font-size: 2.5rem; font-weight: 700; color: #0f172a; line-height: 1.2; }
    .kpi-label { color: #64748b; font-size: 1.05rem; font-weight: 600; margin-top: 8px; }
    </style>
""", unsafe_allow_html=True)

def show_home():
    st.markdown('<h1 class="premium-title">PropertyHub Ecosystem</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748b; font-size:1.2rem; font-weight: 400; margin-bottom: 2rem;">A premium one-stop solution from finding properties to building and settling in.</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown('<div class="kpi-card"><div class="kpi-value">1,250+</div><div class="kpi-label">Premium Properties</div></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="kpi-card" style="border-top-color:#10b981;"><div class="kpi-value">340+</div><div class="kpi-label">Verified Partners</div></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="kpi-card" style="border-top-color:#f59e0b;"><div class="kpi-value">5,000+</div><div class="kpi-label">Happy Customers</div></div>', unsafe_allow_html=True)

def main():
    st.sidebar.markdown("<h3 style='color:#0f172a; font-weight:700;'>🌟 Navigation Menu</h3>", unsafe_allow_html=True)
    
    # Added "✨ Advanced Features" to the menu
    menu = ["🏠 Home (Dashboard)", "🏢 Property Listings", "🛠️ Vendor Ecosystem", "✨ Advanced Features"]
    choice = st.sidebar.radio("", menu)
    
    st.sidebar.write("---")
    st.sidebar.markdown("<small style='color:#64748b; font-weight:500;'>⚡ Single-Page Architecture (Zero Flicker)</small>", unsafe_allow_html=True)

    # Updated Routing Logic
    if choice == "🏠 Home (Dashboard)":
        show_home()
    elif choice == "🏢 Property Listings":
        property_page.show_advanced_filters()
    elif choice == "🛠️ Vendor Ecosystem":
        vendor_page.show_vendor_ecosystem()
    elif choice == "✨ Advanced Features":
        advanced_features.show_advanced_features()

if __name__ == "__main__":
    main()
