import streamlit as st
import pandas as pd

dummy_vendors = pd.DataFrame({
    "Vendor_Name": ["Rahul Architects", "Shree Ram Builders", "A1 Painters", "Modern Interiors", "Gupta Hardware", "Pandit Ji Vastu"],
    "Category": ["आर्किटेक्ट", "कॉन्ट्रैक्टर", "पेंटर", "इंटीरियर डिजाइनर", "हार्डवेयर", "वास्तु / पुजारी"],
    "Location": ["New Amar Nagar", "Wardha Road", "Sitabuldi", "Dharampeth", "New Amar Nagar", "New Amar Nagar"],
    "Experience_Years": [10, 15, 5, 8, 20, 25],
    "Rating": [4.8, 4.5, 4.1, 4.9, 4.3, 5.0],
    "Verified": ["Yes", "Yes", "No", "Yes", "Yes", "Yes"]
})

def show_vendor_ecosystem():
    st.markdown("""
        <style>
        .vendor-card {
            background: #ffffff;
            border-left: 5px solid #0f766e;
            border-radius: 8px;
            padding: 15px 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 12px;
            transition: all 0.2s ease-in-out;
        }
        .vendor-card:hover {
            box-shadow: 0 8px 15px rgba(0,0,0,0.1);
            transform: scale(1.01);
        }
        .verified-tag { color: #059669; font-weight: 700; font-size: 0.9rem; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h2 style="color: #0f766e; font-weight:700;">🛠️ वेंडर इकोसिस्टम</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    category_filter = col1.selectbox("सर्विस चुनें", ["सभी", "आर्किटेक्ट", "कॉन्ट्रैक्टर", "पेंटर", "इंटीरियर डिजाइनर", "हार्डवेयर", "वास्तु / पुजारी"])
    location_filter = col2.selectbox("लोकेशन", ["सभी", "New Amar Nagar", "Wardha Road", "Sitabuldi", "Dharampeth"])
    exp_filter = col3.slider("न्यूनतम अनुभव (वर्ष)", 0, 30, 2)
    
    with st.expander("⭐ ट्रस्ट और क्वालिटी फिल्टर"):
        col4, col5 = st.columns(2)
        rating_filter = col4.slider("न्यूनतम रेटिंग (स्टार्स)", 1.0, 5.0, 4.0, 0.1)
        verified_filter = col5.checkbox("सिर्फ वेरिफाइड वेंडर दिखाएं", value=True)

    st.divider()
    
    filtered_vendors = dummy_vendors.copy()
    if category_filter != "सभी": filtered_vendors = filtered_vendors[filtered_vendors["Category"] == category_filter]
    if location_filter != "सभी": filtered_vendors = filtered_vendors[filtered_vendors["Location"] == location_filter]
    filtered_vendors = filtered_vendors[filtered_vendors["Experience_Years"] >= exp_filter]
    filtered_vendors = filtered_vendors[filtered_vendors["Rating"] >= rating_filter]
    if verified_filter: filtered_vendors = filtered_vendors[filtered_vendors["Verified"] == "Yes"]
        
    st.markdown(f"<p style='color:#64748b; font-weight:600;'>{len(filtered_vendors)} प्रोफेशनल्स मिले</p>", unsafe_allow_html=True)
    
    # वेंडर कार्ड्स रेंडर करना
    for _, row in filtered_vendors.iterrows():
        verified_html = '<span class="verified-tag">✓ Verified Partner</span>' if row['Verified'] == 'Yes' else ''
        st.markdown(f"""
        <div class="vendor-card">
            <h4 style="margin:0; color:#0f172a; font-size:1.2rem;">{row['Vendor_Name']}</h4>
            <p style="margin:4px 0; color:#64748b;">🛠️ {row['Category']} | 📍 {row['Location']}</p>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
                <span style="color:#eab308; font-weight:600;">⭐ {row['Rating']}</span>
                <span style="color:#475569; font-size:0.9rem;">💼 {row['Experience_Years']} वर्ष का अनुभव</span>
                {verified_html}
            </div>
        </div>
        """, unsafe_allow_html=True)
