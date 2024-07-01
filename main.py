from flask import Flask, render_template, request
from wanted_scraper import get_jobs_with_keyword

app = Flask("JobScraper")

db = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    keyword = request.args.get("keyword")
    if keyword in db:
        jobs = db[keyword]
    else:
        jobs = get_jobs_with_keyword(keyword)
        db[keyword] = jobs
    return render_template('search.html', keyword=keyword, jobs=jobs)

app.run('0.0.0.0', 8000)