import pandas as pd
import os


class DataCleaner:
    def cleanMHDistrictCourtData():
        data_list = []
        data_folder = "C:/Users/PalA/OneDrive - Kantar/NLU Data Scraping/scraped_data/MH_Data_Cleaned"

        for file_name in os.listdir(data_folder):
            if file_name.endswith(".csv"):
                file_path = os.path.join(data_folder, file_name)
                df = pd.read_csv(file_path)
                data_list.append(df)

        combined_df = pd.concat(data_list, ignore_index=True)

        new_column_names = {
            "Case ID": "Petitioner vs Respondent",
            "Petitioner vs Respondent": "Details Path",
            "Respondent": "District",
            "View Details": "Court Complex",
        }

        # Rename the columns using the rename() method

        combined_df.rename(columns=new_column_names, inplace=True)
        combined_df["Petitioner vs Respondent"] = combined_df[
            "Petitioner vs Respondent"
        ].str.replace("\n", " ")
        data_new = combined_df["Petitioner vs Respondent"].str.split(
            " versus ", expand=True
        )
        data_new.columns = ["Petitioner", "Repondent"]
        cleaned_data = pd.concat([combined_df, data_new], axis=1)
        cleaned_data.to_csv(
            "./scraped_data/MH_Data_Cleaned/MH_district_court_data_cleaned_disposed.csv", index=False
        )


#
#


DataCleaner.cleanMHDistrictCourtData()
