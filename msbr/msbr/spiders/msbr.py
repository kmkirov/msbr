import scrapy


class QuotesSpider(scrapy.Spider):
    name = "msbr"
    start_urls = [
        "https://mr-bricolage.bg/bg/Каталог/Инструменти/Авто-и-велоаксесоари/Велоаксесоари/c/006008012"
    ]


    def parse(self, response):
        products=response.xpath("//div[@class='col-md-4 mg-bottom-30 product-item']")
        # iterating over search results
        print('product parse bef for') 
        print(products)
        for product in products:
            # Defining the XPaths           
            XPATH_PRODUCT_DETAILSPAGE = ".//div[@class='product']//div[@class='image']//a/@href"
            XPATH_PRODUCT_IMAGE = ".//div[@class='product']//div[@class='image']//a//img/@src"
            XPATH_PRODUCT_NAME = ".//div[@class='product']//div[@class='title']//a[@class='name']/text()"
            XPATH_PRODUCT_PRICE = ".//div[@class='product']//div[@class='price']/text()"

            detailsPageURL = product.xpath(XPATH_PRODUCT_DETAILSPAGE).extract()[0]
            imageURL =  product.xpath(XPATH_PRODUCT_IMAGE).extract()[0]
            productName =  product.xpath(XPATH_PRODUCT_NAME).extract()[0]
            productPrice = product.xpath(XPATH_PRODUCT_PRICE).extract()[0]
            print('product parse bef yield')
            yield {
            'product_name':productName,
            'product_price':productPrice,            
            'product_link':detailsPageURL,
            'image':imageURL
        }
            