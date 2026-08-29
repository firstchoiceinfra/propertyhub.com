import streamlit as st
import pandas as pd
import json
import firebase_admin
from firebase_admin import credentials, firestore

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION (Must be the first command)
# ---------------------------------------------------------
st.set_page_config(page_title="PropertyHub Premium", layout="wide", initial_sidebar_state="expanded")


# ---------------------------------------------------------
# 2. FIREBASE DATABASE CONNECTION (Foolproof Method)
# ---------------------------------------------------------
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        try:
            if "FIREBASE_JSON" in st.secrets:
                cred_dict = json.loads(st.secrets["FIREBASE_JSON"])
            elif "firebase" in st.secrets:
                cred_dict = dict(st.secrets["firebase"])
                if "private_key" in cred_dict:
                    cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n").replace("\\\\n", "\n")
            else:
                st.error("🔥 Firebase secrets missing in Streamlit Cloud!")
                st.stop()
                
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error("🔥 Firebase Connection Error! कृपया असली JSON डेटा Secrets में डालें।")
            st.write(f"Details: {e}")
            st.stop()
    return firestore.client()

db = init_firebase()

# Database Helper Functions
def fetch_all_properties():
    return [doc.to_dict() for doc in db.collection('properties').stream()]

def fetch_all_vendors():
    return [doc.to_dict() for doc in db.collection('vendors').stream()]

def add_property(prop_data):
    try:
        db.collection('properties').add(prop_data)
        return True
    except Exception as e:
        st.error(f"Error adding property: {e}")
        return False

def add_vendor(vendor_data):
    try:
        db.collection('vendors').add(vendor_data)
        return True
    except Exception as e:
        st.error(f"Error adding vendor: {e}")
        return False


