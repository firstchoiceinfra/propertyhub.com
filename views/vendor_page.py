import streamlit as st
import pandas as pd

# डमी वेंडर डेटा 
dummy_vendors = pd.DataFrame({
    "Vendor_Name": ["Rahul Architects", "Shree Ram Builders", "A1 Painters", "Modern Interiors", "Gupta Hardware", "Pandit Ji Vastu"],
    "Category": ["आर्किटेक्ट", "कॉन्ट्रैक्टर", "पेंटर", "इंटीरियर डिजाइनर", "हार्डवेयर", "वास्तु / पुजारी"],
    "Location": ["New Amar Nagar", "Wardha Road", "Sitabuldi", "Dharampeth", "New Amar Nagar", "New Amar Nagar"],
    "Experience_Years": [10, 15, 5, 8, 20, 25],
    "Rating": [4.8, 4.5, 4.1, 4.9, 4.3, 5.0],
    "Verified": ["Yes", "Yes", "No", "Yes", "Yes", "Yes"]
})

def show_vendor_ecosystem():
    st.markdown('<h2 style="color: #0f766e;">🛠️ होम बिल्डिंग एंड वेंडर इकोसिस्टम</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    category_filter = col1.selectbox("सर्विस चुनें", ["सभी", "आर्किटेक्ट", "कॉन्ट्रैक्टर", "बिल्डिंग मटेरियल", "पेंटर", "इंटीरियर डिजाइनर", "हार्डवेयर", "प्लंबर", "वास्तु / पुजारी"])
    location_filter = col2.selectbox("लोकेशन", ["सभी", "New Amar Nagar", "Wardha Road", "Sitabuldi", "Dharampeth"])
    exp_filter = col3.slider("न्यूनतम अनुभव (वर्ष)", 0, 30, 2)
    
    with st.expander("⭐ ट्रस्ट और क्वालिटी फिल्टर"):
        col4, col5 = st.columns(2)
        rating_filter = col4.slider("न्यूनतम रेटिंग (स्टार्स)", 1.0, 5.0, 4.0, 0.1)
        verified_filter = col5.checkbox("सिर्फ वेरिफाइड (Verified) वेंडर दिखाएं", value=True)

    st.divider()
    
    filtered_vendors = dummy_vendors.copy()
    
    if category_filter != "सभी":
        filtered_vendors = filtered_vendors[filtered_vendors["Category"] == category_filter]
    if location_filter != "सभी":
        filtered_vendors = filtered_vendors[filtered_vendors["Location"] == location_filter]
        
    filtered_vendors = filtered_vendors[filtered_vendors["Experience_Years"] >= exp_filter]
    filtered_vendors = filtered_vendors[filtered_vendors["Rating"] >= rating_filter]
    
    if verified_filter:
        filtered_vendors = filtered_vendors[filtered_vendors["Verified"] == "Yes"]
        
    st.success(f"कुल {len(filtered_vendors)} प्रोफेशनल्स आपकी जरूरत के अनुसार मिले हैं!")
    
    for index, row in filtered_vendors.iterrows():
        verified_badge = "✅ Verified" if row["Verified"] == "Yes" else ""
        st.markdown(f"""
        <div style="padding:15px; border:1px solid #ddd; border-radius:10px; margin-bottom:10px; background-color:white;">
            <h4 style="margin:0; color:#1e3a8a;">{row['Vendor_Name']} {verified_badge}</h4>
            <p style="margin:5px 0; color:#555;"><b>सर्विस:</b> {row['Category']} | <b>लोकेशन:</b> {row['Location']}</p>
            <p style="margin:0; color:#0f766e;">⭐ {row['Rating']} Ratings | 💼 अनुभव: {row['Experience_Years']} वर्ष</p>
        </div>
        """, unsafe_allow_html=True)
