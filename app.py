import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# App Configuration
st.set_page_config(page_title="Nutrilink | Surplus Food Network", layout="wide")

# --- Helper Functions for Mock Data ---
def initialize_mock_data():
    if "vendors" not in st.session_state:
        st.session_state.vendors = [
            {"vendor_id": 1, "vendor_name": "Star Kabab - Dhanmondi", "zone": "Dhanmondi", "business_type": "Restaurant"},
            {"vendor_id": 2, "vendor_name": "Sultan's Dine - Gulshan", "zone": "Gulshan", "business_type": "Restaurant"},
            {"vendor_id": 3, "vendor_name": "Tasty Treat - Mirpur", "zone": "Mirpur", "business_type": "Bakery"},
            {"vendor_id": 4, "vendor_name": "Prince Caterers - Uttara", "zone": "Uttara", "business_type": "Caterer"},
        ]

    if "receivers" not in st.session_state:
        st.session_state.receivers = [
            {"receiver_id": 1, "org_name": "Dhaka Food Bank", "org_type": "NGO"},
            {"receiver_id": 2, "org_name": "Gulshan Orphanage", "org_type": "Shelter"},
        ]

    if "batches" not in st.session_state:
        now = datetime.now()
        st.session_state.batches = [
            {
                "batch_id": 1,
                "vendor_id": 1,
                "item_name": "Mutton Kacchi Biryani",
                "quantity": 25,
                "original_price": 350.00,
                "expiry_time": now + timedelta(hours=12),
                "batch_status": "Available",
                "is_veg": False
            },
            {
                "batch_id": 2,
                "vendor_id": 2,
                "item_name": "Beef Tehari Trays",
                "quantity": 15,
                "original_price": 220.00,
                "expiry_time": now + timedelta(minutes=45),
                "batch_status": "Discounted",
                "is_veg": False
            },
            {
                "batch_id": 3,
                "vendor_id": 3,
                "item_name": "Boxed Sourdough & Sweet Pastries",
                "quantity": 10,
                "original_price": 150.00,
                "expiry_time": now + timedelta(hours=5),
                "batch_status": "Available",
                "is_veg": True
            },
            {
                "batch_id": 4,
                "vendor_id": 4,
                "item_name": "Plain Khichuri & Mixed Curry",
                "quantity": 30,
                "original_price": 120.00,
                "expiry_time": now - timedelta(hours=1),
                "batch_status": "Expired",
                "is_veg": False
            },
            {
                "batch_id": 5,
                "vendor_id": 1,
                "item_name": "Chicken Patties & Rolls",
                "quantity": 20,
                "original_price": 80.00,
                "expiry_time": now + timedelta(hours=2),
                "batch_status": "Available",
                "is_veg": False
            },
        ]
        
    if "claims" not in st.session_state:
        st.session_state.claims = [
            {"claim_id": 1, "batch_id": 2, "receiver_id": 1, "claimed_quantity": 5, "total_price": 1100.00, "claim_status": "Reserved"},
            {"claim_id": 2, "batch_id": 3, "receiver_id": 2, "claimed_quantity": 10, "total_price": 0.00, "claim_status": "Completed"}
        ]

initialize_mock_data()

# --- Main Header ---
st.title("Nutrilink: Surplus Food Redistribution")

# --- Navigation ---
nav_selection = st.sidebar.radio(
    "Navigation",
    ["Receiver Marketplace", "Vendor Portal", "Impact Analytics"]
)

def get_vendor(vendor_id):
    return next((v for v in st.session_state.vendors if v["vendor_id"] == vendor_id), None)

def get_badge(expiry_time, status):
    now = datetime.now()
    if status == "Expired" or expiry_time < now:
        return "🔒 Expired (Auto-Locked)"
    
    time_left = expiry_time - now
    hours_left = time_left.total_seconds() / 3600
    
    if hours_left < 1:
        return "⚡ Urgent (< 1h left)"
    elif status == "Discounted":
        return "🟡 Discounted"
    else:
        return "🟢 Fresh Listing"

