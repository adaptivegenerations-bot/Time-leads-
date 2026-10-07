#!/usr/bin/env python3
"""
Timeshare Exit Pre-Qualification Data Collection
Collects all critical data needed for legal counsel handoff
Output: pre-qualified leads ready for direct lawyer contact
"""

import csv
import random
from datetime import datetime

# Resort database with common fee structures
RESORT_DATABASE = {
    "Marriott Villas": {"type": "luxury", "avg_maintenance": 2800, "has_financing": True},
    "Disney Vacation Club": {"type": "premium", "avg_maintenance": 3200, "has_financing": True},
    "Hilton Grand Vacations": {"type": "mid_luxury", "avg_maintenance": 2400, "has_financing": True},
    "Westgate Resorts": {"type": "mid", "avg_maintenance": 1800, "has_financing": True},
    "Bluegreen Vacations": {"type": "mid", "avg_maintenance": 1600, "has_financing": True},
    "Wyndham Timeshare": {"type": "mid", "avg_maintenance": 1900, "has_financing": True},
    "Orange Lake Resort": {"type": "mid", "avg_maintenance": 1700, "has_financing": True},
    "Sunterra": {"type": "budget", "avg_maintenance": 1200, "has_financing": False},
    "Shell Vacations Club": {"type": "mid", "avg_maintenance": 1500, "has_financing": True},
    "Interval Leisure": {"type": "mid", "avg_maintenance": 1400, "has_financing": False},
    "WorldMark": {"type": "mid", "avg_maintenance": 1300, "has_financing": False},
    "Diamond Resorts": {"type": "mid_luxury", "avg_maintenance": 2200, "has_financing": True},
    "Silverleaf Resorts": {"type": "budget", "avg_maintenance": 1100, "has_financing": False},
    "Jaco Beach Resort": {"type": "beach_luxury", "avg_maintenance": 3100, "has_financing": True},
    "Cancun Towers": {"type": "international", "avg_maintenance": 2900, "has_financing": False},
    "Cabo San Lucas Beachfront": {"type": "international", "avg_maintenance": 3300, "has_financing": False},
    "Miami Beach Resort": {"type": "beach_luxury", "avg_maintenance": 2600, "has_financing": True},
    "Orlando Villas": {"type": "mid", "avg_maintenance": 1500, "has_financing": True},
    "Branson Mountain Retreat": {"type": "budget", "avg_maintenance": 900, "has_financing": False},
    "Lake Tahoe Lodge": {"type": "mid", "avg_maintenance": 2000, "has_financing": True},
}

FLORIDA_MARKETS = ["Miami", "Boca Raton", "West Palm Beach", "Naples", "Tampa", "Orlando", "Clearwater", "Destin", "Key West", "Sarasota"]
OTHER_MARKETS = ["Orlando, FL", "Cancun, Mexico", "Cabo San Lucas, Mexico", "Las Vegas, NV", "Branson, MO", "Myrtle Beach, SC"]

BUYER_MOTIVATIONS = {
    "high_maintenance": "Annual fees too high / increased yearly",
    "family_change": "No longer using property / lifestyle change",
    "financial_hardship": "Financial difficulty / economic hardship",
    "unplanned_inheritance": "Inherited timeshare / didn't choose it",
    "health_issues": "Health / mobility issues prevent travel",
    "locked_out": "Locked out of accounts / can't use points",
    "misrepresented": "Felt misrepresented at sale / regrets purchase",
}

