"""
We Work Remotely Spider - Scrapes remote jobs from weworkremotely.com
Uses RSS feeds which are publicly available
"""
import scrapy
from datetime import datetime


class WeWorkRemotelySpider(scrapy.Spider):
    name = 'weworkremotely'
    allowed_domains = ['weworkremotely.com']

    # RSS feeds for different categories
    start_urls = [
        'https://weworkremotely.com/categories/remote-programming-jobs.rss',
        'https://weworkremotely.com/categories/remote-design-jobs.rss',
        'https://weworkremotely.com/categories/remote-customer-support-jobs.rss',
        'https://weworkremotely.com/categories/remote-devops-sysadmin-jobs.rss',
        'https://weworkremotely.com/categories/remote-sales-and-marketing-jobs.rss',
        'https://weworkremotely.com/categories/remote-product-jobs.rss',
    ]

    def parse(self, response):
        # Determine category from URL
        if 'programming' in response.url:
            category = 'Programming'
        elif 'design' in response.url:
            category = 'Design'
        elif 'customer-support' in response.url:
            category = 'Customer Support'
        elif 'devops' in response.url:
            category = 'DevOps'
        elif 'sales' in response.url:
            category = 'Sales & Marketing'
        elif 'product' in response.url:
            category = 'Product'
        else:
            category = 'Remote'

        # Parse RSS feed
        response.selector.remove_namespaces()
        items = response.xpath('//item')

        for item in items[:15]:  # Limit per category
            title_full = item.xpath('title/text()').get() or 'Unknown'

            # Title format is usually "Company: Position"
            if ':' in title_full:
                parts = title_full.split(':', 1)
                company = parts[0].strip()
                title = parts[1].strip()
            else:
                company = 'Unknown'
                title = title_full

            link = item.xpath('link/text()').get() or ''
            pub_date = item.xpath('pubDate/text()').get() or ''
            description = item.xpath('description/text()').get() or ''

            # Clean up description (remove HTML)
            import re
            description = re.sub('<[^<]+?>', '', description)[:500]

            yield {
                'title': title,
                'company': company,
                'url': link,
                'location': 'Remote',
                'source': 'WeWorkRemotely',
                'posted_date': pub_date,
                'description': description,
                'salary': '',
                'category': category
            }