# ---------------------------------------------------------
# 3. PREMIUM UI & CSS STYLING
# ---------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%); border-right: 1px solid #e2e8f0; }
    div.stRadio > div { background-color: transparent; gap: 12px; }
    div.stRadio > div > label { background-color: #ffffff; padding: 12px 20px; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); transition: all 0.3s ease; border: 1px solid #e2e8f0; cursor: pointer; }
    div.stRadio > div > label:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.08); border-color: #3b82f6; }
    
    /* Titles */
    .premium-title { background: linear-gradient(45deg, #1e3a8a, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 2.8rem; margin-bottom: 5px; }
    
    /* KPI Cards */
    .kpi-card { background: #ffffff; padding: 24px; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); text-align: center; border-top: 4px solid #3b82f6; transition: transform 0.3s ease; }
    .kpi-card:hover { transform: translateY(-5px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
    .kpi-value { font-size: 2.5rem; font-weight: 700; color: #0f172a; line-height: 1.2; }
    .kpi-label { color: #64748b; font-size: 1.05rem; font-weight: 600; margin-top: 8px; }

    /* Property & Vendor Cards */
    .property-card, .vendor-card, .admin-card {
        background: #ffffff; border-radius: 12px; padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); border: 1px solid #f1f5f9;
        transition: all 0.3s ease; margin-bottom: 20px;
    }
    .property-card:hover { transform: translateY(-5px); box-shadow: 0 15px 25px -5px rgba(0,0,0,0.1); border-color: #3b82f6; }
    .vendor-card { border-left: 6px solid #0f766e; }
    .vendor-card:hover { transform: translateX(4px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
    .admin-card { border-top: 4px solid #1e3a8a; }
    
    /* Badges & Tags */
    .badge-rera { background: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 600; margin-left: 8px;}
    .badge-status { background: #e0e7ff; color: #3730a3; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 600; }
    .price-tag { color: #1e3a8a; font-size: 1.5rem; font-weight: 700; margin: 12px 0; }
    .verified-tag { color: #059669; font-weight: 600; font-size: 0.85rem; background: #d1fae5; padding: 4px 10px; border-radius: 20px;}
    </style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# 4. MODULE 1: HOME DASHBOARD
# ---------------------------------------------------------
def show_home():
    st.markdown('<h1 class="premium-title">PropertyHub Ecosystem</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748b; font-size:1.2rem; font-weight: 400; margin-bottom: 2rem;">A premium one-stop solution from finding properties to building and settling in.</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown('<div class="kpi-card"><div class="kpi-value">Live</div><div class="kpi-label">Firebase Connected</div></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="kpi-card" style="border-top-color:#10b981;"><div class="kpi-value">340+</div><div class="kpi-label">Verified Partners</div></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="kpi-card" style="border-top-color:#f59e0b;"><div class="kpi-value">Zero</div><div class="kpi-label">Flicker Navigation</div></div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# 5. MODULE 2: PROPERTY LISTINGS
# ---------------------------------------------------------
def show_property_listings():
    st.markdown('<h2 style="color: #1e3a8a; font-weight:700;">🏢 Property Listings</h2>', unsafe_allow_html=True)
    
    raw_data = fetch_all_properties()
    if not raw_data:
        st.info("No properties found. Please add listings via the Admin Panel.")
        return

    df = pd.DataFrame(raw_data)
    
    col1, col2, col3 = st.columns(3)
    loc_filter = col1.selectbox("Location", ["All"] + list(df["Location"].unique()))
    type_filter = col2.selectbox("Property Type", ["All"] + list(df["Type"].unique()))
    
    min_budget = int(df["Budget_Lakhs"].min()) if not df.empty else 10
    max_budget = int(df["Budget_Lakhs"].max()) if not df.empty else 200
    budget_filter = col3.slider("Budget (₹ Lakhs)", min_budget, max_budget, (min_budget, max_budget))
    
    with st.expander("✨ Advanced Filters"):
        col4, col5, col6 = st.columns(3)
        rera_filter = col4.radio("RERA Approved?", ["All", "Yes", "No"], horizontal=True)
        facing_filter = col5.selectbox("Facing", ["All", "East", "West", "North", "South"])
        status_filter = col6.selectbox("Project Status", ["All", "Ready to Move", "Under Construction"])
        
    st.divider()
    
    filtered_df = df.copy()
    if loc_filter != "All": filtered_df = filtered_df[filtered_df["Location"] == loc_filter]
    if type_filter != "All": filtered_df = filtered_df[filtered_df["Type"] == type_filter]
    filtered_df = filtered_df[(filtered_df["Budget_Lakhs"] >= budget_filter[0]) & (filtered_df["Budget_Lakhs"] <= budget_filter[1])]
    if rera_filter != "All": filtered_df = filtered_df[filtered_df["RERA_Approved"] == rera_filter]
    if facing_filter != "All": filtered_df = filtered_df[filtered_df["Facing"] == facing_filter]
    if status_filter != "All": filtered_df = filtered_df[filtered_df["Status"] == status_filter]
        
    st.markdown(f"<p style='color:#64748b; font-weight:600;'>{len(filtered_df)} Properties Found</p>", unsafe_allow_html=True)
    
    for _, row in filtered_df.iterrows():
        rera_badge = '<span class="badge-rera">✅ RERA Approved</span>' if row.get('RERA_Approved') == 'Yes' else ''
        st.markdown(f"""
        <div class="property-card">
            <h3 style="margin:0; color:#0f172a;">{row.get('Property_Name', 'N/A')}</h3>
            <p style="margin:8px 0; color:#64748b;">📍 {row.get('Location', 'N/A')} | 📐 {row.get('Type', 'N/A')} | 🧭 {row.get('Facing', 'N/A')} Facing</p>
            <div class="price-tag">₹ {row.get('Budget_Lakhs', 0)} Lakhs</div>
            <div style="margin-top: 10px;">
                <span class="badge-status">{row.get('Status', 'N/A')}</span> {rera_badge}
            </div>
        </div>
        """, unsafe_allow_html=True)


# ---------------------------------------------------------
# 6. MODULE 3: VENDOR ECOSYSTEM
# ---------------------------------------------------------
def show_vendor_ecosystem():
    st.markdown('<h2 style="color: #0f766e; font-weight:700;">🛠️ Vendor Ecosystem</h2>', unsafe_allow_html=True)
    
    raw_data = fetch_all_vendors()
    if not raw_data:
        st.info("No vendors found. Please register vendors via the Admin Panel.")
        return

    df = pd.DataFrame(raw_data)
    
    col1, col2, col3 = st.columns(3)
    category_filter = col1.selectbox("Select Service", ["All"] + list(df["Category"].unique()))
    location_filter = col2.selectbox("Location", ["All"] + list(df["Location"].unique()))
    max_exp = int(df["Experience_Years"].max()) if not df.empty else 30
    exp_filter = col3.slider("Min Experience (Years)", 0, max_exp, 0)
    
    with st.expander("⭐ Trust Filters"):
        rating_filter = st.slider("Minimum Rating", 1.0, 5.0, 4.0, 0.1)
        verified_filter = st.checkbox("Verified Partners Only", value=True)

    st.divider()
    
    filtered_vendors = df.copy()
    if category_filter != "All": filtered_vendors = filtered_vendors[filtered_vendors["Category"] == category_filter]
    if location_filter != "All": filtered_vendors = filtered_vendors[filtered_vendors["Location"] == location_filter]
    filtered_vendors = filtered_vendors[filtered_vendors["Experience_Years"] >= exp_filter]
    filtered_vendors = filtered_vendors[filtered_vendors["Rating"] >= rating_filter]
    if verified_filter: filtered_vendors = filtered_vendors[filtered_vendors["Verified"] == "Yes"]
        
    st.markdown(f"<p style='color:#64748b; font-weight:600;'>{len(filtered_vendors)} Professionals Found</p>", unsafe_allow_html=True)
    
    for _, row in filtered_vendors.iterrows():
        verified_html = '<span class="verified-tag">✓ Verified Partner</span>' if row.get('Verified') == 'Yes' else ''
        st.markdown(f"""
        <div class="vendor-card">
            <h4 style="margin:0; color:#0f172a; font-size:1.2rem; font-weight: 700;">{row.get('Vendor_Name', 'N/A')}</h4>
            <p style="margin:6px 0; color:#64748b;">🛠️ {row.get('Category', 'N/A')} | 📍 {row.get('Location', 'N/A')}</p>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:12px;">
                <span style="color:#eab308; font-weight:700;">⭐ {row.get('Rating', 0)}</span>
                <span style="color:#475569; font-weight: 500;">💼 {row.get('Experience_Years', 0)} Years Exp.</span>
                {verified_html}
            </div>
        </div>
        """, unsafe_allow_html=True)


# ---------------------------------------------------------
# 7. MODULE 4: ADMIN PANEL
# ---------------------------------------------------------
def show_admin_panel():
    st.markdown('<h2 style="color: #1e3a8a; font-weight:700;">🔐 Admin Control Panel</h2>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🏢 Add New Property", "🛠️ Add New Vendor"])

    with tab1:
        st.markdown('<div class="admin-card">', unsafe_allow_html=True)
        with st.form("property_form", clear_on_submit=True):
            p_name = st.text_input("Property Name")
            col1, col2 = st.columns(2)
            p_type = col1.selectbox("Property Type", ["Plot", "Flat", "Villa", "Commercial"])
            p_loc = col2.text_input("Location", placeholder="e.g., New Amar Nagar")
            col3, col4 = st.columns(2)
            p_budget = col3.number_input("Budget (₹ Lakhs)", min_value=1, max_value=1000, value=25)
            p_facing = col4.selectbox("Facing", ["East", "West", "North", "South"])
            col5, col6 = st.columns(2)
            p_rera = col5.radio("RERA Approved?", ["Yes", "No"], horizontal=True)
            p_status = col6.selectbox("Status", ["Ready to Move", "Under Construction"])

            if st.form_submit_button("🚀 Upload Property", type="primary", use_container_width=True):
                if p_name.strip() and p_loc.strip():
                    if add_property({"Property_Name": p_name, "Type": p_type, "Location": p_loc, "Budget_Lakhs": p_budget, "Facing": p_facing, "RERA_Approved": p_rera, "Status": p_status}):
                        st.success("✅ Property uploaded to Firebase successfully!")
                else:
                    st.error("Please fill Name and Location.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="admin-card">', unsafe_allow_html=True)
        with st.form("vendor_form", clear_on_submit=True):
            v_name = st.text_input("Vendor Name")
            col1, col2 = st.columns(2)
            v_cat = col1.selectbox("Category", ["Architect", "Contractor", "Painter", "Interior Designer", "Hardware", "Vastu / Priest", "Plumber", "Fabricator"])
            v_loc = col2.text_input("Location", placeholder="e.g., Wardha Road")
            col3, col4 = st.columns(2)
            v_exp = col3.number_input("Experience (Years)", min_value=0, max_value=50, value=5)
            v_rating = col4.slider("Rating", 1.0, 5.0, 4.5, 0.1)
            v_verified = st.radio("Verified Partner?", ["Yes", "No"], horizontal=True)

            if st.form_submit_button("🚀 Register Vendor", type="primary", use_container_width=True):
                if v_name.strip() and v_loc.strip():
                    if add_vendor({"Vendor_Name": v_name, "Category": v_cat, "Location": v_loc, "Experience_Years": v_exp, "Rating": v_rating, "Verified": v_verified}):
                        st.success("✅ Vendor registered to Firebase successfully!")
                else:
                    st.error("Please fill Name and Location.")
        st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# 8. MASTER ROUTER (Zero-Flicker Navigation)
# ---------------------------------------------------------
def main():
    st.sidebar.markdown("<h3 style='color:#0f172a; font-weight:700;'>🌟 Navigation Menu</h3>", unsafe_allow_html=True)
    
    menu = [
        "🏠 Home (Dashboard)", 
        "🏢 Property Listings", 
        "🛠️ Vendor Ecosystem", 
        "🔐 Admin Panel"
    ]
    choice = st.sidebar.radio("", menu)
    
    st.sidebar.write("---")
    st.sidebar.markdown("<small style='color:#64748b; font-weight:500;'>⚡ Single-Page Architecture</small>", unsafe_allow_html=True)

    if choice == "🏠 Home (Dashboard)":
        show_home()
    elif choice == "🏢 Property Listings":
        show_property_listings()
    elif choice == "🛠️ Vendor Ecosystem":
        show_vendor_ecosystem()
    elif choice == "🔐 Admin Panel":
        show_admin_panel()

if __name__ == "__main__":
    main()
