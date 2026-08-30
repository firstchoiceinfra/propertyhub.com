import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

# --- Page Config ---
st.set_page_config(page_title="PropertyHub Premium", page_icon="🏢", layout="wide")

# --- Premium Multi-Color Sidebar Design ---
st.markdown(
    """
    <style>
    /* साइडबार का प्रीमियम मल्टी-कलर बैकग्राउंड */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    }
    
    /* साइडबार के टेक्स्ट को सफेद और चमकदार बनाना */
    [data-testid="stSidebar"] .css-17lntkn, 
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] .stRadio label {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Firebase Initialization ---
if not firebase_admin._apps:
    key_dict = json.loads(st.secrets["FIREBASE_JSON"])
    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# --- Database Fetch Functions ---
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

# --- Page 1: Property Listings (with 99acres Search & Lead Form) ---
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
    
    for prop in properties:
        # Filters Logic
        if search_loc and search_loc not in prop.get('location', '').lower():
            continue
        if search_type != "All" and search_type != prop.get('prop_type', ''):
            continue
        if max_budget > 0 and prop.get('price', 0) > max_budget:
            continue

        with st.container():
            # Property Image
            if prop.get('image_url'):
                st.image(prop['image_url'], use_container_width=True)
            
            # Details
            st.subheader(f"{prop.get('title', 'N/A')} ({prop.get('status', 'N/A')})")
            st.markdown(f"**{prop.get('prop_type', '')}** | **{prop.get('bhk', 'N/A')}** | **{prop.get('area', 'N/A')}**")
            st.markdown(f"📍 {prop.get('location', '')} | 🏷️ **₹{prop.get('price', 0):,}**")
            
            if prop.get('rera_id'):
                st.caption(f"✅ RERA ID: {prop.get('rera_id')}")
            
            if prop.get('amenities'):
                st.write(f"✨ **Amenities:** {', '.join(prop.get('amenities', []))}")

            # Contact Seller / Lead Gen Form
            with st.expander("📞 Contact Seller / Express Interest"):
                st.write("Leave your details, and our agent will contact you.")
                buyer_name = st.text_input("Your Name", key=f"name_{prop['doc_id']}")
                buyer_phone = st.text_input("Your Phone Number", key=f"phone_{prop['doc_id']}")
                if st.button("Send Interest", key=f"btn_{prop['doc_id']}"):
                    if buyer_name and buyer_phone:
                        lead_data = {
                            "property_id": prop['doc_id'],
                            "property_title": prop.get('title', 'N/A'),
                            "buyer_name": buyer_name,
                            "buyer_phone": buyer_phone
                        }
                        db.collection('leads').add(lead_data)
                        st.success("✅ Thanks! Your details have been sent.")
                    else:
                        st.warning("⚠️ कृपया अपना नाम और मोबाइल नंबर भरें।")

            # Admin Delete Button
            if st.session_state.get('admin_logged_in', False):
                if st.button("🗑️ Delete Property", key=f"del_{prop['doc_id']}"):
                    db.collection('properties').document(prop['doc_id']).delete()
                    st.rerun()
            st.markdown("---")

# --- Page 2: Vendor Ecosystem (with Filters) ---
def show_vendor_ecosystem():
    st.title("🛠️ Vendor Ecosystem")
    
    st.markdown("### 🔍 Find Service Providers")
    col1, col2 = st.columns(2)
    with col1:
        search_service = st.selectbox("🛠️ Service Type", ["All", "Architecture", "Legal Advisor", "Plumber", "Electrician", "Interior Designer"])
    with col2:
        search_loc = st.text_input("📍 Location (e.g. Nagpur)").lower()

    st.markdown("---")
    
    vendors = fetch_all_vendors()
    for vendor in vendors:
        # Filters Logic
        if search_service != "All" and search_service != vendor.get('service_type', ''):
            continue
        if search_loc and search_loc not in vendor.get('location', '').lower():
            continue

        with st.container():
            st.subheader(vendor.get('name', 'N/A'))
            st.markdown(f"**🛠️ Service:** {vendor.get('service_type', 'N/A')} | **📍 Location:** {vendor.get('location', 'N/A')}")
            st.markdown(f"**📞 Contact:** {vendor.get('contact', 'N/A')}")
            
            # Admin Delete Button
            if st.session_state.get('admin_logged_in', False):
                if st.button("🗑️ Delete Vendor", key=f"del_ven_{vendor['doc_id']}"):
                    db.collection('vendors').document(vendor['doc_id']).delete()
                    st.rerun()
            st.markdown("---")

# --- Page 3: Admin Panel (with Login) ---
def show_admin_panel():
    st.title("🔐 Admin Panel")

    # Login System
    if 'admin_logged_in' not in st.session_state:
        st.session_state['admin_logged_in'] = False

    if not st.session_state['admin_logged_in']:
        st.info("डेटा ऐड करने के लिए एडमिन पासवर्ड डालें।")
        pwd = st.text_input("Admin Password", type="password")
        if st.button("Login"):
            if pwd == "Firstchoice@123":
                st.session_state['admin_logged_in'] = True
                st.rerun()
            else:
                st.error("❌ गलत पासवर्ड!")
        return

    if st.button("Logout 🚪"):
        st.session_state['admin_logged_in'] = False
        st.rerun()
    st.markdown("---")

    # Admin Tabs
    tab1, tab2, tab3 = st.tabs(["🏠 Add Property", "🛠️ Add Vendor", "📞 View Leads"])
    
    with tab1:
        st.subheader("Add New Property")
        title = st.text_input("Property Title (e.g., Luxury 2BHK)")
        prop_type = st.selectbox("Property Type", ["Flat / Apartment", "Plot / Land", "Villa / Independent House", "Commercial"])
        
        col1, col2 = st.columns(2)
        with col1:
            price = st.number_input("Price (₹)", min_value=0)
            area = st.text_input("Area (Sq Ft / Sq Yd)")
            bhk = st.selectbox("BHK", ["N/A", "1 BHK", "2 BHK", "3 BHK", "4+ BHK"])
        with col2:
            location = st.text_input("Location / City")
            status = st.selectbox("Status", ["Ready to Move", "Under Construction", "New Launch", "Sold Out"])
            rera_id = st.text_input("RERA Registration No. (Optional)")
        
        amenities = st.multiselect("Amenities", ["Parking", "Lift", "Garden", "Security", "Club House", "Gym", "Power Backup"])
        image_url = st.text_input("Property Image URL (Optional)")
        
        if st.button("Upload Property"):
            if title and location and price:
                data = {
                    "title": title, "prop_type": prop_type, "price": price, 
                    "area": area, "bhk": bhk, "location": location, 
                    "status": status, "rera_id": rera_id, "amenities": amenities,
                    "image_url": image_url
                }
                db.collection('properties').add(data)
                st.success("✅ प्रॉपर्टी लाइव हो गई!")
            else:
                st.warning("कृपया टाइटल, लोकेशन और प्राइस जरूर भरें।")

    with tab2:
        st.subheader("Add New Vendor")
        v_name = st.text_input("Vendor Name")
        v_service = st.selectbox("Service Type", ["Architecture", "Legal Advisor", "Plumber", "Electrician", "Interior Designer"])
        v_location = st.text_input("Service Location")
        v_contact = st.text_input("Contact Number")
        
        if st.button("Add Vendor"):
            if v_name and v_contact:
                db.collection('vendors').add({
                    "name": v_name, "service_type": v_service,
                    "location": v_location, "contact": v_contact
                })
                st.success("✅ Vendor Added!")

    with tab3:
        st.subheader("📞 Customer Leads (कस्टमर पूछताछ)")
        leads = fetch_all_leads()
        
        if not leads:
            st.info("अभी तक कोई नई लीड नहीं आई है।")
        else:
            for lead in leads:
                with st.container():
                    st.markdown(f"**🏡 Property:** {lead.get('property_title', 'N/A')}")
                    st.markdown(f"**👤 Name:** {lead.get('buyer_name', 'N/A')}")
                    st.markdown(f"**📱 Phone:** {lead.get('buyer_phone', 'N/A')}")
                    
                    if st.button("🗑️ Delete Lead", key=f"del_lead_{lead['doc_id']}"):
                        db.collection('leads').document(lead['doc_id']).delete()
                        st.rerun()
                    st.markdown("---")

# --- Main App Navigation ---
def main():
    st.sidebar.title("Firstchoice Infra")
    menu = ["🏢 Property Listings", "🛠️ Vendor Ecosystem", "🔐 Admin Panel"]
    choice = st.sidebar.radio("Navigation", menu)

    if choice == "🏢 Property Listings":
        show_property_listings()
    elif choice == "🛠️ Vendor Ecosystem":
        show_vendor_ecosystem()
    elif choice == "🔐 Admin Panel":
        show_admin_panel()

if __name__ == '__main__':
    main()
