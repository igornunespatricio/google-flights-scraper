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

        more_flights_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//button[@class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-Bz112c-M1Soyc VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe LQeN7 nJawce OTelKf iIo4pd"]',
                ),
            )
        )
        #  Click the button
        more_flights_button.click()

        time.sleep(10)

        # Get the new HTML content from the driver
        new_html = driver.page_source

        # Use Scrapy to parse the new HTML
        new_response = scrapy.http.HtmlResponse(
            url=driver.current_url, body=new_html, encoding="utf-8"
        )

        # Extract flight details from the response content
        flight_options = new_response.xpath('//li[@class="pIav2d"]')

        # Get the current date and time
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
                "scraped_at": current_date,
            }

            # Insert the data into the database
            self.db_handler.insert_data(
                duration=duration,
                stops=stops,
                price=price,
                departure_landing=departure_landing,
                stopping_locations=stopping_locations,
                company=company,
                scraped_at=current_date,
            )

        # After finishing processing the first URL, check if there's another URL
        index = response.meta.get("index", 0)
        index += 1

        # If there are more URLs, request the next one
        if index < len(self.start_urls):
            yield SeleniumRequest(
                url=self.start_urls[index], callback=self.parse, meta={"index": index}
            )
