import scrapy


class FlightsSpider(scrapy.Spider):
    name = "flights"

    start_urls = [
        "https://www.google.com/travel/flights/search?tfs=CBwQAhooEgoyMDI1LTA4LTI0agwIAhIIL20vMDZnbXJyDAgDEggvbS8wNTJwN0ABSAFwAYIBCwj___________8BmAEC&hl=en&gl=BR"
    ]

    def parse(self, response):
        # Extract all <li> elements with class "pIav2d"
        flight_options = response.xpath('//li[@class="pIav2d"]')

        for item in flight_options:
            # Get flight duration
            duration = item.xpath(
                './/div[contains(@class, "gvkrdb AdWm1c tPgKwe ogfYpf")]/text()'
            ).getall()

            # Get stops
            stops = item.xpath(
                './/div[@class="EfT7Ae AdWm1c tPgKwe"]//span[@class="ogfYpf"]/text()'
            ).getall()

            # Get price
            price = item.xpath('.//div[@class="U3gSDe ETvUZc"]//text()').getall()

            # Get departure and landing places
            departure_landing = " ".join(
                item.xpath(
                    './/div[@class="QylvBf"]//span[@jscontroller="cNtv4b"]/text()'
                ).getall()
            ).strip()

            # Get stopping locations
            stopping_locations = item.xpath(
                './/div[@class="BbR8Ec"]//span[@jscontroller="cNtv4b"]//text()'
            ).getall()
            # Get company
            company = item.xpath(
                './/div[@class="sSHqwe tPgKwe ogfYpf"]/*[1]/text()'
            ).get()

            # Yield the extracted data
            yield {
                "duration": duration,
                "stops": stops,
                "price": price,
                "departure_landing": departure_landing,
                "stopping_locations": stopping_locations,
                "company": company,
            }


# TODO:
# - see how to click button to open more flight options before parsing options
