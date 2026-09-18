import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# App Configuration
st.set_page_config(page_title="Nutrilink | Surplus Food Network", layout="wide")

# Custom CSS — Lato Font + Animated Top Navbar
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&display=swap" rel="stylesheet">
<style>
    html, body, [class*="st-"], .stApp, p, h1, h2, h3, h4, h5, h6, label, div {
        font-family: 'Lato', sans-serif !important;
    }

    /* Animated Top Navigation Bar */
    .nutrilink-nav {
        display: flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 10px 24px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
        position: relative;
        overflow: hidden;
    }
    .nutrilink-nav::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(ellipse at 60% 50%, rgba(99,179,237,0.08) 0%, transparent 60%);
        animation: shimmer 4s ease-in-out infinite alternate;
    }
    @keyframes shimmer {
        0%   { transform: translateX(-10%) rotate(0deg); }
        100% { transform: translateX(10%) rotate(5deg); }
    }
    .nav-brand {
        color: #fff;
        font-size: 1.1rem;
        font-weight: 900;
        letter-spacing: 1px;
        margin-right: 20px;
        white-space: nowrap;
    }
    .nav-spacer { flex: 1; }
    .nav-btn {
        background: transparent;
        color: rgba(255,255,255,0.7);
        border: 1px solid rgba(255,255,255,0.15);
        padding: 7px 20px;
        border-radius: 8px;
        cursor: pointer;
        font-family: 'Lato', sans-serif;
        font-size: 0.88rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        transition: all 0.25s ease;
        white-space: nowrap;
        position: relative;
        z-index: 1;
    }
    .nav-btn:hover {
        background: rgba(255,255,255,0.12);
        color: #fff;
        border-color: rgba(255,255,255,0.4);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .nav-btn.active {
        background: linear-gradient(135deg, #3182ce, #63b3ed);
        color: #fff;
        border-color: transparent;
        box-shadow: 0 4px 14px rgba(49,130,206,0.45);
        transform: translateY(-1px);
    }
    .nav-btn.active::after {
        content: '';
        position: absolute;
        bottom: -3px;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
        height: 2px;
        background: #90cdf4;
        border-radius: 2px;
    }
</style>
""", unsafe_allow_html=True)

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
            },
            {
                "batch_id": 2,
                "vendor_id": 2,
                "item_name": "Beef Tehari Trays",
                "quantity": 15,
                "original_price": 220.00,
                "expiry_time": now + timedelta(minutes=45),
                "batch_status": "Expiring Soon",
            },
            {
                "batch_id": 3,
                "vendor_id": 3,
                "item_name": "Boxed Sourdough & Sweet Pastries",
                "quantity": 10,
                "original_price": 150.00,
                "expiry_time": now + timedelta(hours=5),
                "batch_status": "Available",
            },
            {
                "batch_id": 4,
                "vendor_id": 4,
                "item_name": "Plain Khichuri & Mixed Curry",
                "quantity": 30,
                "original_price": 120.00,
                "expiry_time": now - timedelta(hours=1),
                "batch_status": "Expired",
            },
            {
                "batch_id": 5,
                "vendor_id": 1,
                "item_name": "Chicken Patties & Rolls",
                "quantity": 20,
                "original_price": 80.00,
                "expiry_time": now + timedelta(hours=2),
                "batch_status": "Available",
            },
        ]
        
    if "claims" not in st.session_state:
        st.session_state.claims = [
            {"claim_id": 1, "batch_id": 2, "receiver_id": 1, "claimed_quantity": 5, "total_price": 1100.00, "claim_timestamp": datetime.now(), "claim_status": "Reserved"},
            {"claim_id": 2, "batch_id": 3, "receiver_id": 2, "claimed_quantity": 10, "total_price": 0.00, "claim_timestamp": datetime.now() - timedelta(hours=2), "claim_status": "Completed"}
        ]

initialize_mock_data()

# Helper for status updates
def update_batch_statuses():
    now = datetime.now()
    for batch in st.session_state.batches:
        if batch["expiry_time"] < now:
            batch["batch_status"] = "Expired"
        elif (batch["expiry_time"] - now).total_seconds() / 3600 < 1 and batch["batch_status"] != "Expired":
             batch["batch_status"] = "Urgent"

update_batch_statuses()

# --- Main Header ---
st.title("Nutrilink: Surplus Food Redistribution")
st.caption("Reducing food waste through localized, real-time networking.")
st.divider()

# --- 1. Top-Level Impact KPI Cards ---
active_batches = [b for b in st.session_state.batches if b["batch_status"] != "Expired" and b["quantity"] > 0]
total_portions_available = sum(b["quantity"] for b in active_batches)
active_batches_count = len(active_batches)

# Meals rescued today
today = datetime.now().date()
claims_today = [
    c for c in st.session_state.claims 
    if getattr(c.get("claim_timestamp", datetime.now()), 'date', lambda: datetime.now().date())() == today
]
meals_rescued_today = sum(c["claimed_quantity"] for c in claims_today)

# BDT equivalent of food saved today
bdt_saved_today = sum(c["total_price"] for c in claims_today)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Surplus Portions Available", total_portions_available)
k2.metric("Active Batches Listed", active_batches_count)
k3.metric("Meals Rescued Today", meals_rescued_today)
k4.metric("BDT Value Saved Today", f"{bdt_saved_today:,.0f} BDT")
st.divider()

# --- 2. Animated Top Navigation Bar ---
NAV_ITEMS = ["Receiver Marketplace", "Vendor Portal", "Database Inspector"]
if "nav_role" not in st.session_state:
    st.session_state.nav_role = "Receiver Marketplace"

# Render navbar buttons as a form to capture clicks
with st.container():
    nav_cols = st.columns([2] + [1] * len(NAV_ITEMS) + [2])
    # Brand label
    nav_cols[0].markdown(
        "<div style='padding-top:6px; font-family:Lato,sans-serif; font-weight:900; font-size:1rem; color:#1a202c; letter-spacing:0.5px;'>Nutrilink</div>",
        unsafe_allow_html=True
    )
    for i, item in enumerate(NAV_ITEMS):
        is_active = st.session_state.nav_role == item
        btn_style = (
            "background:linear-gradient(135deg,#3182ce,#63b3ed);color:#fff;border:none;font-weight:700;"
            if is_active else
            "background:#edf2f7;color:#4a5568;border:1px solid #cbd5e0;font-weight:600;"
        )
        if nav_cols[i + 1].button(
            item,
            key=f"nav_{item}",
            use_container_width=True,
        ):
            st.session_state.nav_role = item
            st.rerun()

role = st.session_state.nav_role
st.divider()

def get_vendor(vendor_id):
    return next((v for v in st.session_state.vendors if v["vendor_id"] == vendor_id), None)

# --- Views ---
if role == "Vendor Portal":
    st.header("Vendor Portal")
    st.write("Post surplus inventory to immediately notify nearby charities and reduce food waste.")
    
    with st.form("donor_entry_form", clear_on_submit=True):
        st.subheader("1. Vendor Details")
        c1, c2, c3 = st.columns(3)
        with c1:
            biz_name = st.text_input("Business Name", placeholder="e.g., Star Kabab")
        with c2:
            biz_type = st.selectbox("Business Type", ["Restaurant", "Bakery", "Caterer", "Supermarket"])
        with c3:
            zone = st.selectbox("Dhaka Area / Zone", ["Dhanmondi", "Gulshan", "Mirpur", "Uttara", "Banani", "Old Dhaka"])
            
        st.subheader("2. Surplus Batch Details")
        c4, c5 = st.columns(2)
        with c4:
            item_name = st.text_input("Food Item Name", placeholder="e.g., Mutton Kacchi Biryani")
            portions = st.number_input("Portions (min 1)", min_value=1, step=1, value=10)
        with c5:
            original_price = st.number_input("Original Price per Portion (BDT)", min_value=0.0, step=10.0, value=150.0)
            expiry_hours = st.slider("Expiry Hours from now", min_value=1, max_value=48, value=12)
            
        submitted = st.form_submit_button("Publish Surplus Batch", use_container_width=True)
        
        if submitted:
            if not biz_name.strip() or not item_name.strip():
                st.error("Please fill in both Business Name and Item Name.")
            else:
                # Find or create vendor
                vendor = next((v for v in st.session_state.vendors if v["vendor_name"].lower() == biz_name.lower()), None)
                if not vendor:
                    vendor_id = len(st.session_state.vendors) + 1
                    vendor = {
                        "vendor_id": vendor_id,
                        "vendor_name": biz_name,
                        "zone": zone,
                        "business_type": biz_type
                    }
                    st.session_state.vendors.append(vendor)
                else:
                    vendor_id = vendor["vendor_id"]
                    
                # Create batch
                new_batch = {
                    "batch_id": len(st.session_state.batches) + 1,
                    "vendor_id": vendor_id,
                    "item_name": item_name,
                    "quantity": portions,
                    "original_price": original_price,
                    "expiry_time": datetime.now() + timedelta(hours=expiry_hours),
                    "batch_status": "Available"
                }
                st.session_state.batches.append(new_batch)
                st.toast("Batch listed successfully!")
                st.success(f"Success! {portions} portions of '{item_name}' have been listed and charities in {zone} notified.")

if role == "Receiver Marketplace":
    st.header("Receiver Marketplace")
    
    # 4. Filter bar
    st.subheader("Search & Filter Options")
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        search_q = st.text_input("Search by Item Name", placeholder="e.g., Khichuri")
    with f_col2:
        zone_options = list(set([v["zone"] for v in st.session_state.vendors]))
        selected_zones = st.multiselect("Filter by Dhaka Zone", zone_options, default=[])
    with f_col3:
        status_filter = st.selectbox("Status Filter", ["All", "Available", "Urgent", "Discounted"])
        
    # Apply Filters
    df_batches = []
    for b in st.session_state.batches:
        v = get_vendor(b["vendor_id"])
        if not v: continue
        
        # Determine visual status
        now = datetime.now()
        if b["expiry_time"] < now:
            stat = "Expired"
        elif (b["expiry_time"] - now).total_seconds() / 3600 < 1:
            stat = "Urgent"
        else:
            stat = b["batch_status"]
            
        b["current_status"] = stat
        
        if stat == "Expired" or b["quantity"] <= 0:
            continue
            
        if search_q and search_q.lower() not in b["item_name"].lower():
            continue
        if selected_zones and v["zone"] not in selected_zones:
            continue
        if status_filter != "All" and stat != status_filter:
            continue
            
        df_batches.append({
            "batch_id": b["batch_id"],
            "vendor_name": v["vendor_name"],
            "zone": v["zone"],
            "item_name": b["item_name"],
            "quantity": b["quantity"],
            "price": b["original_price"],
            "expiry": b["expiry_time"],
            "status": stat
        })
        
    st.divider()
    
    if not df_batches:
        st.info("No surplus food batches match your criteria right now.")
    else:
        for item in df_batches:
            with st.container(border=True):
                col1, col2, col3 = st.columns([3, 2, 2])
                with col1:
                    st.markdown(f"#### {item['item_name']}")
                    st.caption(f"Provider: {item['vendor_name']} | Zone: {item['zone']}")
                    
                with col2:
                    if item['status'] == "Urgent":
                        st.markdown("**Status: Urgent (< 1h)**")
                    elif item['status'] == "Discounted":
                        st.markdown("**Status: Discounted**")
                    else:
                        st.markdown("**Status: Available**")
                    
                    st.markdown(f"**Available Portions:** {item['quantity']}")
                    st.markdown(f"**Price:** {item['price']} BDT")
                    
                with col3:
                    with st.expander("Claim Batch"):
                        claim_qty = st.number_input("Portions to claim", min_value=1, max_value=item['quantity'], value=1, key=f"qty_{item['batch_id']}")
                        if st.button("Confirm Claim", type="primary", key=f"claim_{item['batch_id']}", use_container_width=True):
                            # Process Claim
                            for b in st.session_state.batches:
                                if b["batch_id"] == item["batch_id"]:
                                    b["quantity"] -= claim_qty
                                    break
                            # Record Claim
                            new_claim = {
                                "claim_id": len(st.session_state.claims) + 1,
                                "batch_id": item["batch_id"],
                                "receiver_id": 1, # Default mock receiver
                                "claimed_quantity": claim_qty,
                                "total_price": claim_qty * item["price"],
                                "claim_timestamp": datetime.now(),
                                "claim_status": "Reserved"
                            }
                            st.session_state.claims.append(new_claim)
                            st.toast(f"Successfully claimed {claim_qty} portions!")
                            st.balloons()
                            st.rerun()

if role == "Database Inspector":
    st.header("Database Inspector")
    st.write("Real-time view of internal data structures mirroring the relational schema.")
    
    t1, t2, t3, t4 = st.tabs(["vendors", "receivers", "food_batches", "claims"])
    
    with t1:
        st.subheader("Table: vendors")
        st.caption("Engine: InnoDB | PK: vendor_id")
        df_vendors = pd.DataFrame(st.session_state.vendors)
        st.dataframe(df_vendors, use_container_width=True)
        st.write(f"Row count: {len(df_vendors)}")
        
    with t2:
        st.subheader("Table: receivers")
        st.caption("Engine: InnoDB | PK: receiver_id")
        df_receivers = pd.DataFrame(st.session_state.receivers)
        st.dataframe(df_receivers, use_container_width=True)
        st.write(f"Row count: {len(df_receivers)}")
        
    with t3:
        st.subheader("Table: food_batches")
        st.caption("Engine: InnoDB | PK: batch_id | FK: vendor_id -> vendors(vendor_id)")
        df_batches_full = pd.DataFrame(st.session_state.batches)
        if not df_batches_full.empty:
            df_batches_full["expiry_time"] = df_batches_full["expiry_time"].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(x) else "")
        st.dataframe(df_batches_full, use_container_width=True)
        st.write(f"Row count: {len(df_batches_full)}")
        
    with t4:
        st.subheader("Table: claims")
        st.caption("Engine: InnoDB | PK: claim_id | FK: batch_id -> food_batches(batch_id), receiver_id -> receivers(receiver_id)")
        df_claims = pd.DataFrame(st.session_state.claims)
        if not df_claims.empty:
            df_claims["claim_timestamp"] = df_claims["claim_timestamp"].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(x) else "")
        st.dataframe(df_claims, use_container_width=True)
        st.write(f"Row count: {len(df_claims)}")
