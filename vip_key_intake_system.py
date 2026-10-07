#!/usr/bin/env python3
"""
VIP Key Florida Concierge Lead Intake System
Independent contractor lead logging and handoff workflow
"""

import csv
import os
import re
from datetime import datetime
from pathlib import Path

# File paths
INTAKE_LOG = "vip_key_intake_log.csv"
HANDOFF_QUEUE = "vip_key_handoff_queue.csv"
CLOSED_HANDOFFS = "vip_key_closed_handoffs.csv"

INTAKE_HEADERS = [
    "intake_id",
    "date_logged",
    "company_name",
    "contact_name",
    "title",
    "email",
    "phone",
    "city",
    "state",
    "services_interested",
    "initial_notes",
    "contractor_name",
    "status",  # new, qualified, ready_for_handoff
]

HANDOFF_HEADERS = [
    "handoff_id",
    "intake_id",
    "company_name",
    "contact_name",
    "handoff_date",
    "assigned_to",
    "priority",  # high, medium, low
    "follow_up_date",
    "status",  # pending, handed_off, closed
    "handoff_notes",
]


def generate_id(prefix: str) -> str:
    """Generate unique ID with timestamp."""
    return f"{prefix}-{datetime.now().strftime('%Y%m%d%H%M%S')}"


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """Validate phone format (flexible for various formats)."""
    cleaned = re.sub(r"[^0-9+()-]", "", phone)
    return len(cleaned) >= 10


