import pandas as pd
import os


class DataCleaner:
    def cleanBlrDistrictCourtData():
        data_new = pd.DataFrame()
        data = pd.read_csv(
            "C:/Users/PalA/OneDrive - Kantar/NLU Data Scraping/scraped_data/district_court_scraped_data_disposed_2.csv",
            index_col=False,
        )
        data.rename(columns={"Petitioner": "Pet_res_combined"}, inplace=True)
        data.drop(columns=["Respondent"], inplace=True)
        data["Pet_res_combined"] = data["Pet_res_combined"].str.replace("\n", " ")
        data_new = data["Pet_res_combined"].str.split(" Versus ", expand=True)
        data_new.columns = ["Petitioner", "Repondent"]
        cleaned_data = pd.concat([data, data_new], axis=1)
        cleaned_data.to_csv(
            "./scraped_data/blr_district_court_data_cleaned_disposed.csv", index=False
        )


DataCleaner.cleanBlrDistrictCourtData()
