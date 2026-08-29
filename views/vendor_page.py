import streamlit as st
import pandas as pd
from database import fetch_all_vendors

def show_vendor_ecosystem():
    st.markdown("""
        <style>
        .vendor-card {
            background: #ffffff;
            border-left: 6px solid #0f766e;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
            margin-bottom: 15px;
            transition: all 0.3s ease-in-out;
            border-top: 1px solid #f1f5f9;
            border-right: 1px solid #f1f5f9;
            border-bottom: 1px solid #f1f5f9;
        }
        .vendor-card:hover {
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
            transform: translateX(4px);
        }
        .verified-tag { color: #059669; font-weight: 600; font-size: 0.85rem; background: #d1fae5; padding: 4px 10px; border-radius: 20px;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h2 style="color: #0f766e; font-weight:700;">🛠️ Vendor Ecosystem</h2>', unsafe_allow_html=True)
    
    # 1. Fetch Live Data
    raw_data = fetch_all_vendors()
    
    if not raw_data:
        st.info("No vendors found in the database. Please register vendors via the Admin Panel.")
        return

    df = pd.DataFrame(raw_data)
    
    # 2. UI Filters (Dynamic)
    col1, col2, col3 = st.columns(3)
    category_filter = col1.selectbox("Select Service", ["All"] + list(df["Category"].unique()))
    location_filter = col2.selectbox("Location", ["All"] + list(df["Location"].unique()))
    
    max_exp = int(df["Experience_Years"].max()) if not df.empty else 30
    exp_filter = col3.slider("Min Experience (Years)", 0, max_exp, 2)
    
    with st.expander("⭐ Trust & Quality Filters"):
        col4, col5 = st.columns(2)
        rating_filter = col4.slider("Minimum Rating (Stars)", 1.0, 5.0, 4.0, 0.1)
        verified_filter = col5.checkbox("Show Verified Partners Only", value=True)

    st.divider()
    
    # 3. Filter Logic
    filtered_vendors = df.copy()
    if category_filter != "All": filtered_vendors = filtered_vendors[filtered_vendors["Category"] == category_filter]
    if location_filter != "All": filtered_vendors = filtered_vendors[filtered_vendors["Location"] == location_filter]
    filtered_vendors = filtered_vendors[filtered_vendors["Experience_Years"] >= exp_filter]
    filtered_vendors = filtered_vendors[filtered_vendors["Rating"] >= rating_filter]
    if verified_filter: filtered_vendors = filtered_vendors[filtered_vendors["Verified"] == "Yes"]
        
    st.markdown(f"<p style='color:#64748b; font-weight:600;'>{len(filtered_vendors)} Professionals Found</p>", unsafe_allow_html=True)
    
    # 4. Render Vendor Cards
    for _, row in filtered_vendors.iterrows():
        verified_html = '<span class="verified-tag">✓ Verified Partner</span>' if row.get('Verified') == 'Yes' else ''
        st.markdown(f"""
        <div class="vendor-card">
            <h4 style="margin:0; color:#0f172a; font-size:1.2rem; font-weight: 700;">{row.get('Vendor_Name', 'N/A')}</h4>
            <p style="margin:6px 0; color:#64748b; font-size: 0.95rem;">🛠️ {row.get('Category', 'N/A')} | 📍 {row.get('Location', 'N/A')}</p>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:12px;">
                <span style="color:#eab308; font-weight:700;">⭐ {row.get('Rating', 0)}</span>
                <span style="color:#475569; font-size:0.95rem; font-weight: 500;">💼 {row.get('Experience_Years', 0)} Years Exp.</span>
                {verified_html}
            </div>
        </div>
        """, unsafe_allow_html=True)
