import os
import subprocess
import sys


def activate_virtualenv():
    # Activate the virtual environment by using the correct Python path from .venv
    if os.name == "nt":  # If Windows
        python_executable = os.path.join(".venv", "Scripts", "python.exe")
    else:  # If Unix-based systems (Linux/Mac)
        python_executable = os.path.join(".venv", "bin", "python")

    return python_executable


if __name__ == "__main__":
    # Step 1: Enter the google-flights-scraper folder
    project_folder = "google-flights-scraper"
    if os.path.exists(project_folder):
        os.chdir(project_folder)
        print(f"Changed directory to: {os.getcwd()}")
    else:
        print(f"Error: The folder '{project_folder}' does not exist.")
        sys.exit(1)

    # Step 2: Enter the Scrapy project folder
    project_path = (
        "flightscraper"  # Change this to your actual Scrapy project folder name
    )
    if os.path.exists(project_path):
        os.chdir(project_path)
        print(f"Changed directory to Scrapy project folder: {os.getcwd()}")
    else:
        print(f"Error: The Scrapy project folder '{project_path}' does not exist.")
        sys.exit(1)

    # Step 3: Run Scrapy with the Python from the virtual environment
    python_executable = activate_virtualenv()

    # Use the Python executable from the virtual environment to run the Scrapy spider
    subprocess.run([python_executable, "-m", "scrapy", "crawl", "flights-selenium"])
