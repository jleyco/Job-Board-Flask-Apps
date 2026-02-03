"""
Indeed Spider - Uses Indeed's public RSS feeds
"""
import scrapy
import re


class IndeedSpider(scrapy.Spider):
    name = 'indeed'
    allowed_domains = ['www.indeed.com']

    # Search queries to scrape
    queries = [
        'remote+developer',
        'remote+programmer',
        'virtual+assistant',
        'data+entry+remote',
        'freelance+writer',
    ]

    def start_requests(self):
        for query in self.queries:
            url = f'https://www.indeed.com/rss?q={query}&sort=date&limit=25'
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={'query': query.replace('+', ' ')}
            )

    def parse(self, response):
        query = response.meta.get('query', '')

        response.selector.remove_namespaces()
        items = response.xpath('//item')

        for item in items:
            title = item.xpath('title/text()').get() or 'Unknown'
            link = item.xpath('link/text()').get() or ''
            pub_date = item.xpath('pubDate/text()').get() or ''
            description = item.xpath('description/text()').get() or ''

            # Extract company from title (format: "Job Title - Company Name")
            if ' - ' in title:
                parts = title.rsplit(' - ', 1)
                job_title = parts[0].strip()
                company = parts[1].strip() if len(parts) > 1 else 'Unknown'
            else:
                job_title = title
                company = 'Unknown'

            # Clean up description (remove HTML)
            description = re.sub('<[^<]+?>', '', description)[:500]

            yield {
                'title': job_title,
                'company': company,
                'url': link,
                'location': 'Various',
                'source': 'Indeed',
                'posted_date': pub_date,
                'description': description,
                'salary': '',
                'category': query.title()
            }
