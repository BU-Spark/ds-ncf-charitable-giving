from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, ElementNotInteractableException, WebDriverException, ElementNotVisibleException

def clean_text(text):
    # Remove "FUNDER" and "RECIPIENT"
    text = re.sub(r"^(FUNDER|RECIPIENT)\s*", "", text, flags=re.IGNORECASE)
    # Strip labels 
    match = re.search(r"(?:TOTAL AMOUNT:|FISCAL YEAR:|GRANT DURATION:|PRIMARY SUBJECT:|POPULATION SERVED:|SUPPORT STRATEGY:|TRANSACTION TYPE:|PROGRAM AREA:)?\s*\$?\s*(.*)", text, flags=re.IGNORECASE)
    return match.group(1) if match else text

def safe_find_text_by_xpath(driver, xpath):
    try:
        element = driver.find_element(By.XPATH, xpath)
        print(f"Found element for xpath: {xpath}")  # Debug: Print element found
        element_text = element.text
        if not element_text.strip():  # Check if the text is empty or just whitespace
            print(f"No text found for xpath: {xpath}")  # Debug: Print empty text found
            return "Not Specified"
        cleaned_text = clean_text(element_text)
        print(f"Extracted and cleaned text for xpath {xpath}: {cleaned_text}")  # Debug: Print cleaned text
        return cleaned_text
    except (NoSuchElementException, ElementNotVisibleException, WebDriverException) as e:
        print(f"Failed to extract text for xpath: {xpath} - Error: {e}")  # Debug: Print failure reason
        return "Not Available"

def extract_data(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="list-screen-tabs-content"]'))
        )
        rows = driver.find_elements(By.XPATH, '//*[@id="list-screen-tabs-content"]//tr')[2:]  # Skip the first two rows

        for row in rows:
            try:
                details_button = WebDriverWait(row, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'td.cell-details > span.table-detail-icon'))
                )
                details_button.click()
                time.sleep(1)  # Wait a bit for the modal to open

                # Extract data using defined function
                grant_data = {
                    "Grant Funder Name": safe_find_text_by_xpath(driver, '//*[@id="fm-list-1popupprofile-modal-new"]/div/div/div[1]/div[1]/div/div[2]'),
                    "Grant Recipient Name": safe_find_text_by_xpath(driver, '//*[@id="fm-list-1popupprofile-modal-new"]/div/div/div[1]/div[1]/div/div[3]'),
                    "Grant Total Amount": safe_find_text_by_xpath(driver, '/html/body/div[6]/div[3]/div[3]/div[3]/div[10]/div/div/div[1]/div[2]/div[1]/span[1]'),
                    "Grant Fiscal Year": safe_find_text_by_xpath(driver, '/html/body/div[6]/div[3]/div[3]/div[3]/div[10]/div/div/div[1]/div[2]/div[1]/span[2]'),
                    "Grant Duration": safe_find_text_by_xpath(driver, '/html/body/div[6]/div[3]/div[3]/div[3]/div[10]/div/div/div[1]/div[2]/div[1]/span[3]'),
                    "Grant Program Area": safe_find_text_by_xpath(driver, '/html/body/div[6]/div[3]/div[3]/div[3]/div[10]/div/div/div[1]/div[2]/div[3]/div[1]'),
                    "Grant Primary Subject": safe_find_text_by_xpath(driver, '/html/body/div[6]/div[3]/div[3]/div[3]/div[10]/div/div/div[1]/div[2]/div[2]/span[1]'),
                    "Grant Population Served": safe_find_text_by_xpath(driver, '/html/body/div[6]/div[3]/div[3]/div[3]/div[10]/div/div/div[1]/div[2]/div[2]/span[2]'),
                    "Grant Support Strategy": safe_find_text_by_xpath(driver, '/html/body/div[6]/div[3]/div[3]/div[3]/div[10]/div/div/div[1]/div[2]/div[2]/span[3]'),
                    "Grant Transaction Type": safe_find_text_by_xpath(driver, '/html/body/div[6]/div[3]/div[3]/div[3]/div[10]/div/div/div[1]/div[2]/div[2]/span[4]'),
                    "Grant Description": safe_find_text_by_xpath(driver, '/html/body/div[6]/div[3]/div[3]/div[3]/div[10]/div/div/div[1]/div[3]/div[1]')
                }
                all_data.append(grant_data)

                # Close the details modal
                close_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="fm-list-1popupprofile-modal-new"]/div/div/button'))
                )
                close_button.click()
                time.sleep(1)  # Wait a bit for the modal to close
            except ElementClickInterceptedException:
                print("Element not clickable at the moment. Skipping.")
            except Exception as e:
                print(f"An error occurred: {e}")
    except TimeoutException:
        print("Failed to load the table or find rows within the given time.")

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()
driver.get('https://maps.foundationcenter.org/#/list/?subjects=all&popgroups=all&years=all&location=6254926&excludeLocation=0&geoScale=ADM1&layer=geo_area&boundingBox=-139.219,-31.354,135,66.513&gmOrgs=all&recipOrgs=all&tags=all&keywords=&pathwaysOrg=&pathwaysType=&acct=raceequpopup&typesOfSupport=all&transactionTypes=all&amtRanges=all&minGrantAmt=0&maxGrantAmt=0&gmTypes=all&recipTypes=all&minAssetsAmt=0&maxAssetsAmt=0&minGivingAmt=0&maxGivingAmt=0&andOr=0&includeGov=1&custom=all&customArea=all&indicator=&dataSource=oecd&chartType=trends&multiSubject=1&listType=recip&windRoseAnd=undefined&zoom=0')
time.sleep(2)

# Closes the pop-up window
try:
    close_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[class="close"]'))
    )
    close_button.click()
except ElementNotInteractableException as e:
    print("Close button not interactable:", e)
except NoSuchElementException as e:
    print("Close button not found:", e)

time.sleep(1)

# Clicks to open grant section
try:
    recipients = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'GRANTS'))
    )
    recipients.click()
except ElementClickInterceptedException as e:
    print("GRANTS link click intercepted:", e)
except ElementNotInteractableException as e:
    print("GRANTS link not interactable:", e)

time.sleep(1)

all_data = []

# First page data extraction
extract_data(driver)  # Pass 'driver' as an argument

# Handle pagination by iterating through pages
try:
    for page_num in range(2, 100):
        try:
            next_page = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f'/html/body/div[6]/div[3]/div[3]/div[3]/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/div/ul/li[a[text()="{page_num}"]]/a'))
            )
            next_page.click()
            # Wait for the table to refresh to ensure data consistency
            WebDriverWait(driver, 10).until(EC.staleness_of(
                driver.find_element(By.XPATH, '//*[@id="list-screen-tabs-content"]//tr'))
            )
            extract_data(driver)
        except TimeoutException:
            print(f"Timeout occurred while navigating to page {page_num}. Skipping this page.")
        except Exception as e:
            print(f"An error occurred while navigating to page {page_num}: {e}")
            break
except Exception as e:
    print(f"An error occurred during pagination: {e}")

# Save the collected data to a CSV file
df = pd.DataFrame(all_data)
if not df.empty:
    df.to_csv("Grant_Details.csv", index=False)
    print("Data extraction complete and CSV file created.")
else:
    print("No data extracted.")

# Clean up by closing the browser
driver.quit()
