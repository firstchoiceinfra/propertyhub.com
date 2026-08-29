import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# 1. Database Connection Logic
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        cred_dict = {
            "type": st.secrets["firebase"]["type"],
            "project_id": st.secrets["firebase"]["project_id"],
            "private_key_id": st.secrets["firebase"]["private_key_id"],
            "private_key": st.secrets["firebase"]["private_key"].replace('\\n', '\n'),
            "client_email": st.secrets["firebase"]["client_email"],
            "client_id": st.secrets["firebase"]["client_id"],
            "auth_uri": st.secrets["firebase"]["auth_uri"],
            "token_uri": st.secrets["firebase"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
        }
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firebase()

# 2. Read Functions (For fetching data)
def fetch_all_properties():
    """Fetches all property listings from Firebase"""
    docs = db.collection('properties').stream()
    data = []
    for doc in docs:
        prop = doc.to_dict()
        data.append(prop)
    return data

def fetch_all_vendors():
    """Fetches all registered vendors from Firebase"""
    docs = db.collection('vendors').stream()
    data = []
    for doc in docs:
        vendor = doc.to_dict()
        data.append(vendor)
    return data

# 3. Write Functions (For Admin Panel)
def add_property(prop_data):
    """Pushes a new property document to the Firestore 'properties' collection"""
    try:
        db.collection('properties').add(prop_data)
        return True
    except Exception as e:
        st.error(f"Error adding property: {e}")
        return False

def add_vendor(vendor_data):
    """Pushes a new vendor document to the Firestore 'vendors' collection"""
    try:
        db.collection('vendors').add(vendor_data)
        return True
    except Exception as e:
        st.error(f"Error adding vendor: {e}")
        return False
