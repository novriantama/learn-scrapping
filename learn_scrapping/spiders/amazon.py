import scrapy


class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.ae"]
    start_urls = [
        "https://www.amazon.ae/s?k=laptop"
    ]

    def parse(self, response):
        products = response.css('div.s-main-slot div.s-result-item')

        for product in products:
            title = product.css('h2 a span::text').get()
            price_whole = product.css('span.a-price-whole::text').get()
            price_fraction = product.css('span.a-price-fraction::text').get()
            price = f"{price_whole}.{price_fraction}" if price_whole and price_fraction else None
            rating = product.css('span.a-icon-alt::text').get()
            num_reviews = product.css('span.a-size-base::text').get()

            yield {
                'title': title,
                'price': price,
                'rating': rating,
                'num_reviews': num_reviews
            }

        next_page = response.css('ul.a-pagination li.a-last a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
