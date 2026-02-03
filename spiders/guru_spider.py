"""
Guru.com Spider - Scrapes latest jobs from guru.com
Scrapes the public job listings page
"""
import scrapy


class GuruSpider(scrapy.Spider):
    name = 'guru'
    allowed_domains = ['www.guru.com']
    start_urls = ['https://www.guru.com/d/jobs/']

    def parse(self, response):
        # Parse job listings from the main page
        job_cards = response.xpath("//div[contains(@class,'jobRecord')]")

        for card in job_cards[:50]:
            title = card.xpath(".//h2/a/text()").get()
            url = card.xpath(".//h2/a/@href").get()
            description = card.xpath(".//p[contains(@class,'descText')]/text()").get()
            budget = card.xpath(".//span[contains(@class,'budget')]/text()").get()
            posted = card.xpath(".//span[contains(@class,'postDate')]/text()").get()
            skills = card.xpath(".//div[contains(@class,'skills')]//a/text()").getall()

            if title and url:
                yield {
                    'title': title.strip(),
                    'company': 'Guru Employer',
                    'url': response.urljoin(url),
                    'location': 'Remote',
                    'source': 'Guru',
                    'posted_date': posted.strip() if posted else '',
                    'description': description.strip()[:500] if description else '',
                    'salary': budget.strip() if budget else '',
                    'category': ', '.join(skills[:3]) if skills else 'Freelance'
                }

        # Follow pagination (configurable limit)
        current_page = response.meta.get('page', 1)
        max_pages = getattr(self, 'max_pages', 50)  # More pages
        if current_page < max_pages:
            next_page = response.xpath("//a[contains(@class,'next') or @rel='next']/@href").get()
            if not next_page:
                # Try numbered pagination
                next_page = response.xpath(f"//a[contains(@href,'page={current_page + 1}')]/@href").get()
            if next_page:
                self.logger.info(f"Following to page {current_page + 1}")
                yield response.follow(
                    next_page,
                    callback=self.parse,
                    meta={'page': current_page + 1}
                )
