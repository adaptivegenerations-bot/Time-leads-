#!/bin/bash
# Timeshare Lead Scraper - Organized File System Setup
# Creates folder structure for each data source with scraper scripts and call scripts

mkdir -p timeshare_leads/{reddit,craigslist,bbb,yelp,facebook_exports,property_records,class_actions}

echo "Created folder structure:"
echo ""
echo "timeshare_leads/"
echo "├── reddit/"
echo "├── craigslist/"
echo "├── bbb/"
echo "├── yelp/"
echo "├── facebook_exports/"
echo "├── property_records/"
echo "└── class_actions/"
echo ""
echo "Next: Run individual scrapers in each folder"
