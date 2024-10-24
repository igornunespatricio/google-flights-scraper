import subprocess
import shutil
import os
import sys


def create_virtualenv():
    # Step 1: Create a virtual environment called .venv
    subprocess.run([sys.executable, "-m", "venv", ".venv"])


def activate_virtualenv():
    # Step 2: Activate the virtual environment
    activate_script = ".venv\\Scripts\\activate"
    if os.name != "nt":  # If the OS is not Windows
        activate_script = ".venv/bin/activate"
    return activate_script


def install_packages():
    # Step 3: Install required packages with specific versions
    packages = [
        "pyodbc==5.2.0",
        "python-dotenv==1.0.1",
        "Scrapy==2.11.2",
        "scrapy-selenium==0.0.7",
        "selenium==4.25.0",
    ]
    subprocess.run([f".venv\\Scripts\\pip", "install"] + packages, shell=True)


def replace_middleware():
    # Step 4: Replace the scrapy-selenium middleware file
    source_path = os.path.join("custom_scripts", "middlewares.py")
    dest_path = os.path.join(
        ".venv", "Lib", "site-packages", "scrapy_selenium", "middlewares.py"
    )

    if os.path.exists(dest_path):
        shutil.copyfile(source_path, dest_path)
        print(f"Replaced: {dest_path}")
    else:
        print(f"Error: {dest_path} not found.")


if __name__ == "__main__":
    create_virtualenv()
    # Activate the virtual environment (this will be for manual use)
    print(
        f"Run this to activate the virtual environment: \nsource {activate_virtualenv()}"
    )
    install_packages()
    replace_middleware()
