import os
import re
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Target sources & keywords for owner cancellation distress signals
TARGET_FORUMS = [
    {
        "name": "TUG BBS - Timeshare Users Group",
        "url": "https://tugbbs.com/forums/forums/buying-selling-renting-timeshares.13/",
        "base_url": "https://tugbbs.com/forums/"
    }
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Accept-Language": "en-US,en;q=0.5"
}

KEYWORDS = ["exit", "cancel", "deed back", "cancellation", "surrender", "rescind", "relinquish", "developer back"]

def extract_contact_info(text):
    """Parses text for phone numbers and email addresses."""
    emails = re.findall(r'[a-zA-Z0-9%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    phones = re.findall(r'\(?\b[2-9][0-9]{2}\)?[-. ]?[2-9][0-9]{2}[-. ]?[0-9]{4}\b', text)
    
    email = emails[0] if emails else "N/A"
    phone = phones[0] if phones else "N/A"
    return email, phone

def identify_developer(text):
    """Categorizes the lead by developer brand."""
    text_upper = text.upper()
    developers = ["WYNDHAM", "WESTGATE", "MARRIOTT", "DIAMOND", "HILTON", "HGV", "BLUEGREEN", "HOLIDAY INN", "HICV"]
    for dev in developers:
        if dev in text_upper:
            return dev
    return "GENERAL/OTHER"

def run_scraper():
    leads = []
    print("[*] Starting Timeshare Exit Lead Scraper...")

    for forum in TARGET_FORUMS:
        try:
            response = requests.get(forum["url"], headers=HEADERS, timeout=15)
            if response.status_code != 200:
                print(f"[!] Failed to access {forum['name']} (Status: {response.status_code})")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            threads = soup.find_all('div', class_='structItem-title')

            for thread in threads:
                a_tag = thread.find('a', href=True)
                if not a_tag:
                    continue
                
                title = a_tag.text.strip()
                link = forum["base_url"] + a_tag['href'].lstrip('/')

                # Check if thread title matches high-intent keywords
                if any(kw in title.lower() for kw in KEYWORDS):
                    print(f"[+] High-intent match found: {title}")
                    
                    try:
                        time.sleep(1) # Polite delay
                        t_res = requests.get(link, headers=HEADERS, timeout=10)
                        t_soup = BeautifulSoup(t_res.text, 'html.parser')
                        
                        first_post = t_soup.find('div', class_='message-inner')
                        post_text = first_post.text.strip() if first_post else title
                        
                        email, phone = extract_contact_info(post_text)
                        developer = identify_developer(post_text + " " + title)
                        
                        leads.append({
                            "Source": forum["name"],
                            "Developer": developer,
                            "Title/Intent": title,
                            "Email": email,
                            "Phone": phone,
                            "Link": link,
                            "Scraped_Date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
                        })
                    except Exception as e:
                        print(f"[!] Error parsing thread {link}: {e}")

        except Exception as e:
            print(f"[!] Error fetching {forum['name']}: {e}")

    # Output results to CSV
    output_file = "private_leads.csv"
    if leads:
        df = pd.DataFrame(leads)
        df.to_csv(output_file, index=False)
        print(f"[✓] Successfully exported {len(leads)} leads to {output_file}")
    else:
        # Create empty structured file to avoid step failure in Github Actions
        df = pd.DataFrame(columns=["Source", "Developer", "Title/Intent", "Email", "Phone", "Link", "Scraped_Date"])
        df.to_csv(output_file, index=False)
        print("[!] No new leads found. Created blank structure for private_leads.csv")

if __name__ == "__main__":
    run_scraper()