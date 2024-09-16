from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from scraper import knasta, lodoro
import pandas as pd
import os

def main():
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)

    knasta_df = knasta(driver)
    # lodoro_df = lodoro(driver)

    if os.path.exists('resultados_perfumes.xlsx'):
        #if the file exist, dont do anything
        pass
    else:
        #create a file with the name "resultados_perfumes.xlsx"
        open('resultados_perfumes.xlsx', 'w').close()


    
    with pd.ExcelWriter("resultados_perfumes.xlsx") as writer:
    
        # use to_excel function and specify the sheet_name and index 
        # to store the dataframe in specified sheet
        knasta_df.to_excel(writer, sheet_name="Knasta", index=False)
        # lodoro_df.to_excel(writer, sheet_name="Lodoro", index=False)

if __name__ == "__main__":
    main()