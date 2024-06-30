import csv

def save_to_csv(keyword, jobs_db):
    file = open(f"wanted-jobs/{keyword}.csv", "w")
    writer = csv.writer(file)
    writer.writerow(["Title", "Company", "Link"])
    for job in jobs_db:
        writer.writerow(list(job.values()))