# Time-leads-
Scraping by
import csv
import requests
from bs4 import BeautifulSoup

# 1. tug2.net
url = "tug2.net"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

print(f"Connecting to target...")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Common corporate entity indicators to filter out individuals
    corp_indicators = ["llc", "inc", "corp", "properties", "holdings", "trust", "partners", "management", "capital", "group", "fund", "lp", "llp"]
    
    results = []
    
    # Pull all text blocks or list elements from the page
    for element in soup.find_all(['p', 'div', 'li', 'td']):
        text = element.get_text(strip=True)
        # Check if it looks like a corporate entry and has enough length to be meaningful
        if len(text) > 10 and any(ind in text.lower() for ind in corp_indicators):
            results.append({"Extracted Data": text})

    # Deduplicate results
    unique_results = [dict(t) for t in {tuple(d.items()) for d in results}]

    # Save directly to CSV
    with open("leads.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Extracted Data"])
        writer.writeheader()
        if unique_results:
            writer.writerows(unique_results)
        else:
            writer.writerow({"Extracted Data": "No corporate keywords matched. Check page structure."})
            
    print(f"Done. Found {len(unique_results)} matches. Saved to leads.csv.")
else:
    print(f"Error: Received status code {response.status_code}")
