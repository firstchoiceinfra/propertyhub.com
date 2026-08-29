# ... (Keep your existing connection and fetch functions at the top) ...

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
