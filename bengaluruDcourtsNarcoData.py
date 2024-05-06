from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import time
import csv

# URL of the webpage
url = "https://bengaluru.dcourts.gov.in/case-status-search-by-act-type/"

# List to store scraped data
data_list = []

# Initialize a Selenium WebDriver
service = Service(executable_path="C:/webdrivers/chromedriver.exe")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Open the URL
driver.get(url)


# Function to scrape data from the current page
def scrape_data():
    table = driver.find_element(By.CLASS_NAME, "data-table-1")
    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        entry_data = [col.text for col in columns]
        data_list.append(entry_data)


# # Perform initial scraping
# scrape_data()

# Select "CMM Court Complex, Bangalore" from the est_code dropdown
est_code_dropdown = Select(driver.find_element(By.ID, "est_code"))
est_code_dropdown.select_by_visible_text("CMM Court Complex, Bangalore")

# Select "Narcotic Drugs and Psychotropic Substances Act" from the act dropdown
act_dropdown = Select(driver.find_element(By.NAME, "national_act_code"))
act_dropdown.select_by_visible_text("Narcotic Drugs and Psychotropic Substances Act")

# Select "Pending" or "Disposed" in the radio inputs
# ID "chkYesStatus" for Pending
# ID "chkNoStatus" for Disposed

radio_button = driver.find_element(By.ID, "chkNoStatus")
radio_button.click()


print("Please put in the captcha !")
time.sleep(10)

submit_button = driver.find_element(By.NAME, "submit")
submit_button.click()
time.sleep(10)
# Find and click the "Load More" button until it's not present
while True:
    try:
        # load_more_button = WebDriverWait(driver, 15).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, "loadMoreCases"))
        # )

        load_more_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "loadMoreCases"))
        )
        time.sleep(10)
        load_more_button.click()
        time.sleep(10)

    except:
        print("Ded !!")
        break

scrape_data()

# Close the Selenium WebDriver
driver.quit()

# Write scraped data to a CSV file
csv_filename = "district_court_scraped_data_disposed_2.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(
        ["Serial No.", "Case ID", "Petitioner", "Respondent"]
    )  # Add appropriate column headers
    csv_writer.writerows(data_list)

# print(f"Scraped data saved to {csv_filename}")
