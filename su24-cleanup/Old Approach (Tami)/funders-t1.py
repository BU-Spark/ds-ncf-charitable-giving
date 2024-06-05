from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# 1: Initialize Chrome WebDriver
driver = webdriver.Chrome()

# 2: Open Web Page
driver.get('https://maps.foundationcenter.org/#/list/?subjects=all&popgroups=all&years=all&location=6254926&excludeLocation=0&geoScale=ADM1&layer=geo_area&boundingBox=-185.625,7.013667927566642,-19.16015625,74.01954331150228&gmOrgs=all&recipOrgs=all&tags=all&keywords=&pathwaysOrg=&pathwaysType=&acct=raceequpopup&typesOfSupport=all&transactionTypes=all&amtRanges=all&minGrantAmt=0&maxGrantAmt=0&gmTypes=all&recipTypes=all&minAssetsAmt=0&maxAssetsAmt=0&minGivingAmt=0&maxGivingAmt=0&andOr=0&includeGov=1&custom=all&customArea=all&indicator=&dataSource=oecd&chartType=trends&multiSubject=1&listType=gm&windRoseAnd=undefined&zoom=3')

# 3: Close Pop-Up Window
close_button = driver.find_element(By.XPATH, '//*[@id="welcome-modal"]/div/div/div[1]/button')
close_button.click()

# 4: Wait for the table to load
wait = WebDriverWait(driver, 10)
table = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="list-screen-all"]//table')))

# 5: Lists to Hold Headers and All Data
headers = []
all_data = []

# 6: Function to extract data from the current page
def extract_data():
    global headers, all_data
    rows = table.find_elements(By.TAG_NAME, 'tr')
    
    if not headers:
        # Assuming the first row contains the headers
        header_row = rows[0]
        headers = [th.text for th in header_row.find_elements(By.TAG_NAME, 'th')]
        
        if not headers:  # If headers are empty, try the second row
            header_row = rows[1]
            headers = [th.text for th in header_row.find_elements(By.TAG_NAME, 'td')]
        
        print(f"Extracted headers: {headers}")
        
    # Extract data rows, skipping the first header row(s)
    for row in rows[2:]:  # Adjust the starting index if headers span more rows
        cells = row.find_elements(By.TAG_NAME, 'td')
        row_data = [cell.text for cell in cells]
        all_data.append(row_data)

# 7: Extract data from the first page
extract_data()

# 8: Loop through each page number and extract data
for page_num in range(2, 100):  
    try:
        # Find the button for the next page
        page_buttons = driver.find_elements(By.XPATH, '//*[@id="fm-list-1gmfm-list-table_wrapper"]/div[2]/div[2]/div/ul/li/a')
        for button in page_buttons:
            if button.text == str(page_num):
                print(f"Navigating to page {page_num} using button: {button.text}")  # Debug information
                button.click()
                wait.until(EC.staleness_of(table))  # Wait for the table to reload
                table = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="list-screen-all"]//table')))
                extract_data()
                break
    except Exception as e:
        print(f"An error occurred while navigating to page {page_num}: {e}")
        break

# 9: Define CSV file path
csv_file_path = 'funders_data_t1.csv'

# 10: Write data to CSV
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(all_data)

print(f'Data successfully written to {csv_file_path}')

# 11: Pause Execution
input("Press Enter to close the browser")
driver.quit()
