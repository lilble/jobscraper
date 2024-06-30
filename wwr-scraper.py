import requests
from bs4 import BeautifulSoup


jobs_data = []

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    job_list = soup.find("div", id="job_list")
    jobs = job_list.find_all("li")[:-1]

    for job in jobs:
        weworkurl = "https://weworkremotely.com"
        title = job.find("span", class_="title")
        company = job.find("span", class_="company")
        region = job.find("span", class_="region")
        url = weworkurl + job.find("div", class_="tooltip--flag-logo").next_sibling["href"]
        job_data = {
            "title": title.text,
            "company": company.text,
            "region": region.text if region else "",
            # "link": job.find_all("a")[-1]["href"]
            "link": url
        }
        jobs_data.append(job_data)
        # print(f"{job_data["title"]} - {job_data["company"]} - {job_data["region"]} - {job_data["link"]}")

def get_pages(url):
    response = requests.get(url+"?page=1")
    soup = BeautifulSoup(response.content, "html.parser")
    max_page = soup.find("div", class_="pagination").find_all("span", class_="page")[-1].text
    return int(max_page)

remote_full_time_jobs_url = "https://weworkremotely.com/remote-full-time-jobs"
total_pages = get_pages(remote_full_time_jobs_url)
for i in range(1, total_pages+1):
    print("scraping page", i)
    scrape_page(f"{remote_full_time_jobs_url}?page={i}")

print(len(jobs_data))