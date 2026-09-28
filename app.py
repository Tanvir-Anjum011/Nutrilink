import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error
import streamlit.components.v1 as components
import os

# App Configuration
st.set_page_config(page_title="Nutrilink | Surplus Food Network", layout="wide")

# Custom CSS — Enterprise SaaS Theme (Sleek, Modern, Centered Green Title)
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&display=swap" rel="stylesheet">
<style>
    /* Typography */
    p, h1, h2, h3, h4, h5, h6, li, label, .stMarkdown, .stText {
        font-family: 'Lato', sans-serif !important;
    }
    
    /* Professional Header Styling (Centered & Greenish) */
    h1 {
        color: #059669 !important; /* Emerald Green */
        text-align: center !important;
        font-weight: 900 !important;
        letter-spacing: -0.5px;
        animation: fadeInDown 0.6s ease-out;
    }

    /* Modern KPI Metrics */
    [data-testid="stMetricValue"] {
        color: #059669 !important; /* Emerald Green */
        font-weight: 800 !important;
        animation: popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
    }
    [data-testid="stMetricLabel"] {
        font-weight: 600 !important;
        color: #64748b !important; /* Slate Gray */
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.75rem !important;
    }

    /* Glassy Dashboard Cards */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-left: 4px solid #10b981 !important;
        border-radius: 12px !important;
        background: rgba(30, 41, 59, 0.6) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        transition: all 0.3s ease-in-out !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 12px 20px -5px rgba(0,0,0,0.3), 0 8px 10px -4px rgba(0,0,0,0.2) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        background: rgba(30, 41, 59, 0.8) !important;
    }

    /* Enterprise Buttons */
    .stButton > button[kind="primary"] {
        background-color: #0f172a !important; /* Corporate Navy/Slate */
        border: none !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 4px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #334155 !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1) !important;
    }

    /* Keyframe Animations */
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes popIn {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }
    
    /* Professional UI Badges (Pill format) */
    .badge {
        display: inline-block;
        padding: 0.25em 0.75em;
        font-size: 0.75rem;
        font-weight: 700;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .badge-available { background-color: #dcfce7; color: #166534; }
    .badge-discounted { background-color: #fef08a; color: #854d0e; }
    .badge-urgent { background-color: #fee2e2; color: #991b1b; }
    
    /* --- Crazy Ambient Animation Background --- */
    @keyframes ambientGlow {
        0% { box-shadow: 0 0 40px rgba(16, 185, 129, 0.1); }
        50% { box-shadow: 0 0 80px rgba(14, 165, 233, 0.2); }
        100% { box-shadow: 0 0 40px rgba(16, 185, 129, 0.1); }
    }
    .block-container {
        animation: ambientGlow 6s infinite alternate;
        border-radius: 20px;
        padding-top: 3.5rem !important;
        padding-bottom: 50px !important;
        background: rgba(15, 23, 42, 0.2);
        backdrop-filter: blur(10px);
    }

    /* Entry Animation for overall items */
    @keyframes slideUpFade {
        from { opacity: 0; transform: translateY(40px) scale(0.98); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }
    [data-testid="stVerticalBlockBorderWrapper"], form, div[data-testid="stRadio"] {
        animation: slideUpFade 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
    }
    
    /* --- Classy Central Menu --- */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }

    div[data-testid="stRadio"] {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 40px;
        padding: 6px 16px;
        box-shadow: 0 8px 32px 0 rgba(16, 185, 129, 0.15);
        margin: 20px auto 40px auto !important;
        width: max-content;
        display: flex;
        justify-content: center;
        transition: all 0.3s ease;
    }
    div[data-testid="stRadio"]:hover {
        box-shadow: 0 12px 40px 0 rgba(16, 185, 129, 0.3);
        transform: translateY(-2px);
    }
    /* Force centering of the parent wrapper */
    .element-container:has(div[data-testid="stRadio"]) {
        display: flex;
        justify-content: center;
        width: 100%;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] {
        display: flex;
        flex-direction: row;
        justify-content: center !important;
        align-items: center;
        gap: 15px !important;
    }
    /* Hide the default radio circles */
    div[data-testid="stRadio"] div[role="radio"] {
        display: none !important;
    }
    div[data-testid="stRadio"] label > div:first-child {
        display: none !important;
    }
    /* Style the labels */
    div[data-testid="stRadio"] label {
        padding: 8px 20px !important;
        border-radius: 20px;
        transition: all 0.3s ease;
    }
    div[data-testid="stRadio"] label p {
        font-size: 1.05rem !important;
        font-weight: 800 !important;
        color: #94a3b8 !important;
        margin: 0 !important;
        transition: all 0.3s ease-in-out !important;
    }
    /* Active State Hover */
    div[data-testid="stRadio"] label[data-checked="true"] {
        background: rgba(16, 185, 129, 0.15);
    }
    div[data-testid="stRadio"] label[data-checked="true"] p, 
    div[data-testid="stRadio"] label:hover p {
        color: #10b981 !important;
        text-shadow: 0 0 12px rgba(16, 185, 129, 0.5);
        transform: translateY(-2px) scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# --- Database Connection ---
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=st.secrets.get("MYSQL_HOST", "localhost"),
            port=st.secrets.get("MYSQL_PORT", 3306),
            user=st.secrets.get("MYSQL_USER", "root"),
            password=st.secrets.get("MYSQL_PASSWORD", "root1234"),
            database=st.secrets.get("MYSQL_DB", "surplus_food_db")
        )
        return conn
    except Error as e:
        st.error(f"Database Connection Error: {e}")
        return None

# --- Main Header ---
head_col1, head_col2, head_col3 = st.columns([4, 2, 4])
with head_col2:
    try:
        st.image("logo.png", use_container_width=True)
    except Exception:
        pass
st.divider()

# --- 1. Top-Level Impact KPI Cards ---
conn = get_db_connection()
if conn:
    cursor = conn.cursor(dictionary=True)
    
    # Total Active Portions & Listings
    cursor.execute("SELECT SUM(quantity) as total_portions, COUNT(*) as active_listings FROM food_batches WHERE expiry_time > NOW() AND quantity > 0")
    active_stats = cursor.fetchone()
    total_portions = int(active_stats['total_portions'] or 0)
    active_listings = int(active_stats['active_listings'] or 0)
    
    # Rescued Today
    cursor.execute("SELECT SUM(claimed_quantity) as rescued FROM claims WHERE DATE(claim_timestamp) = CURDATE()")
    rescued_stats = cursor.fetchone()
    meals_rescued_today = int(rescued_stats['rescued'] or 0)
    
    k1, k2, k3 = st.columns(3)
    k1.metric("Total Active Portions", f"{total_portions:,}")
    k2.metric("Active Batch Listings", active_listings)
    k3.metric("Portions Rescued Today", meals_rescued_today)
    
    cursor.close()
    conn.close()
st.divider()

# --- 2. Animated Bottom Menu ---
m_col1, m_col2, m_col3 = st.columns([1, 1.5, 1])
with m_col2:
    role = st.radio("Navigation", [
        "Vendor",
        "Receiver",
        "Database"
    ], horizontal=True, label_visibility="collapsed")

# --- Views ---
if role == "Vendor":
    st.header("Vendor Portal")
    
    with st.form("donor_entry_form", clear_on_submit=True):
        st.subheader("1. Organization Details")
        c1, c2, c3 = st.columns(3)
        with c1:
            biz_name = st.text_input("Business Name", placeholder="Enter registered business name")
        with c2:
            biz_type = st.selectbox("Business Type", ["Restaurant", "Bakery", "Caterer", "Supermarket"])
        with c3:
            zone = st.text_input("Operating Zone / Address", placeholder="e.g. United City")
            
        st.subheader("2. Inventory Specifics")
        custom_batch_id = st.number_input("Assign Custom Batch ID (Number)", min_value=0, step=1, value=0)
        c4, c5 = st.columns(2)
        with c4:
            item_name = st.text_input("Commodity Name", placeholder="Enter item description")
            portions = st.number_input("Available Portions", min_value=0, step=1, value=0)
        with c5:
            original_price = st.number_input("Standard Price per Unit (BDT)", min_value=0.0, step=10.0, value=0.0)
            expiry_hours = st.slider("Quality Assurance Window (Hours)", min_value=0, max_value=48, value=0)
            
        submitted = st.form_submit_button("Authorize and Publish Batch", use_container_width=True)
        
        if submitted:
            if not biz_name.strip() or not item_name.strip():
                st.error("Validation Error: Business Name and Commodity Name are required fields.")
            else:
                conn = get_db_connection()
                if conn:
                    try:
                        cursor = conn.cursor(dictionary=True)
                        # Transactional Integrity: Start Transaction
                        conn.start_transaction()
                        
                        # Check if vendor exists, else create
                        cursor.execute("SELECT vendor_id FROM vendors WHERE vendor_name = %s", (biz_name,))
                        vendor = cursor.fetchone()
                        
                        if vendor:
                            vendor_id = vendor['vendor_id']
                        else:
                            cursor.execute(
                                "INSERT INTO vendors (vendor_name, business_type, address) VALUES (%s, %s, %s)", 
                                (biz_name, biz_type, zone)
                            )
                            vendor_id = cursor.lastrowid
                            
                        # Insert batch
                        expiry_time = datetime.now() + timedelta(hours=expiry_hours)
                        cursor.execute(
                            "INSERT INTO food_batches (batch_id, vendor_id, item_name, quantity, original_price, expiry_time, batch_status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (custom_batch_id, vendor_id, item_name, portions, original_price, expiry_time.strftime('%Y-%m-%d %H:%M:%S'), 'Available')
                        )
                        
                        conn.commit()
                        st.toast("Transaction Successful: Batch Registered.")
                        st.success(f"System Update: {portions} units of '{item_name}' successfully committed to the redistribution network.")
                    except Error as e:
                        conn.rollback()
                        if e.errno == 1062:
                            st.error(f"Batch ID {custom_batch_id} already exists. Please pick a different number.")
                        else:
                            st.error(f"Failed to publish batch: {e.msg}")
                    finally:
                        cursor.close()
                        conn.close()

    # --- Week 3 Requirement: DELETE Operation ---
    st.divider()
    st.subheader("3. Batch Management (Delete)")
    with st.form("delete_batch_form"):
        del_batch_id = st.number_input("Enter Batch ID to Remove", min_value=0, step=1, value=0)
        del_submitted = st.form_submit_button("Delete Batch", type="primary")
        
        if del_submitted:
            del_conn = get_db_connection()
            if del_conn:
                try:
                    del_cursor = del_conn.cursor()
                    del_conn.start_transaction()
                    
                    # Execute DELETE statement
                    del_cursor.execute("DELETE FROM food_batches WHERE batch_id = %s", (del_batch_id,))
                    
                    if del_cursor.rowcount > 0:
                        del_conn.commit()
                        st.success(f"Batch {del_batch_id} was successfully deleted from the system.")
                    else:
                        del_conn.rollback()
                        st.warning(f"Batch {del_batch_id} not found.")
                except Error as e:
                    del_conn.rollback()
                    st.error(f"Failed to delete batch: {e.msg}")
                finally:
                    del_cursor.close()
                    del_conn.close()

elif role == "Receiver":
    st.header("Receiver Marketplace")
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # Receiver Selection Context
        cursor.execute("SELECT receiver_id, org_name, daily_quota_limit FROM receivers")
        receivers = cursor.fetchall()
        
        if not receivers:
            st.warning("No receivers found in the database. Please add a receiver to claim food.")
        else:
            receiver_opts = {f"{r['org_name']} (Quota: {r['daily_quota_limit']})": r['receiver_id'] for r in receivers}
            selected_receiver_name = st.selectbox("Receiver:", list(receiver_opts.keys()))
            active_receiver_id = receiver_opts[selected_receiver_name]
        
            f_col1, f_col2, f_col3 = st.columns(3)
            with f_col1:
                search_q = st.text_input("Query by Item", placeholder="Search parameters...")
            with f_col2:
                # Get unique zones
                cursor.execute("SELECT DISTINCT address FROM vendors WHERE address IS NOT NULL")
                zones = [row['address'] for row in cursor.fetchall()]
                selected_zones = st.multiselect("Filter by Zone", zones, default=[])
            
            # Fetch active batches from View (Dynamic Pricing enforced here)
            query = "SELECT * FROM vw_active_batches WHERE 1=1"
            params = []
            
            if search_q:
                query += " AND item_name LIKE %s"
                params.append(f"%{search_q}%")
                
            if selected_zones:
                format_strings = ','.join(['%s'] * len(selected_zones))
                query += f" AND zone IN ({format_strings})"
                params.extend(selected_zones)
                
            query += " ORDER BY expiry_time ASC"
            cursor.execute(query, tuple(params))
            active_batches = cursor.fetchall()
            
            st.divider()
            
            if not active_batches:
                st.info("No active inventory matches the specified query parameters.")
            else:
                for item in active_batches:
                    with st.container(border=True):
                        col1, col2, col3 = st.columns([3, 2, 2])
                        with col1:
                            st.markdown(f"#### {item['item_name']}")
                            st.caption(f"**Origin:** {item['vendor_name']} | **Sector:** {item['zone']}")
                            
                            # Real-Time Expiry Countdown Component
                            # Uses JS to tick down without Streamlit reruns
                            expiry_ts = item['expiry_time'].isoformat()
                            countdown_id = f"countdown_{item['batch_id']}"
                            components.html(
                                f"""
                                <div style='font-family: "Lato", sans-serif; font-size: 0.85rem; padding: 4px 8px; border-radius: 4px; background: #fee2e2; color: #991b1b; display: inline-block; font-weight: 700;'>
                                    <span id='{countdown_id}'>Calculating...</span>
                                </div>
                                <script>
                                    var countDownDate = new Date("{expiry_ts}").getTime();
                                    var x = setInterval(function() {{
                                        var now = new Date().getTime();
                                        var distance = countDownDate - now;
                                        if (distance < 0) {{
                                            clearInterval(x);
                                            document.getElementById("{countdown_id}").innerHTML = "EXPIRED";
                                        }} else {{
                                            var h = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                                            var m = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                                            var s = Math.floor((distance % (1000 * 60)) / 1000);
                                            document.getElementById("{countdown_id}").innerHTML = "Expires in: " + h + "h " + m + "m " + s + "s";
                                        }}
                                    }}, 1000);
                                </script>
                                """,
                                height=40
                            )
                            
                        with col2:
                            if float(item['current_price']) == 0:
                                st.markdown('<span class="badge badge-urgent">FREE / DONATION</span>', unsafe_allow_html=True)
                            elif float(item['current_price']) < float(item['original_price']):
                                st.markdown('<span class="badge badge-discounted">Discounted (50%)</span>', unsafe_allow_html=True)
                            else:
                                st.markdown('<span class="badge badge-available">Available</span>', unsafe_allow_html=True)
                            
                            st.markdown(f"<br>**Stock:** {item['quantity']} units", unsafe_allow_html=True)
                            if float(item['current_price']) == 0:
                                st.markdown("100% Free / Sponsored")
                            elif float(item['current_price']) < float(item['original_price']):
                                st.markdown(f"Discounted: {item['current_price']:.2f} BDT (Standard: {item['original_price']:.2f})")
                            else:
                                st.markdown(f"Price: {item['current_price']:.2f} BDT")
                            
                        with col3:
                            with st.expander("Process Claim", expanded=False):
                                claim_qty = st.number_input("Request Volume", min_value=0, max_value=item['quantity'], value=0, key=f"qty_{item['batch_id']}")
                                if st.button("Execute Transaction", type="primary", key=f"claim_{item['batch_id']}", use_container_width=True):
                                    try:
                                        # Use Stored Procedure for Safe Claim Transaction
                                        cursor.callproc('sp_claim_food', (active_receiver_id, item['batch_id'], claim_qty))
                                        conn.commit()
                                        st.toast("Transaction Completed Successfully.")
                                        st.rerun()
                                    except Error as e:
                                        st.error(f"Transaction Rejected: {e.msg}")
        cursor.close()
        conn.close()

elif role == "Database":
    st.header("Schema & State Inspector")
    st.write("Real-time read replica of the internal relational table structures.")
    
    conn = get_db_connection()
    if conn:
        t1, t2, t3, t4, t5 = st.tabs(["vendors", "receivers", "food_batches", "claims", "vw_active_batches"])
        
        def load_table(table_name):
            cursor = conn.cursor(dictionary=True)
            cursor.execute(f"SELECT * FROM {table_name}")
            data = cursor.fetchall()
            cursor.close()
            return pd.DataFrame(data)
            
        with t1:
            st.subheader("Entity: vendors")
            st.dataframe(load_table("vendors"), use_container_width=True)
            
        with t2:
            st.subheader("Entity: receivers")
            st.dataframe(load_table("receivers"), use_container_width=True)
            
        with t3:
            st.subheader("Entity: food_batches")
            st.dataframe(load_table("food_batches"), use_container_width=True)
            
        with t4:
            st.subheader("Entity: claims")
            st.dataframe(load_table("claims"), use_container_width=True)
            
        with t5:
            st.subheader("View: vw_active_batches (Dynamic Pricing)")
            try:
                st.dataframe(load_table("vw_active_batches"), use_container_width=True)
            except Error as e:
                st.warning(f"View not found. Did you run 03_automation.sql? Error: {e}")
        
        conn.close()