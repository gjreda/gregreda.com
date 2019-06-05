Title: Useful jq commands
Date: 2019-05-26
Slug: jq-tutorial
Tags: data science, command line, unix, tutorial, terminal
Tweet: [new post] I wrote a little tutorial for jq, a command line tool that's great with json data.
Status: Draft

One of the tough things about being downstream from a process that spits out
semi-structured JSON logs is that you never really know your schema -- data
types are inconsistent, fields change, etc.

I've found [jq](https://stedolan.github.io/jq/) to be an invaluable tool for
exploring JSON data, but especially when pipelines go awry.

It's a great and useful command line tool for doing quick analysis of json
files. However, I find jq's documentation is more focused on its API than I
would prefer -- I learn from seeing practical examples and then tinkering.

In the event that others feel the similarly, I wanted to share some one-liners
that I've found useful. To illustrate the concepts, I'll use the City of
Chicago's towed vehicles dataset, which I've uploaded in JSON form
[here](https://gist.github.com/gjreda/d0fb779d787e38d13898d6811ab1077f).

If you're new to the command line or often need to explore datasets that are not
JSON, you might find [this previous
post](/2013/07/15/unix-commands-for-data-science/) helpful.

## jq Basics
The simplest use of jq is piping some data to it in order to view the data in a
nice, clean format.
```bash
# use curl to get a toy example from httpbin.org
$ curl -s -N http://httpbin.org/get?foo=bar | jq
{
  "args": {
    "foo": "bar"
  },
  "headers": {
    "Accept": "*/*",
    "Connection": "close",
    "Host": "httpbin.org",
    "User-Agent": "curl/7.54.0"
  },
  "origin": "98.212.1.58",
  "url": "http://httpbin.org/get?foo=bar"
}
```
In the code above, we're using [curl](https://curl.haxx.se/) to fetch JSON from
a toy endpoint and then piping it to jq for formatting.

It's important to note that expressions always passed to jq as a string. For example, if we only wanted to view the `headers` object in the response above:
```bash
$ curl -s -N http://httpbin.org/get?foo=bar | jq '.headers'
{
  "Accept": "*/*",
  "Connection": "close",
  "Host": "httpbin.org",
  "User-Agent": "curl/7.54.0"
}
```
This is true for nested or layering expressions using pipes and functions.
```bash
# return only the Host value within the headers object
$ curl -s -N http://httpbin.org/get?foo=bar | jq '.headers.Host'
"httpbin.org"

# return the headers object and pass it to the keys function, 
# giving us only its keys
$ curl -s -N http://httpbin.org/get?foo=bar | jq '.headers | keys'
[
  "Accept",
  "Connection",
  "Host",
  "User-Agent"
]
```
Now that you've got the basic concepts, let's move onto some specifics.

## Filtering
Throughout the rest of this post, I'll be using the [City of Chicago's towed
vehicles
dataset](https://gist.github.com/gjreda/d0fb779d787e38d13898d6811ab1077f). This dataset captures information about vehicles towed by the City of Chicago within the past 90 days.


```bash
# vehicles registered in Indiana
$ curl -s -N -L https://reda.io/towed-json | jq '.[] | select(.state == "IN")'
```
Note the above query returns a lot of results, so I've chosen not to paste in the output. In the event that we only want to see a couple results, we can wrap the query in jq's `limit` command.
```bash
$ curl -s -N -L https://reda.io/towed-json | jq 'limit(2; .[] | select(.state == "IN"))'
{
  "sid": 340591,
  "id": "B6C55558-0BFA-4BC9-995A-6967DF1E49BF",
  "position": 340591,
  "created_at": 1537608692,
  "created_meta": "878752",
  "updated_at": 1537608692,
  "updated_meta": "878752",
  "meta": null,
  "tow_date": "2018-09-22T00:00:00",
  "make": "DODG",
  "style": "4D",
  "model": null,
  "color": "MAR",
  "plate": "C174394",
  "state": "IN",
  "towed_to_address": "10300 S. Doty",
  "tow_facility_phone": "(773) 568-8495",
  "inventory_number": "2859533"
}
{
  "sid": 334006,
  "id": "4F752B18-38A3-4ABB-9F54-C7CB1563A896",
  "position": 334006,
  "created_at": 1535133706,
  "created_meta": "878752",
  "updated_at": 1535133706,
  "updated_meta": "878752",
  "meta": null,
  "tow_date": "2018-08-24T00:00:00",
  "make": "TOYT",
  "style": "2D",
  "model": null,
  "color": "RED",
  "plate": "513TND",
  "state": "IN",
  "towed_to_address": "10300 S. Doty",
  "tow_facility_phone": "(773) 568-8495",
  "inventory_number": "2857418"
}
```

### Filters: AND
jq also allows for combining multiple filter conditions through the use of `and` and `or` -- no need to layer in another pipe.
```bash
# Audi vehicles registered in Indiana
$ curl -s -N -L https://reda.io/towed-json | jq '.[] | select(.state == "IN" and .make == "AUDI")'
{
  "sid": 343803,
  "id": "55F6E6E4-F2A6-4A07-8A6C-C8B4760CFB71",
  "position": 343803,
  "created_at": 1538830881,
  "created_meta": "878752",
  "updated_at": 1538830881,
  "updated_meta": "878752",
  "meta": null,
  "tow_date": "2018-10-06T00:00:00",
  "make": "AUDI",
  "style": "4D",
  "model": null,
  "color": "BLK",
  "plate": "551NFQ",
  "state": "IN",
  "towed_to_address": "400 E. Lower Wacker",
  "tow_facility_phone": "(312) 744-7550",
  "inventory_number": "993862"
}
```
### Filters: OR
```bash
# Nobel Prize Winners in Economics from 1999 OR 1985
$ curl -s -N http://api.nobelprize.org/v1/prize.json \
  | jq '.prizes | .[] | select(.category == "economics" and
                              (.year == "1999" or .year == "1985"))'
{
  "year": "1999",
  "category": "economics",
  "laureates": [
    {
      "id": "720",
      "firstname": "Robert A.",
      "surname": "Mundell",
      "motivation": "\"for his analysis of monetary and fiscal policy under different exchange rate regimes and his analysis of optimum currency areas\"",
      "share": "1"
    }
  ]
}
{
  "year": "1985",
  "category": "economics",
  "laureates": [
    {
      "id": "699",
      "firstname": "Franco",
      "surname": "Modigliani",
      "motivation": "\"for his pioneering analyses of saving and of financial markets\"",
      "share": "1"
    }
  ]
}
```

### Filters: Dealing with NULL



## Grouping + Count - Counting GitHub Event Types
```bash
# live querying the GitHub API, so your results will be slightly different
$ curl -s -N https://api.github.com/events | jq '.[] | .type' | sort | uniq -c
   5 "CreateEvent"
   1 "DeleteEvent"
   1 "ForkEvent"
   6 "IssueCommentEvent"
   3 "IssuesEvent"
   1 "PublicEvent"
   4 "PullRequestEvent"
   1 "PullRequestReviewCommentEvent"
   7 "PushEvent"
   1 "WatchEvent"
```
When combined with `sort` and `uniq -c`, jq can be used to effectively group by and count the instances of a given object. In this case, we're living querying the GitHub Events endpoint to get counts of the most recent event types.


## Inconsistent Types
One of the problems with JSON is a lack of strict schema - value types can be mixed throughout your data. Sometimes it's a number, sometimes it's a string, sometimes it's null.

Combining jq's `type` function with `sort` and `uniq` is a quick way of getting an idea of how often these inconsistencies happen within a given field.

```bash
cat senators.json | jq '.objects | .[] | .person.cspanid | type' | sort | uniq -c
   1 "null"
  99 "number"
```

Or maybe you're writing a pipeline to schematize this JSON and would like to know how much space you need to allocate for each field, thus needing to know how many characters are typically in each field.

You can use jq's `length` function to get an idea.


#### Unique keys within a nested JSON object where not all keys are always present
```bash
cat publisher_facebook_post.log | jq --sort-keys \
  '.targeting | keys | .[]' \
  | sort | uniq -c
```
