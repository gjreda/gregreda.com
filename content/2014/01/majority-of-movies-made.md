Title: Finding the midpoint of film releases
Date: 2014-01-23
Slug: film-releases-midpoint
Tags: data science, movies, d3js, visualization
Description: Looking film release dates throughout history to determine the date that has an equal number of films made before and after it.
D3:
Scripts: movie-releases.js
Styles: styles.css

> "We're talking about Thunderdome. It's from before you were born."

> "Most movies are from before I was born."

That statement spurred a pretty interesting question: *what's the date where that statement is no longer true?* Put another way, *what date in history has an equal number of films made before and after it?*

My birthday, November 4, 1985, *felt* like a relatively safe date, but really, no one had a clue if what I said was true, including me. Guesses by about a dozen coworkers included dates from September 1963 all the way to September 2001.

Knowing that [IMDB](http://imdb.com) makes their [data publicly available](http://www.imdb.com/interfaces), I decided to find the actual date. Using the most current [releases.list file](ftp://ftp.fu-berlin.de/pub/misc/movies/database/release-dates.list.gz) (1/17/14 at the time of writing), I held the following assumptions:

1. Only films. The release-dates.list also includes TV shows and video games. It also includes movies that went straight to video - those count.

2. Films with a release date in the future do not count.

3. If the film was released multiple times (different release dates for different countries), use the earliest release date.

4. If only a release month and year were provided, assume the 15th of that month.

5. If only a release year was provided, assume [July 2nd](http://en.wikipedia.org/wiki/July_2) of that year.

The result?

<div id="vis" class="chart"></div>

May 15, 2002.

Of course, given the current rate at which films are being made, this analysis is already out of date.

For those interested, you can find the code [here](https://github.com/gjreda/movie-release-timeline).
