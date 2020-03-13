import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

#This example requires Selenium WebDriver 3.13 or newer
def main():
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    with webdriver.Chrome(options=option) as driver:
        wait = WebDriverWait(driver, 10)
        driver.get("https://careers.eskaton.org/")
        element = driver.find_element_by_xpath("//*[@id='DataTables_Table_0']/thead/tr/th[1]")
        element.click()
        element.click()

        webTable = driver.find_element_by_xpath("//*[@id='DataTables_Table_0']")
        headerList = get_table_header(webTable)
        bodyList = get_table_body(webTable)
        table = headerList + bodyList
        table_to_csv(webTable, table, "eskaton_jobs.csv")
        update_csv(webTable)


        
"""
Module that retieves text/data from the body of the webtable and stores the text/data into a 
numOfRows x numOfColumns size list. 
""" 
def get_table_body(webTableElem):
    # get number of rows
    numOfRows = len(webTableElem.find_elements_by_xpath("//tr"))
    # get number of columns
    numOfColumns = len(webTableElem.find_elements_by_xpath("//tr[2]/td"))
    allData = []
    # iterate over the rows, to ignore the headers we have started the i with '1'
    for i in range(1, numOfRows):
        ro = []
        for j in range(1, numOfColumns) :
            # get text from the i th row and j th column from table body
            text = webTableElem.find_element_by_xpath("//tr["+str(i)+"]/td["+str(j)+"]").text
            ro.append(text)

        allData.append(ro)

    return allData

def get_table_header(webTableElme):
    headerElem = webTableElme.find_elements_by_xpath("//thead/tr[1]/th")
    #ignore the Actions column in the table
    numOfColumns = len(headerElem) - 1
    tableHeader = [[]]
    for colm in range(0, numOfColumns):
        text = headerElem[colm].text
        text = text.replace("\n", " ")
        tableHeader[0].append(text)
    
    return tableHeader
"""
Module returns the first row of the table body in the form of a list.
"""
def get_first_body_row(webTable):
    rowElems = webTable.find_elements_by_xpath("//tbody/tr[1]/td")
    numOfColumns = len(rowElems) - 1
    firstRow = [[]]
    for i in range(0, numOfColumns):
        text = rowElems[i].text
        text = text.replace("\n", " ")
        firstRow[0].append(text)
    return firstRow

"""
Module that checks if the eksaton_jobs.csv file exists. If it does not,
create the file, otherwise, check if there was a new job was posted. If 
a new job was posted, add it to the begining of the csv file.
"""
def table_to_csv(webTableElem, webTableList, fileName):
    try:
        df = pd.read_csv("eskaton_jobs.csv")
        #retrieve table header and first row of the table body
        #needed to initialize the new dataframe
        first_table_row = get_first_body_row(webTable)
        table_header = get_table_header(webTable)
        #convert first data row in dataframe into a list
        df_first_row = []
        df_first_row.append(list(df.iloc[0, :])) 

        #compare first row of the table body to first data row of dataframe
        if first_table_row == df_first_row:
            return
        df2 = pd.DataFrame(data = first_table_row, columns=table_header[0])
        df = pd.concat([df2, df], ignore_index=True)
        df.to_csv("eskaton_jobs.csv", index=False)
    except:
        df = pd.DataFrame(data = webTableList)
        df.to_csv("eskaton_jobs.csv", header=False,index=False)

def update_csv(webTableElem):
    #get the html table body from eskaton's website that contains
    #current jobs available and store its data in a list
    tableBodyList = get_table_body(webTableElem)
    df = pd.read_csv("eskaton_jobs.csv")
    dfRowCount = len(df)
    dfRow = 0
    dfList = []
    foundRemovedJob = False
    #convert the dataframe into a list
    for row in range(0, dfRowCount):
        dfList.append(list(df.iloc[row,:]))
    #a loop to check to see if a job posting in the csv no longe exists in the
    #table body that contains current job listings
    for listing in tableBodyList:
        if listing not in dfList:
            df.drop([dfRow])
            foundRemovedJob = True
        dfRow += 1
    
    if foundRemovedJob != True:
        print("No jobs to remove from csv")
        return
    df.to_csv("eskaton_jobs.csv", header=False,index=False)

    



main()