#!/usr/bin/env python3
"""
High-urgency timeshare exit lead generator
Generates realistic leads with desperation signals for immediate conversion
"""

import csv
import random
from datetime import datetime, timedelta

TIMESHARE_PROPERTIES = [
    "Marriott Villas", "Disney Vacation Club", "Hilton Grand Vacations",
    "Westgate Resorts", "Bluegreen Vacations", "Wyndham Timeshare",
    "Orange Lake Resort", "Sunterra", "Silverleaf Resorts", "Diamond Resorts",
    "Shell Vacations Club", "Interval Leisure", "WorldMark", "Jaco Beach Resort",
    "Cancun Towers", "Cabo San Lucas Beachfront", "Miami Beach Resort", "Orlando Villas",
    "Branson Mountain Retreat", "Lake Tahoe Lodge"
]

FLORIDA_MARKETS = ["Miami", "Boca Raton", "West Palm Beach", "Naples", "Tampa", "Orlando", "Clearwater", "Destin", "Key West", "Sarasota"]
OTHER_MARKETS = ["Orlando, FL", "Cancun, Mexico", "Cabo San Lucas, Mexico", "Las Vegas, NV", "Branson, MO", "Myrtle Beach, SC"]

BUYER_MOTIVATIONS = ["high_maintenance", "family_change", "financial_hardship", "unplanned_inheritance"]

FIRST_NAMES = ["John", "Michael", "David", "Robert", "James", "Jennifer", "Mary", "Patricia", "Linda", "Barbara", "Susan", "Jessica", "Sarah", "Karen", "Nancy"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"]

def generate_realistic_lead():
    """Generate a single realistic timeshare owner lead with desperation signals"""
    
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    owner_name = f"{first_name} {last_name}"
    
    # Email variants
    email_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "aol.com"]
    email_format = random.choice([
        f"{first_name.lower()}.{last_name.lower()}",
        f"{first_name.lower()}{last_name.lower()}",
        f"{first_name[0].lower()}{last_name.lower()}",
        f"{owner_name.lower().replace(' ', '')}"
    ])
    contact_email = f"{email_format}@{random.choice(email_domains)}"
    
    # Realistic phone (US format)
    phone = f"{random.randint(201, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"
    
    # Property details
    property_name = random.choice(TIMESHARE_PROPERTIES)
    location = random.choice(FLORIDA_MARKETS + OTHER_MARKETS)
    
    # Purchase year: older = more regret, longer bleed
    purchase_year = random.randint(2008, 2019)
    years_owned = datetime.now().year - purchase_year
    
    # Annual maintenance: varies widely, but desperation increases with cost
    # Real data: $1,000-$2,500+ annually for decent properties
    base_maintenance = random.randint(1200, 3500)
    annual_maintenance = base_maintenance + (years_owned * random.randint(50, 150))  # Increases over time
    
    # Buyer motivation (correlated with urgency)
    buyer_motivation = random.choice(BUYER_MOTIVATIONS)
    
    # Desperation signals
    contacted_reseller = random.random() < 0.75  # 75% have tried resale
    secondary_market_attempted = random.random() < 0.65  # 65% gave up on secondary
    
    # Desperation level calculation
    desperation_score = 0
    if contacted_reseller:
        desperation_score += 2
    if secondary_market_attempted:
        desperation_score += 2
    if annual_maintenance > 2500:
        desperation_score += 2
    if buyer_motivation == "financial_hardship":
        desperation_score += 2
    if years_owned > 10:
        desperation_score += 1
    
    # Map to desperation levels
    if desperation_score >= 6:
        desperation_level = "critical"
        ready_for_exit = "Yes"
    elif desperation_score >= 4:
        desperation_level = "high"
        ready_for_exit = "Yes"
    elif desperation_score >= 2:
        desperation_level = "medium"
        ready_for_exit = "Maybe"
    else:
        desperation_level = "low"
        ready_for_exit = "No"
    
    return {
        "owner_name": owner_name,
        "contact_email": contact_email,
        "phone": phone,
        "property_name": property_name,
        "location": location,
        "purchase_year": purchase_year,
        "years_owned": years_owned,
        "annual_maintenance": f"${annual_maintenance:,.0f}",
        "buyer_motivation": buyer_motivation,
        "desperation_level": desperation_level,
        "contacted_reseller": "Yes" if contacted_reseller else "No",
        "secondary_market_attempted": "Yes" if secondary_market_attempted else "No",
        "ready_for_exit": ready_for_exit,
        "desperation_score": desperation_score,
        "resale_history": generate_resale_story(contacted_reseller, secondary_market_attempted),
        "conversion_angle": generate_conversion_angle(desperation_level, buyer_motivation, annual_maintenance),
    }


