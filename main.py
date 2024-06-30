from flask import Flask, render_template

app = Flask("JobScraper")

@app.route('/')
def home():
    return render_template('home.html', name='Lily')

@app.route('/about')
def about():
    return '<h1>About Page</h1>'

app.run('0.0.0.0', 8000)