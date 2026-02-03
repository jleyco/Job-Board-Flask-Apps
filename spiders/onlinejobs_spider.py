"""
OnlineJobs.ph Spider - Based on user's original olj4.py
Scrapes ALL job posts from onlinejobs.ph with automatic pagination.
Uses CrawlSpider with Rules like the working olj4.py.
"""
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class OnlineJobsSpider(CrawlSpider):
    name = 'onlinejobs'
    allowed_domains = ['www.onlinejobs.ph']

    # User agent to mimic browser (same as original olj4.py)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0s.0 Safari/537.36'

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    def start_requests(self):
        yield scrapy.Request(url='https://www.onlinejobs.ph/jobseekers/jobsearch', headers={'User-Agent': self.user_agent})

    # Rules for automatic link following - same as olj4.py
    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//div[contains(@class,'desc')]/a")), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths=("//a[@rel='next']")), callback='parse_item', follow=True, process_request='set_user_agent'),
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        title = response.xpath("//h1/text()").get()
        job_type = response.xpath("//dd/p/text()").get()
        salary = response.xpath("(//dd/p/text())[2]").get()
        date_posted = response.xpath("(//dd/p/text())[4]").get()
        job_description = response.xpath("(//div[@class='card-body'])[2]/p/text()").getall()
        url = response.url

        yield {
            'title': title or 'Unknown',
            'company': 'OnlineJobs.ph Employer',
            'url': url,
            'location': 'Remote (Philippines)',
            'source': 'OnlineJobs.ph',
            'posted_date': date_posted or '',
            'description': "\n".join(job_description) if job_description else '',
            'salary': salary or '',
            'category': job_type or 'General'
        }
