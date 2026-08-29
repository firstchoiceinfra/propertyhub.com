import streamlit as st
import pandas as pd

# Dummy Property Data
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
    # Premium Card Styling
    st.markdown("""
        <style>
        .property-card {
            background: #ffffff;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
            border: 1px solid #f1f5f9;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            margin-bottom: 20px;
        }
        .property-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);
            border-color: #3b82f6;
        }
        .badge-rera { background: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 600; margin-left: 8px;}
        .badge-status { background: #e0e7ff; color: #3730a3; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 600; }
        .price-tag { color: #1e3a8a; font-size: 1.5rem; font-weight: 700; margin: 12px 0; }
        .property-title { margin:0; color:#0f172a; font-size: 1.25rem; font-weight: 700; }
        .property-meta { margin:8px 0; color:#64748b; font-size: 0.95rem; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h2 style="color: #1e3a8a; font-weight:700;">🏢 Property Listings</h2>', unsafe_allow_html=True)
    
    # Primary Filters
    col1, col2, col3 = st.columns(3)
    loc_filter = col1.selectbox("Location", ["All", "New Amar Nagar", "Wardha Road", "Sitabuldi"])
    type_filter = col2.selectbox("Property Type", ["All", "Plot", "Flat", "Villa", "Commercial"])
    budget_filter = col3.slider("Budget (₹ Lakhs)", 10, 200, (10, 150))
    
    # Advanced Filters
    with st.expander("✨ Advanced Filters (RERA, Facing, Status)"):
        col4, col5, col6 = st.columns(3)
        rera_filter = col4.radio("RERA Approved?", ["All", "Yes", "No"], horizontal=True)
        facing_filter = col5.selectbox("Facing", ["All", "East", "West", "North", "South"])
        status_filter = col6.selectbox("Project Status", ["All", "Ready to Move", "Under Construction"])
        
    st.divider()
    
    # Filter Logic
    filtered_df = dummy_properties.copy()
    if loc_filter != "All": filtered_df = filtered_df[filtered_df["Location"] == loc_filter]
    if type_filter != "All": filtered_df = filtered_df[filtered_df["Type"] == type_filter]
    filtered_df = filtered_df[(filtered_df["Budget_Lakhs"] >= budget_filter[0]) & (filtered_df["Budget_Lakhs"] <= budget_filter[1])]
    if rera_filter != "All": filtered_df = filtered_df[filtered_df["RERA_Approved"] == rera_filter]
    if facing_filter != "All": filtered_df = filtered_df[filtered_df["Facing"] == facing_filter]
    if status_filter != "All": filtered_df = filtered_df[filtered_df["Status"] == status_filter]
        
    st.markdown(f"<p style='color:#64748b; font-weight:600;'>{len(filtered_df)} Properties Found</p>", unsafe_allow_html=True)
    
    # Render Property Cards
    for _, row in filtered_df.iterrows():
        rera_badge = '<span class="badge-rera">✅ RERA Approved</span>' if row['RERA_Approved'] == 'Yes' else ''
        st.markdown(f"""
        <div class="property-card">
            <h3 class="property-title">{row['Property_Name']}</h3>
            <p class="property-meta">📍 {row['Location']} | 📐 {row['Type']} | 🧭 {row['Facing']} Facing</p>
            <div class="price-tag">₹ {row['Budget_Lakhs']} Lakhs</div>
            <div style="margin-top: 10px;">
                <span class="badge-status">{row['Status']}</span> {rera_badge}
            </div>
        </div>
        """, unsafe_allow_html=True)
