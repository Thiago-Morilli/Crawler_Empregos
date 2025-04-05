import scrapy
import json
from Empregos.items import EmpregosItem


class JobsSpider(scrapy.Spider):
    name = "Jobs"
    domains = "https://www.empregos.com.br/vagas/"
    search = "/python"

    def start_requests(self):
        yield scrapy.Request(
                url=self.domains + self.search,
                method="GET",
                callback=self.parse
        )

    def request_page(self, link):
        yield scrapy.Request(
            url=self.domains + f"p{link}" + self.search,
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
                "description": json_info["description"].replace("\r\r","").replace("\r", ""),
                "salary": response.xpath('//div[@class="grow w-full"]/h2[2]/text()').get().replace("\n  ","").replace("A partir de ","").replace("\n","").replace("Acima de ","")
        }
        yield EmpregosItem(
                data
            )
    
    def next_page(self, response): 
        page = response.xpath('//div[@class="pagination-list area-paginacao"]/a[@title="Próximo"]/@data-valor').get()
        print(page)
        if page:
            yield from self.request_page(page)
