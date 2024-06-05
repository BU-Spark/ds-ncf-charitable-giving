from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import re
import time
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, WebDriverException

def clean_text(text):
    # Remove "FUNDER" and "RECIPIENT" 
    text = re.sub(r"^(FUNDER|RECIPIENT)\s*", "", text, flags=re.IGNORECASE)
    # Strip labels and capture data after patterns like "TOTAL AMOUNT:", "FISCAL YEAR:", etc.
    match = re.search(r"(?:TOTAL AMOUNT:|FISCAL YEAR:|GRANT DURATION:|PRIMARY SUBJECT:|POPULATION SERVED:|SUPPORT STRATEGY:|TRANSACTION TYPE:|GRANT PROGRAM AREA:)?\s*\$?\s*(.*)", text, flags=re.IGNORECASE)
    return match.group(1) if match else text

def safe_find_text_by_xpath(driver, xpath):
    try:
        element_text = driver.find_element(By.XPATH, xpath).text
        if not element_text.strip():  # Check if the text is empty or just whitespace
            raise ValueError("Empty String Found")
        return clean_text(element_text)
    except (NoSuchElementException, ElementNotVisibleException, ValueError, WebDriverException) as e:
        return "Not Available"

driver = webdriver.Chrome()
driver.get('https://maps.foundationcenter.org/#/list/?subjects=all&popgroups=all&years=all&location=6254926&excludeLocation=0&geoScale=ADM1&layer=geo_area&boundingBox=-139.219,-31.354,135,66.513&gmOrgs=all&recipOrgs=all&tags=all&keywords=&pathwaysOrg=&pathwaysType=&acct=raceequpopup&typesOfSupport=all&transactionTypes=all&amtRanges=all&minGrantAmt=0&maxGrantAmt=0&gmTypes=all&recipTypes=all&minAssetsAmt=0&maxAssetsAmt=0&minGivingAmt=0&maxGivingAmt=0&andOr=0&includeGov=1&custom=all&customArea=all&indicator=&dataSource=oecd&chartType=trends&multiSubject=1&listType=recip&windRoseAnd=undefined&zoom=0')
time.sleep(2)

# Closes the pop-up window
close_button = driver.find_element(By.CSS_SELECTOR, 'button[class="close"]')
close_button.click()
time.sleep(1)

# Clicks to open grant section
recipients = driver.find_element(By.PARTIAL_LINK_TEXT, 'GRANTS')
recipients.click()
time.sleep(1)

# Click on the Details button to get to 2nd tier page
details_button = driver.find_element(By.CLASS_NAME, 'cell-details')
details_button.click()
time.sleep(1)

# Extract and clean recipient data using the updated clean_text function
grant_funder_name = safe_find_text_by_xpath(driver, '//*[@id="fm-list-1popupprofile-modal-new"]/div/div/div[1]/div[1]/div/div[2]')
grant_recipient_name = safe_find_text_by_xpath(driver, '//*[@id="fm-list-1popupprofile-modal-new"]/div/div/div[1]/div[1]/div/div[3]')
grant_total_amount = safe_find_text_by_xpath(driver, '/html/body/div[6]/div[3]/div[3]/div[3]/div[10]/div/div/div[1]/div[2]/div[1]/span[1]')
grant_fiscal_year = safe_find_text_by_xpath(driver, '/html/body/div[6]/div[3]/div[3]/div[3]/div[10]/div/div/div[1]/div[2]/div[1]/span[2]')
grant_duration = safe_find_text_by_xpath(driver, '/html/body/div[6]/div[3]/div[3]/div[3]/div[10]/div/div/div[1]/div[2]/div[1]/span[3]')
grant_program_area = safe_find_text_by_xpath(driver, '/html/body/div[6]/div[3]/div[3]/div[3]/div[10]/div/div/div[1]/div[2]/div[3]/div[1]')
grant_primary_subject = safe_find_text_by_xpath(driver, '/html/body/div[6]/div[3]/div[3]/div[3]/div[10]/div/div/div[1]/div[2]/div[2]/span[1]')
grant_population_served = safe_find_text_by_xpath(driver, '/html/body/div[6]/div[3]/div[3]/div[3]/div[10]/div/div/div[1]/div[2]/div[2]/span[2]')
grant_support_strategy = safe_find_text_by_xpath(driver, '/html/body/div[6]/div[3]/div[3]/div[3]/div[10]/div/div/div[1]/div[2]/div[2]/span[3]')
grant_transaction_type = safe_find_text_by_xpath(driver, '/html/body/div[6]/div[3]/div[3]/div[3]/div[10]/div/div/div[1]/div[2]/div[2]/span[4]')
grant_description = safe_find_text_by_xpath(driver, '/html/body/div[6]/div[3]/div[3]/div[3]/div[10]/div/div/div[1]/div[3]/div[1]')

data = {
    "Grant Funder Name": [grant_funder_name],
    "Grant Recipient Name": [grant_recipient_name],
    "Grant Total Amount": [grant_total_amount],
    "Grant Fiscal Year": [grant_fiscal_year],
    "Grant Duration": [grant_duration],
    "Grant Program Area": [grant_program_area],
    "Grant Primary Subject": [grant_primary_subject],
    "Grant Population Served": [grant_population_served],
    "Grant Support Strategy": [grant_support_strategy],
    "Grant Transaction Type": [grant_transaction_type],
    "Grant Description": [grant_description]
}

df = pd.DataFrame(data)
df.to_csv("Grant_Details.csv", index=False)
