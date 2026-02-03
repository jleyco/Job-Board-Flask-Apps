"""
Hubstaff Talent Spider - Scrapes remote jobs from talent.hubstaff.com
Hubstaff Talent is free and allows public browsing
"""
import scrapy


class HubstaffSpider(scrapy.Spider):
    name = 'hubstaff'
    allowed_domains = ['talent.hubstaff.com']
    start_urls = ['https://talent.hubstaff.com/search/jobs']

    def parse(self, response):
        # Parse job cards
        job_cards = response.xpath("//div[contains(@class,'job-card') or contains(@class,'search-result')]")

        for card in job_cards[:50]:
            title = card.xpath(".//h3/a/text() | .//a[contains(@class,'job-title')]/text()").get()
            url = card.xpath(".//h3/a/@href | .//a[contains(@class,'job-title')]/@href").get()
            company = card.xpath(".//span[contains(@class,'company')]/text() | .//div[contains(@class,'employer')]/text()").get()
            description = card.xpath(".//p[contains(@class,'description')]/text() | .//div[contains(@class,'excerpt')]/text()").get()
            budget = card.xpath(".//span[contains(@class,'rate') or contains(@class,'budget')]/text()").get()
            skills = card.xpath(".//span[contains(@class,'skill') or contains(@class,'tag')]/text()").getall()

            if title and url:
                yield {
                    'title': title.strip(),
                    'company': company.strip() if company else 'Hubstaff Employer',
                    'url': response.urljoin(url),
                    'location': 'Remote',
                    'source': 'Hubstaff Talent',
                    'posted_date': '',
                    'description': description.strip()[:500] if description else '',
                    'salary': budget.strip() if budget else '',
                    'category': ', '.join(skills[:3]) if skills else 'Remote'
                }

        # Pagination
        current_page = response.meta.get('page', 1)
        if current_page < 3:
            next_page = response.xpath("//a[contains(@class,'next') or contains(text(),'Next')]/@href").get()
            if next_page:
                yield response.follow(
                    next_page,
                    callback=self.parse,
                    meta={'page': current_page + 1}
                )
