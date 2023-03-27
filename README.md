# Facebook-Marketplace-Vehicle-Scraper

[![CodeQL](https://github.com/livxy/Facebook-Marketplace-Vehicle-Scraper/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/livxy/Facebook-Marketplace-Vehicle-Scraper/actions/workflows/codeql-analysis.yml)

## For use of scraping vehicle information on Facebook Marketplace using Selenium.

Hi so the original person didn't exactly finish the project so I worked on this for a couple of hours and it has customizable features for your needs such as:

- Automatic log-in process on FaceBook using Selenium.
- Customizable Web Driver Path.
- Query customization for different cars or vehicles.
- Minimum & Maximum year customization
- Price range customization
- Vehicle brand customization

![image](https://user-images.githubusercontent.com/67598470/201967975-23994744-3169-44fa-9c3a-a121192b35f3.png)

## How to run/use:

1. Simply clone the repository, and in your favorite text editor edit the file called `setup.json` with your preferences.

2. Change email to your FaceBook phone number/email that is associated with your account, as well as the password, respectively.

3. Download latest Chrome WebDriver at the following link: https://chromedriver.chromium.org/downloads

4. Copy the path located to the Web Driver executable and paste it in the quoted `WebDriver_Path` area.

5. Run `py main.py`

6. View the resulting CSV
