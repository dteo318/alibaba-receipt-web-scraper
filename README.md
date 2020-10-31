# alibaba-receipt-web-scraper



# Alibaba Receipt Web Scraper

A web scraper built with the Selenium framework to automatically and quickly download receipts from the Alibaba web store account. The scraper uses the Chrome browser to conduct the automated downloads.

## Installation

1. Fork this repository and clone it to your local environment.
2. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install virtualenv.

```bash
pip install virtualenv
```

3. Enter the virtual environment within the repository directory.

```bash
source venv/bin/activate
```

4. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install selenium.

```bash
pip install selenium
```

5. Download the appropriate driver for your version of Chrome [here](https://chromedriver.chromium.org/downloads), and place it in the drivers folder, replacing the previous driver.
6. Open the main.py file in a code editor and edit the fields highlighted (account id/pw, file download directory, etc).

## Usage

Run the program using the terminal.

```bash
python main.py
```
