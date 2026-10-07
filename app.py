import os
import re
from datetime import datetime
from uuid import uuid4

import pandas as pd
import streamlit as st

# File paths for two separate models
VIP_INTAKE_FILE = "vip_key_intake_log.csv"
VIP_HANDOFF_FILE = "vip_key_handoff_queue.csv"
VIP_CLOSED_FILE = "vip_key_closed_handoffs.csv"

TIMESHARE_EXIT_INTAKE_FILE = "timeshare_exit_intake_log.csv"
TIMESHARE_EXIT_HANDOFF_FILE = "timeshare_exit_handoff_queue.csv"
TIMESHARE_EXIT_CLOSED_FILE = "timeshare_exit_closed_handoffs.csv"

st.set_page_config(page_title="Lead Desk - VIP Key & Timeshare Exit", layout="wide")

# ============ UTILITY FUNCTIONS ============

def ensure_files():
    files = [
        VIP_INTAKE_FILE, VIP_HANDOFF_FILE, VIP_CLOSED_FILE,
        TIMESHARE_EXIT_INTAKE_FILE, TIMESHARE_EXIT_HANDOFF_FILE, TIMESHARE_EXIT_CLOSED_FILE
    ]
    for path in files:
        if not os.path.exists(path):
            pd.DataFrame().to_csv(path, index=False)


