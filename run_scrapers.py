"""
Run job scrapers and save to scraped_jobs.json

Usage:
    python run_scrapers.py                    # Run all spiders
    python run_scrapers.py onlinejobs         # Run specific spider
    python run_scrapers.py onlinejobs guru    # Run multiple spiders
"""

import sys
import json
from datetime import datetime
from pathlib import Path
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

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


# Available spiders
AVAILABLE_SPIDERS = {
    'onlinejobs': OnlineJobsSpider,
    'remoteok': RemoteOKSpider,
    'weworkremotely': WeWorkRemotelySpider,
    'freelancer': FreelancerSpider,
    'guru': GuruSpider,
    'peopleperhour': PeoplePerHourSpider,
    'indeed': IndeedSpider,
    'hubstaff': HubstaffSpider,
}

# Default spiders to run
DEFAULT_SPIDERS = ['onlinejobs', 'remoteok', 'freelancer']


class JobCollectorPipeline:
    """Pipeline to collect all scraped items"""
    items = []

    def process_item(self, item, spider):
        JobCollectorPipeline.items.append(dict(item))
        return item


def run_spiders(spider_names):
    """Run specified spiders"""
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

    for spider_name in spider_names:
        if spider_name in AVAILABLE_SPIDERS:
            spider_class = AVAILABLE_SPIDERS[spider_name]
            process.crawl(spider_class)
            print(f"[+] Added spider: {spider_name}")
        else:
            print(f"[-] Unknown spider: {spider_name}")

    print("\n" + "=" * 60)
    print("Starting scrapers...")
    print("=" * 60 + "\n")

    process.start()
    return JobCollectorPipeline.items


def save_jobs(jobs, output_file='scraped_jobs.json'):
    """Save jobs to JSON file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)

    print(f"\n[SAVED] {len(jobs)} jobs to {output_file}")

    # Show summary
    by_source = {}
    for job in jobs:
        source = job.get('source', 'Unknown')
        by_source[source] = by_source.get(source, 0) + 1

    print("\nJobs by source:")
    for source, count in sorted(by_source.items()):
        print(f"  - {source}: {count}")


if __name__ == '__main__':
    # Get spider names from command line
    if len(sys.argv) > 1:
        spider_names = sys.argv[1:]
    else:
        spider_names = DEFAULT_SPIDERS

    print("=" * 60)
    print("JOB SCRAPER")
    print("=" * 60)
    print(f"Running spiders: {', '.join(spider_names)}")
    print()

    # Run scrapers
    jobs = run_spiders(spider_names)

    # Save results
    save_jobs(jobs)

    print("\n" + "=" * 60)
    print("DONE! Refresh your Flask app to see the new jobs.")
    print("=" * 60)
