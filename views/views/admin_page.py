import streamlit as st
from database import add_property, add_vendor

def show_admin_panel():
    st.markdown("""
        <style>
        .admin-card {
            background: #ffffff;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
            border: 1px solid #e2e8f0;
            border-top: 4px solid #1e3a8a;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h2 style="color: #1e3a8a; font-weight:700;">🔐 Admin Control Panel</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748b;">Upload new listings and verify partners directly to the live database.</p>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🏢 Add New Property", "🛠️ Add New Vendor"])

    # --- PROPERTY UPLOAD FORM ---
    with tab1:
        st.markdown('<div class="admin-card">', unsafe_allow_html=True)
        with st.form("property_form", clear_on_submit=True):
            st.subheader("Property Details")
            
            p_name = st.text_input("Property Name", placeholder="e.g., Firstchoice Premium Plot")
            
            col1, col2 = st.columns(2)
            p_type = col1.selectbox("Property Type", ["Plot", "Flat", "Villa", "Commercial"])
            p_loc = col2.selectbox("Location", ["New Amar Nagar", "Wardha Road", "Sitabuldi", "Dharampeth"])
            
            col3, col4 = st.columns(2)
            p_budget = col3.number_input("Budget (₹ Lakhs)", min_value=1, max_value=1000, value=25)
            p_facing = col4.selectbox("Facing", ["East", "West", "North", "South"])
            
            col5, col6 = st.columns(2)
            p_rera = col5.radio("RERA Approved?", ["Yes", "No"], horizontal=True)
            p_status = col6.selectbox("Status", ["Ready to Move", "Under Construction"])

            submitted_prop = st.form_submit_button("🚀 Upload Property to Live Database", type="primary", use_container_width=True)

            if submitted_prop:
                if p_name.strip() == "":
                    st.error("Please enter a property name.")
                else:
                    new_prop_data = {
                        "Property_Name": p_name,
                        "Type": p_type,
                        "Location": p_loc,
                        "Budget_Lakhs": p_budget,
                        "Facing": p_facing,
                        "RERA_Approved": p_rera,
                        "Status": p_status
                    }
                    if add_property(new_prop_data):
                        st.success(f"✅ '{p_name}' successfully added to the live database!")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- VENDOR UPLOAD FORM ---
    with tab2:
        st.markdown('<div class="admin-card">', unsafe_allow_html=True)
        with st.form("vendor_form", clear_on_submit=True):
            st.subheader("Vendor / Partner Details")
            
            v_name = st.text_input("Vendor/Company Name", placeholder="e.g., Rahul Architects")
            
            col1, col2 = st.columns(2)
            v_cat = col1.selectbox("Category", ["Architect", "Contractor", "Painter", "Interior Designer", "Hardware", "Vastu / Priest", "Plumber", "Fabricator"])
            v_loc = col2.selectbox("Location", ["New Amar Nagar", "Wardha Road", "Sitabuldi", "Dharampeth"])
            
            col3, col4 = st.columns(2)
            v_exp = col3.number_input("Experience (Years)", min_value=0, max_value=50, value=5)
            v_rating = col4.slider("Initial Rating", 1.0, 5.0, 4.5, 0.1)
            
            v_verified = st.radio("Is this a Verified Partner?", ["Yes", "No"], horizontal=True)

            submitted_vendor = st.form_submit_button("🚀 Register Vendor to Live Database", type="primary", use_container_width=True)

            if submitted_vendor:
                if v_name.strip() == "":
                    st.error("Please enter a vendor name.")
                else:
                    new_vendor_data = {
                        "Vendor_Name": v_name,
                        "Category": v_cat,
                        "Location": v_loc,
                        "Experience_Years": v_exp,
                        "Rating": v_rating,
                        "Verified": v_verified
                    }
                    if add_vendor(new_vendor_data):
                        st.success(f"✅ '{v_name}' successfully registered to the live ecosystem!")
        st.markdown('</div>', unsafe_allow_html=True)
