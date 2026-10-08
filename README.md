name: Lead Scraper Runner

on:
  workflow_dispatch: # Allows manual trigger from your phone's GitHub app

jobs:
  run-scraper:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install requests beautifulsoup4

      - name: Run Scraper Script
        run: python scraper.py

      - name: Upload Results
        uses: actions/upload-artifact@v4
        with:
          name: private-leads
          path: private_leads.csv


pip install -r requirements.txt