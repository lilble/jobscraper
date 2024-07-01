from flask import Flask, render_template, request, redirect, send_file
from wanted_scraper import get_jobs_with_keyword
from datetime import datetime, timedelta
from savetofile import save_to_csv

app = Flask("JobScraper")

db = {} # {keyword: {time: timevalue, jobs: []}}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    keyword = request.args.get("keyword")
    if not keyword:
        return redirect('/')
    curr_time = datetime.now()
    if keyword in db and abs((curr_time - db[keyword]["time"]).total_seconds()) < 3600:
        jobs = db[keyword]["jobs"]
    else:
        jobs = get_jobs_with_keyword(keyword)
        db[keyword] = {"time": datetime.now(), "jobs": jobs}
    return render_template('search.html', keyword=keyword, jobs=jobs)

@app.route('/export')
def export():
    keyword = request.args.get("keyword")
    if not keyword:
        return redirect('/')
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")
    save_to_csv(keyword, db[keyword]["jobs"])
    return send_file(f"wanted-jobs/{keyword}.csv", as_attachment=True)

app.run('0.0.0.0', 8000)