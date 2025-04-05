import scrapy


class EmpregosItem(scrapy.Item):
    title = scrapy.Field()
    company_name = scrapy.Field()
    location = scrapy.Field()
    description = scrapy.Field()
    salary = scrapy.Field()
    
