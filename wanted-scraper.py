from playwright.sync_api import sync_playwright
import time 
from bs4 import BeautifulSoup
import csv

def wait():
    time.sleep(1)

p = sync_playwright().start()
browser = p.chromium.launch(headless=False)
page = browser.new_page()

# Go to wanted
wantedurl = "https://www.wanted.co.kr"
page.goto(f"{wantedurl}/wdlist")
wait()

# Click search button
page.click("button[aria-label=\"검색\"]")
wait() 

# Fill input box
page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter")
wait()

# Press enter key
page.keyboard.down("Enter")
wait()

# Click position tab
page.click("#search_tab_position")
wait()

# Scroll down
page.keyboard.down("End")
wait()
page.keyboard.down("End")
wait()
page.keyboard.down("End")
wait()

content = page.content()
p.stop()

# Get job data
jobs_db = []
soup = BeautifulSoup(content, "html.parser")
jobs_container = soup.find_all("div", {"data-testid" : "SearchPositionListContainer"})[-1]
jobs = jobs_container.find_all("div", role="listitem")
for job in jobs:
    a = job.find("a")
    title_and_company = a.find_all("div")[-1]
    job_data = {
        "title": title_and_company.find("strong").text,
        "company": title_and_company.find("span").find("span").text,
        "link": wantedurl + a["href"],
    }
    jobs_db.append(job_data)

# print(jobs_db)
# print(len(jobs_db))

# Save to csv
file = open("jobs.csv", "w")
writer = csv.writer(file)
writer.writerow(["Title", "Company", "Link"])
for job in jobs_db:
    writer.writerow(list(job.values()))