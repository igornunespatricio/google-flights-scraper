import scrapy


class FlightsSpider(scrapy.Spider):
    name = "flights"

    start_urls = [
        "https://www.google.com/travel/flights/search?tfs=CBwQAhojEgoyMDI1LTA4LTI0agwIAhIIL20vMDZnbXJyBwgBEgNMSVNAAUgBcAGCAQsI____________AZgBAg&hl=en&gl=BR",
        "https://www.google.com/travel/flights/search?tfs=CBwQAhooEgoyMDI1LTA4LTI0agwIAhIIL20vMDZnbXJyDAgDEggvbS8wNTJwN0ABSAFwAYIBCwj___________8BmAEC&hl=en&gl=BR",
    ]

    def parse(self, response):
        # Extract flight details from the response content
        flight_options = response.xpath('//li[@class="pIav2d"]')

        for item in flight_options:
            duration = item.xpath(
                './/div[contains(@class, "gvkrdb AdWm1c tPgKwe ogfYpf")]/text()'
            ).getall()
            stops = item.xpath(
                './/div[@class="EfT7Ae AdWm1c tPgKwe"]//span[@class="ogfYpf"]/text()'
            ).getall()
            price = item.xpath('.//div[@class="U3gSDe ETvUZc"]//text()').getall()
            departure_landing = " ".join(
                item.xpath(
                    './/div[@class="QylvBf"]//span[@jscontroller="cNtv4b"]/text()'
                ).getall()
            ).strip()
            stopping_locations = item.xpath(
                './/div[@class="BbR8Ec"]//span[@jscontroller="cNtv4b"]//text()'
            ).getall()
            company = item.xpath(
                './/div[@class="sSHqwe tPgKwe ogfYpf"]/*[1]/text()'
            ).get()

            yield {
                "duration": duration,
                "stops": stops,
                "price": price,
                "departure_landing": departure_landing,
                "stopping_locations": stopping_locations,
                "company": company,
            }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)
