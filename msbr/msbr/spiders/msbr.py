import scrapy


class QuotesSpider(scrapy.Spider):
    name = "msbr"
    start_urls = [
        "https://mr-bricolage.bg/bg/Каталог/Инструменти/Авто-и-велоаксесоари/Велоаксесоари/c/006008012"
    ]
    prod_details = []

    def parseDetails(self, response):
        XPATH_PRODUCT_DETAILS = "//table[@class='table']//tr//td"
        XPATH_PRODUCT_DETAILS_TEXT = ".//text()"
        print('else statement code')
        details_table = response.xpath(XPATH_PRODUCT_DETAILS)
        zip_object = zip(details_table[::2], details_table[1::2])
        detail_tupleList = list(zip_object)
        for ch, desc in detail_tupleList:
            detail_name = ch.xpath(XPATH_PRODUCT_DETAILS_TEXT).extract()[0]
            detail_spec = desc.extract()[0]
            yield {
                'product_name': 'TEST',
                'product_price': '0',
                'type': 'details',
                'product_link': detail_name,
                'image': detail_spec
            }

    def parse(self, response):
        products = response.xpath(
            "//div[@class='col-md-4 mg-bottom-30 product-item']")

        # Defining the XPaths
        XPATH_PRODUCT_DETAILSPAGE = ".//div[@class='product']//div[@class='image']//a/@href"
        XPATH_PRODUCT_IMAGE = ".//div[@class='product']//div[@class='image']//a//img/@src"
        XPATH_PRODUCT_NAME = ".//div[@class='product']//div[@class='title']//a[@class='name']/text()"
        XPATH_PRODUCT_PRICE = ".//div[@class='product']//div[@class='price']/text()"

        # iterating over product
        for product in products:
            detailsPageURL = product.xpath(
                XPATH_PRODUCT_DETAILSPAGE).extract()[0]
            imageURL = product.xpath(XPATH_PRODUCT_IMAGE).extract()[0]
            productName = product.xpath(XPATH_PRODUCT_NAME).extract()[0]
            productPrice = product.xpath(
                XPATH_PRODUCT_PRICE).extract()[0]
            self.prod_details.append(
                'https://mr-bricolage.bg' + detailsPageURL)

            yield {
                'product_name': productName,
                'product_price': productPrice,
                'product_link': detailsPageURL,
                'image': imageURL,
                'type': 'prod'}

            next_pageURL = response.xpath(
                "//li[@class='pagination-next']//a/@href")
            if len(next_pageURL) > 1:
                next_page_url = 'https://mr-bricolage.bg' + \
                    next_pageURL[0].extract()
                request = scrapy.Request(url=next_page_url)
                yield request
            else:
                for prodURL in self.prod_details:
                    request = scrapy.Request(
                        url=prodURL, callback=self.parseDetails)
                    yield request