def generate_resale_story(contacted_reseller, secondary_market_attempted):
    """Generate realistic resale failure narrative"""
    if not contacted_reseller and not secondary_market_attempted:
        return "No resale attempts yet"
    
    stories = [
        "Contacted 3+ resale brokers, asked for $15k but market only supports $8-10k max",
        "Listed on eBay for $12k, got one lowball offer at $4k, delisted",
        "Tried Facebook Marketplace & Craigslist for 6 months, zero serious inquiries",
        "Paid resale broker $800 upfront fee, they found buyer at $6k (loss after commissions)",
        "Holiday Points trying to offload for 18 months, finally gave up",
        "Listed on Timeshare Resale platform, no qualified buyers in 12 months",
    ]
    
    if contacted_reseller and secondary_market_attempted:
        return random.choice(stories)
    elif contacted_reseller:
        return "Contacted resale brokers, not convinced secondary market is viable"
    else:
        return "Attempted personal sale online, got no serious leads"


def generate_conversion_angle(desperation_level, buyer_motivation, maintenance_cost):
    """Generate the right pitch angle for this lead based on profile"""
    
    base_angle = ""
    
    if desperation_level == "critical":
        base_angle = "URGENT - Owner is bleeding money. Focus on 'stop the bleeding' messaging. Cheapest viable exit is most attractive."
    elif desperation_level == "high":
        base_angle = "HIGH PRIORITY - Clear pain signals. Owner has given up on resale. Emphasize 'peace of mind' and 'problem solved.'"
    elif desperation_level == "medium":
        base_angle = "MEDIUM PRIORITY - Some pain, but may still hold out. Lead with 'worst-case scenario' and total cost comparison."
    else:
        base_angle = "LOW PRIORITY - May not be ready yet. Could become high-priority if maintenance increases or life changes."
    
    if buyer_motivation == "financial_hardship":
        base_angle += " [Financial stress = immediate need]"
    elif buyer_motivation == "high_maintenance":
        base_angle += " [Maintenance cost is the main pain point - lead with cost relief]"
    elif buyer_motivation == "family_change":
        base_angle += " [Life change = timing opportunity - emphasize new chapter]"
    elif buyer_motivation == "unplanned_inheritance":
        base_angle += " [Inherited problem - focus on 'this was not your choice' relief]"
    
    return base_angle


def generate_timeshare_leads(count=15):
    """Generate multiple leads and save to CSV"""
    leads = []
    for _ in range(count):
        leads.append(generate_realistic_lead())
    
    filename = f"timeshare_exit_leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    if leads:
        fieldnames = leads[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(leads)
    
    return filename, leads


if __name__ == "__main__":
    print("=" * 80)
    print("TIMESHARE EXIT LEAD GENERATOR - High-Urgency Prospects for Conversion TODAY")
    print("=" * 80)
    print()
    
    filename, leads = generate_timeshare_leads(15)
    
    print(f"Generated {len(leads)} high-quality timeshare exit leads")
    print(f"Saved to: {filename}")
    print()
    print("=" * 80)
    print("TOP PRIORITY LEADS (CRITICAL DESPERATION - CONVERT TODAY)")
    print("=" * 80)
    
    critical_leads = [l for l in leads if l['desperation_level'] == 'critical']
    critical_leads.sort(key=lambda x: x['desperation_score'], reverse=True)
    
    for i, lead in enumerate(critical_leads[:5], 1):
        print(f"\n{i}. {lead['owner_name']}")
        print(f"   Email: {lead['contact_email']} | Phone: {lead['phone']}")
        print(f"   Property: {lead['property_name']} ({lead['location']})")
        print(f"   Annual Maintenance: {lead['annual_maintenance']} (Owned {lead['years_owned']} years)")
        print(f"   Motivation: {lead['buyer_motivation']}")
        print(f"   Resale History: {lead['resale_history']}")
        print(f"   → ANGLE: {lead['conversion_angle']}")
    
    print()
    print("=" * 80)
    print("HIGH PRIORITY LEADS (HIGH DESPERATION)")
    print("=" * 80)
    
    high_leads = [l for l in leads if l['desperation_level'] == 'high']
    for i, lead in enumerate(high_leads[:3], 1):
        print(f"\n{i}. {lead['owner_name']} | {lead['contact_email']}")
        print(f"   {lead['property_name']} | ${lead['annual_maintenance']}/year")
        print(f"   → {lead['conversion_angle']}")
    
    print()
    print("=" * 80)
    print(f"Full lead list saved to: {filename}")
    print("Open this file in the Streamlit app to start conversions!")
    print("=" * 80)
