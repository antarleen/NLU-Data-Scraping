from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import csv

# URL of the webpage
url = "https://secure.mygov.in/group-issue/inputs-draft-national-education-policy-2016/"

# List to store scraped data
data_list = []

# Initialize a Selenium WebDriver
driver = webdriver.Chrome(executable_path="D:/SW/chromedriver.exe")

# Open the URL
driver.get(url)


# Function to scrape data from the current page
def scrape_data():
    div_elements = driver.find_elements(by=By.CSS_SELECTOR, value="div.comment_col1")

    for div in div_elements:
        user_data = []
        username_element = div.find_element(by=By.CSS_SELECTOR, value="span.username")
        comment_date_element = div.find_element(
            by=By.CSS_SELECTOR, value="span.date_time"
        )
        # comment_element = div.find_element(by=By.CSS_SELECTOR, value="div.comment_body")

        # Add extracted data to a common data list
        user_data = [
            username_element.text,
            comment_date_element.text,
            # comment_element.text,
        ]
        data_list.append(user_data)


# Find and click the "View More" button until it's not present
while True:
    try:
        time.sleep(2)
        load_more_button = driver.find_element_by_css_selector('a[title="View More"]')
        load_more_button.click()
        time.sleep(2)

    except Exception as e:
        print(e)
        print("Ded !!")
        break

scrape_data()

# Close the Selenium WebDriver
driver.quit()


# Write scraped data to a CSV file
txt_filename = "NEPData_UserComments.txt"
csv_filename = "NEPData_UserComments.csv"

# Open the file for writing
with open(txt_filename, "w", encoding="utf-8") as file:
    # Loop through the list of lists
    for sublist in data_list:
        # Convert the inner list to a string and write it to the file
        line = " ".join(map(str, sublist))  # Join elements with space
        file.write(line + "\n")  # Add a newline character after each inner list

print(f"List of lists has been written to {txt_filename}")

with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(
        ["User", "Comment Date"]
        # "Comment"
    )  # Add appropriate column headers
    csv_writer.writerows(data_list)

print(f"Scraped data saved to {csv_filename}")
