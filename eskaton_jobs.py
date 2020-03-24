import pandas as pd
from os import path
from pync import Notifier
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

# Script driver code. Create or update the csv file eskaton_jobs.csv
# containing the web table data.
def main():
    # Follwing two lines ensures no browser window opens while
    # running the script. 
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    with webdriver.Chrome(options=option) as driver:
        wait = WebDriverWait(driver, 10)
        driver.get("https://careers.eskaton.org/")
        # Retrieve the row "Date Opened" element from the table header 
        elem = driver.find_element_by_xpath("//*[@id='DataTables_Table_0']/thead/tr/th[1]")
        # Clicking the element twice organizes the table 
        # from new job listings to old listings.
        elem.click()
        elem.click()

        webTableElem = driver.find_element_by_xpath("//*[@id='DataTables_Table_0']")
        table_to_csv(webTableElem)

"""
Check if the eskaton_jobs.csv file exists. If it does exist,
check if there was a new job was posted, otherwise, create the file.
Also update the csv file for removed job listings.
"""
def table_to_csv(webTableElem):
    if path.isfile("/Users/Jose/Desktop/seleniumProject/eskaton_jobs.csv") is True:
        df = pd.read_csv("eskaton_jobs.csv")
        df, numOfNewJobs = find_new_jobs_posted(webTableElem, df)
        print("number of new jobs: " + str(numOfNewJobs))
        df = update_job_postings(webTableElem, df)
        df.to_csv("eskaton_jobs.csv", index=False)
        return
    else:
        print("create table")
        header = get_table_header(webTableElem)
        body = get_table_body(webTableElem)
        table  = header + body
        df = pd.DataFrame(data = table)
        df.to_csv("eskaton_jobs.csv", header=False,index=False)
        return

"""
Find new job(s) posted in Eskaton's website and adds them to
the dataframe. If no new jobs were posted, return the original 
dataframe. Otherwise, return the updated dataframe. The method
also returns the number of new jobs found.
"""
def find_new_jobs_posted(webTableElem, df):
    tableHeader = get_table_header(webTableElem)
    tableBody = get_table_body(webTableElem)
    dfList = dataframe_to_list(df)
    newJobs = []
    newJobsPosted = False
    numOfNewJobs = 0
    for listing in tableBody:
        if listing not in dfList:
            newJobs.append(listing)
            newJobsPosted = True
            numOfNewJobs += 1
    if newJobsPosted is False:
        return df, numOfNewJobs
    notify_user(newJobs, newJobsPosted)
    df2 = pd.DataFrame(data = newJobs, columns=tableHeader[0])
    df = pd.concat([df2, df], ignore_index=True)
    return df, numOfNewJobs

#Method that searches Eskaton's job postings for removed job(s). 
def update_job_postings(webTableElem, df):
    table = get_table_body(webTableElem)
    dfList = dataframe_to_list(df)
    dfRow = 0 #Will keep track of which row in the dataframe is to be removed
    for listing in dfList:
        if listing not in table:
            df = df.drop(dfRow, axis = 0)
        dfRow += 1
    return df

#Method that converts a dataframe into a list of lists
#Assumes the csv file used to populate dataframe exists.    
def dataframe_to_list(df):
    dfRowCount = len(df)
    dfList = []
    for row in range(0, dfRowCount):
        dfList.append(list(df.iloc[row,:]))
    return dfList

#Output a notification to the computer with the new job(s) found.
def notify_user(newJobsList, numOfNewJobs):
    if numOfNewJobs < 1 or len(newJobsList) is 0:
        return
    for job in newJobsList:
        careerTitle = job[1]
        jobLocation = job[2]
        Notifier.notify(careerTitle, 
                        title='New Job!',
                        subtitle = jobLocation,
                        open='https://careers.eskaton.org/',
                        sound='Hero',
                        appIcon='https://image.shutterstock.com/image-vector/notification-icon-isolated-on-black-600w-1239560479.jpg')

"""
Method that retieves the text from the body of the webtable 
and stores it into a numOfRows x numOfColumns size list. 
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
        tableHeader[0].append(text)
    
    return tableHeader
"""
Retieves the first row of the html table stores the data in a list.
"""
def get_first_body_row(webTable):
    rowElems = webTable.find_elements_by_xpath("//tbody/tr[1]/td")
    numOfColumns = len(rowElems) - 1
    firstRow = [[]]
    for i in range(0, numOfColumns):
        text = rowElems[i].text
        firstRow[0].append(text)
    return firstRow

main()