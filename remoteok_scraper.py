import requests
from bs4 import BeautifulSoup


class JobData:
    def __init__(self, title, company, region, url):
        self.title = title
        self.company = company
        self.region = region
        self.url = url
    def __repr__(self):
        return f"{self.title} - {self.company} - {self.region} - {self.url}"

remoteok_header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}
def scrape_page(url):
    jobs_data = []
    response = requests.get(url, headers = remoteok_header)
    soup = BeautifulSoup(response.content, "html.parser")
    jobs = soup.find("table", id="jobsboard").find_all("td", class_="company")
    for job in jobs:
        title = job.find("h2")
        company = job.find("h3")
        region = job.find("div", class_="location")
        url = "https://remoteok.com" + job.find("a")["href"]

        jobdata = JobData(title.text, company.text, region.text if region else "", url)
        jobs_data.append(jobdata)
        # print(f"{jobdata.title} - {jobdata.company} - {jobdata.region} - {jobdata.url}")
    return jobs_data

jobs_dict = {}
keywords = ["flutter", "python", "golang"]
for keyword in keywords:
    print("scraping", keyword)
    jobs_dict[keyword] = scrape_page(f"https://remoteok.com/remote-{keyword}-jobs")

print(jobs_dict)