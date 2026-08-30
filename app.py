import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

# --- Page Config ---
st.set_page_config(page_title="PropertyHub Premium", page_icon="🏢", layout="wide")

# --- Custom CSS (Sidebar & Buttons) ---
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    }
    [data-testid="stSidebar"] .css-17lntkn, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] .stRadio label {
        color: white !important;
    }
    .whatsapp-btn {
        background-color: #25D366; color: white; padding: 10px 20px; 
        text-align: center; text-decoration: none; display: inline-block; 
        border-radius: 5px; font-weight: bold; width: 100%;
    }
    .whatsapp-btn:hover { background-color: #128C7E; color: white; }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Session State for Wishlist ---
if 'wishlist' not in st.session_state:
    st.session_state['wishlist'] = []

# --- Firebase Initialization ---
if not firebase_admin._apps:
    key_dict = json.loads(st.secrets["FIREBASE_JSON"])
    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def fetch_all_properties():
    properties = []
    for doc in db.collection('properties').stream():
        data = doc.to_dict()
        data['doc_id'] = doc.id
        properties.append(data)
    return properties

def fetch_all_vendors():
    vendors = []
    for doc in db.collection('vendors').stream():
        data = doc.to_dict()
        data['doc_id'] = doc.id
        vendors.append(data)
    return vendors

def fetch_all_leads():
    leads = []
    for doc in db.collection('leads').stream():
        data = doc.to_dict()
        data['doc_id'] = doc.id
        leads.append(data)
    return leads

# --- Page 1: Property Listings ---
def show_property_listings():
    st.title("🏢 Premium Property Listings")
    
    st.markdown("### 🔍 Search your Dream Property")
    col1, col2, col3 = st.columns(3)
    with col1:
        search_loc = st.text_input("📍 Location (e.g. Nagpur)").lower()
    with col2:
        search_type = st.selectbox("🏠 Type", ["All", "Flat / Apartment", "Plot / Land", "Villa / Independent House", "Commercial"])
    with col3:
        max_budget = st.number_input("💰 Max Budget (₹)", min_value=0, value=0, step=100000)

    st.markdown("---")
    properties = fetch_all_properties()
    
    # --- Featured Properties Section ---
    featured_props = [p for p in properties if p.get('is_featured', False)]
    if featured_props and not (search_loc or search_type != "All" or max_budget > 0):
        st.subheader("⭐ Featured Projects")
        cols = st.columns(len(featured_props) if len(featured_props) < 3 else 3)
        for i, prop in enumerate(featured_props[:3]):
            with cols[i % 3]:
                if prop.get('image_url'):
                    st.image(prop['image_url'], use_container_width=True)
                st.markdown(f"**{prop.get('title', 'N/A')}**")
                st.caption(f"📍 {prop.get('location', '')} | ₹{prop.get('price', 0):,}")
        st.markdown("---")
    
    # --- All Properties ---
    st.subheader("🏠 All Properties")
    for prop in properties:
        if search_loc and search_loc not in prop.get('location', '').lower(): continue
        if search_type != "All" and search_type != prop.get('prop_type', ''): continue
        if max_budget > 0 and prop.get('price', 0) > max_budget: continue

        with st.container():
            col_img, col_vid = st.columns(2)
            with col_img:
                if prop.get('image_url'): st.image(prop['image_url'], use_container_width=True)
            with col_vid:
                if prop.get('video_url'): st.video(prop['video_url'])
            
            # Title & MahaRERA Badge
            if prop.get('rera_id'):
                st.subheader(f"✅ {prop.get('title', 'N/A')} (MahaRERA Approved)")
                st.success(f"MahaRERA Reg No: {prop.get('rera_id')}")
            else:
                st.subheader(f"{prop.get('title', 'N/A')} ({prop.get('status', 'N/A')})")
                
            st.markdown(f"**{prop.get('prop_type', '')}** | **{prop.get('bhk', 'N/A')}** | **{prop.get('area', 'N/A')}**")
            st.markdown(f"📍 {prop.get('location', '')} | 🏷️ **₹{prop.get('price', 0):,}**")
            
            if prop.get('amenities'):
                st.write(f"✨ **Amenities:** {', '.join(prop.get('amenities', []))}")

            # Wishlist Button
            if prop['doc_id'] in st.session_state['wishlist']:
                st.button("❤️ Saved in Wishlist", disabled=True, key=f"wish_{prop['doc_id']}")
            else:
                if st.button("🤍 Save to Wishlist", key=f"wish_{prop['doc_id']}"):
                    st.session_state['wishlist'].append(prop['doc_id'])
                    st.rerun()

            # Contact Section
            st.markdown("### 🤝 Interested?")
            col_wa, col_form = st.columns(2)
            with col_wa:
                admin_phone = "919000000000" # <-- यहाँ अपना व्हाट्सएप नंबर डालें
                msg = f"Hello Firstchoice Infra, I am interested in {prop.get('title', 'Property')} at {prop.get('location', '')}."
                wa_link = f"https://wa.me/{admin_phone}?text={msg.replace(' ', '%20')}"
                st.markdown(f'<a href="{wa_link}" target="_blank" class="whatsapp-btn">💬 Chat on WhatsApp</a>', unsafe_allow_html=True)
                
            with col_form:
                with st.expander("📞 Request Call Back"):
                    buyer_name = st.text_input("Your Name", key=f"name_{prop['doc_id']}")
                    buyer_phone = st.text_input("Your Phone Number", key=f"phone_{prop['doc_id']}")
                    if st.button("Send Interest", key=f"btn_{prop['doc_id']}"):
                        if buyer_name and buyer_phone:
                            db.collection('leads').add({
                                "property_id": prop['doc_id'], "property_title": prop.get('title', 'N/A'),
                                "buyer_name": buyer_name, "buyer_phone": buyer_phone
                            })
                            st.success("✅ Thanks! Our team will contact you.")
                        else:
                            st.warning("⚠️ कृपया अपना नाम और मोबाइल नंबर भरें।")

            # Admin Delete Option
            if st.session_state.get('admin_logged_in', False) and st.session_state.get('user_role') == 'Admin':
                if st.button("🗑️ Delete Property (Admin Only)", key=f"del_{prop['doc_id']}"):
                    db.collection('properties').document(prop['doc_id']).delete()
                    st.rerun()
            st.markdown("---")

# --- Page 2: Vendor Ecosystem ---
def show_vendor_ecosystem():
    st.title("🛠️ Vendor Ecosystem")
    col1, col2 = st.columns(2)
    with col1:
        search_service = st.selectbox("🛠️ Service Type", ["All", "Architecture", "Legal Advisor", "Plumber", "Electrician", "Interior Designer"])
    with col2:
        search_loc = st.text_input("📍 Location (e.g. Nagpur)").lower()

    st.markdown("---")
    for vendor in fetch_all_vendors():
        if search_service != "All" and search_service != vendor.get('service_type', ''): continue
        if search_loc and search_loc not in vendor.get('location', '').lower(): continue

        with st.container():
            st.subheader(vendor.get('name', 'N/A'))
            st.markdown(f"**🛠️ Service:** {vendor.get('service_type', 'N/A')} | **📍 Location:** {vendor.get('location', 'N/A')}")
            st.markdown(f"**📞 Contact:** {vendor.get('contact', 'N/A')}")
            
            if st.session_state.get('admin_logged_in', False) and st.session_state.get('user_role') == 'Admin':
                if st.button("🗑️ Delete Vendor", key=f"del_ven_{vendor['doc_id']}"):
                    db.collection('vendors').document(vendor['doc_id']).delete()
                    st.rerun()
            st.markdown("---")

# --- Page 3: Admin & Sales Login ---
def show_admin_panel():
    st.title("🔐 Company Portal (Admin & Sales)")
    if 'admin_logged_in' not in st.session_state: st.session_state['admin_logged_in'] = False

    if not st.session_state['admin_logged_in']:
        st.info("डेटा ऐड करने के लिए लॉगिन करें।")
        username = st.selectbox("Select Role", ["Admin", "Sales Executive"])
        pwd = st.text_input("Password", type="password")
        
        if st.button("Login"):
            # Role-Based Passwords
            if username == "Admin" and pwd == "Firstchoice@123":
                st.session_state['admin_logged_in'] = True
                st.session_state['user_role'] = 'Admin'
                st.rerun()
            elif username == "Sales Executive" and pwd == "Sales@123": # सेल्स टीम का पासवर्ड
                st.session_state['admin_logged_in'] = True
                st.session_state['user_role'] = 'Sales Executive'
                st.rerun()
            else:
                st.error("❌ गलत पासवर्ड!")
        return

    st.success(f"Logged in as: {st.session_state.get('user_role')}")
    if st.button("Logout 🚪"):
        st.session_state['admin_logged_in'] = False
        st.rerun()
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["🏠 Add Property", "🛠️ Add Vendor", "📞 View Leads"])
    
    with tab1:
        st.subheader("Add New Property")
        title = st.text_input("Property Title")
        prop_type = st.selectbox("Property Type", ["Flat / Apartment", "Plot / Land", "Villa / Independent House", "Commercial"])
        
        col1, col2 = st.columns(2)
        with col1:
            price = st.number_input("Price (₹)", min_value=0)
            area = st.text_input("Area (Sq Ft / Sq Yd)")
            bhk = st.selectbox("BHK", ["N/A", "1 BHK", "2 BHK", "3 BHK", "4+ BHK"])
        with col2:
            location = st.text_input("Location / City")
            status = st.selectbox("Status", ["Ready to Move", "Under Construction", "New Launch", "Sold Out"])
            rera_id = st.text_input("MahaRERA Reg No. (Optional)")
        
        amenities = st.multiselect("Amenities", ["Parking", "Lift", "Garden", "Security", "Club House", "Gym", "Power Backup"])
        image_url = st.text_input("Property Image URL")
        video_url = st.text_input("YouTube / 3D Video URL (Optional)")
        
        # Featured Checkbox (Only Admin can feature a project)
        is_featured = False
        if st.session_state.get('user_role') == 'Admin':
            is_featured = st.checkbox("⭐ Mark as Featured Project (होमपेज पर सबसे ऊपर दिखेगा)")

        if st.button("Upload Property"):
            if title and location and price:
                db.collection('properties').add({
                    "title": title, "prop_type": prop_type, "price": price, "area": area, 
                    "bhk": bhk, "location": location, "status": status, "rera_id": rera_id, 
                    "amenities": amenities, "image_url": image_url, "video_url": video_url,
                    "is_featured": is_featured,
                    "added_by": st.session_state.get('user_role') # ट्रैक करेगा किसने ऐड किया
                })
                st.success("✅ प्रॉपर्टी लाइव हो गई!")

    with tab2:
        st.subheader("Add New Vendor")
        v_name = st.text_input("Vendor Name")
        v_service = st.selectbox("Service Type", ["Architecture", "Legal Advisor", "Plumber", "Electrician", "Interior Designer"])
        v_location = st.text_input("Service Location")
        v_contact = st.text_input("Contact Number")
        if st.button("Add Vendor") and v_name and v_contact:
            db.collection('vendors').add({"name": v_name, "service_type": v_service, "location": v_location, "contact": v_contact})
            st.success("✅ Vendor Added!")

    with tab3:
        st.subheader("📞 Customer Leads")
        for lead in fetch_all_leads():
            st.markdown(f"🏡 {lead.get('property_title', 'N/A')} | 👤 {lead.get('buyer_name', 'N/A')} | 📱 {lead.get('buyer_phone', 'N/A')}")
            # Only Admin can delete leads
            if st.session_state.get('user_role') == 'Admin':
                if st.button("🗑️ Delete", key=f"del_lead_{lead['doc_id']}"):
                    db.collection('leads').document(lead['doc_id']).delete()
                    st.rerun()
            st.markdown("---")