def load_df(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return pd.DataFrame()
    return pd.read_csv(path)


def save_df(df, path):
    df.to_csv(path, index=False)


def validate_email(email):
    return bool(re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", str(email).strip()))


def validate_phone(phone):
    cleaned = re.sub(r"[^0-9]", str(phone), flags=re.UNICODE)
    return len(cleaned) >= 10


def generate_intake_id(prefix):
    return f"{prefix}-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid4().hex[:6].upper()}"


# ============ VIP KEY FUNCTIONS ============

def vip_log_intake(company_name, contact_name, title, email, phone, city, state, services_interested, initial_notes, contractor_name):
    if not all([company_name, contact_name, email, phone]):
        st.error("Company name, contact name, email, and phone are required.")
        return None

    if not validate_email(email):
        st.error(f"Invalid email: {email}")
        return None

    if not validate_phone(phone):
        st.error(f"Invalid phone number: {phone}")
        return None

    intake_df = load_df(VIP_INTAKE_FILE)
    new_row = {
        "intake_id": generate_intake_id("VIP"),
        "date_logged": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "company_name": company_name.strip(),
        "contact_name": contact_name.strip(),
        "title": title.strip() if title else "",
        "email": email.strip(),
        "phone": phone.strip(),
        "city": city.strip() if city else "",
        "state": state.strip() if state else "",
        "services_interested": services_interested.strip() if services_interested else "",
        "lead_source": "intake",
        "priority": "medium",
        "fit_score": "pending",
        "initial_notes": initial_notes.strip() if initial_notes else "",
        "contractor_name": contractor_name.strip() if contractor_name else "Unknown",
        "status": "new",
    }

    intake_df = pd.concat([intake_df, pd.DataFrame([new_row])], ignore_index=True)
    save_df(intake_df, VIP_INTAKE_FILE)
    return new_row


def vip_create_handoff(intake_id, assigned_to, priority, follow_up_date, handoff_notes):
    intake_df = load_df(VIP_INTAKE_FILE)
    row = intake_df[intake_df["intake_id"] == intake_id]
    if row.empty:
        st.error(f"Intake ID not found: {intake_id}")
        return None

    intake_df.loc[intake_df["intake_id"] == intake_id, "status"] = "ready_for_handoff"
    save_df(intake_df, VIP_INTAKE_FILE)

    handoff_df = load_df(VIP_HANDOFF_FILE)
    new_row = {
        "handoff_id": generate_intake_id("VIP-HO"),
        "intake_id": intake_id,
        "company_name": row.iloc[0]["company_name"],
        "contact_name": row.iloc[0]["contact_name"],
        "handoff_date": datetime.now().strftime("%Y-%m-%d"),
        "assigned_to": assigned_to.strip(),
        "priority": priority,
        "follow_up_date": follow_up_date if follow_up_date else "",
        "status": "pending",
        "handoff_notes": handoff_notes.strip() if handoff_notes else "",
    }

    handoff_df = pd.concat([handoff_df, pd.DataFrame([new_row])], ignore_index=True)
    save_df(handoff_df, VIP_HANDOFF_FILE)
    return new_row


# ============ TIMESHARE EXIT FUNCTIONS ============

def timeshare_exit_log_intake(
    owner_name, contact_email, phone, property_name, location, 
    purchase_year, annual_maintenance, buyer_motivation, desperation_level, 
    contacted_reseller, secondary_market_attempted, contractor_name
):
    if not all([owner_name, contact_email, phone, property_name]):
        st.error("Owner name, email, phone, and property name are required.")
        return None

    if not validate_email(contact_email):
        st.error(f"Invalid email: {contact_email}")
        return None

    if not validate_phone(phone):
        st.error(f"Invalid phone number: {phone}")
        return None

    intake_df = load_df(TIMESHARE_EXIT_INTAKE_FILE)
    new_row = {
        "intake_id": generate_intake_id("TS"),
        "date_logged": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "owner_name": owner_name.strip(),
        "contact_email": contact_email.strip(),
        "phone": phone.strip(),
        "property_name": property_name.strip(),
        "location": location.strip() if location else "",
        "purchase_year": int(purchase_year) if purchase_year else "",
        "annual_maintenance": float(maintenance_cost) if maintenance_cost else 0,
        "buyer_motivation": buyer_motivation,  # high_maintenance, family_change, financial_hardship, unplanned_inheritance
        "desperation_level": desperation_level,  # low, medium, high, critical
        "contacted_reseller": "Yes" if contacted_reseller else "No",
        "secondary_market_attempted": "Yes" if secondary_market_attempted else "No",
        "ready_for_exit": "Yes" if (contacted_reseller or secondary_market_attempted) else "No",
        "lead_source": "outbound",
        "contractor_name": contractor_name.strip() if contractor_name else "Unknown",
        "status": "new",
        "notes": "",
    }

    intake_df = pd.concat([intake_df, pd.DataFrame([new_row])], ignore_index=True)
    save_df(intake_df, TIMESHARE_EXIT_INTAKE_FILE)
    return new_row


def timeshare_exit_create_handoff(intake_id, assigned_to, exit_solution, follow_up_date, handoff_notes):
    intake_df = load_df(TIMESHARE_EXIT_INTAKE_FILE)
    row = intake_df[intake_df["intake_id"] == intake_id]
    if row.empty:
        st.error(f"Intake ID not found: {intake_id}")
        return None

    intake_df.loc[intake_df["intake_id"] == intake_id, "status"] = "ready_for_handoff"
    save_df(intake_df, TIMESHARE_EXIT_INTAKE_FILE)

    handoff_df = load_df(TIMESHARE_EXIT_HANDOFF_FILE)
    new_row = {
        "handoff_id": generate_intake_id("TS-HO"),
        "intake_id": intake_id,
        "owner_name": row.iloc[0]["owner_name"],
        "property_name": row.iloc[0]["property_name"],
        "desperation_level": row.iloc[0]["desperation_level"],
        "handoff_date": datetime.now().strftime("%Y-%m-%d"),
        "assigned_to": assigned_to.strip(),
        "exit_solution": exit_solution,  # legal_exit, donation, assisted_exit, buyer_match
        "follow_up_date": follow_up_date if follow_up_date else "",
        "status": "pending",
        "handoff_notes": handoff_notes.strip() if handoff_notes else "",
    }

    handoff_df = pd.concat([handoff_df, pd.DataFrame([new_row])], ignore_index=True)
    save_df(handoff_df, TIMESHARE_EXIT_HANDOFF_FILE)
    return new_row


def close_handoff(handoff_id, model_type):
    if model_type == "vip":
        handoff_file = VIP_HANDOFF_FILE
        closed_file = VIP_CLOSED_FILE
    else:
        handoff_file = TIMESHARE_EXIT_HANDOFF_FILE
        closed_file = TIMESHARE_EXIT_CLOSED_FILE

    handoff_df = load_df(handoff_file)
    if handoff_df.empty or handoff_id not in handoff_df["handoff_id"].values:
        st.error(f"Handoff not found: {handoff_id}")
        return False

    row = handoff_df[handoff_df["handoff_id"] == handoff_id].iloc[0]
    row_copy = row.copy()
    row_copy["status"] = "closed"

    closed_df = load_df(closed_file)
    closed_df = pd.concat([closed_df, pd.DataFrame([row_copy])], ignore_index=True)
    save_df(closed_df, closed_file)

    handoff_df = handoff_df[handoff_df["handoff_id"] != handoff_id]
    save_df(handoff_df, handoff_file)

    return True


def get_summary_cards(model_type):
    if model_type == "vip":
        intake_file, handoff_file, closed_file = VIP_INTAKE_FILE, VIP_HANDOFF_FILE, VIP_CLOSED_FILE
    else:
        intake_file, handoff_file, closed_file = TIMESHARE_EXIT_INTAKE_FILE, TIMESHARE_EXIT_HANDOFF_FILE, TIMESHARE_EXIT_CLOSED_FILE

    intake_df = load_df(intake_file)
    handoff_df = load_df(handoff_file)
    closed_df = load_df(closed_file)

    return {
        "Total Intakes": len(intake_df),
        "Pending Handoffs": len(handoff_df[handoff_df["status"] == "pending"]) if not handoff_df.empty else 0,
        "Closed Handoffs": len(closed_df),
    }


ensure_files()

# ============ UI LAYOUT ============

st.title("Lead Desk - VIP Key & Timeshare Exit")

# Model selector
model = st.radio("Select Lead Model", ["VIP Key Florida Concierge", "Timeshare Exit Optimization"])

if model == "VIP Key Florida Concierge":
    st.header("VIP Key Florida Concierge")
    
    summary = get_summary_cards("vip")
    cols = st.columns(3)
    for i, (label, value) in enumerate(summary.items()):
        cols[i].metric(label, value)

    intake_tab, handoff_tab, closed_tab, reports_tab = st.tabs(["Intake", "Handoff Queue", "Closed", "Reports"])

    with intake_tab:
        st.subheader("New VIP Lead Intake")
        with st.form("vip_intake_form", clear_on_submit=True):
            company_name = st.text_input("Company Name")
            contact_name = st.text_input("Contact Name")
            title = st.text_input("Title")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            city = st.text_input("City")
            state = st.text_input("State")
            services_interested = st.text_area("Services Interested")
            initial_notes = st.text_area("Initial Notes")
            contractor_name = st.text_input("Contractor Name")
            submitted = st.form_submit_button("Log VIP Intake")

            if submitted:
                result = vip_log_intake(
                    company_name, contact_name, title, email, phone,
                    city, state, services_interested, initial_notes, contractor_name
                )
                if result:
                    st.success(f"Lead logged: {result['intake_id']}")

    with handoff_tab:
        st.subheader("VIP Handoff Queue")
        handoff_df = load_df(VIP_HANDOFF_FILE)
        if handoff_df.empty or (handoff_df["status"] == "pending").sum() == 0:
            st.info("No pending handoffs.")
        else:
            pending_df = handoff_df[handoff_df["status"] == "pending"].copy()
            st.dataframe(pending_df, use_container_width=True)

            if not pending_df.empty:
                handoff_selection = st.selectbox("Select handoff to close", pending_df["handoff_id"].tolist())
                with st.form("close_vip_handoff"):
                    completion_notes = st.text_area("Completion Notes")
                    close_submit = st.form_submit_button("Close Handoff")
                    if close_submit:
                        if close_handoff(handoff_selection, "vip"):
                            st.success(f"Handoff closed: {handoff_selection}")
                            st.rerun()

    with closed_tab:
        st.subheader("Closed VIP Handoffs")
        closed_df = load_df(VIP_CLOSED_FILE)
        if closed_df.empty:
            st.info("No closed handoffs yet.")
        else:
            st.dataframe(closed_df, use_container_width=True)

    with reports_tab:
        st.subheader("VIP Reports")
        intake_df = load_df(VIP_INTAKE_FILE)
        if not intake_df.empty:
            st.metric("Total Intakes", len(intake_df))
            if "state" in intake_df.columns:
                by_state = intake_df.groupby("state").size().sort_values(ascending=False)
                st.bar_chart(by_state)
            st.dataframe(intake_df, use_container_width=True)

else:
    st.header("Timeshare Exit - Desperation-Driven Lead Optimization")
    st.markdown("""
    **Target Profile:** Timeshare owners who have:
    - Already attempted secondary market sales (gave up on resale)
    - Contacted resale companies (wasted money on failed brokers)
    - High annual maintenance costs they can no longer afford
    - Given up on selling; now seeking cheapest exit
    """)
    
    summary = get_summary_cards("timeshare_exit")
    cols = st.columns(3)
    for i, (label, value) in enumerate(summary.items()):
        cols[i].metric(label, value)

    intake_tab, handoff_tab, closed_tab, reports_tab = st.tabs(["Intake", "Handoff Queue", "Closed", "Reports"])

    with intake_tab:
        st.subheader("Timeshare Exit Lead Intake")
        st.markdown("**Focus on owners who have failed secondary market & gave up on selling**")
        
        with st.form("ts_exit_intake_form", clear_on_submit=True):
            owner_name = st.text_input("Owner Name")
            contact_email = st.text_input("Email")
            phone = st.text_input("Phone")
            property_name = st.text_input("Property Name")
            location = st.text_input("Location (State/Region)")
            purchase_year = st.number_input("Purchase Year", min_value=1990, max_value=2024, step=1)
            annual_maintenance = st.number_input("Annual Maintenance Cost ($)", min_value=0, step=50)
            
            buyer_motivation = st.selectbox(
                "Primary Motivation",
                ["high_maintenance", "family_change", "financial_hardship", "unplanned_inheritance"]
            )
            
            desperation_level = st.selectbox(
                "Desperation Level (High = Cheapest Exit Seeker)",
                ["low", "medium", "high", "critical"]
            )
            
            contacted_reseller = st.checkbox("Has contacted resale brokers? (Failed attempt)")
            secondary_market_attempted = st.checkbox("Attempted secondary market sale? (Gave up)")
            
            contractor_name = st.text_input("Your Name")
            submitted = st.form_submit_button("Log Timeshare Exit Lead")

            if submitted:
                result = timeshare_exit_log_intake(
                    owner_name, contact_email, phone, property_name, location,
                    purchase_year, annual_maintenance, buyer_motivation, desperation_level,
                    contacted_reseller, secondary_market_attempted, contractor_name
                )
                if result:
                    st.success(f"Lead logged: {result['intake_id']}")
                    st.info("✓ Lead shows strong exit intent — ready for qualification")

    with handoff_tab:
        st.subheader("Timeshare Exit Handoff Queue")
        handoff_df = load_df(TIMESHARE_EXIT_HANDOFF_FILE)
        if handoff_df.empty or (handoff_df["status"] == "pending").sum() == 0:
            st.info("No pending handoffs.")
        else:
            pending_df = handoff_df[handoff_df["status"] == "pending"].copy()
            st.dataframe(pending_df, use_container_width=True)

            if not pending_df.empty:
                handoff_selection = st.selectbox("Select handoff to close", pending_df["handoff_id"].tolist())
                with st.form("close_ts_handoff"):
                    exit_solution = st.selectbox(
                        "Exit Solution Offered",
                        ["legal_exit", "donation", "assisted_exit", "buyer_match"]
                    )
                    follow_up_date = st.date_input("Follow-up Date")
                    completion_notes = st.text_area("Resolution Notes")
                    close_submit = st.form_submit_button("Close Handoff")
                    if close_submit:
                        if close_handoff(handoff_selection, "timeshare_exit"):
                            st.success(f"Handoff closed: {handoff_selection}")
                            st.rerun()

    with closed_tab:
        st.subheader("Closed Timeshare Exit Handoffs")
        closed_df = load_df(TIMESHARE_EXIT_CLOSED_FILE)
        if closed_df.empty:
            st.info("No closed handoffs yet.")
        else:
            st.dataframe(closed_df, use_container_width=True)

    with reports_tab:
        st.subheader("Timeshare Exit Analytics")
        intake_df = load_df(TIMESHARE_EXIT_INTAKE_FILE)
        
        if not intake_df.empty:
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Leads", len(intake_df))
            
            if "desperation_level" in intake_df.columns:
                critical = len(intake_df[intake_df["desperation_level"] == "critical"])
                col2.metric("Critical Desperation (Highest Priority)", critical)
            
            if "secondary_market_attempted" in intake_df.columns:
                gave_up = len(intake_df[intake_df["secondary_market_attempted"] == "Yes"])
                col3.metric("Gave Up On Resale", gave_up)

            st.subheader("Desperation Distribution")
            if "desperation_level" in intake_df.columns:
                desperation_counts = intake_df["desperation_level"].value_counts()
                st.bar_chart(desperation_counts)

            st.subheader("Buyer Motivation Breakdown")
            if "buyer_motivation" in intake_df.columns:
                motivation_counts = intake_df["buyer_motivation"].value_counts()
                st.bar_chart(motivation_counts)

            st.subheader("All Timeshare Exit Leads")
            st.dataframe(intake_df, use_container_width=True)
