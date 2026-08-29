import streamlit as st
# Import all your modules
from views import property_page, vendor_page, advanced_features, admin_page

st.set_page_config(page_title="PropertyHub Premium", layout="wide", initial_sidebar_state="expanded")

# ... (Keep your exact same CSS styling from previous steps here) ...

def show_home():
    # ... (Keep your exact same show_home code here) ...
    pass

def main():
    st.sidebar.markdown("<h3 style='color:#0f172a; font-weight:700;'>🌟 Navigation Menu</h3>", unsafe_allow_html=True)
    
    # Added "🔐 Admin Panel" to the menu
    menu = [
        "🏠 Home (Dashboard)", 
        "🏢 Property Listings", 
        "🛠️ Vendor Ecosystem", 
        "✨ Advanced Features", 
        "🔐 Admin Panel"
    ]
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
    elif choice == "🔐 Admin Panel":
        admin_page.show_admin_panel()

if __name__ == "__main__":
    main()
