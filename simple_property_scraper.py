#DISCLAIMER: The following software is not for commercial use and is only intended for personal portfolio use.
# The scraped data is publically available, will not be sold, and will be scraped at a reasonable rate.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#Using chrome as our webdriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

#Specify the URL we want to scrape
url = 'https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E87490&sortType=6&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords='

#Use user-agent header to allow for request to pass
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Open the webpage
driver.get(url)

# Wait for the content to load and find elements (adjust as necessary)
driver.implicitly_wait(10) # Adjust the wait time as needed
property_addresses = driver.find_elements(By.CSS_SELECTOR, 'address.propertyCard-address.property-card-updates')

for address in property_addresses:
    print(address.text)

driver.quit()