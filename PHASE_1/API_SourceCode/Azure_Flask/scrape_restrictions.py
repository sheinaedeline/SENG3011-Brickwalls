import requests 
from bs4 import BeautifulSoup
import json

actData = [{"state": "Australian Captital Territory"}]
nswData = [{"state": "New South Wales"}]
ntData = [{"state": "Northern Territory"}]
qldData = [{"state": "Queensland"}]
saData = [{"state": "South Australia"}]
tasData = [{"state": "Tasmania"}]
vicData = [{"state": "Victoria"}]
waData = [{"state": "Western Australia"}]

# def scrape_state_restrictions(location=None):
#     if location == "Australian Capital Territory":
#         URL = "https://www.covid19.act.gov.au/community/travel"
#     elif location == "New South Wales":
#         URL = "https://www.nsw.gov.au/covid-19/what-you-can-and-cant-do-under-rules/border-restrictions/public-transport"
#     elif location == "Northern Territory":
#         URL = "https://coronavirus.nt.gov.au/travel/quarantine"
#     elif location == "Queensland":
#         URL = "https://www.qld.gov.au/health/conditions/health-alerts/coronavirus-covid-19/stay-informed/travel-advice"
#     page = requests.get(URL)
#     soup = BeautifulSoup(page.content, "html.parser")

def scrape_nsw_restriction():
    URL = "https://www.nsw.gov.au/covid-19/what-you-can-and-cant-do-under-rules/border-restrictions/public-transport"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    # get last updated date from the web 
    # to see when restriction come into place 
    count = 1
    restrictions = soup.find(class_="nsw-wysiwyg-content")
    ul = restrictions.find("ul")
    rules = ul.findAll("li")
    for rule in rules:
        nswItem = {}
        r = rule.text.strip()
        nswItem['rule ' + str(count)] = r
        count += 1
        nswData.append(nswItem)
    # rule = restriction.text.strip()
    # for line in rule.splitlines():
    #     print(line)
    #     nswItem['rule ' + str(count)] = line
    #     count =+ 1
    # # print(rule.text.strip())
    # nswData.append(nswItem)
    # print(rule)

    for i in soup.findAll('time'):
        if i.has_attr('datetime'):
            date = i['datetime']
            nswItem['date effective'] = date
            nswData.append(nswItem)
    with open("./state_data/nswTravelRestriction.json", "w") as nswOutfile:
        json.dump(nswData, nswOutfile, indent = 2)
    return nswData


def scrape_act_restriction():
    URL = "https://www.covid19.act.gov.au/community/travel"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    actions = soup.find("div", id="TOCScannableArea")
    ul = actions.find("ul")
    l = ul.findAll("li")
    strategy = 1
    for i in l:
        preventativeActions = {}
        act = i.text.strip()
        preventativeActions['action ' + str(strategy)] = act
        strategy += 1
        actData.append(preventativeActions)
    restrictions = soup.findAll("p")
    count = 1
    for restriction in restrictions:
        actItem = {}
        rule = restriction.text.strip()
        # date = datefinder.find_dates(rule)
        # print(date)
        actItem['rule' + str(count)] = rule 
        count += 1
        # going to assume when the last time this 
        # website was updated is going to be when these 
        # restrictions are in effect because 
        date = soup.find(id="dateLastUpdated")
        dateEffective = date.text.strip()
        actItem['date effective'] = dateEffective
        actData.append(actItem)
    with open("./state_data/actTravelRestriction.json", "w") as actOutfile:
        json.dump(actData, actOutfile, indent = 2)
    return actData

def scrape_nt_restriction():
    URL = "https://coronavirus.nt.gov.au/travel/quarantine"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    restrictions = soup.find("div",id="content_container_809791")
    ul = restrictions.find("ul")
    p = restrictions.find("p").text.strip()
    rules = ul.findAll("li")
    count = 1
    for rule in rules:
        ntItem = {}
        r = rule.text.strip()
        ntItem['rule ' + str(count)] = r
        count += 1
        ntData.append(ntItem)
    with open("./state_data/ntTravelRestriction.json", "w") as ntOutfile:
        json.dump(ntData, ntOutfile, indent = 2)
    return ntData


    # restrictions = soup.findAll("p")
    # for restriction in restrictions:
    #     rule = restriction.text.strip()
    #     print(rule)

