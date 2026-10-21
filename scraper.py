import csv
import requests
from bs4 import BeautifulSoup

# Example placeholder script
data = [{"Name": "Example Company", "Email": "info@example.com"}]

with open("private_leads.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Name", "Email"])
    writer.writeheader()
    writer.writerows(data)

print("Leads successfully saved to private_leads.csv")