"""
RemoteOK Spider - Scrapes remote jobs from remoteok.com
RemoteOK provides a public API, but this spider scrapes the HTML for more details
"""
import scrapy
import json


class RemoteOKSpider(scrapy.Spider):
    name = 'remoteok'
    allowed_domains = ['remoteok.com']
    start_urls = ['https://remoteok.com/api']

    def parse(self, response):
        try:
            data = json.loads(response.text)
            # First item is metadata, skip it
            for job in data[1:51]:  # Limit to 50 jobs
                if isinstance(job, dict):
                    tags = job.get('tags', [])
                    yield {
                        'title': job.get('position', 'Unknown'),
                        'company': job.get('company', 'Unknown'),
                        'url': job.get('url', f"https://remoteok.com/remote-jobs/{job.get('id', '')}"),
                        'location': job.get('location', 'Remote'),
                        'source': 'RemoteOK',
                        'posted_date': job.get('date', ''),
                        'description': (job.get('description', '') or '')[:500],
                        'salary': job.get('salary', ''),
                        'category': ', '.join(tags[:3]) if tags else 'Remote'
                    }
        except json.JSONDecodeError:
            self.logger.error("Failed to parse RemoteOK API response")
