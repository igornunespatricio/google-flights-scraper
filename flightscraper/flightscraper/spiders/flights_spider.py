import scrapy


class FlightsSpider(scrapy.Spider):
    name = "flights"

    start_urls = [
        "https://www.google.com/travel/flights/search?tfs=CBwQAhojEgoyMDI1LTA4LTI0agwIAhIIL20vMDZnbXJyBwgBEgNMSVNAAUgBcAGCAQsI____________AZgBAg&hl=en&gl=BR",
        "https://www.google.com/travel/flights/search?tfs=CBwQAhooEgoyMDI1LTA4LTI0agwIAhIIL20vMDZnbXJyDAgDEggvbS8wNTJwN0ABSAFwAYIBCwj___________8BmAEC&hl=en&gl=BR",
        "https://www.google.com/travel/flights/search?tfs=CBwQAhojEgoyMDI1LTA4LTI1agwIAhIIL20vMDZnbXJyBwgBEgNaUkgaIxIKMjAyNS0wOC0yOGoHCAESA1pSSHIMCAISCC9tLzA2Z21yQAFIAXABggELCP___________wGYAQE&hl=en&gl=BR",
    ]

    def parse(self, response):
        # Extract flight details from the response content
        flight_options = response.xpath('//li[@class="pIav2d"]')

        departure_landing_cities = ";".join(
            response.xpath('.//span[@class="yPKHsc"]//text()').getall()
        ).strip()

        ticket_type = response.xpath('//span[@id="i7"]//text()').getall()

        number_passengers = response.xpath('//span[@jsname="xAX4ff"]//text()').getall()

        flight_class = response.xpath('//span[@id="i20"]//text()').getall()

        departure_date = response.xpath(
            '//div[@class="GYgkab YICvqf kStSsc ieVaIb"]/@data-value'
        ).get()

        return_date = response.xpath(
            '//div[@class="GYgkab YICvqf lJODHb qXDC9e"]/@data-value'
        ).get()

        for item in flight_options:
            duration = item.xpath(
                './/div[contains(@class, "gvkrdb AdWm1c tPgKwe ogfYpf")]/text()'
            ).getall()
            number_stops = item.xpath(
                './/div[@class="EfT7Ae AdWm1c tPgKwe"]//span[@class="ogfYpf"]/text()'
            ).getall()
            price = item.xpath('.//div[@class="U3gSDe ETvUZc"]//text()').getall()
            departure_landing_airports = ";".join(
                item.xpath(
                    './/div[@class="QylvBf"]//span[@jscontroller="cNtv4b"]/text()'
                ).getall()
            ).strip()
            stopping_locations = ";".join(
                item.xpath(
                    './/div[@class="BbR8Ec"]//span[@jscontroller="cNtv4b"]//text()'
                ).getall()
            ).strip()
            company = item.xpath(
                './/div[@class="sSHqwe tPgKwe ogfYpf"]/*[1]/text()'
            ).get()
            departure_landing_times = ";".join(
                item.xpath(
                    './/span[@class="mv1WYe"]/span/span/span/@aria-label'
                ).getall()
            ).strip()

            yield {
                "duration": duration,
                "number_stops": number_stops,
                "price": price,
                "departure_landing_airports": departure_landing_airports,
                "departure_landing_cities": departure_landing_cities,
                "stopping_locations": stopping_locations,
                "company": company,
                "ticket_type": ticket_type,
                "number_passengers": number_passengers,
                "flight_class": flight_class,
                "departure_date": departure_date,
                "return_date": return_date,
                "departure_landing_times": departure_landing_times,
            }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)
