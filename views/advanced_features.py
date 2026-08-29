import streamlit as st

def show_advanced_features():
    st.markdown("""
        <style>
        .feature-card {
            background: #ffffff;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
            border: 1px solid #f1f5f9;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }
        .feature-card:hover {
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
            border-color: #3b82f6;
        }
        .tab-content {
            padding: 20px 0;
        }
        .action-btn {
            background-color: #1e3a8a;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            display: inline-block;
            margin-top: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h2 style="color: #1e3a8a; font-weight:700;">✨ Advanced Features</h2>', unsafe_allow_html=True)
    
    # Premium Tabs
    tab1, tab2, tab3 = st.tabs(["🎮 3D Virtual Tours", "🤖 AI Property Valuation", "🏦 Legal & Home Loans"])
    
    with tab1:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        st.markdown("""
        <div class="feature-card">
            <h3 style="color:#0f172a; margin-bottom: 10px;">Immersive 3D Layouts</h3>
            <p style="color:#64748b;">Allow buyers to walk through plots and apartments using Virtual Reality (VR) before visiting the site.</p>
            <div style="background:#f8fafc; height:200px; border-radius:8px; display:flex; align-items:center; justify-content:center; border:2px dashed #cbd5e1;">
                <p style="color:#94a3b8; font-weight:600;">[ 3D Video/VR Viewer Player Placeholder ]</p>
            </div>
            <a href="#" class="action-btn">Upload 3D Layout</a>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        st.markdown("""
        <div class="feature-card">
            <h3 style="color:#0f172a; margin-bottom: 10px;">Smart Price Predictor</h3>
            <p style="color:#64748b;">Enter property details to get an AI-estimated market value based on current real estate trends in Nagpur.</p>
        """, unsafe_allow_html=True)
        
        # Interactive AI Form
        col1, col2 = st.columns(2)
        col1.selectbox("Select Area", ["New Amar Nagar", "Wardha Road", "Sitabuldi"])
        col2.number_input("Property Size (Sq. Ft)", min_value=500, max_value=10000, step=100)
        st.button("Calculate Estimated Price", type="primary")
        
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        st.markdown("""
        <div class="feature-card">
            <h3 style="color:#0f172a; margin-bottom: 10px;">One-Click Loan Approvals & Registry</h3>
            <p style="color:#64748b;">Connect directly with banking partners for instant EMI calculations and legal experts for hassle-free RERA registration.</p>
            <ul>
                <li style="color:#475569; margin-bottom:8px;">✅ Instant EMI Calculator</li>
                <li style="color:#475569; margin-bottom:8px;">✅ Document Verification Services</li>
                <li style="color:#475569; margin-bottom:8px;">✅ Direct Bank Tie-ups (SBI, HDFC)</li>
            </ul>
            <a href="#" class="action-btn">Contact Legal Team</a>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
