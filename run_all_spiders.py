"""
Run ALL job scrapers at once

This script runs all available Scrapy spiders and saves results to scraped_jobs.json

Usage:
    python run_all_spiders.py
"""

import sys
import json
from datetime import datetime
from pathlib import Path
from scrapy.crawler import CrawlerProcess

# Import spiders
sys.path.insert(0, str(Path(__file__).parent / 'spiders'))

from onlinejobs_spider import OnlineJobsSpider
from remoteok_spider import RemoteOKSpider
from weworkremotely_spider import WeWorkRemotelySpider
from freelancer_spider import FreelancerSpider
from guru_spider import GuruSpider
from peopleperhour_spider import PeoplePerHourSpider
from indeed_spider import IndeedSpider
from hubstaff_spider import HubstaffSpider


# All available spiders
ALL_SPIDERS = [
    ('onlinejobs', OnlineJobsSpider, 'OnlineJobs.ph'),
    ('remoteok', RemoteOKSpider, 'RemoteOK.com'),
    ('weworkremotely', WeWorkRemotelySpider, 'WeWorkRemotely.com'),
    ('freelancer', FreelancerSpider, 'Freelancer.com'),
    ('guru', GuruSpider, 'Guru.com'),
    ('peopleperhour', PeoplePerHourSpider, 'PeoplePerHour.com'),
    ('indeed', IndeedSpider, 'Indeed.com'),
    ('hubstaff', HubstaffSpider, 'Hubstaff Talent'),
]


class JobCollectorPipeline:
    """Pipeline to collect all scraped items"""
    items = []

    def process_item(self, item, spider):
        JobCollectorPipeline.items.append(dict(item))
        return item


def run_all_spiders():
    """Run all available spiders"""
    JobCollectorPipeline.items = []

    settings = {
        'BOT_NAME': 'job_scrapers',
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 2,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'COOKIES_ENABLED': False,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'AUTOTHROTTLE_ENABLED': True,
        'LOG_LEVEL': 'INFO',
        'ITEM_PIPELINES': {
            '__main__.JobCollectorPipeline': 300,
        },
    }

    process = CrawlerProcess(settings)

    # Add all spiders to the process
    print("\nAdding spiders:")
    print("-" * 60)
    for spider_name, spider_class, website in ALL_SPIDERS:
        process.crawl(spider_class)
        print(f"  ✓ {spider_name.ljust(20)} ({website})")

    print("\n" + "=" * 60)
    print("STARTING ALL SCRAPERS...")
    print("=" * 60 + "\n")

    # Start scraping
    process.start()

    return JobCollectorPipeline.items


def save_jobs(jobs, output_file='scraped_jobs.json'):
    """Save jobs to JSON file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)

    print(f"\n{'=' * 60}")
    print(f"RESULTS")
    print("=" * 60)
    print(f"\nTotal jobs scraped: {len(jobs)}")
    print(f"Saved to: {output_file}")

    # Show summary by source
    by_source = {}
    for job in jobs:
        source = job.get('source', 'Unknown')
        by_source[source] = by_source.get(source, 0) + 1

    if by_source:
        print("\nJobs by source:")
        for source, count in sorted(by_source.items()):
            print(f"  • {source}: {count} jobs")


if __name__ == '__main__':
    print("=" * 60)
    print("RUN ALL JOB SCRAPERS")
    print("=" * 60)
    print(f"\nThis will scrape from all {len(ALL_SPIDERS)} job websites:")
    for spider_name, _, website in ALL_SPIDERS:
        print(f"  • {website}")

    print("\nPress Ctrl+C to cancel at any time...")
    print()

    try:
        # Run all scrapers
        jobs = run_all_spiders()

        # Save results
        save_jobs(jobs)

        print("\n" + "=" * 60)
        print("✓ DONE! Refresh your Flask app to see the new jobs.")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\n\n[!] Scraping cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n[ERROR] Failed to run scrapers: {e}")
        sys.exit(1)
