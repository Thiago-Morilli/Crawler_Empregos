
import scrapy


class EmpregosItem(scrapy.Item):
  
    title = scrapy.Field()
    company_name = scrapy.Field()
    location = scrapy.Field()
    description = scrapy.Field()
    salary = scrapy.Field()
    ref = scrapy.Field()
    type_work = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field() 