def scrape_qld_restriction():
    URL = "https://www.qld.gov.au/health/conditions/health-alerts/coronavirus-covid-19/stay-informed/travel-advice"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    advices = soup.findAll("div", class_="qg-index-item")
    count = 1
    for advice in advices:
        qldItem = {}
        rule1Title = advice.find("span")
        title = rule1Title.text.strip()
        rule1 = advice.find("p")
        r1 = rule1.text.strip()
        rule1Link = advice.find("a")["href"]
        qldItem['title'] = title
        qldItem['rule ' + str(count)] = r1
        qldItem['link'] = rule1Link
        count += 1
        qldData.append(qldItem)
    with open("./state_data/qldTravelRestriction.json", "w") as qldOutfile:
        json.dump(qldData, qldOutfile, indent = 2)
    return qldData


def scrape_sa_restriction():
    URL = "https://www.covid-19.sa.gov.au/restrictions-and-responsibilities/travel-restrictions"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    restrictions = soup.findAll("h2")
    rules = soup.findAll("p")
    count = 1
    for rule in rules:
        saItem = {}
        r = rule.text.strip()
        saItem['rule ' + str(count)] = r
        count += 1
        saData.append(saItem)
        # for title in restrictionTitles:
        #     rule = title.find("p")
        #     print(rule.text.strip())
    with open("./state_data/saTravelRestriction.json", "w") as saOutfile:
        json.dump(saData, saOutfile, indent = 2)
    return saData

def scrape_tas_restriction():
    URL = "https://www.coronavirus.tas.gov.au/travellers-and-visitors"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    restrictions = soup.findAll("div", class_="card")
    count = 1
    for restriction in restrictions:
        tasItem = {}
        title = restriction.find("h5", class_="card-title")
        ruleTitle = title.text.strip()
        tasItem['title'] = ruleTitle
        info = restriction.find("p", class_="card-text")
        ruleInfo = info.text.strip()
        tasItem['rule ' + str(count)] = ruleInfo
        link = restriction.find("a")["href"]
        tasItem['link'] = link
        date = soup.find("div", class_="date-removal")
        effectiveDate = date.text.strip().replace("Last Updated: ", "")
        tasItem['date effective'] = effectiveDate
        count += 1
        tasData.append(tasItem)
    with open("./state_data/tasTravelRestriction.json", "w") as tasOutfile:
        json.dump(tasData, tasOutfile, indent = 2)
    return tasData

def scrape_vic_restriction():
    URL = "https://www.coronavirus.vic.gov.au/covidsafe-travel-victoria"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    advice = soup.find("div", class_="callout-wrapper")
    ul = advice.find("ul")
    adviceList = ul.findAll("li")
    count = 1
    for rule in adviceList:
        vicItem = {}
        r = rule.text.strip()
        vicItem['rule ' + str(count)] = r
        count += 1
        date = soup.find("p", class_="rpl-updated-date")
        effectiveDate = date.text.strip().replace("Reviewed ", "")
        vicItem['date effective'] = effectiveDate
        vicData.append(vicItem)
    with open("./state_data/vicTravelRestriction.json", "w") as vicOutfile:
        json.dump(vicData, vicOutfile, indent = 2)
    return vicData

def scrape_wa_restriction():
    URL = "https://www.wa.gov.au/organisation/department-of-the-premier-and-cabinet/covid-19-coronavirus-travel-and-quarantine#wa-state-border-closure"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    dateSection = soup.find("blockquote")
    date = dateSection.find("p")
    effectiveDate = date.text.strip()
    ul = dateSection.find("ul")
    rules = ul.findAll("li")
    count = 1
    for rule in rules:
        waItem = {}
        link = rule.find("a")['href']
        r = rule.text.strip()
        waItem['rule ' + str(count)] = r
        waItem['date effective'] = effectiveDate
        waItem['link'] = link
        count += 1
        waData.append(waItem)
    with open("./state_data/waTravelRestriction.json", "w") as waOutfile:
        json.dump(waData, waOutfile, indent = 2)
    return waData



#scrape_nsw_restriction()
#scrape_act_restriction()
#scrape_nt_restriction()
#scrape_qld_restriction()
#scrape_sa_restriction()
#scrape_tas_restriction()
#scrape_vic_restriction()
#print(scrape_wa_restriction())