def log_intake(
    company_name: str,
    contact_name: str,
    title: str,
    email: str,
    phone: str,
    city: str,
    state: str,
    services_interested: str,
    initial_notes: str = "",
    contractor_name: str = "Unknown",
) -> dict | None:
    """Log a new client intake."""
    
    # Validation
    if not all([company_name, contact_name, email, phone]):
        print("ERROR: Missing required fields (company_name, contact_name, email, phone)")
        return None
    
    if not validate_email(email):
        print(f"ERROR: Invalid email format: {email}")
        return None
    
    if not validate_phone(phone):
        print(f"ERROR: Invalid phone format: {phone}")
        return None
    
    # Create intake record
    intake_id = generate_id("INT")
    intake_record = {
        "intake_id": intake_id,
        "date_logged": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "company_name": company_name,
        "contact_name": contact_name,
        "title": title,
        "email": email,
        "phone": phone,
        "city": city,
        "state": state,
        "services_interested": services_interested,
        "initial_notes": initial_notes,
        "contractor_name": contractor_name,
        "status": "new",
    }
    
    # Append to intake log
    file_exists = Path(INTAKE_LOG).exists()
    with open(INTAKE_LOG, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=INTAKE_HEADERS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(intake_record)
    
    print(f"✓ Intake logged: {intake_id} - {company_name}")
    return intake_record


def create_handoff(
    intake_id: str,
    assigned_to: str,
    priority: str = "medium",
    follow_up_date: str = None,
    handoff_notes: str = "",
) -> dict | None:
    """Move qualified intake to handoff queue."""
    
    # Find intake record
    intake_record = None
    with open(INTAKE_LOG, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["intake_id"] == intake_id:
                intake_record = row
                break
    
    if not intake_record:
        print(f"ERROR: Intake ID not found: {intake_id}")
        return None
    
    # Update intake status
    update_intake_status(intake_id, "ready_for_handoff")
    
    # Create handoff record
    handoff_id = generate_id("HO")
    handoff_record = {
        "handoff_id": handoff_id,
        "intake_id": intake_id,
        "company_name": intake_record["company_name"],
        "contact_name": intake_record["contact_name"],
        "handoff_date": datetime.now().strftime("%Y-%m-%d"),
        "assigned_to": assigned_to,
        "priority": priority,
        "follow_up_date": follow_up_date or "",
        "status": "pending",
        "handoff_notes": handoff_notes,
    }
    
    # Append to handoff queue
    file_exists = Path(HANDOFF_QUEUE).exists()
    with open(HANDOFF_QUEUE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HANDOFF_HEADERS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(handoff_record)
    
    print(f"✓ Handoff created: {handoff_id} - Assigned to {assigned_to}")
    return handoff_record


def update_intake_status(intake_id: str, new_status: str) -> bool:
    """Update intake status."""
    rows = []
    found = False
    
    with open(INTAKE_LOG, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["intake_id"] == intake_id:
                row["status"] = new_status
                found = True
            rows.append(row)
    
    if found:
        with open(INTAKE_LOG, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=INTAKE_HEADERS)
            writer.writeheader()
            writer.writerows(rows)
        return True
    
    return False


def close_handoff(handoff_id: str, completion_notes: str = "") -> bool:
    """Close a handoff and move to closed handoffs."""
    handoff_record = None
    remaining_handoffs = []
    
    with open(HANDOFF_QUEUE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["handoff_id"] == handoff_id:
                row["status"] = "closed"
                handoff_record = row
            remaining_handoffs.append(row)
    
    if not handoff_record:
        print(f"ERROR: Handoff ID not found: {handoff_id}")
        return False
    
    # Update handoff queue
    with open(HANDOFF_QUEUE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HANDOFF_HEADERS)
        writer.writeheader()
        writer.writerows(remaining_handoffs)
    
    # Append to closed handoffs
    file_exists = Path(CLOSED_HANDOFFS).exists()
    with open(CLOSED_HANDOFFS, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HANDOFF_HEADERS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(handoff_record)
    
    print(f"✓ Handoff closed: {handoff_id}")
    return True


def view_pending_handoffs() -> list[dict]:
    """View all pending handoffs."""
    if not Path(HANDOFF_QUEUE).exists():
        print("No handoff queue found.")
        return []
    
    pending = []
    with open(HANDOFF_QUEUE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["status"] == "pending":
                pending.append(row)
    
    if pending:
        print(f"\n{'ID':<20} {'Company':<25} {'Assigned To':<20} {'Priority':<10}")
        print("-" * 75)
        for p in pending:
            print(f"{p['handoff_id']:<20} {p['company_name']:<25} {p['assigned_to']:<20} {p['priority']:<10}")
    else:
        print("No pending handoffs.")
    
    return pending


def view_intake_status(contractor_name: str = None) -> list[dict]:
    """View intake log, optionally filtered by contractor."""
    if not Path(INTAKE_LOG).exists():
        print("No intake log found.")
        return []
    
    records = []
    with open(INTAKE_LOG, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if contractor_name is None or row["contractor_name"] == contractor_name:
                records.append(row)
    
    if records:
        print(f"\n{'ID':<20} {'Company':<25} {'Status':<20} {'Date':<20}")
        print("-" * 85)
        for r in records:
            print(f"{r['intake_id']:<20} {r['company_name']:<25} {r['status']:<20} {r['date_logged']:<20}")
    else:
        print("No intake records found.")
    
    return records


def export_handoff_report() -> str:
    """Generate a summary handoff report."""
    if not Path(HANDOFF_QUEUE).exists():
        return "No handoff data available."
    
    pending = []
    with open(HANDOFF_QUEUE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["status"] == "pending":
                pending.append(row)
    
    report = f"\n{'='*80}\n"
    report += f"VIP KEY FLORIDA - HANDOFF REPORT\n"
    report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"{'='*80}\n\n"
    report += f"PENDING HANDOFFS: {len(pending)}\n\n"
    
    for p in pending:
        report += f"Handoff ID: {p['handoff_id']}\n"
        report += f"  Company: {p['company_name']}\n"
        report += f"  Contact: {p['contact_name']}\n"
        report += f"  Assigned To: {p['assigned_to']}\n"
        report += f"  Priority: {p['priority']}\n"
        report += f"  Follow-up: {p['follow_up_date']}\n"
        report += f"  Notes: {p['handoff_notes']}\n"
        report += "-" * 80 + "\n"
    
    return report


if __name__ == "__main__":
    print("VIP Key Florida Concierge Lead Intake System")
    print("(Import functions for use in your workflow)")
