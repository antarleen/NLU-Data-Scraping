from bs4 import BeautifulSoup
import requests
import pandas as pd

# url = "https://www.scrapethissite.com/pages/simple/"
# Create a master list to store the data
master_list = []
# Iterate through all the tables present in the webpage by changing the table_split variable
for table_split in range(1, 25):
    url = f"https://www.scrapethissite.com/pages/forms/?page_num={table_split}"
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    # Find all table rows in each webpage
    table_rows = soup.find_all("tr")
    # For eacg table row get each team name and year data
    for table_row in table_rows:
        table_data = table_row.find_all("td", class_=["name", "year"])
        # Append each row to a l`ist and add it to the master list
        list_data = []
        for td_el in table_data:
            list_data.append(td_el.text.strip("\n").strip())
        master_list.append(list_data)

# Remove any empty lists that are being created
master_list = [x for x in master_list if x]
# Create a dataframe
df = pd.DataFrame(master_list, columns=["Name", "Year"])
print(df)

# headers3 = soup.find_all("h3")
# for header in headers3:
#    print(header.text)


# Formatted string
# 200 Sucessful
# 400 Client Error
# 500 Server Error
