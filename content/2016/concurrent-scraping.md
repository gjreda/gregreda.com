Title: Asynchronous Scraping with Python
Date: 2016-10-16
Slug: asynchronous-scraping-with-python
Tags: scraping, python, tutorial
Description: Instead of scraping or doing other work synchronously, this post shows how to use Python3's concurrent.futures library to do work asynchronously -- more than one at a time.

Previously, I've written about the [basics of scraping](http://www.gregreda.com/2013/03/03/web-scraping-101-with-python/) and how you can [find API calls](http://www.gregreda.com/2015/02/15/web-scraping-finding-the-api/) in order to fetch data that isn't easily downloadable.

For simplicity, the code in these posts has always been synchronous -- given a list of URLs, we process one, then the next, then the next, and so on. While this makes for code that's straight-forward, it can also be slow.

This doesn't have to be the case though. Scraping is often an example of code that is [embarrassingly parallel](https://en.wikipedia.org/wiki/Embarrassingly_parallel). With some slight changes, our tasks can be done asynchronously, allowing us to process more than one URL at a time.

In version 3.2, Python introduced the [`concurrent.futures`](https://docs.python.org/3/library/concurrent.futures.html) module, which is a joy to use for parallelizing tasks like scraping. The rest of this post will show how we can use the module to make our previously synchronous code asynchronous.

### Parallelizing your tasks
Imagine we have a list of several thousand URLs. In previous posts, we've always written something that looks like this:

```python
from csv import DictWriter

URLS = [ ... ]  # thousands of urls for pages we'd like to parse

def parse(url):
    # our logic for parsing the page
    return data  # probably a dict

results = []
for url in URLS:  # go through each url one by one
    results.append(parse(url))

with open('results.csv', 'w') as f:
    writer = DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)
```

The above is an example of synchronous code -- we're looping through a list of URLs, processing one at a time. If the list of URLs is relatively small or we're not concerned about execution time, there's little reason to [parallelize](https://en.wikipedia.org/wiki/Task_parallelism) these tasks -- we might as well keep things simple and wait it out.

However, sometimes we have a huge list of URLs -- at least several thousand -- and we can't wait hours for them to finish.

With `concurrent.futures`, we can work on multiple URLs at once by adding a `ProcessPoolExecutor` and making a slight change to how we fetch our results.

But first, a reminder: _if you're scraping, don't be a jerk_. Space out your requests appropriately and don't hammer the site (i.e. use `time.sleep` to wait briefly between each request and set `max_workers` to a small number). Being a jerk runs the risk of getting your IP address blocked -- good luck getting that data now.

```python
from concurrent.futures import ProcessPoolExecutor
import concurrent.futures

URLS = [ ... ]

def parse(url):
    # our logic for parsing the page
    return data  # still probably a dict

with ProcessPoolExecutor(max_workers=4) as executor:
    future_results = {executor.submit(parse, url): url for url in URLS}

    results = []
    for future in concurrent.futures.as_completed(future_results):
        results.append(future.result())
```

In the above code, we're submitting tasks to the executor -- four workers -- each of which will execute the `parse` function against a URL. This execution does not happen immediately. For each submission, the executor returns an instance of a `Future`, which tells us that our task will be executed at some point in the ... well, future. The `as_completed` function watches our `future_results` for completion, upon which we'll be able to fetch each result via the `result` method.

My favorite part about this module is the clarity of its API -- tasks are _submitted_ to an _executor_, which is made up of one or more workers, each of which is churning through our tasks. Because our tasks are executed asynchronously, we are not waiting for a given task's completion before submitting another -- we are doing so at-will, with completion happening in the _future_. Once completed, we can get the task's _result_.

### Closing up
With a few changes to your code and some `concurrent.futures` love, you no longer have to fetch those basketball stats one page at a time.

But don't be a jerk either.
