import streamlit as st
import pandas as pd

# डमी प्रॉपर्टी डेटा 
dummy_properties = pd.DataFrame({
    "Property_Name": ["Firstchoice Premium Plot", "Earth Heights 2 Flat", "Luxury Villa", "Commercial Shop"],
    "Type": ["Plot", "Flat", "Villa", "Commercial"],
    "Location": ["New Amar Nagar", "New Amar Nagar", "Wardha Road", "Sitabuldi"],
    "Budget_Lakhs": [25, 45, 120, 80],
    "RERA_Approved": ["Yes", "Yes", "Yes", "No"],
    "Facing": ["East", "East", "North", "West"],
    "Status": ["Ready to Move", "Under Construction", "Ready to Move", "Ready to Move"]
})

def show_advanced_filters():
    st.markdown('<h2 style="color: #1e3a8a;">🏢 प्रॉपर्टी लिस्टिंग (Buy / Rent / Sell)</h2>', unsafe_allow_html=True)
    
    st.markdown("### 🔍 बेसिक डिटेल्स")
    col1, col2, col3 = st.columns(3)
    loc_filter = col1.selectbox("लोकेशन", ["सभी", "New Amar Nagar", "Wardha Road", "Sitabuldi"])
    type_filter = col2.selectbox("प्रॉपर्टी का प्रकार", ["सभी", "Plot", "Flat", "Villa", "Commercial"])
    budget_filter = col3.slider("बजट (लाख ₹ में)", 10, 200, (10, 150))
    
    with st.expander("✨ एडवांस फिल्टर (RERA, फेसिंग, स्टेटस)"):
        col4, col5, col6 = st.columns(3)
        rera_filter = col4.radio("RERA एप्रूव्ड?", ["सभी", "Yes", "No"], horizontal=True)
        facing_filter = col5.selectbox("फेसिंग (दिशा)", ["सभी", "East", "West", "North", "South"])
        status_filter = col6.selectbox("प्रोजेक्ट स्टेटस", ["सभी", "Ready to Move", "Under Construction"])
        
    st.divider()
    
    filtered_df = dummy_properties.copy()
    
    if loc_filter != "सभी":
        filtered_df = filtered_df[filtered_df["Location"] == loc_filter]
    if type_filter != "सभी":
        filtered_df = filtered_df[filtered_df["Type"] == type_filter]
        
    filtered_df = filtered_df[(filtered_df["Budget_Lakhs"] >= budget_filter[0]) & 
                              (filtered_df["Budget_Lakhs"] <= budget_filter[1])]
    
    if rera_filter != "सभी":
        filtered_df = filtered_df[filtered_df["RERA_Approved"] == rera_filter]
    if facing_filter != "सभी":
        filtered_df = filtered_df[filtered_df["Facing"] == facing_filter]
    if status_filter != "सभी":
        filtered_df = filtered_df[filtered_df["Status"] == status_filter]
        
    st.success(f"कुल {len(filtered_df)} प्रॉपर्टीज़ आपकी सर्च के अनुसार मिली हैं!")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