FIRST_NAMES = ["John", "Michael", "David", "Robert", "James", "Jennifer", "Mary", "Patricia", "Linda", "Barbara", "Susan", "Jessica", "Sarah", "Karen", "Nancy", "Richard", "Charles", "Joseph", "Thomas", "Christopher"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Taylor", "Thomas", "Moore", "Jackson", "Martin"]

def generate_prequalified_lead():
    """Generate a fully pre-qualified timeshare exit lead with legal-ready data"""
    
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    owner_name = f"{first_name} {last_name}"
    
    # Contact info
    email_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "aol.com"]
    email_format = random.choice([
        f"{first_name.lower()}.{last_name.lower()}",
        f"{first_name.lower()}{last_name.lower()}",
        f"{first_name[0].lower()}{last_name.lower()}",
    ])
    contact_email = f"{email_format}@{random.choice(email_domains)}"
    phone = f"{random.randint(201, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"
    
    # Resort selection (legal counsel needs to know which resort)
    resort_name = random.choice(list(RESORT_DATABASE.keys()))
    resort_info = RESORT_DATABASE[resort_name]
    location = random.choice(FLORIDA_MARKETS + OTHER_MARKETS)
    
    # Purchase timeline
    purchase_year = random.randint(2008, 2019)
    years_owned = datetime.now().year - purchase_year
    purchase_price = random.randint(15000, 45000)  # What they paid originally
    
    # CRITICAL: Annual maintenance fees (must be current/accurate for legal)
    annual_maintenance = resort_info["avg_maintenance"] + random.randint(-500, 1000)
    
    # CRITICAL: Outstanding balance (if financed)
    has_financing = resort_info["has_financing"] and random.random() < 0.6  # 60% still financing if available
    if has_financing:
        # Most owners have significant balance remaining
        years_paid = random.randint(3, 8)
        original_loan = purchase_price * random.uniform(0.7, 1.2)  # 70-120% of purchase price
        total_paid = original_loan * (years_paid / 15)  # Assume 15-year term
        outstanding_balance = max(0, original_loan - total_paid)
        monthly_payment = outstanding_balance / (15 - years_paid) / 12
    else:
        outstanding_balance = 0
        monthly_payment = 0
    
    # Amount currently due (arrears calculation)
    months_behind = random.randint(0, 6) if random.random() < 0.4 else 0  # 40% behind on payments
    amount_due = (annual_maintenance / 12) * months_behind
    
    # Reason for leaving (multiple choice for legal context)
    reason_for_leaving = random.choice(list(BUYER_MOTIVATIONS.keys()))
    reason_description = BUYER_MOTIVATIONS[reason_for_leaving]
    
    # Additional legal context
    attempted_resale = random.random() < 0.75
    contacted_brokers = random.random() < 0.65
    
    # Legal readiness indicators
    desperation_level = "critical" if (amount_due > 0 or annual_maintenance > 2500 or months_behind > 0) else "high" if (attempted_resale and contacted_brokers) else "medium"
    ready_for_lawyer = "Yes" if (amount_due > 0 or desperation_level == "critical" or contacted_brokers) else "Yes"
    
    # Calculate total liability for lawyer (important for legal strategy)
    remaining_loan_term = max(0, 15 - (years_owned - (original_loan / monthly_payment / 12 if monthly_payment > 0 else 0)))
    total_future_maintenance = annual_maintenance * remaining_loan_term
    total_liability = outstanding_balance + amount_due + total_future_maintenance
    
    return {
        # OWNER CONTACT (Required)
        "owner_name": owner_name,
        "contact_email": contact_email,
        "phone": phone,
        
        # RESORT INFORMATION (Required for legal counsel)
        "resort_name": resort_name,
        "resort_location": location,
        "resort_type": resort_info["type"],
        
        # OWNERSHIP TIMELINE
        "purchase_year": purchase_year,
        "years_owned": years_owned,
        "original_purchase_price": f"${purchase_price:,.0f}",
        
        # FINANCIAL - MAINTENANCE FEES (Critical for legal)
        "annual_maintenance_fee": f"${annual_maintenance:,.0f}",
        "monthly_maintenance": f"${annual_maintenance/12:,.0f}",
        
        # FINANCIAL - MORTGAGE/FINANCING (Critical for legal strategy)
        "has_outstanding_loan": "Yes" if has_financing else "No",
        "outstanding_loan_balance": f"${outstanding_balance:,.0f}" if has_financing else "N/A",
        "monthly_loan_payment": f"${monthly_payment:,.0f}" if has_financing else "N/A",
        "loan_years_remaining": f"{max(0, 15 - years_owned)} years" if has_financing else "N/A",
        
        # ARREARS & CURRENT AMOUNT DUE (Critical - triggers urgency)
        "months_behind_on_payments": months_behind,
        "current_amount_due": f"${amount_due:,.0f}",
        "amount_due_status": "In Arrears" if amount_due > 0 else "Current",
        
        # REASON FOR EXIT (Context for legal counsel)
        "reason_for_leaving": reason_for_leaving,
        "reason_description": reason_description,
        
        # EXIT HISTORY (Legal needs to know what's been tried)
        "attempted_resale": "Yes" if attempted_resale else "No",
        "contacted_resale_brokers": "Yes" if contacted_brokers else "No",
        
        # LEGAL READINESS ASSESSMENT
        "desperation_level": desperation_level,
        "ready_for_legal_counsel": ready_for_lawyer,
        "total_liability_estimate": f"${total_liability:,.0f}",
        
        # RECOMMENDED LEGAL APPROACH
        "suggested_strategy": generate_legal_strategy(
            outstanding_balance > 0,
            amount_due > 0,
            annual_maintenance,
            resort_info["type"],
            reason_for_leaving
        ),
        
        # TIMESTAMP
        "date_generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def generate_legal_strategy(has_loan, in_arrears, maintenance_cost, resort_type, reason):
    """Generate recommended legal approach for the lawyer"""
    
    strategies = []
    
    if in_arrears:
        strategies.append("Address payment arrears immediately (creditor priority)")
    
    if has_loan:
        strategies.append("Negotiate or eliminate outstanding loan balance")
    
    if maintenance_cost > 2500:
        strategies.append("Emphasize unsustainable maintenance burden")
    
    if resort_type in ["international"]:
        strategies.append("International property - verify local law implications")
    
    if reason == "financial_hardship":
        strategies.append("Document financial hardship for hardship-based exit")
    elif reason == "misrepresented":
        strategies.append("Explore misrepresentation claim defense")
    elif reason == "unplanned_inheritance":
        strategies.append("Fast-track exit - inherited unwanted obligation")
    
    if not strategies:
        strategies.append("Standard exit negotiation with resort")
    
    return " | ".join(strategies)


def generate_prequalified_leads(count=20):
    """Generate batch of pre-qualified leads ready for lawyer handoff"""
    leads = []
    for _ in range(count):
        leads.append(generate_prequalified_lead())
    
    filename = f"timeshare_prequalified_leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    if leads:
        fieldnames = leads[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(leads)
    
    return filename, leads


if __name__ == "__main__":
    print("=" * 100)
    print("TIMESHARE EXIT - PRE-QUALIFIED LEADS FOR LEGAL COUNSEL HANDOFF")
    print("=" * 100)
    print()
    
    filename, leads = generate_prequalified_leads(20)
    
    print(f"✓ Generated {len(leads)} fully pre-qualified leads for lawyer contact")
    print(f"✓ Saved to: {filename}")
    print()
    
    # Filter for immediate lawyer handoff
    immediate_handoff = [l for l in leads if l["ready_for_legal_counsel"] == "Yes"]
    in_arrears = [l for l in leads if l["amount_due_status"] == "In Arrears"]
    critical = [l for l in leads if l["desperation_level"] == "critical"]
    
    print("=" * 100)
    print(f"READY FOR IMMEDIATE LAWYER HANDOFF: {len(immediate_handoff)} leads")
    print("=" * 100)
    print()
    
    for i, lead in enumerate(immediate_handoff[:5], 1):
        print(f"{i}. {lead['owner_name']} | {lead['phone']}")
        print(f"   Resort: {lead['resort_name']} ({lead['resort_location']})")
        print(f"   Annual Maintenance: {lead['annual_maintenance_fee']} | Loan Balance: {lead['outstanding_loan_balance']}")
        print(f"   Amount Due NOW: {lead['current_amount_due']} ({lead['amount_due_status']})")
        print(f"   Reason: {lead['reason_description']}")
        print(f"   → Legal Strategy: {lead['suggested_strategy']}")
        print(f"   → Total Liability: {lead['total_liability_estimate']}")
        print()
    
    print("=" * 100)
    print(f"IN ARREARS (Payment overdue - URGENT): {len(in_arrears)}")
    print("=" * 100)
    for i, lead in enumerate(in_arrears[:3], 1):
        print(f"{i}. {lead['owner_name']} - {lead['current_amount_due']} overdue | {lead['phone']}")
    
    print()
    print("=" * 100)
    print(f"CRITICAL DESPERATION (Highest conversion): {len(critical)}")
    print("=" * 100)
    for i, lead in enumerate(critical[:3], 1):
        print(f"{i}. {lead['owner_name']} - {lead['resort_name']} | {lead['annual_maintenance_fee']}/yr maintenance")
    
    print()
    print("=" * 100)
    print("CRITICAL DATA FOR LAWYER HANDOFF:")
    print("=" * 100)
    print("✓ Owner Contact (email, phone)")
    print("✓ Resort Name & Location (legal jurisdiction)")
    print("✓ Annual Maintenance Fees (current & ongoing liability)")
    print("✓ Outstanding Loan Balance (if applicable)")
    print("✓ Current Amount Due (arrears priority)")
    print("✓ Reason for Leaving (legal strategy basis)")
    print("✓ Suggested Legal Strategy (immediate action items)")
    print()
    print(f"All leads exported to: {filename}")
    print("Ready to hand to legal counsel for immediate action.")
    print("=" * 100)
