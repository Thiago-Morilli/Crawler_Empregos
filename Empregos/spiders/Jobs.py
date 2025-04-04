import scrapy
import json


class JobsSpider(scrapy.Spider):
    name = "Jobs"
    domains = "https://www.empregos.com.br"
    search = "/vagas/python"

    def start_requests(self):
        yield scrapy.Request(
                url=self.domains + self.search,
                method="GET",
                callback=self.parse
        )

    def request_page(self, link):
        yield scrapy.Request(
            url=link,
            method="GET",
            callback=self.parse
        )

    def parse(self, response):
        for link in response.xpath('//div[@class="descricao grid-12-16"]/h2/a/@href').getall():
            yield scrapy.Request(
                url=link,
                method="GET",
                callback=self.collecting_data
            )   
        yield from self.next_page(response)

    def collecting_data(self, response):
        
        path_json = response.xpath('//script[@type="application/ld+json"]/text()').get()
        json_info = json.loads(path_json)  

        data = {
                "title": json_info["title"],
                "company_name": json_info["hiringOrganization"]["name"],
                "location": json_info["jobLocation"]["address"]["addressLocality"],
               "description": json_info["description"].replace("\r\r","").replace("\r", "")
        }
    
    def next_page(self, response):
        page = response.xpath('//div[@class="pagination-list area-paginacao"]/a[@title="Próximo"]/@href').get()
        if page:
            yield from self.request_page(page)
