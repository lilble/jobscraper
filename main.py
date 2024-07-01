from flask import Flask, render_template, request, redirect
from wanted_scraper import get_jobs_with_keyword
from datetime import datetime, timedelta

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
    if keyword in db and abs((curr_time - db[keyword]["time"]).total_seconds()) > 3600:
        jobs = db[keyword]
    else:
        jobs = get_jobs_with_keyword(keyword)
        db[keyword] = {"time": datetime.now(), "jobs": jobs}
    return render_template('search.html', keyword=keyword, jobs=jobs)

app.run('0.0.0.0', 8000)