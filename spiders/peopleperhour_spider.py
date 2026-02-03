"""
PeoplePerHour Spider - Scrapes latest projects from peopleperhour.com
"""
import scrapy
import json


class PeoplePerHourSpider(scrapy.Spider):
    name = 'peopleperhour'
    allowed_domains = ['www.peopleperhour.com']

    def start_requests(self):
        # PeoplePerHour project listing page
        yield scrapy.Request(
            url='https://www.peopleperhour.com/freelance-jobs',
            callback=self.parse
        )

    def parse(self, response):
        # Parse job/project cards
        job_cards = response.xpath("//div[contains(@class,'job-card') or contains(@class,'project-item')]")

        for card in job_cards[:50]:
            title = card.xpath(".//h3/a/text() | .//h2/a/text() | .//a[contains(@class,'title')]/text()").get()
            url = card.xpath(".//h3/a/@href | .//h2/a/@href | .//a[contains(@class,'title')]/@href").get()
            description = card.xpath(".//p[contains(@class,'description')]/text() | .//div[contains(@class,'desc')]/text()").get()
            budget = card.xpath(".//span[contains(@class,'budget') or contains(@class,'price')]/text()").get()
            posted = card.xpath(".//span[contains(@class,'date') or contains(@class,'time')]/text()").get()
            category = card.xpath(".//span[contains(@class,'category')]/text() | .//a[contains(@class,'category')]/text()").get()

            if title and url:
                yield {
                    'title': title.strip(),
                    'company': 'PPH Client',
                    'url': response.urljoin(url),
                    'location': 'Remote',
                    'source': 'PeoplePerHour',
                    'posted_date': posted.strip() if posted else '',
                    'description': description.strip()[:500] if description else '',
                    'salary': budget.strip() if budget else '',
                    'category': category.strip() if category else 'Freelance'
                }

        # Check for next page (configurable limit)
        current_page = response.meta.get('page', 1)
        max_pages = getattr(self, 'max_pages', 50)  # More pages
        if current_page < max_pages:
            next_page = response.xpath("//a[@rel='next']/@href | //a[contains(@class,'next')]/@href").get()
            if not next_page:
                # Try numbered pagination
                next_page = response.xpath(f"//a[contains(@href,'page/{current_page + 1}') or contains(@href,'page={current_page + 1}')]/@href").get()
            if next_page:
                self.logger.info(f"Following to page {current_page + 1}")
                yield response.follow(
                    next_page,
                    callback=self.parse,
                    meta={'page': current_page + 1}
                )