if nav_selection == "Receiver Marketplace":
    st.header("Receiver Marketplace")
    
    # Filter Bar
    f1, f2, f3 = st.columns([2, 1, 1])
    search_query = f1.text_input("Search available items...", placeholder="e.g., Kacchi Biryani")
    zone_filter = f2.selectbox("Filter by Zone", ["All", "Dhanmondi", "Gulshan", "Mirpur", "Uttara"])
    
    # Align checkbox vertically
    with f3:
        st.write("")
        st.write("")
        veg_filter = st.checkbox("Vegetarian Only")
    
    st.divider()
    
    # Filter Logic
    now = datetime.now()
    filtered_batches = st.session_state.batches
    
    if search_query:
        filtered_batches = [b for b in filtered_batches if search_query.lower() in b["item_name"].lower()]
    if zone_filter != "All":
        filtered_batches = [b for b in filtered_batches if get_vendor(b["vendor_id"])["zone"] == zone_filter]
    if veg_filter:
        filtered_batches = [b for b in filtered_batches if b.get("is_veg", False)]
        
    for batch in filtered_batches:
        vendor = get_vendor(batch["vendor_id"])
        vendor_name = vendor["vendor_name"] if vendor else "Unknown Vendor"
        zone = vendor["zone"] if vendor else "Unknown"
        
        badge_text = get_badge(batch["expiry_time"], batch["batch_status"])
        
        with st.container(border=True):
            c1, c2, c3 = st.columns([3, 2, 2])
            
            with c1:
                st.markdown(f"### {batch['item_name']}")
                st.caption(f"Provider: **{vendor_name}** ({zone})")
                
                # Progress bar for expiry
                total_shelf_life_hours = 24.0
                if batch["expiry_time"] > now:
                    hours_left = (batch["expiry_time"] - now).total_seconds() / 3600.0
                    prog = min(max(hours_left / total_shelf_life_hours, 0.0), 1.0)
                    st.progress(prog, text=f"Expires at: {batch['expiry_time'].strftime('%I:%M %p, %d %b')}")
                else:
                    st.progress(0.0, text="Expired")

            with c2:
                st.markdown(f"**Status:** {badge_text}")
                st.markdown(f"**Available:** {batch['quantity']} portions")
                st.markdown(f"**Price:** ৳{batch['original_price']:.2f}")
                
            with c3:
                is_expired = batch["batch_status"] == "Expired" or batch["expiry_time"] <= now
                if is_expired:
                    st.button("Locked", key=f"btn_{batch['batch_id']}", disabled=True, use_container_width=True)
                else:
                    if st.button("Claim Batch", key=f"btn_{batch['batch_id']}", type="primary", use_container_width=True):
                        # TODO: Week 3 execute UPDATE food_batches SET quantity ...
                        st.success(f"Claimed batch #{batch['batch_id']}!")

elif nav_selection == "Vendor Portal":
    st.header("Vendor Portal")
    
    st.subheader("List New Surplus Batch")
    
    with st.form("add_batch_form", clear_on_submit=True):
        vendor_options = {v["vendor_name"]: v["vendor_id"] for v in st.session_state.vendors}
        selected_vendor_name = st.selectbox("Select Vendor", list(vendor_options.keys()))
        
        item_name = st.text_input("Food Item Name", placeholder="e.g., Mutton Kacchi Biryani")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            quantity = st.number_input("Quantity (Portions/Kg)", min_value=1, max_value=500, value=10)
        with c2:
            original_price = st.number_input("Price per Portion (৳)", min_value=0.0, value=150.0, step=10.0)
        with c3:
            st.write("")
            st.write("")
            is_veg = st.checkbox("Vegetarian")
            
        shelf_hours = st.slider("Shelf-Life Window (Hours from now)", min_value=1, max_value=48, value=12)
        submit_batch = st.form_submit_button("Post Batch to Inventory", use_container_width=True)
        
        if submit_batch:
            if not item_name.strip():
                st.error("Please enter a valid food item name.")
            else:
                vendor_id = vendor_options[selected_vendor_name]
                new_item = {
                    "batch_id": len(st.session_state.batches) + 1,
                    "vendor_id": vendor_id,
                    "item_name": item_name,
                    "quantity": quantity,
                    "original_price": original_price,
                    "expiry_time": datetime.now() + timedelta(hours=shelf_hours),
                    "batch_status": "Available",
                    "is_veg": is_veg
                }
                st.session_state.batches.append(new_item)
                st.success(f"Batch '{item_name}' added successfully!")

elif nav_selection == "Impact Analytics":
    st.header("Impact Analytics")
    
    # Calculate mock metrics
    total_portions_saved = sum(c.get("claimed_quantity", 0) for c in st.session_state.claims)
    
    active_donors = len(set(b["vendor_id"] for b in st.session_state.batches if b["batch_status"] != "Expired" and b["expiry_time"] > datetime.now()))
    
    # Value diverted from waste (Original Price * Claimed Quantity)
    bdt_diverted = 0.0
    for claim in st.session_state.claims:
        batch = next((b for b in st.session_state.batches if b["batch_id"] == claim["batch_id"]), None)
        if batch:
            bdt_diverted += batch["original_price"] * claim["claimed_quantity"]
        
    k1, k2, k3 = st.columns(3)
    k1.metric("Total Portions Saved", f"{total_portions_saved}")
    k2.metric("Active Donors", f"{active_donors}")
    k3.metric("BDT Diverted from Waste", f"৳{bdt_diverted:,.2f}")
    
    st.divider()
    st.info("Further analytics and charts will be implemented in future weeks.")