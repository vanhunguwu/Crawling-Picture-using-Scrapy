import scrapy

class CardSetsSpider(scrapy.Spider):
    name = 'card_sets_spider'
    start_urls = ['https://battle-spirits.fandom.com/wiki/Card_Sets']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    def parse(self, response):
        sets = response.css('th[align="center"]')

        for set in sets:
            name = set.css('a::text').get()
            if name:
                set_name = name.strip()
                url = set.css('a::attr(href)').get()
                full_url = response.urljoin(url)

                if name is not None and full_url != "https://battle-spirits.fandom.com/wiki/Card_Sets":
                    yield scrapy.Request(full_url, callback=self.parse_set_page, headers={'User-Agent': 'Mozilla/5.0'}, meta={'set_name': set_name})

    def parse_set_page(self, response):
        set_name = response.meta['set_name']
        td_tags = response.css('td')

        for td in td_tags:
            card_name = td.css('a::text').get()
            card_url = td.css('a::attr(href)').get()
            
            if card_name and card_url:
                card_name = card_name.strip()
                card_url = response.urljoin(card_url)

                # Check if card_url is not the same as response URL
                if card_url != response.url:
                    yield scrapy.Request(card_url, callback=self.parse_card_page, headers={'User-Agent': 'Mozilla/5.0'}, meta={'set_name': set_name, 'card_name': card_name})

    def parse_card_page(self, response):
        set_name = response.meta['set_name']
        card_name = response.meta['card_name']
        image_url = response.css('div[style="min-width: 300px; max-width: 300px;"] a.image::attr(href)').get()
        card_type = response.xpath('//td[b="Card Type"]/following-sibling::td/a/text()').get()

        if image_url and card_type and card_type.strip().lower() == 'spirit':
            yield {
                'set_name': set_name,
                'card_name': card_name,
                'image_url': image_url,
                'card_type': card_type.strip()
            }
