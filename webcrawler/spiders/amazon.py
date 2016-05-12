import scrapy
from webcrawler.items import AmazonItem

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.com"]
    # first page of Amazon's search results of "Electronics - Television & Video - Televisions"
    start_urls = ["http://www.amazon.com/gp/search/ref=sr_nr_n_1?fst=as%3Aoff&rh=n%3A172282%2Cn%3A1266092011%2Cn%3A172659%2Ck%3ATV&keywords=TV&ie=UTF8&qid=1449805375&rnid=493964"]


    custom_settings = {"ITEM_PIPELINES": {'webcrawler.pipelines.PostprocessPipeline': 300,
                                          'webcrawler.pipelines.MariaDBPipeline': 500},
                        "DB_HOST": 'localhost',
                        "DB_USER": 'root',
                        "DB": 'Test'
                       }


    def parse(self, response):
        dp_urls = response.xpath('//a[contains(@class,"s-access-detail-page")]/@href')
        for dpurl in dp_urls:
            # use callbacks to asynchronously parse pages
            yield scrapy.Request(dpurl.extract(), callback=self.parse_detailpage)
        nextpage = response.xpath('//a[@class="pagnNext"]')
        if nextpage:
            url = 'http://www.amazon.com' + nextpage.xpath('@href')[0].extract()
            yield scrapy.Request(url)

    def parse_detailpage(self, response):
        item = AmazonItem()
        item['url'] = response.url
        item['name'] = response.xpath('//span[@id="productTitle"]/text()').extract()
        item['rating'] = response.xpath('//span[@id="acrPopover"]/@title').extract()
        item['reviews'] = response.xpath('//span[@id="acrCustomerReviewText"]/text()').extract()
        item['price'] = response.xpath('//span[@id="priceblock_ourprice"]/text()').extract()
        item['save'] = response.xpath('//tr[@id="regularprice_savings"]/td[2]//text()').extract()
        detailKeys = response.xpath('//div[@id="technical-data"]//ul/li/b/text()').extract()
        detailValues = response.xpath('//div[@id="technical-data"]//ul/li/text()').extract()
        for i in range(0, len(detailKeys)):
            value = detailValues[i]
            if detailKeys[i] == 'Brand Name':
                item['brand'] = value[2:]
            elif detailKeys[i] == 'Display Technology':
                item['display'] = value[2:]
            elif detailKeys[i] == 'Display Size':
                item['size'] = value[2:]
        yield item
