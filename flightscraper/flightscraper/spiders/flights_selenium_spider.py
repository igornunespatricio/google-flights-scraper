import time
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from database import DBHandler


class FlightsSpider(scrapy.Spider):
    name = "flights-selenium"

    start_urls = [
        "https://www.google.com/travel/flights/search?tfs=CBwQAhojEgoyMDI1LTA4LTI0agwIAhIIL20vMDZnbXJyBwgBEgNMSVNAAUgBcAGCAQsI____________AZgBAg&hl=en&gl=BR",
        "https://www.google.com/travel/flights/search?tfs=CBwQAhooEgoyMDI1LTA4LTI0agwIAhIIL20vMDZnbXJyDAgDEggvbS8wNTJwN0ABSAFwAYIBCwj___________8BmAEC&hl=en&gl=BR",
        "https://www.google.com/travel/flights/search?tfs=CBwQAhojEgoyMDI1LTA4LTI1agwIAhIIL20vMDZnbXJyBwgBEgNNQU8aIxIKMjAyNS0wOC0yOWoHCAESA01BT3IMCAISCC9tLzA2Z21yQAFIAXABggELCP___________wGYAQE&hl=en&gl=BR",
        "https://www.google.com/travel/flights/search?tfs=CBwQAhojEgoyMDI1LTA4LTI1agwIAhIIL20vMDZnbXJyBwgBEgNTU0EaIxIKMjAyNS0wOC0yOWoHCAESA1NTQXIMCAISCC9tLzA2Z21yQAFIAXABggELCP___________wGYAQE&hl=en&gl=BR",
        "https://www.google.com/travel/flights/search?tfs=CBwQAhojEgoyMDI1LTA4LTAzagwIAhIIL20vMDZnbXJyBwgBEgNGRU4aIxIKMjAyNS0wOC0wOWoHCAESA0ZFTnIMCAISCC9tLzA2Z21yQAFIAXABggELCP___________wGYAQE&hl=en&gl=BR",
        "https://www.google.com/travel/flights/search?tfs=CBwQAhojEgoyMDI1LTA4LTI1agwIAhIIL20vMDZnbXJyBwgBEgNUUlUaIxIKMjAyNS0wOC0yOWoHCAESA1RSVXIMCAISCC9tLzA2Z21yQAFIAXABggELCP___________wGYAQE&hl=en&gl=BR",
    ]

    def __init__(self, *args, **kwargs):
        super(FlightsSpider, self).__init__(*args, **kwargs)
        self.db_handler = DBHandler()  # Initialize the database handler
        self.db_handler.create_table()  # Create the table if it doesn't exist

    def start_requests(self):
        yield SeleniumRequest(
            url=self.start_urls[0], callback=self.parse, meta={"index": 0}
        )

    def parse(self, response):

        # Access selenium driver
        driver = response.meta["driver"]

        # Attempt to find and click the "More Flights" button
        time.sleep(10)
        try:
            more_flights_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//button[@class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-Bz112c-M1Soyc VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe LQeN7 nJawce OTelKf iIo4pd"]',
                    ),
                )
            )
            # Click the button
            more_flights_button.click()
            time.sleep(10)

        except Exception as e:
            self.logger.warning(f"Failed to click 'More Flights' button: {e}")
            # Skip to the next URL if clicking the button fails
            index = response.meta.get("index", 0)
            index += 1
            if index < len(self.start_urls):
                yield SeleniumRequest(
                    url=self.start_urls[index],
                    callback=self.parse,
                    meta={"index": index},
                )
            return  # Exit the parse method early

        # Get the new HTML content from the driver
        new_html = driver.page_source

        # Use Scrapy to parse the new HTML
        new_response = scrapy.http.HtmlResponse(
            url=driver.current_url, body=new_html, encoding="utf-8"
        )

        # Extract flight details from the response content
        flight_options = new_response.xpath('//li[@class="pIav2d"]')

        departure_landing_cities = ";".join(
            new_response.xpath('//span[@class="yPKHsc"]//text()').getall()
        ).strip()

        print(departure_landing_cities)

        ticket_type = ";".join(
            new_response.xpath('//span[@id="i7"]//text()').getall()
        ).strip()

        number_passengers = ";".join(
            new_response.xpath('//span[@jsname="xAX4ff"]//text()').getall()
        ).strip()

        flight_class = ";".join(
            new_response.xpath('//span[@id="i20"]//text()').getall()
        ).strip()

        departure_date = new_response.xpath(
            '//div[@class="GYgkab YICvqf kStSsc ieVaIb"]/@data-value'
        ).get()

        return_date = new_response.xpath(
            '//div[@class="GYgkab YICvqf lJODHb qXDC9e"]/@data-value'
        ).get()

        # Get the current date and time
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for item in flight_options:
            duration = ";".join(
                item.xpath(
                    './/div[contains(@class, "gvkrdb AdWm1c tPgKwe ogfYpf")]/text()'
                ).getall()
            ).strip()
            number_stops = ";".join(
                item.xpath(
                    './/div[@class="EfT7Ae AdWm1c tPgKwe"]//span[@class="ogfYpf"]/text()'
                ).getall()
            ).strip()
            price = ";".join(
                item.xpath('.//div[@class="U3gSDe ETvUZc"]//text()').getall()
            ).strip()
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

            # Insert the data into the database
            self.db_handler.insert_data(
                duration=duration,
                number_stops=number_stops,  # Assuming stops corresponds to number_stops
                price=price,
                departure_landing_airports=departure_landing_airports,  # Add this parameter
                departure_landing_cities=departure_landing_cities,  # Add this parameter
                stopping_locations=stopping_locations,
                company=company,
                ticket_type=ticket_type,  # Add this parameter
                number_passengers=number_passengers,  # Add this parameter
                flight_class=flight_class,  # Add this parameter
                departure_date=departure_date,  # Add this parameter
                return_date=return_date,  # Add this parameter
                departure_landing_times=departure_landing_times,  # Add this parameter
                scraped_at=current_date,
            )

        # Clear the browser cache and cookies
        driver.delete_all_cookies()

        # After finishing processing the first URL, check if there's another URL
        index = response.meta.get("index", 0)
        index += 1

        # If there are more URLs, request the next one
        if index < len(self.start_urls):
            yield SeleniumRequest(
                url=self.start_urls[index], callback=self.parse, meta={"index": index}
            )
