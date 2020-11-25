Title: Scraping Craigslist for sold out concert tickets
Date: 2014-07-27
Slug: scraping-craigslist-for-tickets
Tags: scraping, tutorial, python, data
Description: Explaining how to use Python to automate Craigslist searches and send SMS messages for new results.

Recently, I've been listening to a lot of lo-fi rock band, [Cloud Nothings](http://en.wikipedia.org/wiki/Cloud_Nothings). Their album, [Here & Nowhere Else](http://www.amazon.com/gp/product/B00HZJH97Q/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B00HZJH97Q&linkCode=as2&tag=gjreda-20&linkId=H7HYP35ZYKFAKH7H), has been [critically lauded](http://www.metacritic.com/music/here-and-nowhere-else/cloud-nothings), including [garnering "Best New Music" from Pitchfork](http://pitchfork.com/reviews/albums/19075-cloud-nothings-here-and-nowhere-else/). As a result, when they came to Chicago's tiny Lincoln Hall in May, tickets sold out in a hurry - well before I found out about the show. Desperately wanting to go, I started checking Craigslist every day or two for tickets.

Lincoln Hall only holds about 500 people, so Craigslist postings were few and far between. When a post did pop up, I always ended up seeing it a couple hours after it was posted and was too late - the tickets had been sold. Noticing that my frustration was beginning to grow, I figured it was time to automate my Craigslist searches for tickets.

If you search on Craigslist and look at the URL of the results page, you'll notice that it looks very similar to this:

![Craigslist Search Results URL](/images/craigslist-search-results-url.png)

Note the section that says `query=this+is+my+search+term` - that's where your search term gets passed to the databases that back Craigslist (with spaces replaced by + signs). This means we can write code to automate any "for sale" search by hitting `http://<city>.craigslist.org/search/sss?query=<term>` where `<city>` corresponds to the subdomain of your city's respective Craigslist and `<term>` is our search term.

For my use case, there were very few Craigslist results for each search of "Cloud Nothings" and none of them were spammy. I decided to write a script which would run every 10 minutes and send me a text message if any of the results were new. If I got a text, I could quickly head over to Craigslist, email the seller, and go back about my day. I was lucky that ticket brokers hadn't started putting "Cloud Nothings" in their spammy posts - if they had, this solution likely would not have worked - the text messages would have been more noise than signal.

Thankfully, it worked. I was able to get a ticket for face value two nights before the show.

In the sections below, I'll walk through the code behind it all. If you're unfamiliar with web scraping, I suggest reading my previous posts [here](http://www.gregreda.com/2013/03/03/web-scraping-101-with-python/) and [here](http://www.gregreda.com/2013/05/06/more-web-scraping-with-python/).

### Code Walk-Through
Most of the code's functionality is contained within the four functions below.

#### parse_results
```python
def parse_results(search_term):
    results = []
    search_term = search_term.strip().replace(' ', '+')
    search_url = BASE_URL.format(search_term)
    soup = BeautifulSoup(urlopen(search_url).read())
    rows = soup.find('div', 'content').find_all('p', 'row')
    for row in rows:
        url = 'http://chicago.craigslist.org' + row.a['href']
        create_date = row.find('span', 'date').get_text()
        title = row.find_all('a')[1].get_text()
        results.append({'url': url, 'create_date': create_date, 'title': title})
    return results
```
The above function takes a `search_term`, which is used to execute a search on Craigslist. It returns a list of dictionaries, where each dictionary represents a post found within the search results.

Note the global `BASE_URL` variable - this is the search results URL mentioned earlier. Here, we're injecting our search term into the section of the URL that had `query=<term>`.

The majority of this function utilizes [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) to parse the HTML of Craigslist's search results page. For each post in the search results, we store the URL of the post, its creation date, and its title.

In the next function, we'll write these results to a CSV file, which we'll later use to check whether or not there are "new" posts.

#### write_results
```python
def write_results(results):
    """Writes list of dictionaries to file."""
    fields = results[0].keys()
    with open('results.csv', 'w') as f:
        dw = csv.DictWriter(f, fieldnames=fields, delimiter='|')
        dw.writer.writerow(dw.fieldnames)
        dw.writerows(results)
```
As mentioned above, `write_results` takes a list of dictionaries and writes them to a CSV file called `results.csv`. Each line of the file will store a post's title, create date, and URL.

You can think of this file similarly to how you might think of a database - we're storing information that we'll need to refer to later on. Since we aren't storing much data, there's really no need to use something like SQLite, MySQL or any other datastore - a text file works just fine for our use case. I'm a big proponent of [KISS methodology](http://en.wikipedia.org/wiki/KISS_principle) (Keep It Simple, Stupid).

#### has_new_records
```python
def has_new_records(results):
    current_posts = [x['url'] for x in results]
    fields = results[0].keys()
    if not os.path.exists('results.csv'):
        return True

    with open('results.csv', 'r') as f:
        reader = csv.DictReader(f, fieldnames=fields, delimiter='|')
        seen_posts = [row['url'] for row in reader]

    is_new = False
    for post in current_posts:
        if post in seen_posts:
            pass
        else:
            is_new = True
    return is_new
```
This function determines whether or not any of the posts are new (not present in the results from the last time our code was run).

It takes a list of dictionaries (exactly the same as the one `parse_results` returns) and checks it against the CSV file we created with the `write_results` function. Since a URL can only point to one post, we can consider it a [unique key](http://en.wikipedia.org/wiki/Unique_key) to check against.

If any of the URLs in results are not found within the CSV file, this function will return `True`, which we'll use as a trigger to sending off a text message as notification.

#### send_text
```python
def send_text(phone_number, msg):
    fromaddr = "Craigslist Checker"
    toaddrs = phone_number + "@txt.att.net"
    msg = ("From: {0}\r\nTo: {1}\r\n\r\n{2}").format(fromaddr, toaddrs, msg)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(config.email['username'], config.email['password'])
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()
```
`send_text` requires two parameters - the first being the 10-digit phone number that will receive the SMS message, and the second being the content of the message.

This function makes use of the [Simple Mail Transfer Protocol](http://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol) (or SMTP) as well as AT&T's email-to-SMS gateway (notice the `@txt.att.net`). This allows us to use a GMail account to send the text message.

Note that if you are not a GMail user or do not use AT&T for your cell phone service, you'll need to make some changes to this function. You can find a list of other email-to-SMS gateways [here](http://www.emailtextmessages.com/).

Since this function uses my GMail credentials, I've stored them in a separate Python file which I am referencing when I call `config.email['username']` and `config.email['password']`. You can find the config setup [here](https://github.com/gjreda/craigslist-checker/blob/master/config.py). Just make sure you don't accidentally check in your GMail credentials if you're putting this on GitHub.

#### Putting it all together
You can take a look at the final script [here](https://github.com/gjreda/craigslist-checker/blob/master/craigslist.py). Feel free to use it however you'd like. Deploying it is as simple as spinning up a micro EC2 instance and setting up a cronjob to run the script as often as you'd like.

Did you like this post? Was there something I missed? [Let me know on Twitter](https://twitter.com/gjreda).