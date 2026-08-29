import streamlit as st
import pandas as pd

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
    # प्रीमियम कार्ड स्टाइलिंग
    st.markdown("""
        <style>
        .property-card {
            background: #ffffff;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
            border: 1px solid #e2e8f0;
            transition: all 0.3s ease;
            margin-bottom: 15px;
        }
        .property-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 20px -3px rgba(0,0,0,0.15);
            border-color: #3b82f6;
        }
        .badge-rera { background: #dcfce7; color: #166534; padding: 4px 8px; border-radius: 6px; font-size: 0.8rem; font-weight: 600; }
        .badge-status { background: #e0e7ff; color: #3730a3; padding: 4px 8px; border-radius: 6px; font-size: 0.8rem; font-weight: 600; }
        .price-tag { color: #1e3a8a; font-size: 1.4rem; font-weight: 700; margin: 10px 0; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h2 style="color: #1e3a8a; font-weight:700;">🏢 प्रॉपर्टी लिस्टिंग</h2>', unsafe_allow_html=True)
    
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
    if loc_filter != "सभी": filtered_df = filtered_df[filtered_df["Location"] == loc_filter]
    if type_filter != "सभी": filtered_df = filtered_df[filtered_df["Type"] == type_filter]
    filtered_df = filtered_df[(filtered_df["Budget_Lakhs"] >= budget_filter[0]) & (filtered_df["Budget_Lakhs"] <= budget_filter[1])]
    if rera_filter != "सभी": filtered_df = filtered_df[filtered_df["RERA_Approved"] == rera_filter]
    if facing_filter != "सभी": filtered_df = filtered_df[filtered_df["Facing"] == facing_filter]
    if status_filter != "सभी": filtered_df = filtered_df[filtered_df["Status"] == status_filter]
        
    st.markdown(f"<p style='color:#64748b; font-weight:600;'>{len(filtered_df)} प्रॉपर्टीज़ मिलीं</p>", unsafe_allow_html=True)
    
    # प्रॉपर्टी कार्ड्स रेंडर करना
    for _, row in filtered_df.iterrows():
        rera_badge = '<span class="badge-rera">✅ RERA Approved</span>' if row['RERA_Approved'] == 'Yes' else ''
        st.markdown(f"""
        <div class="property-card">
            <h3 style="margin:0; color:#0f172a;">{row['Property_Name']}</h3>
            <p style="margin:5px 0; color:#64748b;">📍 {row['Location']} | 📐 {row['Type']} | 🧭 {row['Facing']} Facing</p>
            <div class="price-tag">₹ {row['Budget_Lakhs']} Lakhs</div>
            <div>
                <span class="badge-status">{row['Status']}</span> {rera_badge}
            </div>
        </div>
        """, unsafe_allow_html=True)
