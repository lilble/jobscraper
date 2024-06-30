from playwright.sync_api import sync_playwright
import time 
from bs4 import BeautifulSoup
from savetofile import save_to_csv

wantedurl = "https://www.wanted.co.kr"

def wait():
    time.sleep(1)

def scrape_page(page, keyword):
    # Click search button
    page.click("button[aria-label=\"검색\"]")
    wait() 

    # Fill input box
    page.get_by_placeholder("검색어를 입력해 주세요.").fill(keyword)
    wait()

    # Press enter key
    page.keyboard.down("Enter")
    wait()

    # Click position tab
    page.click("#search_tab_position")
    wait()

    # Scroll down 3 times
    page.keyboard.down("End")
    page.keyboard.down("End")
    page.keyboard.down("End")
    wait()

    content = page.content()
    return content

def get_jobs(content):
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
    return jobs_db

def scrape_wanted(keywords):
    # Launch browser
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    # Go to wanted
    page.goto(f"{wantedurl}/wdlist")
    wait()
    for keyword in keywords:
        jobs = get_jobs(scrape_page(page, keyword))
        save_to_csv(keyword, jobs)
    p.stop()

keywords = ["flutter", "python", "golang"]
scrape_wanted(keywords)