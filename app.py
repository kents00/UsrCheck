import os
from flask import Flask, render_template, request
from flask_caching import Cache
from sherlockapi.sites import SitesInformation
from sherlockapi.sherlock import sherlock
from sherlockapi.result import QueryStatus

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


class QueryNotify:
    def __init__(self, result=None):
        self.result = result

    def update(self, message=None):
        self.result = message

    def __str__(self):
        return str(self.result)


class QueryNotifyPrint(QueryNotify):
    def __init__(self, result=None):
        super().__init__(result)

    def start(self, message):
        title = "Checking username"
        print(f"[*] {title} {message} on:")

    def update(self, result):
        self.result = result
        response_time_text = f" [{round(self.result.query_time * 1000)} ms]" if self.result.query_time else ""
        print(f'[+]{response_time_text} checking => {self.result.site_name}')
        if result.status == QueryStatus.CLAIMED:
            print(f"found: {self.result.site_url_user}")

    def __str__(self):
        return str(self.result)


def getresult(username):
    data_path = os.path.join(os.path.dirname(
        __file__), "sherlockapi/resources/data.json")
    sites = SitesInformation(data_path)
    site_data = {site.name: site.information for site in sites}
    query_notify = QueryNotifyPrint(result=None)
    results = sherlock(
        username=username,
        site_data=site_data,
        query_notify=query_notify
    )
    responses = [result["url_user"] for website_name, result in results.items(
    ) if result.get("status").status == QueryStatus.CLAIMED]
    return responses


@app.before_request
def clear_cache():
    cache.clear()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    input_username = request.form['username'].strip()
    usernames = input_username.split()
    results = {}
    for username in usernames:
        result = cache.get(username)
        if result is None:
            result = getresult(username)
            cache.set(username, result, timeout=120)  # Cache for 1 hour
        results[username] = result
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
