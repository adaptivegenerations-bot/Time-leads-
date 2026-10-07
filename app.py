import os
import re
from datetime import datetime
from uuid import uuid4

import pandas as pd
import streamlit as st

INTAKE_FILE = "vip_key_intake_log.csv"
HANDOFF_FILE = "vip_key_handoff_queue.csv"
CLOSED_FILE = "vip_key_closed_handoffs.csv"

st.set_page_config(page_title="VIP Key Lead Desk", layout="wide")


def ensure_files():
    for path in [INTAKE_FILE, HANDOFF_FILE, CLOSED_FILE]:
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


def generate_intake_id():
    return f"INT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid4().hex[:6].upper()}"


def generate_handoff_id():
    return f"HO-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid4().hex[:6].upper()}"


def log_intake_record(
    company_name,
    contact_name,
    title,
    email,
    phone,
    city,
    state,
    services_interested,
    initial_notes,
    contractor_name,
):
    if not company_name or not contact_name or not email or not phone:
        st.error("Company name, contact name, email, and phone are required.")
        return None

    if not validate_email(email):
        st.error(f"Invalid email: {email}")
        return None

    if not validate_phone(phone):
        st.error(f"Invalid phone number: {phone}")
        return None

    intake_df = load_df(INTAKE_FILE)
    new_row = {
        "intake_id": generate_intake_id(),
        "date_logged": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "company_name": company_name.strip(),
        "contact_name": contact_name.strip(),
        "title": title.strip() if title else "",
        "email": email.strip(),
        "phone": phone.strip(),
        "city": city.strip() if city else "",
        "state": state.strip() if state else "",
        "services_interested": services_interested.strip() if services_interested else "",
        "initial_notes": initial_notes.strip() if initial_notes else "",
        "contractor_name": contractor_name.strip() if contractor_name else "Unknown",
        "status": "new",
    }

    intake_df = pd.concat([intake_df, pd.DataFrame([new_row])], ignore_index=True)
    save_df(intake_df, INTAKE_FILE)
    return new_row


def create_handoff_record(intake_id, assigned_to, priority, follow_up_date, handoff_notes):
    intake_df = load_df(INTAKE_FILE)
    row = intake_df[intake_df["intake_id"] == intake_id]
    if row.empty:
        st.error(f"Intake ID not found: {intake_id}")
        return None

    intake_df.loc[intake_df["intake_id"] == intake_id, "status"] = "ready_for_handoff"
    save_df(intake_df, INTAKE_FILE)

    handoff_df = load_df(HANDOFF_FILE)
    new_row = {
        "handoff_id": generate_handoff_id(),
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
    save_df(handoff_df, HANDOFF_FILE)
    return new_row


def close_handoff_record(handoff_id):
    handoff_df = load_df(HANDOFF_FILE)
    if handoff_df.empty or handoff_id not in handoff_df["handoff_id"].values:
        st.error(f"Handoff not found: {handoff_id}")
        return False

    row = handoff_df[handoff_df["handoff_id"] == handoff_id].iloc[0]
    row_copy = row.copy()
    row_copy["status"] = "closed"

    closed_df = load_df(CLOSED_FILE)
    closed_df = pd.concat([closed_df, pd.DataFrame([row_copy])], ignore_index=True)
    save_df(closed_df, CLOSED_FILE)

    handoff_df = handoff_df[handoff_df["handoff_id"] != handoff_id]
    save_df(handoff_df, HANDOFF_FILE)

    return True


def get_summary_cards():
    intake_df = load_df(INTAKE_FILE)
    handoff_df = load_df(HANDOFF_FILE)
    closed_df = load_df(CLOSED_FILE)

    return {
        "Total Intakes": len(intake_df),
        "Pending Handoffs": len(handoff_df[handoff_df["status"] == "pending"]),
        "Closed Handoffs": len(closed_df),
    }


ensure_files()

st.title("VIP Key Florida Concierge Lead Desk")

summary = get_summary_cards()
cols = st.columns(3)
for i, (label, value) in enumerate(summary.items()):
    cols[i].metric(label, value)

# Tabs
intake_tab, handoff_tab, closed_tab, reports_tab = st.tabs(
    ["Intake", "Handoff Queue", "Closed Handoffs", "Reports"]
)

with intake_tab:
    st.subheader("New Lead Intake")
    with st.form("intake_form", clear_on_submit=True):
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
        submitted = st.form_submit_button("Log Intake")

        if submitted:
            result = log_intake_record(
                company_name,
                contact_name,
                title,
                email,
                phone,
                city,
                state,
                services_interested,
                initial_notes,
                contractor_name,
            )
            if result:
                st.success(f"Lead logged successfully: {result['intake_id']}")

with handoff_tab:
    st.subheader("Handoff Queue")
    handoff_df = load_df(HANDOFF_FILE)
    if handoff_df.empty:
        st.info("No pending handoffs.")
    else:
        handoff_df = handoff_df[handoff_df["status"] == "pending"].copy()
        if handoff_df.empty:
            st.info("No pending handoffs.")
        else:
            st.dataframe(handoff_df, use_container_width=True)

            handoff_selection = st.selectbox("Select handoff to close", handoff_df["handoff_id"].tolist())
            selected_row = handoff_df[handoff_df["handoff_id"] == handoff_selection].iloc[0]
            with st.form("close_handoff_form"):
                completion_notes = st.text_area("Completion Notes")
                close_submit = st.form_submit_button("Close Handoff")
                if close_submit:
                    success = close_handoff_record(handoff_selection)
                    if success:
                        st.success(f"Handoff closed: {handoff_selection}")
                        st.rerun()

with closed_tab:
    st.subheader("Closed Handoffs")
    closed_df = load_df(CLOSED_FILE)
    if closed_df.empty:
        st.info("No closed handoffs yet.")
    else:
        st.dataframe(closed_df, use_container_width=True)

with reports_tab:
    st.subheader("Reports")
    intake_df = load_df(INTAKE_FILE)
    if intake_df.empty:
        st.info("No intake data available.")
    else:
        st.metric("Total Intakes", len(intake_df))
        st.metric("New Leads", int((intake_df["status"] == "new").sum()))
        st.metric("Ready for Handoff", int((intake_df["status"] == "ready_for_handoff").sum()))

        by_state = intake_df.groupby("state").size().sort_values(ascending=False)
        st.bar_chart(by_state)

        by_contractor = intake_df.groupby("contractor_name").size().sort_values(ascending=False)
        st.bar_chart(by_contractor)

        st.dataframe(intake_df, use_container_width=True)

    # Simple handoff report export
    st.markdown("### Handoff summary")
    handoff_df = load_df(HANDOFF_FILE)
    if handoff_df.empty:
        st.info("No handoff data available yet.")
    else:
        st.dataframe(handoff_df, use_container_width=True)
