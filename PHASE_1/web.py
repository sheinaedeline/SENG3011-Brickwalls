from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
PATH ="C:\Program Files (x86)\chromedriver.exe"
def webscrap(initialDate,finalDate,location,*keywords):
    links = []
    finalReports = []
    for keyword in keywords:
        driver = webdriver.Chrome(PATH)
        driver.get("http://outbreaknewstoday.com/")
        search = driver.find_element_by_name("s")
        searchTerms = location + " " + keyword
        search.send_keys(searchTerms)
        search.send_keys(Keys.RETURN)
        ##searching the combination of searchterm and location
        ##exception below is due to delay
        try:
            result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "post_area"))
            )
        except:
            driver.quit()
        reports = result.find_elements_by_class_name("posttitle")
        linkTemp = []
        for report in reports:
            header = report.find_element_by_tag_name("a")
            link = report.find_element_by_link_text(header.text)
            print(link.get_attribute('href'))
            linkTemp.append(link)
            ##page change and add after the for loop below
        for link in linkTemp:
            link1 = link.get_attribute('href')

            driver2 = webdriver.Chrome(PATH)
            driver2.get(link1)
            date_of_publication = driver2.find_element_by_class_name('datsingle').text
            if checkDate(date_of_publication,initialDate,finalDate) == 1:
                links.append(link1)
            if checkDate(date_of_publication,initialDate,finalDate) == 2:
                break
    for link in links:
        driver3 = webdriver.Chrome(PATH)
        driver3.get(link)
        paras = driver3.find_element_by_class_name("postcontent")
        text = paras.text
        reportArticle = dataParser(text,location,*keywords)
        print(reportArticle)
        finalReports = finalReports.append(reportArticle)
        print(finalReports)

    ##basically have a list of all relevent links
    ##now we need to compare dates
    ## format should be like [1,13,2018] january 13
def checkDate(date,initialDate,finalDate):
    months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    date = date.split(' ')
    date1 = date[1].split(',')
    x = 0
    for month in months:
        if month == date[0]:
         x = x + 1
    date[0] = x
    date[1] = date1[0]
    d1 = datetime.datetime(int(date[2]),int(date[0]),int(date[1]))
    d2 = datetime.datetime(initialDate[2],initialDate[0],initialDate[1])
    d3 = datetime.datetime(finalDate[2],finalDate[0],finalDate[1])
    if d2 <= d1 <= d3:
        return 1
    elif d2 > d1:
        return 2
    else:
        return 0

def dataParser(text,location,*keywords):
    arrayText = text.split('.')
    for sentence in arrayText:
        wordArray = sentence.split(' ')
        x = 0
        print(wordArray)
        for word in wordArray:
            if word.isdigit():
                if wordArray[x+1] == "cases" or wordArray[x+2] == "cases" or wordArray[x+3] == "cases":
                    return word
            x = x + 1
    ##shittiest function ive ever written but dont know what else to write here
    ##someone needs to work on this i don't got a clue


webscrap([1,2,2018],[1,27,2021],"india","poliovirus")
