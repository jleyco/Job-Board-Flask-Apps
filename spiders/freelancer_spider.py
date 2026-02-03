"""
Freelancer.com Spider - Scrapes latest projects from freelancer.com
Note: Freelancer has an API but requires authentication
This scrapes the public projects listing page
"""
import scrapy
import json
import re


class FreelancerSpider(scrapy.Spider):
    name = 'freelancer'
    allowed_domains = ['www.freelancer.com']

    def start_requests(self):
        # Freelancer's API endpoint for public projects
        # This is the same endpoint their website uses
        url = 'https://www.freelancer.com/api/projects/0.1/projects/active'
        params = {
            'compact': 'true',
            'limit': '50',
            'offset': '0',
            'project_statuses[]': 'active',
            'sort_field': 'time_submitted',
            'sort_order': 'desc'
        }
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        yield scrapy.Request(
            url=f"{url}?{query_string}",
            callback=self.parse,
            headers={
                'Accept': 'application/json',
                'Freelancer-Developer-Auth-V1': 'public',
            }
        )

    def parse(self, response):
        try:
            data = json.loads(response.text)
            projects = data.get('result', {}).get('projects', [])

            for project in projects[:50]:
                # Extract budget
                budget = project.get('budget', {})
                min_budget = budget.get('minimum', 0)
                max_budget = budget.get('maximum', 0)
                currency = project.get('currency', {}).get('code', 'USD')

                if min_budget and max_budget:
                    salary = f"{currency} {min_budget}-{max_budget}"
                elif min_budget:
                    salary = f"{currency} {min_budget}+"
                else:
                    salary = ''

                # Extract skills/categories
                jobs = project.get('jobs', [])
                categories = [job.get('name', '') for job in jobs[:3]]

                yield {
                    'title': project.get('title', 'Unknown'),
                    'company': project.get('owner_username', 'Unknown'),
                    'url': f"https://www.freelancer.com/projects/{project.get('seo_url', '')}",
                    'location': 'Remote',
                    'source': 'Freelancer',
                    'posted_date': '',
                    'description': (project.get('preview_description', '') or '')[:500],
                    'salary': salary,
                    'category': ', '.join(categories) if categories else 'Freelance'
                }
        except json.JSONDecodeError:
            self.logger.error("Failed to parse Freelancer API response")
