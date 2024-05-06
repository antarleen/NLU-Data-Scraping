from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import time
import csv


def scrape_data(district_name, court):
    table = driver.find_element(By.ID, "titlehid")
    rows = table.find_elements(By.TAG_NAME, "tr")
    rows = rows[1:]
    for row in rows[1:]:
        columns = row.find_elements(By.TAG_NAME, "td")
        if columns:
            entry_data = [col.text for col in columns]
            entry_data.extend([district_name, court])
            data_list.append(entry_data)


def writeDataToCsvByDistrict(data, district):
    # Write scraped data to a CSV file
    csv_filename = f"MH_scraped_data_disposed_{district}.csv"
    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(
            [
                "Serial No.",
                "Case ID",
                "Petitioner vs Respondent",
                "Respondent",
                "View Details",
            ]
        )  # Add appropriate column headers
        csv_writer.writerows(data_list)


# District Court Key for 309 Data
district_code_key_MH = {
    # "Dhule": 2,
    # "Gadchiroli": 12,
    # "Chandrapur": 13,
    # "Buldhana": 4,
    # "Beed": 27,
    # "Bhahdara": 10,
    # "Gonda": 11,
    # "Latur": 28,
    # "Maharastra CoOperative Courts": 41,
    # "Kohlapur": 34,
    # "Jalna": 18,
    # "Jalgaon": 3,
    # "Aurangabad": 19,
    # "Amravati": 7, --  Missed one Check and add manually
    # "Ahmednagar": 26,
    # "Akola": 5,
    # "Maharastra Family Courts": 42,
    # "Maharastra Industrial Labour Courts": 40,
    # "Wardha": 8,
    # "Washim": 36,
    # "Thane": 21, -- Missed one Check and add manually
    # "Solapur": 30,
    # "Satara": 31,
    # "Sindhudurg": 33,
    # "Yavatmal": 14,
    # "Sangli": 35,
    # "Ratnagiri": 32,
    # "Mumbai Small Courts": 38,
    # "Nagpur": 9,
    # "Mumbai Motor Accident Claims Tribunal": 39,
    "Mumbai CMM Courts": 23,
    # "Mumbai City Civil Court": 37,
    # "Nanded": 15,
    # "Nadurbar": 1,
    # "Pune": 25, -- Vadgaon Civil Court Senior Division data maybe missing. Check manually.
    # "Raigad": 24,
    # "Parbhani": 17,
    # "Osmanabad": 29,
    # "Nashik": 20,
}


# Iterate through every district and navigate to their webpage
for district_name, code in district_code_key_MH.items():
    data_list = []
    url = f"https://services.ecourts.gov.in/ecourtindia_v4_bilingual/cases/s_actwise.php?state=D&state_cd=1&dist_cd={code}"

    # List to store scraped data

    # Initialize a Selenium WebDriver
    # Initialize a Selenium WebDriver
    service = Service(executable_path="C:/webdrivers/chromedriver.exe")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    # Open the URL
    driver.get(url)
    time.sleep(5)

    # Select court complex name
    cc_code_dropdown = Select(driver.find_element(By.NAME, "court_complex_code"))

    # Get all the options from the dropdown
    options = cc_code_dropdown.options

    # Iterate through the options and print their text values
    for option in options[1:]:
        cc_code_dropdown.select_by_visible_text(option.text)
        # ID of the table to be captured titlehid
        # Find the input box element by
        act_input_box = driver.find_element(By.ID, "search_act")

        # Input text into the input box
        act_input_box.send_keys("Indian Penal Code")

        # Select Act Type
        act_type_dropdown = Select(driver.find_element(By.ID, "actcode"))
        flag = False
        act_options = act_type_dropdown.options
        # Check if INDIAN PENAL CODE is Present in the Options
        for act_option in act_options:
            # print(f"Hi ---- {act_option.text}")
            if act_option.text == "INDIAN PENAL CODE":
                flag = True
                break

        # Will consider both INDIAN PENAL CODE and Indian Penal Code, depending on which is present in the dropdown
        try:
            if flag:
                act_type_dropdown.select_by_visible_text("INDIAN PENAL CODE")
            else:
                act_type_dropdown.select_by_visible_text("Indian Penal Code")

            # Find the section input box
            under_sec_input_box = driver.find_element(By.ID, "under_sec")
            # Input text into the input box
            under_sec_input_box.send_keys("309")

            # Set the radio button for disposed
            radio_button = driver.find_element(By.ID, "radD")
            radio_button.click()

            submit_button = driver.find_element(By.NAME, "submit1")
            print("Enter the CAPTCHA!")
            time.sleep(20)
            submit_button.click()
            time.sleep(15)
            table_element = driver.find_element(By.ID, "titlehid")
            if table_element:
                scrape_data(district_name, option.text)
        except:
            continue

    # Close the Selenium WebDriver
    driver.quit()

    writeDataToCsvByDistrict(data_list, district_name)