# --- My Wishlist Page ---
def show_wishlist():
    st.title("❤️ My Wishlist")
    if not st.session_state['wishlist']:
        st.info("अभी तक आपने कोई प्रॉपर्टी सेव नहीं की है।")
        return
        
    properties = fetch_all_properties()
    saved_props = [p for p in properties if p['doc_id'] in st.session_state['wishlist']]
    
    for prop in saved_props:
        with st.container():
            st.subheader(prop.get('title', 'N/A'))
            st.markdown(f"📍 {prop.get('location', '')} | 🏷️ **₹{prop.get('price', 0):,}**")
            if st.button("❌ Remove from Wishlist", key=f"rem_{prop['doc_id']}"):
                st.session_state['wishlist'].remove(prop['doc_id'])
                st.rerun()
            st.markdown("---")

# --- Main App ---
def main():
    st.sidebar.title("Firstchoice Infra")
    menu = ["🏢 Property Listings", "❤️ My Wishlist", "🛠️ Vendor Ecosystem", "🔐 Company Portal"]
    choice = st.sidebar.radio("Navigation", menu)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🧮 EMI Calculator")
    loan_amt = st.sidebar.number_input("Loan Amount (₹)", value=1500000, step=100000)
    interest = st.sidebar.slider("Interest Rate (%)", 5.0, 15.0, 8.5)
    tenure = st.sidebar.slider("Tenure (Years)", 1, 30, 15)
    if st.sidebar.button("Calculate EMI"):
        r = (interest / 12) / 100
        n = tenure * 12
        emi = loan_amt * r * ((1 + r)**n) / (((1 + r)**n) - 1)
        st.sidebar.success(f"Monthly EMI: ₹{int(emi):,}")

    if choice == "🏢 Property Listings": show_property_listings()
    elif choice == "❤️ My Wishlist": show_wishlist()
    elif choice == "🛠️ Vendor Ecosystem": show_vendor_ecosystem()
    elif choice == "🔐 Company Portal": show_admin_panel()

if __name__ == '__main__':
    main()