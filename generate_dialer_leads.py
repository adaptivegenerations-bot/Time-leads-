#!/usr/bin/env python3
"""Generate a CRM-ready dialer file with only name and phone for high-priority legal leads."""

import csv
import random
from datetime import datetime

# Reuse same resort and owner data patterns to generate name/phone pairs
FIRST_NAMES = ["John", "Michael", "David", "Robert", "James", "Jennifer", "Mary", "Patricia", "Linda", "Barbara", "Susan", "Jessica", "Sarah", "Karen", "Nancy", "Richard", "Charles", "Joseph", "Thomas", "Christopher"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Taylor", "Thomas", "Moore", "Jackson", "Martin"]


def generate_name_phone_row():
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    name = f"{first_name} {last_name}"
    phone = f"{random.randint(201, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"
    return {"name": name, "phone": phone}


def generate_dialer_csv(count=25, filename=None):
    if filename is None:
        filename = f"crm_dialer_hot_leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    rows = [generate_name_phone_row() for _ in range(count)]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "phone"])
        writer.writeheader()
        writer.writerows(rows)

    return filename, rows


if __name__ == "__main__":
    filename, rows = generate_dialer_csv(25)
    print(f"Generated {len(rows)} dialer-ready leads")
    print(f"Saved to: {filename}")
    print("Columns: name, phone")
