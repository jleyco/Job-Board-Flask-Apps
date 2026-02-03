# How to Run Job Scrapers

This folder contains everything you need to scrape jobs and display them on the Flask website.

## Quick Start

### Option 1: Run Default Spiders (Easiest)
Double-click: `scrape_jobs.bat`

This will scrape from:
- OnlineJobs.ph
- RemoteOK
- Freelancer

### Option 2: Run Specific Spiders

```bash
# Run single spider
python run_scrapers.py onlinejobs

# Run multiple spiders
python run_scrapers.py onlinejobs guru peopleperhour

# Run all available spiders
python run_scrapers.py onlinejobs remoteok weworkremotely freelancer guru peopleperhour indeed hubstaff
```

### Option 3: Run Individual Spider File

```bash
# Using scrapy runspider
scrapy runspider spiders/onlinejobs_spider.py -o jobs.json

# Or for a specific spider
scrapy runspider spiders/freelancer_spider.py -o freelancer_jobs.json
```

## Available Spiders

| Spider Name | Website | Description |
|------------|---------|-------------|
| `onlinejobs` | OnlineJobs.ph | Philippines remote jobs |
| `remoteok` | RemoteOK.com | Remote tech jobs |
| `weworkremotely` | WeWorkRemotely.com | Remote jobs |
| `freelancer` | Freelancer.com | Freelance projects |
| `guru` | Guru.com | Freelance jobs |
| `peopleperhour` | PeoplePerHour.com | Freelance projects |
| `indeed` | Indeed.com | Various jobs |
| `hubstaff` | Hubstaff Talent | Remote jobs |

## After Scraping

1. Jobs are saved to `scraped_jobs.json`
2. Refresh your browser (if Flask is running)
3. New jobs will appear automatically

## Complete Workflow

```bash
# 1. Scrape jobs
python run_scrapers.py onlinejobs freelancer

# 2. Start Flask (if not already running)
python app.py

# 3. Visit http://localhost:5000
```

## Troubleshooting

**Issue**: Spider not found
- Make sure the spider name is correct (see table above)
- Spider names are lowercase

**Issue**: No jobs scraped
- Check your internet connection
- Some websites may block scrapers temporarily
- Try running a single spider to test

**Issue**: Import errors
- Install dependencies: `pip install -r requirements.txt`
- Make sure Scrapy is installed: `pip install scrapy`
