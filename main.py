import os
import subprocess

if __name__ == "__main__":
    # Define the path to your Scrapy project
    project_path = "flightscraper"  # Change this to your actual path

    # Change the current working directory to the project path
    os.chdir(project_path)

    # Run the Scrapy crawl command
    subprocess.run(["scrapy", "crawl", "flights-selenium"])
